import json
import os

base_path = 'C:/Users/Lecoo/projects/GnomoriaTranslator/Gnomoria_en_ru_translated_final.json'
current_path = 'C:/Users/Lecoo/projects/GnomoriaTranslator/Gnomoria_current.json'
output_path = 'C:/Users/Lecoo/projects/GnomoriaTranslator/Gnomoria_merged.json'

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        # Remove common corruption
        content = content.replace('\\"', '"')
        try:
            return json.loads(content)
        except:
            # Try second pass if first fails
            try: return json.loads(content.replace('\\', '\\\\'))
            except: return {}

base_data = load_json(base_path)
current_data = load_json(current_path)

# Merge: prioritize base_data for translations, 
# keep current_data for keys found during play.
final_data = {}

# All unique keys from both
all_keys = list(current_data.keys())
for k in base_data:
    if k not in all_keys:
        all_keys.append(k)

for k in all_keys:
    # If we have a translation in base, take it
    val = base_data.get(k, current_data.get(k, k))
    
    # If base value was same as key (untranslated), 
    # try to see if it's a known string I can translate now
    if val == k:
       # Hardcoded small fixes for obvious UI
       if k == "Load Game": val = "Загрузить игру"
       if k == "Spring": val = "Весна"
       if k == "Summer": val = "Лето"
       if k == "Autumn": val = "Осень"
       if k == "Winter": val = "Зима"
    
    final_data[k] = val

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(final_data, f, ensure_ascii=False, indent=2)

print(f"Merged {len(final_data)} entries.")
