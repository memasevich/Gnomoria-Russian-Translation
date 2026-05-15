import json
import re

def get_db():
    return {
        # --- НОВОЕ ИЗ WIKI ---
        "Sandstone": "песчаник", "Serpentine": "серпентин", "Bauxite": "боксит",
        "Granite": "гранит", "Basalt": "базальт", "Marble": "мрамор", "Lapis Lazuli": "лазурит",
        "Tin": "олово", "Lead": "свинец", "Platinum": "платина",
        "Birch": "береза", "Cedar": "кедр", "Walnut": "орех", "Cherry": "вишня",
        "Sapphire": "сапфир", "Emerald": "изумруд", "Bear": "медведь", "Ogre": "огр",
        "Raw Hide": "шкура", "Bear Hide": "медвежья шкура", "Ogre Hide": "шкура огра",
        "Cotton": "хлопок", "Wool": "шерсть", "Silk": "шелк",
        
        # --- БАЗОВЫЕ ПОНЯТИЯ ---
        "Kingdom": "Королевство", "Stocks": "Запасы", "Population": "Население",
        "Military": "Армия", "Events": "События", "Help": "Помощь",
        "Sunset": "Закат", "Sunrise": "Рассвет", "Depth": "Глубина",
        "Food": "Еда", "Drink": "Питье", "Year": "Год", "Day": "День",
        "Spring": "Весна", "Summer": "Лето", "Autumn": "Осень", "Winter": "Зима",
        "Loading": "Загрузка", "Load": "Загрузить", "Save": "Сохранить",
        "New Game": "Новая игра", "Options": "Настройки", "Exit": "Выход",
        "Back": "Назад", "Apply": "Применить", "Cancel": "Отмена",
        "Delete": "Удалить", "Name": "Имя", "Size": "Размер",
        "Difficulty": "Сложность", "Normal": "Обычная", "Standard": "Стандарт",
        "Tree": "дерево", "Wall": "стена", "Floor": "пол", "Stairs": "лестница",
        "Ramp": "скат", "Hole": "яма", "Workbench": "верстак", "Workshop": "мастерская",
        "Farm": "ферма", "Pasture": "пастбище", "Grove": "роща", "Room": "комната",
        "Hospital": "госпиталь", "Stockpile": "склад", "Area": "зона",
        
        # --- МАТЕРИАЛЫ ---
        "steel": "сталь", "iron": "железо", "lead": "свинец", "bronze": "бронза",
        "copper": "медь", "silver": "серебро", "gold": "золото", "tin": "олово",
        "pine": "сосна", "orange wood": "апельсин", "wild": "дикий",
        "apple": "яблоко", "strawberry": "клубника", "grape": "виноград",
        "dirt": "земля", "soil": "земля", "stone": "камень", "log": "бревно",
        "plank": "доска", "block": "блок", "ceramic": "керамика", "bone": "кость",
        "leather": "кожа", "thatch": "солома", "cloth": "ткань", "fiber": "волокно",
        "malachite": "малахит",
        
        # --- ПРЕДМЕТЫ ---
        "pickaxe": "кирка", "axe": "топор", "sword": "меч", "hammer": "молот",
        "helmet": "шлем", "breastplate": "нагрудник", "pauldron": "наплечник",
        "greave": "поножи", "gauntlet": "перчатка", "boot": "сапог", "shield": "щит",
        "crate": "ящик", "barrel": "бочка", "bag": "мешок", "bin": "контейнер",
        "torch": "факел", "pillar": "колонна", "statue": "статуя", "bed": "кровать",
        "chair": "стул", "table": "стол", "door": "дверь", "mechanism": "механизм",
        
        # --- ИНТЕРФЕЙС / ГЛАГОЛЫ ---
        "Show": "Показать", "Hide": "Скрыть", "Build": "Строить", "Mine": "Рыть",
        "Dig": "Копать", "Cut": "Срезать", "Fell": "Рубить", "Plant": "Сажать",
        "Replace": "Заменить", "Remove": "Убрать", "Deconstruct": "Разобрать",
        "Designate": "Разметить", "Suspend": "Пауза", "Resume": "Пуск",
        "Overview": "Сводка", "Diplomacy": "Дипломатия", "Deceased": "Погибшие",
        "Injured": "Раненые", "Idle": "Бездельники", "Total": "Всего",
        "Worth": "Ценность", "Friendly": "Друзья", "Distance": "Путь",
        "Gameplay": "Игра", "Controls": "Управление", "Audio": "Звук", "Video": "Видео",
        
        # --- ФРАГМЕНТЫ ПРЕДЛОЖЕНИЙ ---
        "played by": "управляя", "controlling your": "вашими", "creating jobs": "создавая задачи",
        "of the world": "мира", "at anytime": "в любое время", "to manage": "для управления",
        "watch your": "наблюдайте за", "get to work": "за работой", "needs to": "нужно",
        "it's your job": "ваша задача", "to help": "помочь", "provide for": "обеспечить",
        "survive in": "выжить в", "harsh world": "суровом мире", "takes place": "происходит",
        "split into": "разбит на", "3D world": "3D мир", "many resources": "кучу ресурсов",
        "fully deformable": "изменяем", "used to be": "использовать для", "crafted into": "крафта",
        "new items": "новых вещей"
    }

def run():
    with open('C:/Users/Lecoo/projects/GnomoriaTranslator/Gnomoria_raw_catch.json', 'r', encoding='utf-8', errors='ignore') as f:
        keys = re.findall(r'\"([^\"]+)\"\s*:', f.read())
    
    db = get_db()
    sorted_pats = sorted(db.keys(), key=len, reverse=True)
    
    final = {}
    obsidian_md = "# Wiki-Master База перевода (v3.9)\n\n| English | Russian |\n| --- | --- |\n"
    
    for k in set(keys):
        if not k.strip() or k == '?': continue
        val = k
        if k == "v1.0": val = "v0.0.2 | memasevich 2026"
        else:
            for p in sorted_pats:
                pattern = re.compile(re.escape(p), re.IGNORECASE)
                def rep_f(m):
                    r = db[p]
                    orig = m.group(0)
                    if orig.isupper(): return r.upper()
                    if orig[0].isupper(): return r.capitalize()
                    return r
                val = pattern.sub(rep_f, val)
        
        val = re.sub(r'\s+', ' ', val).strip()
        final[k] = val
        obsidian_md += f"| {k} | {val} |\n"

    # Запись в игру
    with open('D:/steam/steamapps/common/Gnomoria/Gnomoria_en_ru.json', 'w', encoding='utf-8') as f:
        json.dump(final, f, ensure_ascii=False, indent=2)
    
    # Синхронизация Obsidian
    with open('C:/Obsidian/obsidian-hesh/Проекты/GnomoriaTranslator/Словарь_перевода.md', 'w', encoding='utf-8') as f:
        f.write(obsidian_md)
    
    print(f"OMNI-DICT v3.9 generated: {len(final)} strings. Added Wiki materials.")

run()
