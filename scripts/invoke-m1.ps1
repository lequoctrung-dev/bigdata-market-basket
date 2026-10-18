[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('Setup','Preflight','Build','StartMongo','StopMongo','StartWeb','StopWeb','Status','RunSample','VerifyWeb')]
    [string]$Action,
    [ValidateSet('TV1','TV2')][string]$MachineRole = 'TV1',
    [string]$PythonPath,
    [string]$MongoPath
)

$ErrorActionPreference = 'Stop'
$m1Root = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$m1Artifacts = Join-Path $m1Root 'artifacts/m1'
$m1Python = Join-Path $m1Root '.venv/Scripts/python.exe'
$m1Maven = Join-Path $m1Root 'tmp/tools/apache-maven-3.9.16/bin/mvn.cmd'
$m1Jar = Join-Path $m1Root 'web/target/market-basket-m1-0.0.1-SNAPSHOT.jar'
New-Item -ItemType Directory -Path $m1Artifacts -Force | Out-Null

function Write-M1Json($Path, $Value) {
    $m1Encoded = $Value | ConvertTo-Json -Depth 12
    [IO.File]::WriteAllText($Path, $m1Encoded, (New-Object Text.UTF8Encoding($false)))
}

function Invoke-M1Checked([string]$Executable, [string[]]$Arguments) {
    & $Executable @Arguments
    if ($LASTEXITCODE -ne 0) { throw "Command failed (exit $LASTEXITCODE): $Executable" }
}

function Get-M1ReceiptPath([string]$Kind) { Join-Path $m1Artifacts "$Kind-process.json" }

function Get-M1OwnedProcess([string]$Kind) {
    $m1Path = Get-M1ReceiptPath $Kind
    if (-not (Test-Path -LiteralPath $m1Path)) { return $null }
    $m1Receipt = Get-Content -LiteralPath $m1Path -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($m1Receipt.root -ne $m1Root -or $m1Receipt.kind -ne $Kind) { throw 'Receipt does not belong to this workspace.' }
    $m1Process = Get-Process -Id $m1Receipt.process_id -ErrorAction SilentlyContinue
    if ($null -eq $m1Process) { return $null }
    $m1Cim = Get-CimInstance Win32_Process -Filter "ProcessId = $($m1Receipt.process_id)" -ErrorAction Stop
    if ($m1Process.StartTime.ToUniversalTime().Ticks -ne ([DateTime]$m1Receipt.started_at_utc).ToUniversalTime().Ticks `
        -or $m1Cim.ExecutablePath -ne $m1Receipt.executable `
        -or (Get-FileHash -LiteralPath $m1Receipt.executable -Algorithm SHA256).Hash -ne $m1Receipt.executable_sha256) {
        throw 'Process identity changed; refusing lifecycle action.'
    }
    if ([string]::IsNullOrEmpty($m1Cim.CommandLine) -or -not $m1Cim.CommandLine.Contains($m1Receipt.identity_path)) {
        throw 'Process command line does not match project receipt.'
    }
    if ($Kind -eq 'web' -and (Get-FileHash -LiteralPath $m1Receipt.identity_path -Algorithm SHA256).Hash -ne $m1Receipt.jar_sha256) {
        throw 'Pinned web JAR changed; stop using the original receipt before rebuilding.'
    }
    $m1Listener = @(Get-NetTCPConnection -State Listen -LocalPort $m1Receipt.port -ErrorAction SilentlyContinue)
    foreach ($m1Socket in $m1Listener) {
        if ($m1Socket.OwningProcess -ne $m1Receipt.process_id -or $m1Socket.LocalAddress -ne '127.0.0.1') {
            throw 'Unexpected listener owner/address; refusing lifecycle action.'
        }
    }
    return [pscustomobject]@{ Receipt=$m1Receipt; Process=$m1Process }
}

