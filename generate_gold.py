import json
import os

def get_master_map():
    return {
        # Metals & Minerals
        "steel": "сталь", "iron": "железо", "lead": "свинец", "bronze": "бронза", "copper": "медь",
        "malachite": "малахит", "silver": "серебро", "gold": "золото", "rose gold": "розовое золото",
        "platinum": "платина", "tin": "олово", "metal": "металл", "ore": "руда", "bar": "слиток",
        "sliver": "стружка", "coal": "уголь", "silica": "кремнезем",

        # Wood & Plants
        "pine": "сосна", "orange wood": "апельсиновое дерево", "apple": "яблоко", "strawberry": "земляника",
        "orange": "апельсин", "grape": "виноград", "wild": "дикая", "tree": "дерево", "plant": "растение",
        "clipping": "побег", "grain": "зерно", "straw": "солома", "log": "бревно", "plank": "доска",
        "stick": "палка", "thatch": "солома",

        # Stone & Soil
        "soil": "земля", "dirt": "грязь", "stone": "камень", "raw stone": "необр. камень", "block": "блок",
        "tile": "плитка", "chiseled": "тесаный", "engraved": "гравированный", "smooth": "гладкий",
        "carved": "резной", "decorative": "декоративный", "clay": "глина", "ceramic": "керамика",

        # Items & Tools
        "pickaxe": "кирка", "felling axe": "топор лесоруба", "hand axe": "ручной топор", "battle axe": "боевой топор",
        "sword": "меч", "claymore": "клеймор", "hammer": "молот", "warhammer": "боевой молот",
        "crossbow": "арбалет", "bolt": "болт", "quiver": "колчан", "pistol": "пистолет", "blunderbuss": "мушкетон",
        "helmet": "шлем", "breastplate": "нагрудник", "pauldron": "наплечник", "greave": "поножи",
        "gauntlet": "перчатка", "boot": "ботинок", "shield": "щит", "platemail": "латный доспех",
        "cuirass": "кираса", "bracer": "наруч", "glove": "перчатка", "shirt": "рубаха",
        "crate": "ящик", "barrel": "бочка", "bag": "мешок", "bin": "контейнер",
        "workbench": "верстак", "furnace": "печь", "hearth": "очаг", "mold": "форма",
        "anvil": "наковальня", "loom": "ткацкий станок", "wheelbarrow": "тачка", "bucket": "ведро",
        "chisel": "зубило", "knife": "нож", "sawblade": "лезвие пилы", "file": "напильник",
        "wrench": "ключ", "bellows": "мехи", "bandage": "бинт", "mattress": "матрас",
        "statuette": "статуэтка", "rock": "камень", "puzzle box": "шкатулка", "coin": "монета",
        "ring": "кольцо", "necklace": "ожерелье", "bone needle": "костяная игла",

        # Food & Drink
        "meat": "мясо", "sausage": "сосиска", "bread": "хлеб", "sandwich": "сэндвич", "mushroom": "гриб",
        "cheese": "сыр", "omelette": "омлет", "egg": "яйцо", "milk": "молоко", "wine": "вино",
        "beer": "пиво", "tea": "чай", "food": "еда", "drink": "питье",

        # Professions & Skills
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

        # UI & Actions
        "New Game": "Новая игра", "Options": "Настройки", "Steam Workshop": "Мастерская Steam",
        "Exit": "Выход", "Controls": "Управление", "Gameplay": "Геймплей", "Audio": "Аудио",
        "Video": "Видео", "Display:": "Дисплей:", "Windowed": "Оконный", "Resolution:": "Разрешение:",
        "Custom:": "Свое:", "Vertical Sync": "Верт. синхронизация", "Back": "Назад", "Apply": "Применить",
        "Load Game": "Загрузить игру", "Delete": "Удалить", "Load": "Загрузить",
        "Save": "Сохранить", "Cancel": "Отмена", "Suspend": "Пауза", "Resume": "Продолжить",
        "Mine Wall": "Копать стену", "Mine Stairs": "Копать лестницу", "Mine Ramp": "Копать скат",
        "Dig Hole": "Рыть яму", "Replace Wall": "Заменить стену", "Replace Floor": "Заменить пол",
        "Build": "Строить", "Deconstruct": "Разобрать", "Remove": "Удалить",
        "Stockpile": "Склад", "Farm": "Ферма", "Pasture": "Пастбище", "Grove": "Роща",
        "Kingdom": "Королевство", "Stocks": "Запасы", "Population": "Население", "Military": "Армия",
        "Events": "События", "Help": "Помощь", "Overview": "Сводка", "Rooms": "Комнаты",
        "Diplomacy": "Дипломатия", "Deceased": "Погибшие", "Injured": "Раненые",
        "Uniform": "Униформа", "Formation": "Построение", "Squad": "Отряд", "Enemy": "Враг",

        # Grammar/Misc
        "day of": "день", "Spring": "Весны", "Summer": "Лета", "Autumn": "Осени", "Winter": "Зимы",
        "Year": "Год", "Depth": "Глубина", "Worth": "Ценность", "Total": "Всего", "Idle": "Бездельник",
        "Nothing": "Ничего", "Good": "Хорошо", "Female": "Жен.", "Male": "Муж.", "Race": "Раса",
        "Gender": "Пол", "Joined": "Вступил", "is in good health": "в добром здравии"
    }

def generate_clean_dictionary():
    # Мы НЕ читаем старые файлы, мы берем только чистые английские ключи 
    # из последнего дампа и применяем к ним перевод.
    with open('C:/Users/Lecoo/projects/GnomoriaTranslator/Gnomoria_raw_catch.json', 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    import re
    # Извлекаем все ключи в кавычках (только латиница и знаки препинания)
    keys = re.findall(r'\"([a-zA-Z0-9\s\.\:\(\)\-\,\'\/]+)\"\s*:', content)
    
    m = get_master_map()
    sorted_keys = sorted(m.keys(), key=len, reverse=True)
    
    final_dict = {}
    for k in set(keys):
        if k == "v1.0":
            final_dict[k] = "v0.0.2 | memasevich 2026"
            continue
            
        val = k
        for eng in sorted_keys:
            if eng.lower() in val.lower():
                rus = m[eng]
                # Умная замена (регистр)
                val = val.replace(eng, rus)
                val = val.replace(eng.capitalize(), rus.capitalize())
                val = val.replace(eng.lower(), rus)
        
        final_dict[k] = val

    # Сохраняем как PURE_GOLD.json
    output_path = 'C:/Users/Lecoo/projects/GnomoriaTranslator/Gnomoria_PURE_GOLD.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_dict, f, ensure_ascii=False, indent=2)
    
    print(f"Master dictionary generated: {len(final_dict)} strings.")

generate_clean_dictionary()
