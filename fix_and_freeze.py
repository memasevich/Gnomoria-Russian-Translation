import json
import re

def get_final_mapping():
    return {
        # --- МЕНЮ (ГЛАВНОЕ) ---
        "New Game": "Новая игра",
        "Options": "Настройки",
        "Steam Workshop": "Мастерская Steam",
        "Exit": "Выход",
        "v1.0": "v0.0.2 | memasevich 2026",
        "Load Game": "Загрузить игру",

        # --- МАТЕРИАЛЫ ---
        "steel": "сталь", "iron": "железо", "lead": "свинец", "bronze": "бронза", "copper": "медь",
        "malachite": "малахит", "silver": "серебро", "gold": "золото", "rose gold": "роз. золото",
        "platinum": "платина", "tin": "олово", "metal": "металл", "ore": "руда", "bar": "слиток",
        "sliver": "стружка", "coal": "уголь", "silica": "кремнезем",
        "pine": "сосна", "orange wood": "апельсин", "wild strawberry": "земляника",
        "apple": "яблоко", "orange": "апельсин", "grape": "виноград", "strawberry": "земляника",
        "soil": "земля", "dirt": "грязь", "stone": "камень", "log": "бревно", "plank": "доска",
        "ceramic": "керамика", "bone": "кость", "thatch": "солома", "leather": "кожа",

        # --- ПРОФЕССИИ ---
        "Miner": "Шахтер", "Mason": "Каменщик", "Stonecarver": "Резчик по камню",
        "Woodcutter": "Дровосек", "Carpenter": "Плотник", "Woodcarver": "Резчик по дереву",
        "Smelter": "Плавильщик", "Blacksmith": "Кузнец", "Metalworker": "Металлург",
        "Weaponsmith": "Оружейник", "Armorer": "Бронник", "Gemcutter": "Огранщик",
        "Jeweler": "Ювелир", "Weaver": "Ткач", "Tailor": "Портной", "Potter": "Гончар",
        "Leatherworker": "Кожевник", "Bonecarver": "Резчик по кости", "Prospector": "Старатель",
        "Tinkerer": "Жестянщик", "Machinist": "Машинист", "Engineer": "Инженер",
        "Mechanic": "Механик", "Rancher": "Животновод", "Butcher": "Мясник",
        "Gardener": "Садовник", "Farmer": "Фермер", "Chef": "Повар", "Brewer": "Пивовар",
        "Medic": "Медик", "Caretaker": "Смотритель", "Builder": "Строитель", "Hauler": "Носильщик",
        "Soldier": "Солдат",

        # --- КЛЮЧИ HUD ---
        "Depth": "Глубина", "Food": "Еда", "Drink": "Питье", "Sunrise": "Рассвет", "Sunset": "Закат",
        "Year": "Год", "day of": "день", "Spring": "Весны", "Summer": "Лета", "Autumn": "Осени", "Winter": "Зимы",
        "Worth": "Ценность", "Total": "Всего", "Idle": "Бездельники", "Injured": "Раненые",
        "Deceased": "Погибшие", "Overview": "Сводка", "Rooms": "Комнаты", "Workshops": "Мастерские"
    }

def process():
    # Берем чистые ключи из дампа
    with open('C:/Users/Lecoo/projects/GnomoriaTranslator/Gnomoria_raw_catch.json', 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    keys = re.findall(r'\"([^\"]+)\"\s*:', content)
    m = get_final_mapping()
    sorted_keys = sorted(m.keys(), key=len, reverse=True)
    
    final_dict = {}
    for k in set(keys):
        if not k.strip() or k == '?': continue
        
        val = k
        if k == "v1.0":
            val = "v0.0.2 | memasevich 2026"
        else:
            # Многопроходный перевод фрагментов
            for eng in sorted_keys:
                if eng.lower() in val.lower():
                    rus = m[eng]
                    val = val.replace(eng, rus)
                    val = val.replace(eng.capitalize(), rus.capitalize())
                    val = val.replace(eng.lower(), rus)
        
        final_dict[k] = val

    # Сохраняем напрямую через Python (гарантия UTF-8 без BOM)
    target = 'D:/steam/steamapps/common/Gnomoria/Gnomoria_en_ru.json'
    with open(target, 'w', encoding='utf-8') as f:
        json.dump(final_dict, f, ensure_ascii=False, indent=2)
    
    # Также в папку мода
    with open('D:/steam/steamapps/common/Gnomoria_RUS_Mod/Gnomoria_en_ru.json', 'w', encoding='utf-8') as f:
        json.dump(final_dict, f, ensure_ascii=False, indent=2)

    print(f"ULTRA-CLEAN dictionary generated: {len(final_dict)} entries.")

process()
