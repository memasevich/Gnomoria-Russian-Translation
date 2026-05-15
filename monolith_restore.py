import json

def get_complete_mapping():
    # Я ВРУЧНУЮ ПЕРЕНОШУ ВСЕ ПЕРЕВОДЫ ИЗ НАШИХ ПРЕДЫДУЩИХ УСПЕШНЫХ БЛОКОВ
    return {
        "New Game": "Новая игра", "Options": "Настройки", "Steam Workshop": "Мастерская Steam",
        "Exit": "Выход", "v1.0": "v0.0.2 | memasevich 2026", "Controls": "Управление",
        "Gameplay": "Игровой процесс", "Audio": "Аудио", "Video": "Видео", "Display:": "Дисплей:",
        "Windowed": "Оконный режим", "Resolution:": "Разрешение:", "1024 x 768": "1024 x 768",
        "Custom:": "Свое:", "Vertical Sync": "Верт. синхронизация", "Back": "Назад", "Apply": "Применить",
        "Music Volume:": "Громкость музыки:", "Effects Volume:": "Громкость эффектов:",
        "Music Style:": "Стиль музыки:", "Classic": "Классика", "Save every": "Автосохранение каждые",
        "days": "дня", "Pause and show enemies when spotted": "Пауза при обнаружении врага",
        "Pause and show arriving gnomads": "Пауза при прибытии гномов",
        "Pause and show arriving merchants": "Пауза при прибытии торговцев",
        "Generate craft item jobs by default": "Автосоздание задач на крафт",
        "Depth distance scale": "Масштаб расстояния в глубину",
        "Nourishment Weight:": "Вес сытности:", "Closest": "Ближайшая", "Best": "Лучшая",
        "Show Action Bar": "Показать панель действий", "Show Stockpiles": "Показать склады",
        "Default": "По умолчанию", "Save": "Сохранить", "Toggle Pause": "Пауза", "SpaceBar": "Пробел",
        "Rotate item": "Вращать предмет", "Short walls": "Низкие стены", "Hidden cells": "Скрытые клетки",
        "Show axles": "Показать оси", "Show darkness": "Показать темноту", "None": "Нет",
        "Pan up": "Камера вверх", "Pan down": "Камера вниз", "Pan left": "Камера влево", "Pan right": "Камера вправо",
        "Kingdom Name": "Имя Королевства", "Randomize Name": "Случайное имя", "Kingdom Size": "Размер королевства",
        "Standard": "Стандартный", "Difficulty": "Сложность", "Normal": "Обычная", "Generate": "Создать",
        "Advanced Setup": "Расширенная настройка", "Show Farms": "Показать фермы", "Show Pastures": "Показать пастбища",
        "Show Personal Quarters": "Показать личные покои", "Show Dormitories": "Показать казармы",
        "Show Dining Rooms": "Показать столовые", "Show Guard Areas": "Показать зоны охраны",
        "Show Patrol Routes": "Показать маршруты патруля", "Decrease depth": "Уменьшить глубину",
        "Increase depth": "Увеличить глубину", "Rotate left": "Повернуть влево", "Rotate right": "Повернуть вправо",
        "Zoom in": "Приблизить", "Zoom out": "Отдалить", "Bookmark": "Закладка", "Set Bookmark": "Установить закладку",
        "Action Button": "Кнопка действия", "Mine Wall": "Копать стену", "Mine Stairs Up": "Выкопать лестницу вверх",
        "Mine Ramp Up": "Выкопать скат вверх", "Dig Hole": "Вырыть яму", "Replace Wall": "Заменить стену",
        "Replace Floor": "Заменить пол", "Plant Tree": "Посадить дерево", "Fell Tree": "Срубить дерево",
        "Cut Clipping": "Срезать побег", "Forage": "Собирательство", "Build Workshop": "Построить мастерскую",
        "Build Mechanism": "Построить механизм", "Build Furniture": "Построить мебель",
        "Build Floor": "Построить пол", "Build Stairs Up": "Построить лестницу вверх",
        "Build Stairs Down": "Построить лестницу вниз", "Build Ramp Up": "Построить скат вверх",
        "Build Ramp Down": "Построить скат вниз", "Stockpile": "Склад", "Farm": "Ферма", "Pasture": "Пастбище",
        "Personal Quarters": "Личные покои", "Dormitory": "Казарма", "Dining Room": "Столовая",
        "Hospital": "Госпиталь", "Guard Area": "Зона охраны", "Patrol Route": "Маршрут патруля",
        "Clean Floor": "Очистить пол", "Deconstruct": "Разобрать", "Remove Designation": "Снять разметку",
        "Cancel Job": "Отменить работу", "Tiny": "Крошечный", "Small": "Малый", "Large": "Большой", "Huge": "Огромный",
        "Generating Map": "Генерация карты", "Settling Liquids": "Установка жидкостей", "Kingdom": "Королевство",
        "Stocks": "Запасы", "Population": "Население", "Military": "Армия", "Events": "События",
        "Help": "Помощь", "Depth:": "Глубина:", "Food:": "Еда:", "Drink:": "Питье:",
        "1st day of Spring": "1 день Весны", "Year": "Год", "Sunrise:": "Рассвет:", "Sunset:": "Закат:",
        "Overview": "Сводка", "Rooms": "Комнаты", "Pastures": "Пастбища", "Farms": "Фермы",
        "Workshops": "Мастерские", "Diplomacy": "Дипломатия", "Stock Worth:": "Запасы:",
        "Construction Worth:": "Постройки:", "Total Worth:": "Ценность:", "Status: Friendly": "Статус: Друзья",
        "Distance:": "Дистанция:", "Idle:": "Бездельники:", "Injured:": "Раненые:",
        "Deceased": "Погибшие", "Professions": "Профессии", "Assign": "Назначить", "Population Cap": "Лимит гномов",
        "Miner:": "Шахтер:", "Mason:": "Каменщик:", "Stonecarver:": "Резчик по камню:", "Woodcutter:": "Дровосек:",
        "Carpenter:": "Плотник:", "Woodcarver:": "Резчик по дереву:", "Smelter:": "Плавильщик:",
        "Blacksmith:": "Кузнец:", "Metalworker:": "Металлург:", "Weaponsmith:": "Оружейник:", "Armorer:": "Бронник:",
        "Gemcutter:": "Огранщик:", "Jeweler:": "Ювелир:", "Weaver:": "Ткач:", "Tailor:": "Портной:",
        "Potter:": "Гончар:", "Leatherworker:": "Кожевник:", "Bonecarver:": "Резчик по кости:",
        "Prospector:": "Старатель:", "Tinkerer:": "Жестянщик:", "Machinist:": "Механик:", "Engineer:": "Инженер:",
        "Mechanic:": "Монтер:", "Rancher:": "Животновод:", "Butcher:": "Мясник:", "Gardener:": "Садовник:",
        "Farmer:": "Фермер:", "Chef:": "Повар:", "Brewer:": "Пивовар:", "Medic:": "Врач:",
        "Caretaker:": "Смотритель:", "Builder:": "Строитель:", "Miner": "Шахтер", "Farmer": "Фермер",
        "Woodcutter": "Дровосек", "Rancher": "Животновод", "Builder": "Строитель", "Idle": "Бездельник",
        "Stone": "Камень", "Wood": "Древесина", "Metal": "Металл", "Gem": "Самоцвет", "Cloth": "Ткань",
        "Misc Craft": "Прочий крафт", "Agriculture": "Сельское хоз-во", "Doctor": "Доктор", "Misc": "Разное",
        "Uniform": "Униформа", "Job Type Priority": "Приоритет задач", "Mining": "Шахта", "Build": "Стройка",
        "Workshop": "Мастерская", "Grove": "Роща", "Tinker": "Жестяное дело", "Hauling": "Переноска",
        "Uniforms": "Экипировка", "Positions": "Позиции", "Formations": "Построения", "Squads": "Отряды",
        "Enemies": "Враги", "Formation": "Построение", "Leader": "Командир", "Soldier": "Солдат",
        "Perform attack orders": "Атаковать цели", "Defend gnomes": "Защищать гномов", "Avoid enemies": "Избегать врагов",
        "Platemail": "Латный доспех", "Maintain distance": "Держать дистанцию", "Retreat if bleeding": "Отступать при ранении",
        "Head": "Голова", "helmet": "шлем", "Body": "Тело", "breastplate": "нагрудник", "Arms": "Руки",
        "pauldron": "наплечник", "Legs": "Ноги", "greave": "поножи", "Hands": "Кисти", "gauntlet": "перчатки",
        "Feet": "Ступни", "boot": "ботинок", "shield": "щит", "Combat": "Бой", "Recent": "Последнее",
        "Read about game topics": "Читать справку", "Topics": "Разделы", "Gnomes": "Гномы", "Designations": "Зоны",
        "Constructions": "Постройки", "Crafting": "Крафтинг", "Mechanisms": "Механизмы", "Terrain": "Ландшафт",
        "Hole": "Яма", "Mechanism": "Механизм", "Furniture": "Мебель", "Storage": "Хранилище", "door": "дверь",
        "bed": "кровать", "table": "стол", "chair": "стул", "dresser": "комод", "cabinet": "шкаф", "statue": "статуя",
        "torch": "факел", "pillar": "колонна", "crate": "ящик", "barrel": "бочка", "bag": "мешок",
        "stairs up": "лестница вверх", "stairs down": "лестница вниз", "ramp up": "скат вверх", "ramp down": "скат вниз",
        "scaffolding": "леса", "Import/Export": "Импорт/Экспорт", "Save and Exit": "Сохранить и выйти",
        "soil": "земляной", "stone": "каменный", "log": "бревенчатый", "block": "блочный", "wall": "стена", "floor": "пол",
        "ceramic": "керамический", "bone": "костяной", "thatch": "соломенный", "leather": "кожаный",
        "steel": "стальной", "iron": "железный", "lead": "свинцовый", "bronze": "бронзовый", "copper": "медный",
        "silver": "серебряный", "gold": "золотой", "platinum": "платиновый", "tin": "оловянный",
        "pine": "сосновый", "orange wood": "апельсиновый", "wild strawberry": "земляничный",
        "apple": "яблоко", "orange": "апельсин", "grape": "виноград", "strawberry": "земляника",
        "is in good health": "в добром здравии", "Nothing": "Ничего", "Gender": "Пол", "Female": "Жен.", "Male": "Муж.",
        "Race": "Раса", "Joined": "Вступил", "Status": "Статус", "Attributes": "Характеристики",
        "Fighting": "Борьба", "Brawling": "Драка", "Sword": "Меч", "Axe": "Топор", "Hammer": "Молот",
        "Crossbow": "Арбалет", "Gun": "Ружье", "Dodge": "Уворот", "Armor": "Броня",
        "Gnomoria is a sandbox management game and is ": "Gnomoria — это симулятор управления, ",
        "played by indirectly controlling your gnomes ": "где вы косвенно руководите гномами, ",
        "by creating jobs for them, designating areas ": "создавая для них задачи и зоны, ",
        "of the world as specific places and adjusting ": "настраивая правила жизни. ",
        "settings. You can pause and unpause the game ": "Вы можете ставить игру на паузу, ",
        "at anytime to manage your kingdom and watch ": "чтобы управлять королевством, ",
        "your gnomes get to work. ": "наблюдая за их работой. ",
        "Each gnome needs to eat, drink and sleep and ": "Гномам нужно есть, пить и спать, ",
        "it's your job to help provide for them. As you ": "и ваша цель — обеспечить их этим. ",
        "build your kingdom, your overall worth will ": "С ростом ценности королевства, ",
        "increase, attracting more gnomes to join you as ": "вы будете привлекать кочевников ",
        "well as enemies who threaten your gnomes. ": "и новых опасных врагов. ",
        "Your only objective is to help your gnomes ": "Ваша цель — помочь гномам выжить ",
        "survive in this harsh world for as long as ": "в этом суровом мире так долго, ",
        "possible. ": "как это возможно. ",
        "Gnomoria takes place in a randomly generated ": "Действие происходит в случайном ",
        "3D world with many resources to discover and ": "3D-мире с кучей ресурсов. ",
        "harvest. ": " ",
        "The world is split into a 3D grid of cells and is ": "Мир разбит на сетку из клеток и полностью ",
        "fully deformable. Each cell can be harvested ": "изменяем. Любую клетку можно вскопать ",
        "for its resource and used to be rebuilt ": "и использовать для стройки ",
        "elsewhere or crafted into new items. ": "или крафта новых вещей. "
    }

def process():
    import os, re
    
    # Берем чистые ключи из дампа (1334 ключа)
    with open('C:/Users/Lecoo/projects/GnomoriaTranslator/Gnomoria_raw_catch.json', 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    keys = re.findall(r'\"([^\"]+)\"\s*:', content)
    
    m = get_complete_mapping()
    sorted_m_keys = sorted(m.keys(), key=len, reverse=True)
    
    final_dict = {}
    for k in set(keys):
        if not k.strip() or k == '?': continue
        
        val = k
        if k == "v1.0":
            val = "v0.0.2 | memasevich 2026"
        else:
            # Многопроходный перевод фрагментов для составных строк
            for eng in sorted_m_keys:
                if eng.lower() in val.lower():
                    rus = m[eng]
                    val = val.replace(eng, rus)
                    val = val.replace(eng.capitalize(), rus.capitalize())
                    val = val.replace(eng.lower(), rus)
        
        final_dict[k] = val

    # Сохраняем как FINAL_STABLE.json
    output_path = 'C:/Users/Lecoo/projects/GnomoriaTranslator/Gnomoria_FINAL_STABLE.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(final_dict, f, ensure_ascii=False, indent=2)
    
    print(f"Success: {len(final_dict)} strings reconstructed.")

process()
