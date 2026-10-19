[CmdletBinding()]
param([Parameter(Mandatory=$true)][ValidateSet('StartWeb','StopWeb','Status','Build')][string]$Action, [Parameter(Mandatory=$true)][string]$Session)
$ErrorActionPreference='Stop'
$m6Root=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$m6Out=[IO.Path]::GetFullPath((Join-Path $m6Root $Session))
$m6Allowed=[IO.Path]::GetFullPath((Join-Path $m6Root 'artifacts/m6'))+[IO.Path]::DirectorySeparatorChar
if(-not $m6Out.StartsWith($m6Allowed,[StringComparison]::OrdinalIgnoreCase)) { throw 'M6 session outside evidence root' }
& (Join-Path $m6Root '.venv/Scripts/python.exe') -X utf8 -c 'import sys; from pathlib import Path; sys.path.insert(0,"pipeline"); from m6_common import context; context(Path(sys.argv[1]))' $m6Out
if($LASTEXITCODE -ne 0) { throw 'M6 session machine/reference guard failed' }
$m6ReceiptPath=Join-Path $m6Out 'web-process.json'
New-Item -ItemType Directory -Force -Path $m6Out | Out-Null
function Save-M6($Path,$Value) { [IO.File]::WriteAllText($Path,($Value|ConvertTo-Json -Depth 12),[Text.UTF8Encoding]::new($false)) }
function Get-M6Owned {
    if(-not(Test-Path -LiteralPath $m6ReceiptPath)) { return $null }
    $m6Saved=Get-Content -LiteralPath $m6ReceiptPath -Raw|ConvertFrom-Json
    if($m6Saved.root -ne $m6Root -or $m6Saved.port -ne 8081 -or $m6Saved.database -ne 'bigdata_m6' -or $m6Saved.mode -ne 'DEVELOPMENT') { throw 'M6 receipt destination mismatch' }
    $m6Process=Get-Process -Id $m6Saved.process_id -ErrorAction SilentlyContinue
    if($null -eq $m6Process) { return $null }
    $m6Cim=Get-CimInstance Win32_Process -Filter "ProcessId = $($m6Saved.process_id)" -ErrorAction Stop
    if($m6Process.StartTime.ToUniversalTime().Ticks -ne ([datetime]$m6Saved.started_at_utc).ToUniversalTime().Ticks -or
       $m6Cim.ExecutablePath -ne $m6Saved.executable -or
       (Get-FileHash -LiteralPath $m6Saved.executable).Hash -ne $m6Saved.executable_sha256 -or
       (Get-FileHash -LiteralPath $m6Saved.identity_path).Hash -ne $m6Saved.jar_sha256 -or
       [string]::IsNullOrEmpty($m6Cim.CommandLine) -or -not $m6Cim.CommandLine.Contains($m6Saved.identity_path) -or
       -not $m6Cim.CommandLine.Contains('--app.mode=DEVELOPMENT') -or
       -not $m6Cim.CommandLine.Contains('127.0.0.1:27019/bigdata_m6')) { throw 'M6 web process identity mismatch' }
    foreach($m6Socket in @(Get-NetTCPConnection -State Listen -LocalPort 8081 -ErrorAction SilentlyContinue)) {
        if($m6Socket.OwningProcess -ne $m6Saved.process_id -or $m6Socket.LocalAddress -ne '127.0.0.1') { throw 'M6 listener mismatch' }
    }
    return [pscustomobject]@{Receipt=$m6Saved;Process=$m6Process}
}
switch($Action) {
    'Build' {
        if($null -ne (Get-M6Owned)) { throw 'Stop the owned M6 web before build' }
        if(@(Get-NetTCPConnection -State Listen -LocalPort 8081 -ErrorAction SilentlyContinue).Count) { throw '8081 still occupied; inspect and stop only its verified owner before build' }
        $m6Repository=Join-Path $m6Root 'tmp/maven-repository'
        & (Join-Path $m6Root 'tmp/tools/apache-maven-3.9.16/bin/mvn.cmd') -o -B -ntp "-Dmaven.repo.local=$m6Repository" -f (Join-Path $m6Root 'web/pom.xml') verify
        if($LASTEXITCODE -ne 0) { throw 'M6 build failed' }
    }
    'StartWeb' {
        if($null -ne (Get-M6Owned)) { throw 'M6 already running; use Status' }
        if(@(Get-NetTCPConnection -State Listen -LocalPort 8081 -ErrorAction SilentlyContinue).Count) { throw '8081 occupied; do not stop unknown owner' }
        & (Join-Path $m6Root 'scripts/invoke-m2.ps1') -Action Status
        if($null -eq (Get-Process -Id ((Get-Content (Join-Path $m6Root 'artifacts/m2/mongo-process.json') -Raw|ConvertFrom-Json).process_id) -ErrorAction SilentlyContinue)) { throw 'Start verified Mongo M2 before web' }
        $m6Built=Join-Path $m6Root 'web/target/market-basket-m1-0.0.1-SNAPSHOT.jar'
        $m6Hash=(Get-FileHash -LiteralPath $m6Built).Hash
        $m6Runtime=Join-Path $m6Out 'runtime'
        New-Item -ItemType Directory -Force -Path $m6Runtime | Out-Null
        $m6Jar=Join-Path $m6Runtime "web-$m6Hash.jar"
        if(-not(Test-Path -LiteralPath $m6Jar)) { Copy-Item -LiteralPath $m6Built -Destination $m6Jar }
        if((Get-FileHash -LiteralPath $m6Jar).Hash -ne $m6Hash) { throw 'Runtime JAR hash mismatch' }
        $m6Java=(Get-Command java -ErrorAction Stop).Source
        $m6Stamp=[datetime]::UtcNow.ToString('yyyyMMddTHHmmss')
        $m6Args=@('-Xmx256m','-jar',('"'+$m6Jar+'"'),'--app.mode=DEVELOPMENT','--server.address=127.0.0.1','--server.port=8081',
            '--spring.mongodb.uri=mongodb://127.0.0.1:27019/bigdata_m6?directConnection=true&serverSelectionTimeoutMS=3000&connectTimeoutMS=3000&socketTimeoutMS=5000')
        $m6Stdout=Join-Path $m6Out "web-$m6Stamp-stdout.log"
        $m6Stderr=Join-Path $m6Out "web-$m6Stamp-stderr.log"
        $m6Process=Start-Process -FilePath $m6Java -ArgumentList $m6Args -WorkingDirectory $m6Root -WindowStyle Hidden -PassThru -RedirectStandardOutput $m6Stdout -RedirectStandardError $m6Stderr
        $m6Process.Refresh()
        Save-M6 $m6ReceiptPath ([ordered]@{root=$m6Root;database='bigdata_m6';mode='DEVELOPMENT';port=8081;process_id=$m6Process.Id;started_at_utc=$m6Process.StartTime.ToUniversalTime().ToString('o');
            executable=$m6Java;executable_sha256=(Get-FileHash -LiteralPath $m6Java).Hash;identity_path=$m6Jar;jar_sha256=$m6Hash;arguments=$m6Args;stdout=$m6Stdout;stderr=$m6Stderr})
        $m6Watch=[Diagnostics.Stopwatch]::StartNew()
        $m6Listening=$false
        for($m6Attempt=0;$m6Attempt -lt 45;$m6Attempt++) {
            Start-Sleep -Milliseconds 1000
            if($null -eq (Get-M6Owned)) { throw 'M6 exited; inspect logs' }
            if(@(Get-NetTCPConnection -State Listen -LocalPort 8081 -ErrorAction SilentlyContinue).Count) { $m6Listening=$true;break }
        }
        Save-M6 (Join-Path $m6Out "startup-$m6Stamp.json") @{listening=$m6Listening;observed_wait_seconds=$m6Watch.Elapsed.TotalSeconds;method='1s poll plus identity/CIM/listener checks; excludes launcher prep';checked_at_utc=[datetime]::UtcNow.ToString('o')}
        if(-not $m6Listening) { throw 'M6 not listening yet; receipt retained for Status/Stop' }
        Write-Output 'M6 at http://127.0.0.1:8081; listening is not acceptance.'
    }
    'StopWeb' {
        $m6Owned=Get-M6Owned
        if($null -eq $m6Owned) { Write-Output 'M6 not running';break }
        Stop-Process -Id $m6Owned.Receipt.process_id -ErrorAction Stop
        if(-not $m6Owned.Process.WaitForExit(15000)) { throw 'Owned web has not exited' }
        Save-M6 (Join-Path $m6Out ('stop-'+[datetime]::UtcNow.ToString('yyyyMMddTHHmmss')+'.json')) @{status='STOPPED';process_id=$m6Owned.Receipt.process_id;checked_at_utc=[datetime]::UtcNow.ToString('o');data_retained=$true}
    }
    'Status' {
        $m6Owned=Get-M6Owned
        @{running=($null -ne $m6Owned);port=8081;checked_at_utc=[datetime]::UtcNow.ToString('o')}|ConvertTo-Json
    }
}
