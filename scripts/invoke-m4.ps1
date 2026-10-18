[CmdletBinding()]
param([Parameter(Mandatory=$true)][ValidateSet('StartWeb','StopWeb','Status','Build')][string]$Action)
$ErrorActionPreference='Stop'
$m4Root=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$m4Out=Join-Path $m4Root 'artifacts/m4'
$m4ReceiptPath=Join-Path $m4Out 'web-process.json'
New-Item -ItemType Directory -Force -Path $m4Out | Out-Null
function Save-M4($Path,$Value) { [IO.File]::WriteAllText($Path,($Value|ConvertTo-Json -Depth 12),[Text.UTF8Encoding]::new($false)) }
function Get-M4Owned {
    if(-not(Test-Path -LiteralPath $m4ReceiptPath)) { return $null }
    $m4Saved=Get-Content -LiteralPath $m4ReceiptPath -Raw|ConvertFrom-Json
    if($m4Saved.root -ne $m4Root -or $m4Saved.port -ne 8081 -or $m4Saved.mode -ne 'DEVELOPMENT') { throw 'M4 receipt destination mismatch' }
    $m4Process=Get-Process -Id $m4Saved.process_id -ErrorAction SilentlyContinue
    if($null -eq $m4Process) { return $null }
    $m4Cim=Get-CimInstance Win32_Process -Filter "ProcessId = $($m4Saved.process_id)" -ErrorAction Stop
    if($m4Process.StartTime.ToUniversalTime().Ticks -ne ([datetime]$m4Saved.started_at_utc).ToUniversalTime().Ticks -or
       $m4Cim.ExecutablePath -ne $m4Saved.executable -or
       (Get-FileHash -LiteralPath $m4Saved.executable).Hash -ne $m4Saved.executable_sha256 -or
       (Get-FileHash -LiteralPath $m4Saved.identity_path).Hash -ne $m4Saved.jar_sha256 -or
       [string]::IsNullOrEmpty($m4Cim.CommandLine) -or -not $m4Cim.CommandLine.Contains($m4Saved.identity_path) -or
       -not $m4Cim.CommandLine.Contains('--app.mode=DEVELOPMENT') -or
       -not $m4Cim.CommandLine.Contains('127.0.0.1:27019/bigdata_m2')) { throw 'M4 web process identity mismatch' }
    foreach($m4Socket in @(Get-NetTCPConnection -State Listen -LocalPort 8081 -ErrorAction SilentlyContinue)) {
        if($m4Socket.OwningProcess -ne $m4Saved.process_id -or $m4Socket.LocalAddress -ne '127.0.0.1') { throw 'M4 listener mismatch' }
    }
    return [pscustomobject]@{Receipt=$m4Saved;Process=$m4Process}
}
switch($Action) {
    'Build' {
        if($null -ne (Get-M4Owned)) { throw 'Stop the owned M4 web before build' }
        $m4Repository=Join-Path $m4Root 'tmp/maven-repository'
        & (Join-Path $m4Root 'tmp/tools/apache-maven-3.9.16/bin/mvn.cmd') -o -B -ntp "-Dmaven.repo.local=$m4Repository" -f (Join-Path $m4Root 'web/pom.xml') verify
        if($LASTEXITCODE -ne 0) { throw 'M4 build failed' }
    }
    'StartWeb' {
        if($null -ne (Get-M4Owned)) { throw 'M4 already running; use Status' }
        if(@(Get-NetTCPConnection -State Listen -LocalPort 8081 -ErrorAction SilentlyContinue).Count) { throw '8081 occupied; do not stop unknown owner' }
        & (Join-Path $m4Root 'scripts/invoke-m2.ps1') -Action Status
        if($null -eq (Get-Process -Id ((Get-Content (Join-Path $m4Root 'artifacts/m2/mongo-process.json') -Raw|ConvertFrom-Json).process_id) -ErrorAction SilentlyContinue)) { throw 'Start verified Mongo M2 before web' }
        $m4Built=Join-Path $m4Root 'web/target/market-basket-m1-0.0.1-SNAPSHOT.jar'
        $m4Hash=(Get-FileHash -LiteralPath $m4Built).Hash
        $m4Runtime=Join-Path $m4Out 'runtime'
        New-Item -ItemType Directory -Force -Path $m4Runtime | Out-Null
        $m4Jar=Join-Path $m4Runtime "web-$m4Hash.jar"
        if(-not(Test-Path -LiteralPath $m4Jar)) { Copy-Item -LiteralPath $m4Built -Destination $m4Jar }
        if((Get-FileHash -LiteralPath $m4Jar).Hash -ne $m4Hash) { throw 'Runtime JAR hash mismatch' }
        $m4Java=(Get-Command java -ErrorAction Stop).Source
        $m4Stamp=[datetime]::UtcNow.ToString('yyyyMMddTHHmmss')
        $m4Args=@('-Xmx256m','-jar',('"'+$m4Jar+'"'),'--app.mode=DEVELOPMENT','--server.address=127.0.0.1','--server.port=8081',
            '--spring.mongodb.uri=mongodb://127.0.0.1:27019/bigdata_m2?directConnection=true&serverSelectionTimeoutMS=3000&connectTimeoutMS=3000&socketTimeoutMS=5000')
        $m4Stdout=Join-Path $m4Out "web-$m4Stamp-stdout.log"
        $m4Stderr=Join-Path $m4Out "web-$m4Stamp-stderr.log"
        $m4Process=Start-Process -FilePath $m4Java -ArgumentList $m4Args -WorkingDirectory $m4Root -WindowStyle Hidden -PassThru -RedirectStandardOutput $m4Stdout -RedirectStandardError $m4Stderr
        $m4Process.Refresh()
        Save-M4 $m4ReceiptPath ([ordered]@{root=$m4Root;mode='DEVELOPMENT';port=8081;process_id=$m4Process.Id;started_at_utc=$m4Process.StartTime.ToUniversalTime().ToString('o');
            executable=$m4Java;executable_sha256=(Get-FileHash -LiteralPath $m4Java).Hash;identity_path=$m4Jar;jar_sha256=$m4Hash;arguments=$m4Args;stdout=$m4Stdout;stderr=$m4Stderr})
        $m4Watch=[Diagnostics.Stopwatch]::StartNew()
        $m4Listening=$false
        for($m4Attempt=0;$m4Attempt -lt 45;$m4Attempt++) {
            Start-Sleep -Milliseconds 1000
            if($null -eq (Get-M4Owned)) { throw 'M4 exited; inspect logs' }
            if(@(Get-NetTCPConnection -State Listen -LocalPort 8081 -ErrorAction SilentlyContinue).Count) { $m4Listening=$true;break }
        }
        Save-M4 (Join-Path $m4Out "startup-$m4Stamp.json") @{listening=$m4Listening;observed_wait_seconds=$m4Watch.Elapsed.TotalSeconds;method='1s poll plus identity/CIM/listener checks; excludes launcher prep';checked_at_utc=[datetime]::UtcNow.ToString('o')}
        if(-not $m4Listening) { throw 'M4 not listening yet; receipt retained for Status/Stop' }
        Write-Output 'M4 at http://127.0.0.1:8081; listening is not acceptance.'
    }
    'StopWeb' {
        $m4Owned=Get-M4Owned
        if($null -eq $m4Owned) { Write-Output 'M4 not running';break }
        Stop-Process -Id $m4Owned.Receipt.process_id -ErrorAction Stop
        if(-not $m4Owned.Process.WaitForExit(15000)) { throw 'Owned web has not exited' }
        Save-M4 (Join-Path $m4Out ('stop-'+[datetime]::UtcNow.ToString('yyyyMMddTHHmmss')+'.json')) @{status='STOPPED';process_id=$m4Owned.Receipt.process_id;checked_at_utc=[datetime]::UtcNow.ToString('o');data_retained=$true}
    }
    'Status' {
        $m4Owned=Get-M4Owned
        @{running=($null -ne $m4Owned);port=8081;checked_at_utc=[datetime]::UtcNow.ToString('o')}|ConvertTo-Json
    }
}
