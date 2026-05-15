import json
import re

def get_master_map():
    return {
        # --- ТЕКСТ ОБУЧЕНИЯ И ПОМОЩИ ---
        "Gnomoria is a sandbox management game and is ": "Gnomoria — это песочница и симулятор управления, ",
        "played by indirectly controlling your gnomes ": "где вы косвенно управляете гномами, ",
        "by creating jobs for them, designating areas ": "создавая задачи, размечая зоны ",
        "of the world as specific places and adjusting ": "и настраивая правила жизни. ",
        "settings. You can pause and unpause the game ": "Вы можете ставить игру на паузу в любой момент, ",
        "at anytime to manage your kingdom and watch ": "чтобы управлять королевством или наблюдать, ",
        "your gnomes get to work. ": "как гномы трудятся. ",
        "Each gnome needs to eat, drink and sleep and ": "Каждому гному нужно есть, пить и спать, ",
        "it's your job to help provide for them. As you ": "и ваша задача — обеспечить их этим. По мере ",
        "build your kingdom, your overall worth will ": "роста королевства растет его ценность, ",
        "increase, attracting more gnomes to join you as ": "привлекая новых гномадов и, увы, врагов, ",
        "well as enemies who threaten your gnomes. ": "которые будут вам угрожать. ",
        "Your only objective is to help your gnomes ": "Ваша единственная цель — помочь гномам ",
        "survive in this harsh world for as long as ": "выживать в этом суровом мире так долго, ",
        "possible. ": "как это возможно. ",
        "Gnomoria takes place in a randomly generated ": "Действие происходит в случайно сгенерированном ",
        "3D world with many resources to discover and ": "3D-мире с ресурсами для добычи. ",
        "harvest. ": " ",
        "The world is split into a 3D grid of cells and is ": "Мир разбит на 3D-сетку клеток и полностью ",
        "fully deformable. Each cell can be harvested ": "изменяем. Любую клетку можно вскопать ",
        "for its resource and used to be rebuilt ": "и использовать материалы для стройки ",
        "elsewhere or crafted into new items. ": "или крафта новых предметов. ",
        
        # --- СТАНДАРТНЫЙ СЛОВАРЬ (МАСТЕР) ---
        "New Game": "Новая игра", "Options": "Настройки", "Steam Workshop": "Мастерская Steam",
        "Exit": "Выход", "v1.0": "v0.0.2 | memasevich 2026", "Controls": "Управление",
        "Gameplay": "Геймплей", "Audio": "Аудио", "Video": "Видео", "Display:": "Дисплей:",
        "Windowed": "Оконный", "Resolution:": "Разрешение:", "Custom:": "Свое:",
        "Vertical Sync": "Верт. синхронизация", "Back": "Назад", "Apply": "Применить",
        "Load Game": "Загрузить игру", "Delete": "Удалить", "Load": "Загрузить",
        "Save": "Сохранить", "Cancel": "Отмена", "Suspend": "Пауза", "Resume": "Продолжить",
        "Mine Wall": "Копать стену", "Mine Stairs": "Копать лестницу", "Mine Ramp": "Копать скат",
        "Dig Hole": "Рыть яму", "Replace Wall": "Заменить стену", "Replace Floor": "Заменить пол",
        "Plant Tree": "Посадить дерево", "Fell Tree": "Срубить дерево", "Cut Clipping": "Срезать побег",
        "Forage": "Собирательство", "Build Workshop": "Построить мастерскую", "Mechanism": "Механизм",
        "Furniture": "Мебель", "Floor": "Пол", "Stockpile": "Склад", "Farm": "Ферма", "Pasture": "Пастбище",
        "Dormitory": "Казарма", "Dining Room": "Столовая", "Hospital": "Госпиталь", "Clean": "Очистить",
        "Deconstruct": "Разобрать", "Remove Designation": "Снять разметку", "Cancel Job": "Отменить работу",
        "Generating Map": "Генерация карты", "Settling Liquids": "Расчет жидкостей", "Kingdom": "Королевство",
        "Stocks": "Запасы", "Population": "Население", "Military": "Армия", "Events": "События",
        "Help": "Помощь", "Sunrise": "Рассвет", "Sunset": "Закат", "Overview": "Сводка",
        "Rooms": "Комнаты", "Workshops": "Мастерские", "Diplomacy": "Дипломатия",
        "Stock Worth:": "Запасы:", "Construction Worth:": "Постройки:", "Total Worth:": "Ценность:",
        "Friendly": "Дружелюбно", "Distance": "Дистанция", "Idle": "Бездельники", "Injured": "Раненые",
        "Deceased": "Погибшие", "Professions": "Профессии", "Assign": "Назначить", "Cap": "Лимит",
        "Skills": "Навыки", "Miner": "Шахтер", "Mason": "Каменщик", "Stonecarver": "Резчик по камню",
        "Woodcutter": "Дровосек", "Carpenter": "Плотник", "Woodcarver": "Резчик по дереву",
        "Smelter": "Плавильщик", "Blacksmith": "Кузнец", "Metalworker": "Металлург",
        "Weaponsmith": "Оружейник", "Armorer": "Бронник", "Gemcutter": "Огранщик",
        "Jeweler": "Ювелир", "Weaver": "Ткач", "Tailor": "Портной", "Potter": "Гончар",
        "Leatherworker": "Кожевник", "Bonecarver": "Резчик по кости", "Prospector": "Старатель",
        "Tinkerer": "Жестянщик", "Machinist": "Машинист", "Engineer": "Инженер",
        "Mechanic": "Механик", "Rancher": "Животновод", "Butcher": "Мясник",
        "Gardener": "Садовник", "Farmer": "Фермер", "Chef": "Повар", "Brewer": "Пивовар",
        "Medic": "Медик", "Caretaker": "Смотритель", "Builder": "Строитель", "Hauler": "Носильщик",
        "Soldier": "Солдат", "Agriculture": "Сельское хоз-во", "Misc": "Разное", "Uniform": "Униформа",
        "Mining": "Шахта", "Build": "Стройка", "Grove": "Роща", "Hauling": "Переноска",
        "Squads": "Отряды", "Enemies": "Враги", "Formation": "Построение", "Leader": "Лидер",
        "Attack": "Атака", "Defend": "Защита", "Avoid": "Избегать", "Retreat": "Отступить",
        "helmet": "шлем", "breastplate": "нагрудник", "pauldron": "наплечник", "greave": "поножи",
        "gauntlet": "перчатка", "boot": "ботинок", "shield": "щит", "Combat": "Бой",
        "Crafting": "Крафт", "Terrain": "Ландшафт", "Wall": "Стена", "Stairs": "Лестница",
        "Ramp": "Скат", "Hole": "Яма", "Storage": "Склад", "door": "дверь", "bed": "кровать",
        "table": "стол", "chair": "стул", "statue": "статуя", "torch": "факел", "pillar": "колонна",
        "crate": "ящик", "barrel": "бочка", "bag": "мешок", "Import/Export": "Импорт/Экспорт",
        "Save and Exit": "Сохранить и выйти", "Load Game": "Загрузить игру",
        "Spring": "Весна", "Summer": "Лето", "Autumn": "Осень", "Winter": "Зима",
        "steel": "сталь", "iron": "железо", "lead": "свинец", "bronze": "бронза", "copper": "медь",
        "malachite": "малахит", "silver": "серебро", "gold": "золото", "rose gold": "розовое золото",
        "platinum": "платина", "tin": "олово", "pine": "сосна", "orange wood": "апельсиновое дерево",
        "wild strawberry": "земляника", "apple": "яблоко", "orange": "апельсин", "grape": "виноград",
        "dirt": "земля", "soil": "земля", "stone": "камень", "log": "бревно", "plank": "доска",
        "metal": "металл", "ceramic": "керамика", "bone": "кость", "thatch": "солома",
        "is in good health": "в добром здравии", "Nothing": "Ничего", "Gender": "Пол",
        "Female": "Жен.", "Male": "Муж.", "Race": "Раса", "Joined": "Вступил", "Status": "Статус",
        "Name": "Имя", "Attributes": "Характеристики", "Fighting": "Борьба", "Brawling": "Драка",
        "Sword": "Меч", "Axe": "Топор", "Hammer": "Молот", "Crossbow": "Арбалет", "Gun": "Ружье",
        "Dodge": "Уворот", "Armor": "Броня", "Total": "Всего", "Worth": "Ценность"
    }

