$base = "C:\Users\Lecoo\projects\GnomoriaTranslator"
$rel = Join-Path $base "Release"
if (Test-Path $rel) { Remove-Item $rel -Recurse -Force }
New-Item -ItemType Directory -Path $rel -Force

Copy-Item (Join-Path $base "Patcher\bin\Release\net472\Patcher.exe") $rel -Force
Copy-Item (Join-Path $base "Patcher\bin\Release\net472\Mono.Cecil.dll") $rel -Force
Copy-Item (Join-Path $base "Translator\bin\Release\net472\Translator.dll") $rel -Force
Copy-Item (Join-Path $base "Translator\bin\Release\net472\0Harmony.dll") $rel -Force
Copy-Item (Join-Path $base "Translator\bin\Release\net472\Newtonsoft.Json.dll") $rel -Force
Copy-Item (Join-Path $base "Gnomoria_en_ru_final.json") (Join-Path $rel "Gnomoria_en_ru.json") -Force
Copy-Item (Join-Path $base "README.md") $rel -Force

$zipPath = Join-Path $base "Gnomoria_Rus_Release.zip"
if (Test-Path $zipPath) { Remove-Item $zipPath -Force }
Compress-Archive -Path "$rel\*" -DestinationPath $zipPath -Force
Write-Host "Zipped successfully to $zipPath"
