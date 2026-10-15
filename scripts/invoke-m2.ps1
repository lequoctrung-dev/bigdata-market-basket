[CmdletBinding()]
param([Parameter(Mandatory=$true)][ValidateSet('StartMongo','StopMongo','Status','Preflight')][string]$Action,
      [ValidateSet('TV1','TV2')][string]$MachineRole = 'TV1')
$ErrorActionPreference = 'Stop'
$m2Root = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$m2Artifacts = Join-Path $m2Root 'artifacts/m2'
$m2ReceiptPath = Join-Path $m2Artifacts 'mongo-process.json'
$m2Python = Join-Path $m2Root '.venv/Scripts/python.exe'
New-Item -ItemType Directory -Force -Path $m2Artifacts | Out-Null
function Save-M2Json($Path, $Value) {
    [IO.File]::WriteAllText($Path, ($Value | ConvertTo-Json -Depth 12), [Text.UTF8Encoding]::new($false))
}
function Get-M2Owned {
    if (-not (Test-Path -LiteralPath $m2ReceiptPath)) { return $null }
    $m2Saved = Get-Content -LiteralPath $m2ReceiptPath -Raw | ConvertFrom-Json
    if ($m2Saved.root -ne $m2Root -or $m2Saved.port -ne 27019) { throw 'Wrong M2 receipt' }
    $m2Process = Get-Process -Id $m2Saved.process_id -ErrorAction SilentlyContinue
    if ($null -eq $m2Process) { return $null }
    $m2Cim = Get-CimInstance Win32_Process -Filter "ProcessId = $($m2Saved.process_id)"
    if ($m2Process.StartTime.ToUniversalTime().Ticks -ne ([datetime]$m2Saved.started_at_utc).ToUniversalTime().Ticks -or
        $m2Cim.ExecutablePath -ne $m2Saved.executable -or
        (Get-FileHash -LiteralPath $m2Saved.executable).Hash -ne $m2Saved.executable_sha256 -or
        [string]::IsNullOrEmpty($m2Cim.CommandLine) -or -not $m2Cim.CommandLine.Contains($m2Saved.identity_path)) {
        throw 'M2 process identity mismatch'
    }
    foreach ($m2Socket in @(Get-NetTCPConnection -State Listen -LocalPort 27019 -ErrorAction SilentlyContinue)) {
        if ($m2Socket.LocalAddress -ne '127.0.0.1' -or $m2Socket.OwningProcess -ne $m2Saved.process_id) {
            throw 'M2 listener mismatch'
        }
    }
    return [pscustomobject]@{Receipt=$m2Saved; Process=$m2Process}
}
switch ($Action) {
    'Preflight' {
        $m2Os = Get-CimInstance Win32_OperatingSystem
        $m2Env = [ordered]@{checked_at_utc=[datetime]::UtcNow.ToString('o'); machine_role=$MachineRole;
            windows=$m2Os.Caption; version=$m2Os.Version; architecture=$m2Os.OSArchitecture;
            cpu=@(Get-CimInstance Win32_Processor | ForEach-Object Name);
            total_ram_bytes=[long]$m2Os.TotalVisibleMemorySize*1024;
            available_ram_bytes=[long]$m2Os.FreePhysicalMemory*1024;
            free_disk_bytes=(Get-PSDrive D).Free; powershell=$PSVersionTable.PSVersion.ToString();
            listeners=@(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue |
                Where-Object LocalPort -in 27017,27018,27019,8081 |
                Select-Object LocalAddress,LocalPort,OwningProcess)}
        Save-M2Json (Join-Path $m2Artifacts "preflight-$([datetime]::UtcNow.ToString('yyyyMMddTHHmmss')).json") $m2Env
        $m2Env | ConvertTo-Json -Depth 6
    }
    'StartMongo' {
        if ($null -ne (Get-M2Owned)) { throw 'M2 MongoDB already running; use Status' }
        if (@(Get-NetTCPConnection -State Listen -LocalPort 27019 -ErrorAction SilentlyContinue).Count) { throw '27019 occupied' }
        $m2Exe = (Get-Command mongod -ErrorAction Stop).Source
        $m2Dbpath = Join-Path $m2Artifacts 'mongo-data'
        New-Item -ItemType Directory -Force -Path $m2Dbpath | Out-Null
        $m2Stamp = [datetime]::UtcNow.ToString('yyyyMMddTHHmmss')
        $m2Process = Start-Process -FilePath $m2Exe -ArgumentList @('--bind_ip','127.0.0.1','--port','27019',
            '--dbpath',('"'+$m2Dbpath+'"'),'--wiredTigerCacheSizeGB','0.25') -WorkingDirectory $m2Root -WindowStyle Hidden -PassThru `
            -RedirectStandardOutput (Join-Path $m2Artifacts "mongo-$m2Stamp-stdout.log") `
            -RedirectStandardError (Join-Path $m2Artifacts "mongo-$m2Stamp-stderr.log")
        $m2Process.Refresh()
        Save-M2Json $m2ReceiptPath ([ordered]@{root=$m2Root; port=27019; database='bigdata_m2'; process_id=$m2Process.Id;
            executable=$m2Exe; executable_sha256=(Get-FileHash -LiteralPath $m2Exe).Hash;
            started_at_utc=$m2Process.StartTime.ToUniversalTime().ToString('o'); identity_path=$m2Dbpath})
        for ($m2Attempt=0; $m2Attempt -lt 45; $m2Attempt++) {
            Start-Sleep -Milliseconds 1000
            $m2Owned = Get-M2Owned
            if ($null -eq $m2Owned) { throw 'M2 MongoDB exited; read logs' }
            if (@(Get-NetTCPConnection -State Listen -LocalPort 27019 -ErrorAction SilentlyContinue).Count) {
                Write-Output 'Owned MongoDB listening on 127.0.0.1:27019; data retained'; break
            }
        }
        if ($m2Attempt -eq 45) { throw 'Startup not ready; inspect receipt before any retry' }
    }
    'StopMongo' {
        $m2Owned = Get-M2Owned
        if ($null -eq $m2Owned) { Write-Output 'Owned process absent'; break }
        & $m2Python -c 'from pymongo import MongoClient; from pymongo.errors import AutoReconnect; c=MongoClient("mongodb://127.0.0.1:27019/?directConnection=true&serverSelectionTimeoutMS=5000"); exec("try:\n c.admin.command(\"shutdown\",force=False)\nexcept AutoReconnect:\n pass")'
        if ($LASTEXITCODE -ne 0) { throw 'Shutdown command failed' }
        if (-not $m2Owned.Process.WaitForExit(15000)) { throw 'Process still running; no force kill' }
        Save-M2Json (Join-Path $m2Artifacts "stop-$([datetime]::UtcNow.ToString('yyyyMMddTHHmmss')).json") `
            @{status='STOPPED'; process_id=$m2Owned.Receipt.process_id; data_retained=$true;
              checked_at_utc=[datetime]::UtcNow.ToString('o'); listener_count=@(Get-NetTCPConnection -State Listen -LocalPort 27019 -ErrorAction SilentlyContinue).Count}
        Write-Output 'Owned MongoDB stopped gracefully; data retained'
    }
    'Status' {
        $m2Owned = Get-M2Owned
        [pscustomobject]@{running=($null -ne $m2Owned); port=27019} | ConvertTo-Json
    }
}
