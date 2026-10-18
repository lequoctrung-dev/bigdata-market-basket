[CmdletBinding()]
param([Parameter(Mandatory=$true)][ValidateSet('StartWeb','StopWeb','Status','Build')][string]$Action)
$ErrorActionPreference='Stop'
$m5Root=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$m5Out=Join-Path $m5Root 'artifacts/m5'
$m5ReceiptPath=Join-Path $m5Out 'web-process.json'
New-Item -ItemType Directory -Force -Path $m5Out | Out-Null
function Save-M5($Path,$Value) { [IO.File]::WriteAllText($Path,($Value|ConvertTo-Json -Depth 12),[Text.UTF8Encoding]::new($false)) }
function Get-M5Owned {
    if(-not(Test-Path -LiteralPath $m5ReceiptPath)) { return $null }
    $m5Saved=Get-Content -LiteralPath $m5ReceiptPath -Raw|ConvertFrom-Json
    if($m5Saved.root -ne $m5Root -or $m5Saved.port -ne 8081 -or $m5Saved.mode -ne 'DEVELOPMENT') { throw 'M5 receipt destination mismatch' }
    $m5Process=Get-Process -Id $m5Saved.process_id -ErrorAction SilentlyContinue
    if($null -eq $m5Process) { return $null }
    $m5Cim=Get-CimInstance Win32_Process -Filter "ProcessId = $($m5Saved.process_id)" -ErrorAction Stop
    if($m5Process.StartTime.ToUniversalTime().Ticks -ne ([datetime]$m5Saved.started_at_utc).ToUniversalTime().Ticks -or
       $m5Cim.ExecutablePath -ne $m5Saved.executable -or
       (Get-FileHash -LiteralPath $m5Saved.executable).Hash -ne $m5Saved.executable_sha256 -or
       (Get-FileHash -LiteralPath $m5Saved.identity_path).Hash -ne $m5Saved.jar_sha256 -or
       [string]::IsNullOrEmpty($m5Cim.CommandLine) -or -not $m5Cim.CommandLine.Contains($m5Saved.identity_path) -or
       -not $m5Cim.CommandLine.Contains('--app.mode=DEVELOPMENT') -or
       -not $m5Cim.CommandLine.Contains('127.0.0.1:27019/bigdata_m2')) { throw 'M5 web process identity mismatch' }
    foreach($m5Socket in @(Get-NetTCPConnection -State Listen -LocalPort 8081 -ErrorAction SilentlyContinue)) {
        if($m5Socket.OwningProcess -ne $m5Saved.process_id -or $m5Socket.LocalAddress -ne '127.0.0.1') { throw 'M5 listener mismatch' }
    }
    return [pscustomobject]@{Receipt=$m5Saved;Process=$m5Process}
}
switch($Action) {
    'Build' {
        if($null -ne (Get-M5Owned)) { throw 'Stop the owned M5 web before build' }
        $m5Repository=Join-Path $m5Root 'tmp/maven-repository'
        & (Join-Path $m5Root 'tmp/tools/apache-maven-3.9.16/bin/mvn.cmd') -o -B -ntp "-Dmaven.repo.local=$m5Repository" -f (Join-Path $m5Root 'web/pom.xml') verify
        if($LASTEXITCODE -ne 0) { throw 'M5 build failed' }
    }
    'StartWeb' {
        if($null -ne (Get-M5Owned)) { throw 'M5 already running; use Status' }
        if(@(Get-NetTCPConnection -State Listen -LocalPort 8081 -ErrorAction SilentlyContinue).Count) { throw '8081 occupied; do not stop unknown owner' }
        & (Join-Path $m5Root 'scripts/invoke-m2.ps1') -Action Status
        if($null -eq (Get-Process -Id ((Get-Content (Join-Path $m5Root 'artifacts/m2/mongo-process.json') -Raw|ConvertFrom-Json).process_id) -ErrorAction SilentlyContinue)) { throw 'Start verified Mongo M2 before web' }
        $m5Built=Join-Path $m5Root 'web/target/market-basket-m1-0.0.1-SNAPSHOT.jar'
        $m5Hash=(Get-FileHash -LiteralPath $m5Built).Hash
        $m5Runtime=Join-Path $m5Out 'runtime'
        New-Item -ItemType Directory -Force -Path $m5Runtime | Out-Null
        $m5Jar=Join-Path $m5Runtime "web-$m5Hash.jar"
        if(-not(Test-Path -LiteralPath $m5Jar)) { Copy-Item -LiteralPath $m5Built -Destination $m5Jar }
        if((Get-FileHash -LiteralPath $m5Jar).Hash -ne $m5Hash) { throw 'Runtime JAR hash mismatch' }
        $m5Java=(Get-Command java -ErrorAction Stop).Source
        $m5Stamp=[datetime]::UtcNow.ToString('yyyyMMddTHHmmss')
        $m5Args=@('-Xmx256m','-jar',('"'+$m5Jar+'"'),'--app.mode=DEVELOPMENT','--server.address=127.0.0.1','--server.port=8081',
            '--spring.mongodb.uri=mongodb://127.0.0.1:27019/bigdata_m2?directConnection=true&serverSelectionTimeoutMS=3000&connectTimeoutMS=3000&socketTimeoutMS=5000')
        $m5Stdout=Join-Path $m5Out "web-$m5Stamp-stdout.log"
        $m5Stderr=Join-Path $m5Out "web-$m5Stamp-stderr.log"
        $m5Process=Start-Process -FilePath $m5Java -ArgumentList $m5Args -WorkingDirectory $m5Root -WindowStyle Hidden -PassThru -RedirectStandardOutput $m5Stdout -RedirectStandardError $m5Stderr
        $m5Process.Refresh()
        Save-M5 $m5ReceiptPath ([ordered]@{root=$m5Root;mode='DEVELOPMENT';port=8081;process_id=$m5Process.Id;started_at_utc=$m5Process.StartTime.ToUniversalTime().ToString('o');
            executable=$m5Java;executable_sha256=(Get-FileHash -LiteralPath $m5Java).Hash;identity_path=$m5Jar;jar_sha256=$m5Hash;arguments=$m5Args;stdout=$m5Stdout;stderr=$m5Stderr})
        $m5Watch=[Diagnostics.Stopwatch]::StartNew()
        $m5Listening=$false
        for($m5Attempt=0;$m5Attempt -lt 45;$m5Attempt++) {
            Start-Sleep -Milliseconds 1000
            if($null -eq (Get-M5Owned)) { throw 'M5 exited; inspect logs' }
            if(@(Get-NetTCPConnection -State Listen -LocalPort 8081 -ErrorAction SilentlyContinue).Count) { $m5Listening=$true;break }
        }
        Save-M5 (Join-Path $m5Out "startup-$m5Stamp.json") @{listening=$m5Listening;observed_wait_seconds=$m5Watch.Elapsed.TotalSeconds;method='1s poll plus identity/CIM/listener checks; excludes launcher prep';checked_at_utc=[datetime]::UtcNow.ToString('o')}
        if(-not $m5Listening) { throw 'M5 not listening yet; receipt retained for Status/Stop' }
        Write-Output 'M5 at http://127.0.0.1:8081; listening is not acceptance.'
    }
    'StopWeb' {
        $m5Owned=Get-M5Owned
        if($null -eq $m5Owned) { Write-Output 'M5 not running';break }
        Stop-Process -Id $m5Owned.Receipt.process_id -ErrorAction Stop
        if(-not $m5Owned.Process.WaitForExit(15000)) { throw 'Owned web has not exited' }
        Save-M5 (Join-Path $m5Out ('stop-'+[datetime]::UtcNow.ToString('yyyyMMddTHHmmss')+'.json')) @{status='STOPPED';process_id=$m5Owned.Receipt.process_id;checked_at_utc=[datetime]::UtcNow.ToString('o');data_retained=$true}
    }
    'Status' {
        $m5Owned=Get-M5Owned
        @{running=($null -ne $m5Owned);port=8081;checked_at_utc=[datetime]::UtcNow.ToString('o')}|ConvertTo-Json
    }
}
