import json
import re

def get_master_map():
    # Massive hardcoded map from all previous sessions
    return {
        "New Game": "Новая игра", "Options": "Настройки", "Steam Workshop": "Мастерская Steam",
        "Exit": "Выход", "v1.0": "v0.0.2 | memasevich 2026", "Controls": "Управление",
        "Gameplay": "Геймплей", "Audio": "Аудио", "Video": "Видео", "Display:": "Дисплей:",
        "Windowed": "Оконный", "Resolution:": "Разрешение:", "Custom:": "Свое:",
        "Vertical Sync": "Верт. синхронизация", "Back": "Назад", "Apply": "Применить",
        "Music Volume:": "Громкость музыки:", "Effects Volume:": "Громкость эффектов:",
        "Save every": "Автосохранение каждые", "days": "дня", "Pause": "Пауза",
        "enemies when spotted": "врагов при обнаружении", "gnomads": "гномадов",
        "merchants": "торговцев", "craft item jobs": "задачи на крафт",
        "Depth": "Глубина", "Nourishment": "Сытость", "Weight": "Вес",
        "Closest": "Ближайшая", "Best": "Лучшая", "Show Action Bar": "Показать панель действий",
        "Show Stockpiles": "Показать склады", "Default": "По умолчанию", "Save": "Сохранить",
        "Rotate": "Повернуть", "item": "предмет", "Short walls": "Низкие стены",
        "Hidden cells": "Скрытые клетки", "Show axles": "Показать оси", "Show darkness": "Показать темноту",
        "Pan up": "Камера вверх", "Pan down": "Камера вниз", "Pan left": "Камера влево", "Pan right": "Камера вправо",
        "Kingdom Name": "Имя королевства", "Randomize": "Случайно", "Size": "Размер",
        "Standard": "Стандарт", "Difficulty": "Сложность", "Normal": "Обычная", "Generate": "Создать",
        "Advanced Setup": "Настройки", "Farms": "Фермы", "Pastures": "Пастбища",
        "Personal Quarters": "Личные покои", "Dormitories": "Казармы", "Dining Rooms": "Столовые",
        "Guard Areas": "Зоны охраны", "Patrol Routes": "Маршруты патруля", "Decrease": "Уменьшить",
        "Increase": "Увеличить", "Zoom in": "Приблизить", "Zoom out": "Отдалить",
        "Bookmark": "Закладка", "Set Bookmark": "Установить закладку", "Action Button": "Кнопка",
        "Mine Wall": "Копать стену", "Mine Stairs": "Копать лестницу", "Mine Ramp": "Копать скат",
        "Dig Hole": "Рыть яму", "Replace Wall": "Заменить стену", "Replace Floor": "Заменить пол",
        "Plant Tree": "Посадить дерево", "Fell Tree": "Срубить дерево", "Cut Clipping": "Срезать побег",
        "Forage": "Собирательство", "Build Workshop": "Построить мастерскую", "Mechanism": "Механизм",
        "Furniture": "Мебель", "Floor": "Пол", "Stockpile": "Склад", "Farm": "Ферма", "Pasture": "Пастбище",
        "Dormitory": "Казарма", "Dining Room": "Столовая", "Hospital": "Госпиталь", "Clean": "Очистить",
        "Deconstruct": "Разобрать", "Remove Designation": "Снять разметку", "Cancel Job": "Отменить работу",
        "Tiny": "Крошечный", "Small": "Малый", "Large": "Большой", "Huge": "Огромный",
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
    # Read raw capture
    with open('C:/Users/Lecoo/projects/GnomoriaTranslator/Gnomoria_raw_catch.json', 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Regex keys
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
            # Multi-pass translation for phrases
            for eng in sorted_map_keys:
                if eng.lower() in val.lower():
                    rus = t_map[eng]
                    # Check case
                    if eng[0].isupper():
                        val = val.replace(eng, rus.capitalize())
                    else:
                        val = val.replace(eng, rus)
        
        final_dict[k] = val

    # Final Gold File
    with open('C:/Users/Lecoo/projects/GnomoriaTranslator/Gnomoria_FINAL_GOLD.json', 'w', encoding='utf-8') as f:
        json.dump(final_dict, f, ensure_ascii=False, indent=2)
    
    print(f"Final Gold reconstructed: {len(final_dict)} entries.")

process()
