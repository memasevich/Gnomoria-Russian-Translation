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
        'Mining:' = (U '0428 0430 0445 0442 0435 0440 0441 0442 0432 043E 003A')
        'Build Sawmill' = (U '041F 043E 0441 0442 0440 043E 0438 0442 044C 0020 043B 0435 0441 043E 043F 0438 043B 043A 0443')
        'Craft Item' = (U '0421 043E 0437 0434 0430 0442 044C 0020 043F 0440 0435 0434 043C 0435 0442')
        'Craft plank' = (U '0421 043E 0437 0434 0430 0442 044C 0020 0434 043E 0441 043A 0443')
        'workbench' = (U '0432 0435 0440 0441 0442 0430 043A')
        'Crude Workbench' = (U '0413 0440 0443 0431 044B 0439 0020 0432 0435 0440 0441 0442 0430 043A')
        'plank' = (U '0434 043E 0441 043A 0430')
        'chair' = (U '0441 0442 0443 043B')
        'Sunset:' = (U '0417 0430 043A 0430 0442 003A')
        'Worth:' = (U '0426 0435 043D 043D 043E 0441 0442 044C 003A')
        'dirt wall' = (U '0437 0435 043C 043B 044F 043D 0430 044F 0020 0441 0442 0435 043D 0430')
        'Mining' = (U '0413 043E 0440 043D 043E 0435 0020 0434 0435 043B 043E')
        'raw stone' = (U '0441 044B 0440 043E 0439 0020 043A 0430 043C 0435 043D 044C')
        'any barrel' = (U '043B 044E 0431 0430 044F 0020 0431 043E 0447 043A 0430')
        'yak' = (U '044F 043A')
        'miner' = (U '0448 0430 0445 0442 0451 0440')
        'bear' = (U '043C 0435 0434 0432 0435 0434 044C')
        'Pastured Animals:' = (U '0416 0438 0432 043E 0442 043D 044B 0435 0020 043D 0430 0020 0432 044B 043F 0430 0441 0435 003A')
        'Raznorab' = (U '0420 0430 0437 043D 043E 0440 0430 0431 043E 0447 0438 0439')
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
    @{ Name = 'Sunset time'; Input = 'Sunset: 17:02'; Expected = (U '0417 0430 043A 0430 0442 003A 0020 0031 0037 003A 0030 0032') }
    @{ Name = 'Worth counter'; Input = 'Worth: 0'; Expected = (U '0426 0435 043D 043D 043E 0441 0442 044C 003A 0020 0030') }
    @{ Name = 'Population counter'; Input = 'Population: 9'; Expected = (U '041D 0430 0441 0435 043B 0435 043D 0438 0435 003A 0020 0039') }
    @{ Name = 'Deceased counter'; Input = 'Deceased: 0'; Expected = (U '041F 043E 0433 0438 0431 0448 0438 0435 003A 0020 0030') }
    @{ Name = 'Injured counter'; Input = 'Injured: 0'; Expected = (U '0420 0430 043D 0435 043D 044B 0435 003A 0020 0030') }
    @{ Name = 'Idle counter'; Input = 'Idle: 0'; Expected = (U '0411 0435 0437 0020 0434 0435 043B 0430 003A 0020 0030') }
    @{ Name = 'Total counter'; Input = 'Total (2)'; Expected = (U '0412 0441 0435 0433 043E 0020 0028 0032 0029') }
    @{ Name = 'Required carpentry'; Input = 'Required Carpentry: 1'; Expected = (U '0422 0440 0435 0431 0443 0435 0442 0441 044F 0020 043F 043B 043E 0442 043D 0438 0446 043A 043E 0435 0020 0434 0435 043B 043E 003A 0020 0031') }
    @{ Name = 'Required construction'; Input = 'Required Construction: 1'; Expected = (U '0422 0440 0435 0431 0443 0435 0442 0441 044F 0020 0441 0442 0440 043E 0438 0442 0435 043B 044C 0441 0442 0432 043E 003A 0020 0031') }
    @{ Name = 'Efficiency'; Input = 'Efficiency: 100%'; Expected = (U '042D 0444 0444 0435 043A 0442 0438 0432 043D 043E 0441 0442 044C 003A 0020 0031 0030 0030 0025') }
    @{ Name = 'Available space'; Input = 'Available Space: 20 / 20'; Expected = (U '0421 0432 043E 0431 043E 0434 043D 043E 0435 0020 043C 0435 0441 0442 043E 003A 0020 0032 0030 0020 002F 0020 0032 0030') }
    @{ Name = 'Dormitory count'; Input = 'Dormitories (1)'; Expected = (U '041E 0431 0449 0438 0435 0020 0441 043F 0430 043B 044C 043D 0438 0020 0028 0031 0029') }
    @{ Name = 'Item count'; Input = 'dirt pile (64/64)'; Expected = (U '043A 0443 0447 0430 0020 0437 0435 043C 043B 0438 0020 0028 0036 0034 002F 0036 0034 0029') }
    @{ Name = 'Quantity item'; Input = '1x workbench (0)'; Expected = (U '0031 0078 0020 0432 0435 0440 0441 0442 0430 043A 0020 0028 0030 0029') }
    @{ Name = 'Static profession'; Input = 'Engineer:'; Expected = (U '0418 043D 0436 0435 043D 0435 0440 003A') }
    @{ Name = 'Static combat group'; Input = 'melee'; Expected = (U '0431 043B 0438 0436 043D 0438 0439 0020 0431 043E 0439') }
    @{ Name = 'Static combat group 2'; Input = 'ranged'; Expected = (U '0434 0430 043B 044C 043D 0438 0439 0020 0431 043E 0439') }
    @{ Name = 'Dynamic skill level'; Input = 'Mining: 24'; Expected = (U '0428 0430 0445 0442 0435 0440 0441 0442 0432 043E 003A 0020 0032 0034') }
    @{ Name = 'Date with year'; Input = '2nd day of Spring, Year 1'; Expected = (U '0032 002D 0439 0020 0434 0435 043D 044C 0020 0432 0435 0441 043D 044B 002C 0020 0413 043E 0434 0020 0031') }
    @{ Name = 'Date without year'; Input = '2nd day of Spring'; Expected = (U '0032 002D 0439 0020 0434 0435 043D 044C 0020 0432 0435 0441 043D 044B') }
    @{ Name = 'Sleep event'; Input = 'Ban falls asleep on the floor.'; Expected = (U '0042 0061 006E 0020 0437 0430 0441 044B 043F 0430 0435 0442 0020 043D 0430 0020 043F 043E 043B 0443 002E') }
    @{ Name = 'Task building'; Input = 'Task: Build Sawmill'; Expected = (U '0417 0430 0434 0430 0447 0430 003A 0020 041F 043E 0441 0442 0440 043E 0438 0442 044C 0020 043B 0435 0441 043E 043F 0438 043B 043A 0443') }
    @{ Name = 'Task craft'; Input = 'Task: Craft Item'; Expected = (U '0417 0430 0434 0430 0447 0430 003A 0020 0421 043E 0437 0434 0430 0442 044C 0020 043F 0440 0435 0434 043C 0435 0442') }
    @{ Name = 'Craft plank'; Input = 'Craft plank'; Expected = (U '0421 043E 0437 0434 0430 0442 044C 0020 0434 043E 0441 043A 0443') }
    @{ Name = 'Craft for dependency'; Input = 'plank (for workbench)'; Expected = (U '0434 043E 0441 043A 0430 0020 0028 0434 043B 044F 003A 0020 0432 0435 0440 0441 0442 0430 043A 0029') }
    @{ Name = 'Craft needs dependency'; Input = 'chair (needs plank)'; Expected = (U '0441 0442 0443 043B 0020 0028 0442 0440 0435 0431 0443 0435 0442 0441 044F 003A 0020 0434 043E 0441 043A 0430 0029') }
    @{ Name = 'Workbench for at'; Input = 'For workbench at'; Expected = (U '0414 043B 044F 003A 0020 0432 0435 0440 0441 0442 0430 043A 0020 0432') }
    @{ Name = 'Crude workbench efficiency'; Input = 'Crude Workbench (Efficiency: 70%)'; Expected = (U '0413 0440 0443 0431 044B 0439 0020 0432 0435 0440 0441 0442 0430 043A 0020 0028 042D 0444 0444 0435 043A 0442 0438 0432 043D 043E 0441 0442 044C 003A 0020 0037 0030 0025 0029') }
    @{ Name = 'Dirt wall'; Input = 'dirt wall'; Expected = (U '0437 0435 043C 043B 044F 043D 0430 044F 0020 0441 0442 0435 043D 0430') }
    @{ Name = 'Numbered skill'; Input = '(26) Mining'; Expected = (U '0028 0032 0036 0029 0020 0413 043E 0440 043D 043E 0435 0020 0434 0435 043B 043E') }
    @{ Name = 'Quantity item raw stone'; Input = '16x raw stone'; Expected = (U '0031 0036 0078 0020 0441 044B 0440 043E 0439 0020 043A 0430 043C 0435 043D 044C') }
    @{ Name = 'Stock any barrel'; Input = 'any barrel (2)'; Expected = (U '043B 044E 0431 0430 044F 0020 0431 043E 0447 043A 0430 0020 0028 0032 0029') }
    @{ Name = 'Stock yak count'; Input = 'yak (2)'; Expected = (U '044F 043A 0020 0028 0032 0029') }
    @{ Name = 'Profession colon'; Input = 'miner:'; Expected = (U '0448 0430 0445 0442 0451 0440 003A') }
    @{ Name = 'Death event'; Input = 'Ban has died.'; Expected = (U '0042 0061 006E 0020 043F 043E 0433 0438 0431 0430 0435 0442 002E') }
    @{ Name = 'Creature spotted'; Input = 'A bear has been spotted.'; Expected = (U '0417 0430 043C 0435 0447 0435 043D 003A 0020 043C 0435 0434 0432 0435 0434 044C 002E') }
    @{ Name = 'Gnomads arrived'; Input = '3 gnomads have arrived.'; Expected = (U '0033 0020 043F 0440 0438 0431 044B 043B 043E 0020 0433 043D 043E 043C 043E 0432 002D 043A 043E 0447 0435 0432 043D 0438 043A 043E 0432 002E') }
    @{ Name = 'Season summer'; Input = 'It is now summer.'; Expected = (U '041D 0430 0441 0442 0443 043F 0438 043B 043E 0020 043B 0435 0442 043E 002E') }
    @{ Name = 'Corpse'; Input = "Ban's corpse"; Expected = (U '0422 0440 0443 043F 003A 0020 0042 0061 006E') }
    @{ Name = 'Water pct'; Input = '150% water'; Expected = (U '0031 0035 0030 0025 0020 0432 043E 0434 044B') }
    @{ Name = 'Good health event'; Input = 'Gas is in good health'; Expected = (U '0047 0061 0073 0020 0432 0020 0434 043E 0431 0440 043E 043C 0020 0437 0434 0440 0430 0432 0438 0438') }
    @{ Name = 'Pastured animals colon'; Input = 'Pastured Animals: 0/20'; Expected = (U '0416 0438 0432 043E 0442 043D 044B 0435 0020 043D 0430 0020 0432 044B 043F 0430 0441 0435 003A 0020 0030 002F 0032 0030') }
    @{ Name = 'Gnome custom profession'; Input = 'Gas Raznorab'; Expected = (U '0047 0061 0073 0020 0420 0430 0437 043D 043E 0440 0430 0431 043E 0447 0438 0439') }
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
