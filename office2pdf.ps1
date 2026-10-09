param(
  [Parameter(Mandatory=$true)][string]$In,
  [Parameter(Mandatory=$true)][string]$Out,
  [int]$TimeoutSec = 180
)
$ErrorActionPreference = 'Stop'
$ext = [System.IO.Path]::GetExtension($In).ToLower()
Write-Output ("[office2pdf] " + $In + " -> " + $Out + " (" + $ext + ")")
try {
  if ($ext -in @('.doc', '.docx', '.rtf', '.odt', '.txt')) {
    $app = New-Object -ComObject Word.Application
    $app.Visible = $false
    $app.DisplayAlerts = 0
    $doc = $app.Documents.Open($In, $false, $true)
    $doc.SaveAs([ref]$Out, [ref]17)   # 17 = wdFormatPDF
    $doc.Close($false)
    $app.Quit()
  }
  elseif ($ext -in @('.xls', '.xlsx', '.xlsm', '.csv')) {
    $app = New-Object -ComObject Excel.Application
    $app.Visible = $false
    $app.DisplayAlerts = $false
    $wb = $app.Workbooks.Open($In)
    $wb.ExportAsFixedFormat(0, $Out)  # 0 = xlTypePDF
    $wb.Close($false)
    $app.Quit()
  }
  elseif ($ext -in @('.ppt', '.pptx', '.pptm')) {
    $app = New-Object -ComObject PowerPoint.Application
    $pres = $app.Presentations.Open($In, $true, $false, $false)
    $pres.SaveAs($Out, 32)            # 32 = ppSaveAsPDF
    $pres.Close()
    $app.Quit()
  }
  else {
    Write-Output ("[office2pdf] unsupported: " + $ext)
    exit 2
  }
  [System.GC]::Collect()
  [System.GC]::WaitForPendingFinalizers()
  if (Test-Path $Out) { Write-Output "[office2pdf] OK"; exit 0 }
  Write-Output "[office2pdf] output missing"; exit 1
}
catch {
  Write-Output ("[office2pdf] ERR " + $_.Exception.Message)
  exit 1
}
