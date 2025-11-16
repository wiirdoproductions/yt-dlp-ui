# Add ffmpeg to user PATH
$currentPath = [System.Environment]::GetEnvironmentVariable('Path', 'User')
$ffmpegPath = 'C:\ffmpeg\bin'

if ($currentPath -notlike "*$ffmpegPath*") {
    $newPath = "$currentPath;$ffmpegPath"
    [System.Environment]::SetEnvironmentVariable('Path', $newPath, 'User')
    Write-Host "Successfully added $ffmpegPath to user PATH"
    Write-Host "Please restart your terminal or applications for the change to take effect"
} else {
    Write-Host "$ffmpegPath is already in user PATH"
}

# Verify
Write-Host "`nCurrent user PATH entries containing 'ffmpeg':"
[System.Environment]::GetEnvironmentVariable('Path', 'User') -split ';' | Where-Object { $_ -like '*ffmpeg*' }