function Start-M1Process([string]$Kind, [string]$Executable, [string[]]$Arguments, [string]$IdentityPath, [int]$Port) {
    if ($null -ne (Get-M1OwnedProcess $Kind)) { throw "$Kind is already running; use Status." }
    if (@(Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue).Count -gt 0) {
        throw "Port $Port is occupied; do not stop an unrelated process."
    }
    $m1Output = Join-Path $m1Artifacts "$Kind-stdout.log"
    $m1Error = Join-Path $m1Artifacts "$Kind-stderr.log"
    $m1TaskProcess = Start-Process -FilePath $Executable -ArgumentList $Arguments -WorkingDirectory $m1Root `
        -WindowStyle Hidden -PassThru -RedirectStandardOutput $m1Output -RedirectStandardError $m1Error
    $m1TaskProcess.Refresh()
    $m1Receipt = [ordered]@{
        kind=$Kind; root=$m1Root; process_id=$m1TaskProcess.Id; port=$Port;
        started_at_utc=$m1TaskProcess.StartTime.ToUniversalTime().ToString('o');
        executable=[IO.Path]::GetFullPath($Executable);
        executable_sha256=(Get-FileHash -LiteralPath $Executable -Algorithm SHA256).Hash;
        identity_path=$IdentityPath; stdout=$m1Output; stderr=$m1Error
    }
    if ($Kind -eq 'web') { $m1Receipt.jar_sha256 = (Get-FileHash -LiteralPath $IdentityPath -Algorithm SHA256).Hash }
    Write-M1Json (Get-M1ReceiptPath $Kind) $m1Receipt
    $m1Ready = $false
    for ($m1Attempt=0; $m1Attempt -lt 45; $m1Attempt++) {
        Start-Sleep -Milliseconds 1000
        $m1Owned = Get-M1OwnedProcess $Kind
        if ($null -eq $m1Owned) { throw "$Kind exited; inspect project stdout/stderr logs." }
        if (@(Get-NetTCPConnection -State Listen -LocalPort $Port -ErrorAction SilentlyContinue).Count -gt 0) {
            $m1Ready=$true; break
        }
    }
    if (-not $m1Ready) { throw "$Kind has not listened yet; receipt remains available for Status/Stop." }
    Write-Output "$Kind started on 127.0.0.1:$Port; process receipt saved. Port ready is not acceptance PASS."
}

Push-Location $m1Root
try {
    switch ($Action) {
        'Setup' {
            if (-not $PythonPath) { $PythonPath = (Get-Command python -ErrorAction Stop).Source }
            if (-not (Test-Path -LiteralPath $m1Python)) { Invoke-M1Checked $PythonPath @('-m','venv','.venv') }
            Invoke-M1Checked $m1Python @('-m','pip','install','--disable-pip-version-check','--no-input','--cache-dir','tmp/pip-cache','-r','pipeline/requirements.txt')
            if (-not (Test-Path -LiteralPath $m1Maven)) {
                $m1Tools = Join-Path $m1Root 'tmp/tools'
                New-Item -ItemType Directory -Path $m1Tools -Force | Out-Null
                $m1Archive = Join-Path $m1Tools 'apache-maven-3.9.16-bin.zip'
                $m1ShaPath = "$m1Archive.sha512"
                Invoke-WebRequest -UseBasicParsing -Uri 'https://dlcdn.apache.org/maven/maven-3/3.9.16/binaries/apache-maven-3.9.16-bin.zip' -OutFile $m1Archive
                Invoke-WebRequest -UseBasicParsing -Uri 'https://downloads.apache.org/maven/maven-3/3.9.16/binaries/apache-maven-3.9.16-bin.zip.sha512' -OutFile $m1ShaPath
                $m1Expected = (Get-Content -LiteralPath $m1ShaPath -Raw).Trim().Split(' ')[0]
                if ((Get-FileHash -LiteralPath $m1Archive -Algorithm SHA512).Hash -ne $m1Expected) { throw 'Maven SHA512 mismatch.' }
                Expand-Archive -LiteralPath $m1Archive -DestinationPath $m1Tools -Force
            }
            Invoke-M1Checked $m1Maven @('-version')
            $m1Repository=Join-Path $m1Root 'tmp/maven-repository'
            $m1ConnectorDirectory=Join-Path $m1Root 'tmp/connector'
            Invoke-M1Checked $m1Maven @('-B','-ntp',"-Dmaven.repo.local=$m1Repository",'-f','pipeline/connector-pom.xml',
                'dependency:copy-dependencies',"-DoutputDirectory=$m1ConnectorDirectory",'-DincludeScope=runtime')
        }
        'Preflight' {
            $m1Os = Get-CimInstance Win32_OperatingSystem
            $m1Cpu = Get-CimInstance Win32_Processor
            $m1Java = (Get-Command java -ErrorAction Stop).Source
            if (-not $PythonPath) { $PythonPath = (Get-Command python -ErrorAction Stop).Source }
            if (-not $MongoPath) { $MongoPath = (Get-Command mongod -ErrorAction Stop).Source }
            $m1Environment = [ordered]@{
                machine_role=$MachineRole; checked_at_utc=[DateTime]::UtcNow.ToString('o');
                windows=$m1Os.Caption; windows_version=$m1Os.Version; architecture=$m1Os.OSArchitecture;
                cpu=@($m1Cpu | ForEach-Object Name); cores=@($m1Cpu | ForEach-Object NumberOfCores);
                ram_gib=[Math]::Round($m1Os.TotalVisibleMemorySize/1MB,2);
                free_ram_gib=[Math]::Round($m1Os.FreePhysicalMemory/1MB,2);
                java_version=(& $m1Java -version 2>&1 | Out-String).Trim();
                python_version=(& $PythonPath --version 2>&1 | Out-String).Trim();
                mongod_version=(& $MongoPath --version | Out-String).Trim();
                environment_only=$true; runtime_acceptance=$false
            }
            $m1RolePath=Join-Path $m1Artifacts $MachineRole
            New-Item -ItemType Directory -Path $m1RolePath -Force | Out-Null
            Write-M1Json (Join-Path $m1RolePath 'environment.json') $m1Environment
            $m1Environment | ConvertTo-Json -Depth 6
        }
        'Build' {
            if ($null -ne (Get-M1OwnedProcess 'web')) { throw 'Stop the pinned web process before rebuilding.' }
            $m1Repository=Join-Path $m1Root 'tmp/maven-repository'
            Invoke-M1Checked $m1Maven @('-B','-ntp',"-Dmaven.repo.local=$m1Repository",'-f','web/pom.xml','verify')
        }
        'StartMongo' {
            if (-not $MongoPath) { $MongoPath=(Get-Command mongod -ErrorAction Stop).Source }
            $m1DatabasePath=Join-Path $m1Artifacts 'mongo-data'
            New-Item -ItemType Directory -Path $m1DatabasePath -Force | Out-Null
            Start-M1Process 'mongo' $MongoPath @('--bind_ip','127.0.0.1','--port','27018','--dbpath',('"'+$m1DatabasePath+'"'),
                '--wiredTigerCacheSizeGB','0.25') $m1DatabasePath 27018
        }
        'StartWeb' {
            if (-not (Test-Path -LiteralPath $m1Jar)) { throw 'Build the M1 JAR first.' }
            Start-M1Process 'web' (Get-Command java -ErrorAction Stop).Source @('-Xmx256m','-jar',('"'+$m1Jar+'"'),
                '--app.mode=SAMPLE','--spring.mongodb.uri=mongodb://127.0.0.1:27018/bigdata_m1_sample?directConnection=true&serverSelectionTimeoutMS=5000') $m1Jar 8081
        }
        'StopMongo' {
            $m1Owned=Get-M1OwnedProcess 'mongo'
            if ($null -eq $m1Owned) { Write-Output 'mongo is not running'; break }
            Invoke-M1Checked $m1Python @('scripts/m1_control.py','shutdown-mongo')
            if (-not $m1Owned.Process.WaitForExit(15000)) { throw 'MongoDB has not exited; inspect receipt/log, do not kill by port/name.' }
            Write-Output 'Owned MongoDB stopped gracefully; data retained.'
        }
        'StopWeb' {
            $m1Owned=Get-M1OwnedProcess 'web'
            if ($null -eq $m1Owned) { Write-Output 'web is not running'; break }
            Stop-Process -Id $m1Owned.Receipt.process_id -ErrorAction Stop
            Write-Output 'Owned web process stopped.'
        }
        'Status' {
            foreach ($m1Kind in @('mongo','web')) {
                $m1Owned=Get-M1OwnedProcess $m1Kind
                [pscustomobject]@{Kind=$m1Kind;Running=($null -ne $m1Owned)} | ConvertTo-Json -Compress
            }
        }
        'RunSample' {
            if ($null -eq (Get-M1OwnedProcess 'mongo')) { throw 'Start owned M1 MongoDB first.' }
            if ($null -ne (Get-M1OwnedProcess 'web')) { throw 'Stop web during the first small-memory M1 batch; start it after batch.' }
            Invoke-M1Checked $m1Python @('pipeline/sample_pipeline.py','--machine-role',$MachineRole)
        }
        'VerifyWeb' {
            if ($null -eq (Get-M1OwnedProcess 'web')) { throw 'Start owned M1 web first.' }
            Invoke-M1Checked $m1Python @('scripts/m1_control.py','verify-web','--machine-role',$MachineRole)
        }
    }
} finally { Pop-Location }
