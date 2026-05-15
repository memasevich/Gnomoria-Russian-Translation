import json
import re

def get_exhaustive_map():
    return {
        # --- MATERIALS (METALS) ---
        "Tin": "олово", "Malachite": "малахит", "Copper": "медь", "Bronze": "бронза",
        "Lead": "свинец", "Iron": "железо", "Steel": "сталь", "Silver": "серебро",
        "Gold": "золото", "Platinum": "платина", "Rose Gold": "роз. золото",
        "metal": "металл", "ore": "руда", "bar": "слиток", "sliver": "стружка", "coal": "уголь",
        
        # --- MATERIALS (STONE) ---
        "Basalt": "базальт", "Bauxite": "боксит", "Granite": "гранит", "Lapis Lazuli": "лазурит",
        "Marble": "мрамор", "Sandstone": "песчаник", "Serpentine": "серпентин", "stone": "камень",
        "raw stone": "необр. камень", "block": "блок", "tile": "плитка", "clay": "глина",
        "ceramic": "керамика", "silica": "кремнезем",
        
        # --- MATERIALS (WOOD) ---
        "Pine": "сосна", "Birch": "береза", "Apple Wood": "яблоня", "Orange Wood": "апельсин",
        "Cedar": "кедр", "Walnut": "орех", "Cherry": "вишня", "wood": "дерево", "tree": "дерево",
        "log": "бревно", "plank": "доска", "stick": "палка", "thatch": "солома",
        
        # --- MATERIALS (ORGANIC) ---
        "Raw Hide": "шкура", "Bear Hide": "шкура медведя", "Ogre Hide": "шкура огра",
        "Leather": "кожа", "Bone": "кость", "Skull": "череп", "Cotton": "хлопок",
        "Wool": "шерсть", "Silk": "шелк", "Fiber": "волокно", "Cloth": "ткань",
        
        # --- FURNITURE ---
        "Straw Bed": "соломенная кровать", "Bed": "кровать", "Four Poster Bed": "кровать с балдахином",
        "Table": "стол", "Chair": "стул", "Torch": "факел", "Statue": "статуя", "Statuette": "статуэтка",
        "Door": "дверь", "Dresser": "комод", "Cabinet": "шкаф", "Pillar": "колонна",
        "Crate": "ящик", "Barrel": "бочка", "Bag": "мешок", "Bin": "контейнер",
        
        # --- WEAPONS & ARMOR ---
        "Pickaxe": "кирка", "Felling Axe": "топор", "Hand Axe": "топорик", "Battle Axe": "боевой топор",
        "Sword": "меч", "Claymore": "клеймор", "Hammer": "молот", "Warhammer": "боевой молот",
        "Crossbow": "арбалет", "Bolt": "болт", "Quiver": "колчан", "Pistol": "пистолет",
        "Blunderbuss": "мушкетон", "Helmet": "шлем", "Breastplate": "нагрудник", "Pauldron": "наплечник",
        "Greave": "поножи", "Gauntlet": "перчатка", "Boot": "сапог", "Shield": "щит",
        "Platemail": "латный доспех", "Cuirass": "кираса", "Bracer": "наруч", "Glove": "перчатка",
        "Shirt": "рубаха", "Worn": "изнош.", "Quality": "качество",
        
        # --- MECHANISMS ---
        "Hand Crank": "рукоятка", "Windmill": "ветряк", "Steam Engine": "паровой двигатель",
        "Axle": "ось", "Vertical Axle": "верт. ось", "Gear Box": "коробка передач",
        "Lever": "рычаг", "Pressure Plate": "нажимная плита", "Mechanical Wall": "мех. стена",
        "Hatch": "люк", "Pump": "насос", "Spike Trap": "ловушка-шипы", "Blade Trap": "ловушка-лезвия",
        "mechanism": "механизм", "linkage": "передача", "switch": "переключатель",
        
        # --- WORKSHOPS ---
        "Crude Workshop": "примитивный верстак", "Sawmill": "лесопилка", "Carpenter": "плотник",
        "Woodcarver": "резчик по дереву", "Stonecutter": "камнерез", "Stonemason": "каменщик",
        "Stonecarver": "резчик по камню", "Furnace": "печь", "Forge": "кузница",
        "Blacksmith": "слесарная", "Metalworker": "металлообработка", "Weaponsmith": "оружейная",
        "Armorer": "броня", "Loom": "ткацкий станок", "Tailor": "портной", "Leatherworker": "кожевник",
        "Bonecarver": "костерез", "Butcher": "мясник", "Kitchen": "кухня", "Distillery": "пивоварня",
        "Tinker Bench": "верстак жестянщика", "Machine Shop": "машинный цех", "Engineer Shop": "инженерный цех",
        "Jeweler": "ювелирная", "Gemcutter": "огранщик", "Kiln": "обжиговая печь",
        "Market Stall": "прилавок", "Training Grounds": "тренировочная площадка", "Well": "колодец",
        
        # --- DESIGNATIONS ---
        "Stockpile": "склад", "Farm": "ферма", "Pasture": "пастбище", "Grove": "роща",
        "Personal Quarters": "личные покои", "Dormitory": "казарма", "Dining Room": "столовая",
        "Hospital": "госпиталь", "Great Hall": "большой зал", "Guard Area": "зона охраны",
        "Patrol Route": "маршрут патруля", "Hospital Bed": "больничная койка",
        
        # --- PROFESSIONS & SKILLS ---
        "Miner": "Шахтер", "Mason": "Каменщик", "Woodcutter": "Дровосек", "Farmer": "Фермер",
        "Rancher": "Животновод", "Builder": "Строитель", "Engineer": "Инженер",
        "Blacksmith": "Кузнец", "Jeweler": "Ювелир", "Chef": "Повар", "Brewer": "Пивовар",
        "Medic": "Медик", "Caretaker": "Смотритель", "Hauler": "Носильщик", "Soldier": "Солдат",
        "Mining": "Шахтерство", "Masonry": "Каменное дело", "Woodcutting": "Лесозаготовка",
        "Carpentry": "Плотничество", "Smelting": "Плавка", "Animal Husbandry": "Животноводство",
        "Butchery": "Убой", "Horticulture": "Садоводство", "Farming": "Земледелие",
        "Cooking": "Кулинария", "Brewing": "Пивоварение", "Medicine": "Медицина",
        "Prospecting": "Поиск руды", "Pottery": "Гончарное дело", "Tinkering": "Жестяное дело",
        
        # --- COMBAT & STATS ---
        "Fighting": "Борьба", "Brawling": "Драка", "Dodge": "Уворот", "Fighting:": "Борьба:",
        "Fitness": "Сила", "Nimbleness": "Ловкость", "Curiosity": "Любознательность",
        "Focus": "Внимание", "Charm": "Обаяние", "Health": "Здоровье", "Injured": "Ранен",
        "Deceased": "Погиб", "Idle": "Бездельник", "Status": "Статус",
        
        # --- UI BASIC ---
        "New Game": "Новая игра", "Options": "Настройки", "Steam Workshop": "Мастерская Steam",
        "Exit": "Выход", "Back": "Назад", "Apply": "Применить", "Save": "Сохранить",
        "Cancel": "Отмена", "Delete": "Удалить", "Load": "Загрузить", "Loading": "Загрузка",
        "Kingdom": "Королевство", "Stocks": "Запасы", "Population": "Население",
        "Military": "Армия", "Events": "События", "Help": "Помощь", "Overview": "Сводка",
        "Sunrise": "Рассвет", "Sunset": "Закат", "Year": "Год", "Day": "День",
        "Spring": "Весна", "Summer": "Лето", "Autumn": "Осень", "Winter": "Зима",
        "Display:": "Дисплей:", "Resolution:": "Разрешение:", "Windowed": "Оконный",
        
        # --- VERBS ---
        "Build": "Строить", "Mine": "Рыть", "Dig": "Копать", "Replace": "Заменить",
        "Remove": "Убрать", "Deconstruct": "Разобрать", "Show": "Показать", "Hide": "Скрыть"
    }

