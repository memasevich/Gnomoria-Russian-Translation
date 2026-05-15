import json

def get_translation_map():
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

def process():
    # Load the big catch (1334 strings)
    with open('C:/Users/Lecoo/projects/GnomoriaTranslator/Gnomoria_raw_catch.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    t_map = get_translation_map()
    
    # Sort keys by length descending to avoid partial matches (e.g., 'iron' vs 'iron bar')
    sorted_mats = sorted(t_map.keys(), key=len, reverse=True)
    
    final = {}
    for k in data:
        # Start with original or existing
        val = k
        
        # Apply mapping
        processed = k
        for eng in sorted_mats:
            if eng in processed.lower():
                # Case sensitive replacement for start of sentence
                rus = t_map[eng]
                processed = processed.replace(eng, rus)
                processed = processed.replace(eng.capitalize(), rus.capitalize())
        
        # Watermark
        if k == "v1.0":
            val = "v0.0.2 | memasevich 2026"
        else:
            val = processed
            
        final[k] = val

    with open('C:/Users/Lecoo/projects/GnomoriaTranslator/Gnomoria_TOTAL_CLEAN.json', 'w', encoding='utf-8') as f:
        json.dump(final, f, ensure_ascii=False, indent=2)
    
    print(f"Total processed: {len(final)}")

process()
