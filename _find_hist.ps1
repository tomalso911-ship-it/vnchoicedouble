$root = 'C:\Users\tomal\AppData\Local\CodeBuddyExtension\Data'
$roots = Get-ChildItem $root -Directory
Write-Host "=== Data 下的 UUID 目录 ==="
$roots | ForEach-Object { Write-Host $_.Name '  lastWrite=' $_.LastWriteTime }

Write-Host ""
Write-Host "=== 所有 history 会话 index.json（含标题+最后消息时间）==="
Get-ChildItem $root -Recurse -Filter index.json -File | ForEach-Object {
    try {
        $txt = Get-Content $_.FullName -Raw -ErrorAction Stop
        if ($txt -match '"conversations"') {
            $j = $txt | ConvertFrom-Json
            $c = $j.conversations[0]
            $path = $_.FullName
            Write-Host "NAME: $($c.name)  | lastMsg: $($c.lastMessageAt)  | created: $($c.createdAt)"
            Write-Host "   PATH: $path"
            Write-Host ""
        }
    } catch {}
}
