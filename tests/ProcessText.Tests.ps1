param(
    [Parameter(Mandatory = $true)]
    [string]$AssemblyPath,
    [string]$DictionaryPath
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $AssemblyPath)) {
    throw "Assembly not found: $AssemblyPath"
}

$assembly = [System.Reflection.Assembly]::LoadFrom((Resolve-Path -LiteralPath $AssemblyPath).Path)
$hookType = $assembly.GetType('GnomoriaTranslator.Hook', $true)
$processText = $hookType.GetMethod(
    'ProcessText',
    [System.Reflection.BindingFlags]::Public -bor [System.Reflection.BindingFlags]::Static
)

function U([string]$codePoints) {
    return -join ($codePoints -split ' ' | ForEach-Object {
        [char]([Convert]::ToInt32($_, 16))
    })
}

if ($DictionaryPath) {
    if (-not (Test-Path -LiteralPath $DictionaryPath)) {
        throw "Dictionary not found: $DictionaryPath"
    }
    $jsonAssembly = Join-Path (Split-Path -Parent (Resolve-Path -LiteralPath $AssemblyPath).Path) 'Newtonsoft.Json.dll'
    if (Test-Path -LiteralPath $jsonAssembly) {
        Add-Type -Path $jsonAssembly
    }
    $jsonText = [System.IO.File]::ReadAllText((Resolve-Path -LiteralPath $DictionaryPath).Path)
    $translations = [Newtonsoft.Json.JsonConvert]::DeserializeObject(
        $jsonText,
        [System.Collections.Generic.Dictionary[string,string]]
    )
} else {
    $translations = New-Object 'System.Collections.Generic.Dictionary[string,string]'
    $staticTranslations = @{
        'Engineer:' = (U '0418 043D 0436 0435 043D 0435 0440 003A')
        'melee' = (U '0431 043B 0438 0436 043D 0438 0439 0020 0431 043E 0439')
        'ranged' = (U '0434 0430 043B 044C 043D 0438 0439 0020 0431 043E 0439')
    }
    foreach ($entry in $staticTranslations.GetEnumerator()) {
        $translations[$entry.Key] = $entry.Value
    }
}
$hookType.GetField('Translations').SetValue($null, $translations)

$cases = @(
    @{ Name = 'Food counter'; Input = 'Food: 104'; Expected = (U '0415 0434 0430 003A 0020 0031 0030 0034') }
    @{ Name = 'Drink counter'; Input = 'Drink: 121'; Expected = (U '041F 0438 0442 044C 0451 003A 0020 0031 0032 0031') }
    @{ Name = 'Sunrise time'; Input = 'Sunrise: 07:10'; Expected = (U '0412 043E 0441 0445 043E 0434 003A 0020 0030 0037 003A 0031 0030') }
    @{ Name = 'Population counter'; Input = 'Population: 9'; Expected = (U '041D 0430 0441 0435 043B 0435 043D 0438 0435 003A 0020 0039') }
    @{ Name = 'Deceased counter'; Input = 'Deceased: 0'; Expected = (U '041F 043E 0433 0438 0431 0448 0438 0435 003A 0020 0030') }
    @{ Name = 'Injured counter'; Input = 'Injured: 0'; Expected = (U '0420 0430 043D 0435 043D 044B 0435 003A 0020 0030') }
    @{ Name = 'Idle counter'; Input = 'Idle: 0'; Expected = (U '0411 0435 0437 0020 0434 0435 043B 0430 003A 0020 0030') }
    @{ Name = 'Total counter'; Input = 'Total (2)'; Expected = (U '0412 0441 0435 0433 043E 0020 0028 0032 0029') }
    @{ Name = 'Required carpentry'; Input = 'Required Carpentry: 1'; Expected = (U '0422 0440 0435 0431 0443 0435 0442 0441 044F 0020 043F 043B 043E 0442 043D 0438 0446 043A 043E 0435 0020 0434 0435 043B 043E 003A 0020 0031') }
    @{ Name = 'Efficiency'; Input = 'Efficiency: 100%'; Expected = (U '042D 0444 0444 0435 043A 0442 0438 0432 043D 043E 0441 0442 044C 003A 0020 0031 0030 0030 0025') }
    @{ Name = 'Available space'; Input = 'Available Space: 20 / 20'; Expected = (U '0421 0432 043E 0431 043E 0434 043D 043E 0435 0020 043C 0435 0441 0442 043E 003A 0020 0032 0030 0020 002F 0020 0032 0030') }
    @{ Name = 'Dormitory count'; Input = 'Dormitories (1)'; Expected = (U '041E 0431 0449 0438 0435 0020 0441 043F 0430 043B 044C 043D 0438 0020 0028 0031 0029') }
    @{ Name = 'Item count'; Input = 'dirt pile (64/64)'; Expected = (U '043A 0443 0447 0430 0020 0437 0435 043C 043B 0438 0020 0028 0036 0034 002F 0036 0034 0029') }
    @{ Name = 'Static profession'; Input = 'Engineer:'; Expected = (U '0418 043D 0436 0435 043D 0435 0440 003A') }
    @{ Name = 'Static combat group'; Input = 'melee'; Expected = (U '0431 043B 0438 0436 043D 0438 0439 0020 0431 043E 0439') }
    @{ Name = 'Static combat group 2'; Input = 'ranged'; Expected = (U '0434 0430 043B 044C 043D 0438 0439 0020 0431 043E 0439') }
)

$failures = foreach ($case in $cases) {
    $actual = [string]$processText.Invoke($null, @($case.Input))
    if ($actual -cne $case.Expected) {
        [pscustomobject]@{
            Name = $case.Name
            Input = $case.Input
            Expected = $case.Expected
            Actual = $actual
        }
    }
}

if ($failures) {
    $failures | Format-Table -AutoSize | Out-String | Write-Host
    exit 1
}

Write-Host ("PASS: {0} ProcessText cases" -f $cases.Count)
