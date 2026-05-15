import json

game_json = 'D:/steam/steamapps/common/Gnomoria/Gnomoria_en_ru.json'

with open(game_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

missing = [k for k, v in data.items() if k == v and k != '?']
translated = [k for k, v in data.items() if k != v]

print(f"Total entries: {len(data)}")
print(f"Translated: {len(translated)}")
print(f"Missing (English): {len(missing)}")
print("\nFirst 30 missing strings:")
for m in missing[:30]:
    print(f" - {m}")