def process():
    with open('C:/Users/Lecoo/projects/GnomoriaTranslator/Gnomoria_raw_catch.json', 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    keys = re.findall(r'\"([^\"]+)\"\s*:', content)
    t_map = get_master_map()
    sorted_map_keys = sorted(t_map.keys(), key=len, reverse=True)
    
    final_dict = {}
    for k in set(keys):
        if not k.strip(): continue
        val = k
        if k == "v1.0":
            val = "v0.0.2 | memasevich 2026"
        else:
            # Сначала проверяем на полное совпадение для длинных фраз обучения
            if k in t_map:
                val = t_map[k]
            else:
                # Если полного совпадения нет, переводим по частям (для предметов)
                for eng in sorted_map_keys:
                    if eng.lower() in val.lower():
                        rus = t_map[eng]
                        if eng[0].isupper():
                            val = val.replace(eng, rus.capitalize())
                        else:
                            val = val.replace(eng, rus)
        final_dict[k] = val

    with open('C:/Users/Lecoo/projects/GnomoriaTranslator/Gnomoria_FINAL_GOLD.json', 'w', encoding='utf-8') as f:
        json.dump(final_dict, f, ensure_ascii=False, indent=2)
    print(f"Dictionary updated with tutorial: {len(final_dict)} entries.")

process()
