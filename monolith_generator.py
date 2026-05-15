import json
import os
import re

def get_full_translation_db():
    return {
        # --- UI & Menus ---
        "New Game": "Новая игра",
        "Options": "Настройки",
        "Steam Workshop": "Мастерская Steam",
        "Exit": "Выход",
        "Load Game": "Загрузить игру",
        "Delete": "Удалить",
        "Load": "Загрузить",
        "Loading": "Загрузка",
        "Back": "Назад",
        "Apply": "Применить",
        "Save": "Сохранить",
        "Cancel": "Отмена",
        "Suspend": "Пауза",
        "Resume": "Продолжить",
        "Display:": "Дисплей:",
        "Windowed": "Оконный режим",
        "Resolution:": "Разрешение:",
        "Custom:": "Свое:",
        "Controls": "Управление",
        "Gameplay": "Геймплей",
        "Audio": "Аудио",
        "Video": "Видео",
        "Vertical Sync": "Верт. синхронизация",

        # --- HUD & Stats ---
        "Depth": "Глубина",
        "Depth:": "Глубина:",
        "Food": "Еда",
        "Food:": "Еда:",
        "Drink": "Питье",
        "Drink:": "Питье:",
        "Sunrise": "Рассвет",
        "Sunrise:": "Рассвет:",
        "Sunset": "Закат",
        "Sunset:": "Закат:",
        "Year": "Год",
        "Spring": "Весна",
        "Summer": "Лето",
        "Autumn": "Осень",
        "Winter": "Зима",
        "day of": "день",
        "Worth": "Ценность",
        "Worth:": "Ценность:",
        "Total": "Всего",
        "Idle": "Бездельники",
        "Idle:": "Бездельники:",
        "Population": "Население",
        "Population:": "Население:",
        "Military": "Армия",
        "Events": "События",
        "Help": "Помощь",
        "Overview": "Сводка",

        # --- Professions ---
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

        # --- Materials ---
        "steel": "сталь", "iron": "железо", "lead": "свинец", "bronze": "бронза", "copper": "медь",
        "malachite": "малахит", "silver": "серебро", "gold": "золото", "rose gold": "роз. золото",
        "platinum": "платина", "tin": "олово", "metal": "металл", "ore": "руда", "bar": "слиток",
        "sliver": "стружка", "coal": "уголь", "silica": "кремнезем",
        "pine": "сосна", "orange wood": "апельсин", "wild strawberry": "земляника",
        "apple": "яблоко", "orange": "апельсин", "grape": "виноград", "strawberry": "земляника",
        "soil": "земля", "dirt": "грязь", "stone": "камень", "log": "бревно", "plank": "доска",
        "ceramic": "керамика", "bone": "кость", "thatch": "солома", "leather": "кожа",

        # --- Items ---
        "pickaxe": "кирка", "felling axe": "топор", "hand axe": "топорик", "sword": "меч", "hammer": "молот",
        "crossbow": "арбалет", "helmet": "шлем", "breastplate": "нагрудник", "pauldron": "наплечник",
        "greave": "поножи", "gauntlet": "перчатка", "boot": "ботинок", "shield": "щит",
        "crate": "ящик", "barrel": "бочка", "bag": "мешок", "bin": "контейнер",
        "workbench": "верстак", "furnace": "печь", "hearth": "очаг", "mold": "форма",
        "door": "дверь", "bed": "кровать", "table": "стол", "chair": "стул", "statue": "статуя",
        "torch": "факел", "pillar": "колонна", "Wall": "Стена", "Floor": "Пол", "Stairs": "Лестница",

        # --- Help/Tutorial Blocks ---
        "Gnomoria is a sandbox management game and is ": "Gnomoria — это симулятор управления гномами, ",
        "played by indirectly controlling your gnomes ": "где вы косвенно руководите ими, ",
        "by creating jobs for them, designating areas ": "создавая задачи и зоны, ",
        "of the world as specific places and adjusting ": "настраивая правила жизни. ",
        "settings. You can pause and unpause the game ": "Вы можете ставить игру на паузу, ",
        "at anytime to manage your kingdom and watch ": "чтобы управлять королевством, ",
        "your gnomes get to work. ": "наблюдая за работой гномов. ",
        "Each gnome needs to eat, drink and sleep and ": "Гномам нужно есть, пить и спать, ",
        "it's your job to help provide for them. As you ": "и ваша цель — обеспечить их этим. ",
        "build your kingdom, your overall worth will ": "С ростом ценности королевства, ",
        "increase, attracting more gnomes to join you as ": "вы будете привлекать кочевников ",
        "well as enemies who threaten your gnomes. ": "и новых опасных врагов. ",
        "Your only objective is to help your gnomes ": "Ваша цель — помочь гномам выжить ",
        "survive in this harsh world for as long as ": "в этом суровом мире так долго, ",
        "possible. ": "как это возможно. "
    }

def build_monolith():
    # Load all unique keys caught so far
    with open('C:/Users/Lecoo/projects/GnomoriaTranslator/Gnomoria_raw_catch.json', 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    keys = re.findall(r'\"([^\"]+)\"\s*:', content)
    unique_keys = set(keys)
    
    db = get_full_translation_db()
    # Sort by length descending for fragment replacement
    sorted_patterns = sorted(db.keys(), key=len, reverse=True)
    
    final_dict = {}
    for k in unique_keys:
        if not k.strip() or k == '?': continue
        
        # Fixed mapping (full match)
        if k in db:
            val = db[k]
        elif k == "v1.0":
            val = "v0.0.2 | memasevich 2026"
        else:
            # Fragment replacement
            val = k
            for pattern in sorted_patterns:
                # Use word boundaries for small words like 'iron' to avoid corrupting 'ironic'
                # But for Gnomoria, simple replace often works if we sort by length.
                if pattern.lower() in val.lower():
                    rep = db[pattern]
                    # Preserve case for first letter
                    val = val.replace(pattern, rep)
                    val = val.replace(pattern.capitalize(), rep.capitalize())
                    val = val.replace(pattern.lower(), rep)
        
        final_dict[k] = val

    # Save to file
    out_path = 'D:/steam/steamapps/common/Gnomoria/Gnomoria_en_ru.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(final_dict, f, ensure_ascii=False, indent=2)
    
    print(f"Monolith dictionary built: {len(final_dict)} entries.")

if __name__ == "__main__":
    build_monolith()
