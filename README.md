# Gnomoria Russian Translation Mod (Live Rendering Engine)

This project provides a robust, real-time Russian translation for the game **Gnomoria**. Since Gnomoria uses compiled XNA `.xnb` font files that lack Cyrillic support, standard string replacement results in "??????" characters.

This mod solves the issue elegantly:
1. It injects a **Harmony hook** directly into `Gnomoria.exe` via `Mono.Cecil`.
2. It intercepts all `SpriteBatch.DrawString` calls.
3. Instead of trying to render unsupported text, it **dynamically draws the Russian text onto a transparent Texture2D** using system fonts (Arial) and renders that image instead.
4. It caches the textures for optimal performance.

## Installation

1. Copy `Translator.dll` and `0Harmony.dll` to your Gnomoria root folder (e.g., `Steam\steamapps\common\Gnomoria`).
2. Copy `Gnomoria_en_ru_translated_final.json` to the root folder and rename it to `Gnomoria_en_ru.json`.
3. Use the `Patcher` console app to inject the hook into `Gnomoria.exe`. (A backup will be created automatically).

## Contributing
To add more translations, simply play the game! Any untranslated English text will automatically be appended to `Gnomoria_en_ru.json`. Open the file, add your translations, and restart the game.
