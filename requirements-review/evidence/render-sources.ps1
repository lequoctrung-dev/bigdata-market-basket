$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Runtime.WindowsRuntime
[Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime] | Out-Null
[Windows.Data.Pdf.PdfDocument,Windows.Data.Pdf,ContentType=WindowsRuntime] | Out-Null
[Windows.Storage.Streams.InMemoryRandomAccessStream,Windows.Storage.Streams,ContentType=WindowsRuntime] | Out-Null
[Windows.Data.Pdf.PdfPageRenderOptions,Windows.Data.Pdf,ContentType=WindowsRuntime] | Out-Null
$taskMethod = [System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.IsGenericMethod -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' } | Select-Object -First 1
$actionMethod = [System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and -not $_.IsGenericMethod -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncAction' } | Select-Object -First 1
function Await-Operation($operation, [Type]$resultType) {
    $task = $taskMethod.MakeGenericMethod($resultType).Invoke($null,@($operation))
    $task.GetAwaiter().GetResult()
}
foreach ($label in @('A','B')) {
    $filePath = Join-Path $PSScriptRoot ($label+'-source.pdf')
    $file = Await-Operation ([Windows.Storage.StorageFile]::GetFileFromPathAsync($filePath)) ([Windows.Storage.StorageFile])
    $pdf = Await-Operation ([Windows.Data.Pdf.PdfDocument]::LoadFromFileAsync($file)) ([Windows.Data.Pdf.PdfDocument])
    for ($i=0; $i -lt $pdf.PageCount; $i++) {
        $page = $pdf.GetPage($i)
        $stream = New-Object Windows.Storage.Streams.InMemoryRandomAccessStream
        try {
            $options = New-Object Windows.Data.Pdf.PdfPageRenderOptions
            $options.DestinationWidth = 1300
            $task = $actionMethod.Invoke($null,@($page.RenderToStreamAsync($stream,$options)))
            $task.GetAwaiter().GetResult()
            $stream.Seek(0)
            $readStream = [System.IO.WindowsRuntimeStreamExtensions]::AsStreamForRead($stream)
            $target = Join-Path $PSScriptRoot ('{0}-page-{1:D2}.png' -f $label,($i+1))
            $outStream = [System.IO.File]::Create($target)
            try { $readStream.CopyTo($outStream) } finally { $outStream.Dispose() }
        } finally { $stream.Dispose(); $page.Dispose() }
    }
    Write-Output ($label+': rendered '+$pdf.PageCount+' pages')
}