def run():
    import json, re, os
    
    # 1. Читаем все наловленные ключи
    raw_path = 'C:/Users/Lecoo/projects/GnomoriaTranslator/Gnomoria_raw_catch.json'
    with open(raw_path, 'r', encoding='utf-8', errors='ignore') as f:
        keys = re.findall(r'\"([^\"]+)\"\s*:', f.read())
    
    db = get_exhaustive_map()
    # Сортируем от самых длинных к самым коротким
    sorted_pats = sorted(db.keys(), key=len, reverse=True)
    
    final = {}
    obsidian_md = "# Exhaustive Gnomoria Dictionary (v4.0 Final)\n\n| English | Russian |\n| --- | --- |\n"
    
    for k in set(keys):
        if not k.strip() or k == '?': continue
        
        val = k
        if k == "v1.0": 
            val = "v1.0  |  memasevich 2026"
        else:
            # Умный регистронезависимый перевод фрагментов
            # Мы идем по отсортированному списку патернов
            for p in sorted_pats:
                # Регулярка для замены слова (с учетом границ слов \b для коротких материалов)
                # Чтобы 'iron' не ломало 'ironic', но ловило 'iron bar'
                pattern_str = re.escape(p)
                # Если патерн короткий (меньше 4 букв) - используем границы слов
                if len(p) <= 4:
                    pattern = re.compile(r'\b' + pattern_str + r'\b', re.IGNORECASE)
                else:
                    pattern = re.compile(pattern_str, re.IGNORECASE)
                
                def replace_func(match):
                    rus = db[p]
                    original = match.group(0)
                    if original.isupper(): return rus.upper()
                    if original[0].isupper(): return rus.capitalize()
                    return rus
                
                val = pattern.sub(replace_func, val)
        
        # Очистка двойных пробелов
        val = re.sub(r'\s+', ' ', val).strip()
        final[k] = val
        obsidian_md += f"| {k} | {val} |\n"

    # Запись в игру
    with open('D:/steam/steamapps/common/Gnomoria/Gnomoria_en_ru.json', 'w', encoding='utf-8') as f:
        json.dump(final, f, ensure_ascii=False, indent=2)
    
    # Запись в Obsidian
    with open('C:/Obsidian/obsidian-hesh/Проекты/GnomoriaTranslator/Словарь_перевода.md', 'w', encoding='utf-8') as f:
        f.write(obsidian_md)
    
    print(f"EXHAUSTIVE-DICT v4.0 generated: {len(final)} strings. Wiki-based mapping complete.")

run()
