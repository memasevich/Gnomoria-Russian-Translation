import json
import re

def get_mega_map():
    return {
        # --- БАЗОВЫЙ ИНТЕРФЕЙС ---
        "New Game": "Новая игра", "Options": "Настройки", "Exit": "Выход",
        "Load Game": "Загрузить игру", "Delete": "Удалить", "Load": "Загрузить",
        "Back": "Назад", "Apply": "Применить", "Save": "Сохранить",
        "Cancel": "Отмена", "Suspend": "Пауза", "Resume": "Продолжить",
        "Controls": "Управление", "Gameplay": "Геймплей", "Audio": "Аудио", "Video": "Видео",
        "Display:": "Дисплей:", "Windowed": "Оконный", "Resolution:": "Разрешение:",
        "Custom:": "Свое:", "Vertical Sync": "Верт. синхронизация",
        "Music Volume:": "Громкость музыки:", "Effects Volume:": "Громкость эффектов:",
        "Save every": "Автосохранение каждые", "days": "дня",
        "Kingdom Name": "Имя королевства", "Kingdom Size": "Размер мира",
        "Standard": "Стандартный", "Difficulty": "Сложность", "Normal": "Обычная",
        "Generate": "Создать", "Advanced Setup": "Настройки", "Default": "По умолчанию",

        # --- ГЛАВНЫЙ ЭКРАН (HUD) ---
        "Stocks": "Запасы", "Population": "Население", "Military": "Армия",
        "Events": "События", "Help": "Помощь", "Depth": "Глубина",
        "Food": "Еда", "Drink": "Питье", "Sunrise": "Рассвет", "Sunset": "Закат",
        "Year": "Год", "day of": "день", "Spring": "Весны", "Summer": "Лета", "Autumn": "Осени", "Winter": "Зимы",
        "Worth": "Ценность", "Total": "Всего", "Idle": "Бездельники", "Injured": "Раненые",
        "Deceased": "Погибшие", "Overview": "Сводка", "Rooms": "Комнаты", "Workshops": "Мастерские",
        "Diplomacy": "Дипломатия", "Friendly": "Друзья", "Distance": "Дистанция",
        "Sunrise:": "Рассвет:", "Sunset:": "Закат:", "Depth:": "Глубина:",

        # --- ПРОФЕССИИ И НАВЫКИ ---
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
        "Soldier": "Солдат", "Hauling": "Переноска", "Mining": "Горное дело", "Woodcutting": "Лесозаготовка",
        "Animal Husbandry": "Животноводство", "Butchery": "Убой", "Horticulture": "Садоводство",
        "Farming": "Земледелие", "Cooking": "Кулинария", "Brewing": "Пивоварение",
        "Crafting": "Крафт", "Stonecarving:": "Резьба по камню:", "Metalworking:": "Металлургия:",

        # --- МАТЕРИАЛЫ И МЕТАЛЛЫ ---
        "steel": "сталь", "iron": "железо", "lead": "свинец", "bronze": "бронза", "copper": "медь",
        "malachite": "малахит", "silver": "серебро", "gold": "золото", "rose gold": "роз. золото",
        "platinum": "платина", "tin": "олово", "metal": "металл", "ore": "руда", "bar": "слиток",
        "sliver": "стружка", "coal": "уголь", "silica": "кремнезем",
        "pine": "сосна", "orange wood": "апельсин", "wild strawberry": "земляника",
        "apple": "яблоко", "orange": "апельсин", "grape": "виноград", "strawberry": "земляника",
        "soil": "земля", "dirt": "грязь", "stone": "камень", "log": "бревно", "plank": "доска",
        "ceramic": "керамика", "bone": "кость", "thatch": "солома", "leather": "кожа",

        # --- ПРЕДМЕТЫ И ПОСТРОЙКИ ---
        "pickaxe": "кирка", "felling axe": "топор", "hand axe": "топорик", "sword": "меч", "hammer": "молот",
        "crossbow": "арбалет", "helmet": "шлем", "breastplate": "нагрудник", "pauldron": "наплечник",
        "greave": "поножи", "gauntlet": "перчатка", "boot": "ботинок", "shield": "щит",
        "crate": "ящик", "barrel": "бочка", "bag": "мешок", "bin": "контейнер",
        "workbench": "верстак", "furnace": "печь", "hearth": "очаг", "mold": "форма",
        "door": "дверь", "bed": "кровать", "table": "стол", "chair": "стул", "statue": "статуя",
        "torch": "факел", "pillar": "колонна", "scaffolding": "леса",
        "Wall": "Стена", "Floor": "Пол", "Stairs": "Лестница", "Ramp": "Скат", "Hole": "Яма",

        # --- СПЕЦИАЛЬНЫЕ ФРАЗЫ ---
        "is in good health": "в добром здравии", "Nothing": "Ничего", "worn": "изнош.",
        "LeftShift": "Лев. Shift", "LeftControl": "Лев. Ctrl", "SpaceBar": "Пробел",
        "Bookmark": "Закладка", "Set Bookmark": "Уст. закладку", "Action Button": "Кнопка",
        "Show Action Bar": "Показать панель", "Show Stockpiles": "Показать склады",
        "Nourishment": "Сытость", "Weight": "Вес", "Closest": "Ближе", "Best": "Лучше",

        # --- ТЕКСТ ПОМОЩИ (ФРАГМЕНТЫ) ---
        "Gnomoria is a sandbox management game and is ": "Gnomoria — симулятор управления гномами, ",
        "played by indirectly controlling your gnomes ": "где вы косвенно руководите ими, ",
        "by creating jobs for them, designating areas ": "создавая задачи и зоны, ",
        "of the world as specific places and adjusting ": "настраивая правила мира. ",
        "settings. You can pause and unpause the game ": "Вы можете ставить игру на паузу, ",
        "at anytime to manage your kingdom and watch ": "чтобы управлять королевством, ",
        "your gnomes get to work. ": "наблюдая за работой гномов. ",
        "Each gnome needs to eat, drink and sleep and ": "Гномам нужно есть, пить и спать, ",
        "it's your job to help provide for them. As you ": "и ваша цель — обеспечить их этим. ",
        "build your kingdom, your overall worth will ": "С ростом ценности королевства, ",
        "increase, attracting more gnomes to join you as ": "вы будете привлекать гномадов ",
        "well as enemies who threaten your gnomes. ": "и новых врагов. ",
        "Your only objective is to help your gnomes ": "Ваша цель — помочь гномам выжить ",
        "survive in this harsh world for as long as ": "в этом суровом мире так долго, ",
        "possible. ": "как только возможно. "
    }

def process():
    # Берем самый свежий дамп из игры
    with open('D:/steam/steamapps/common/Gnomoria/Gnomoria_en_ru.json', 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Чистим ключи
    keys = re.findall(r'\"([^\"]+)\"\s*:', content)
    m = get_mega_map()
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

    # Пишем напрямую в папку игры
    target = 'D:/steam/steamapps/common/Gnomoria/Gnomoria_en_ru.json'
    with open(target, 'w', encoding='utf-8') as f:
        json.dump(final_dict, f, ensure_ascii=False, indent=2)
    
    # Дублируем в папку мода
    with open('D:/steam/steamapps/common/Gnomoria_RUS_Mod/Gnomoria_en_ru.json', 'w', encoding='utf-8') as f:
        json.dump(final_dict, f, ensure_ascii=False, indent=2)

    print(f"ULTRA-DICT generated: {len(final_dict)} entries.")

process()
