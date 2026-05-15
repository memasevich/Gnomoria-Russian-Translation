Set-Location 'C:\Users\Lecoo\projects\GnomoriaTranslator'
dotnet build Translator\Translator.csproj -c Release
Copy-Item 'C:\Users\Lecoo\projects\GnomoriaTranslator\Translator\bin\Release\net472\Translator.dll' 'D:\steam\steamapps\common\Gnomoria\Translator.dll' -Force

$json = '{ "New Game": "Новая игра", "Options": "Настройки", "v1.0": "v0.0.2 | Перевод: memasevich", "Exit": "Выход" }'
[System.IO.File]::WriteAllText('D:\steam\steamapps\common\Gnomoria\Gnomoria_en_ru.json', $json)
