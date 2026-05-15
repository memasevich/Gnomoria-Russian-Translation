import json
import re

def get_clean_db():
    return {
        # --- ЦЕЛЫЕ ФРАЗЫ (Приоритет 1) ---
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
        "increase, attracting more gnomes to join you as ": "вы будете привлекать кочевников ",
        "well as enemies who threaten your gnomes. ": "и новых опасных врагов. ",
        "Your only objective is to help your gnomes ": "Ваша цель — помочь гномам выжить ",
        "survive in this harsh world for as long as ": "в этом суровом мире так долго, ",
        "possible. ": "как только возможно. ",
        "The world is split into a 3D grid of cells and is ": "Мир разбит на сетку из клеток и полностью ",
        "fully deformable. Each cell can be harvested ": "изменяем. Любую клетку можно вскопать ",
        "for its resource and used to be rebuilt ": "и использовать для стройки ",
        "elsewhere or crafted into new items. ": "или крафта новых вещей. ",
        
        # --- ИНТЕРФЕЙС (Приоритет 2) ---
        "New Game": "Новая игра", "Options": "Настройки", "Steam Workshop": "Мастерская Steam",
        "Exit": "Выход", "Load Game": "Загрузить игру", "Delete": "Удалить", "Load": "Загрузить",
        "Loading": "Загрузка", "Back": "Назад", "Apply": "Применить", "Save": "Сохранить",
        "Cancel": "Отмена", "Suspend": "Пауза", "Resume": "Продолжить", "Controls": "Управление",
        "Gameplay": "Геймплей", "Audio": "Аудио", "Video": "Видео", "Display:": "Дисплей:",
        "Windowed": "Оконный", "Resolution:": "Разрешение:", "Kingdom Name": "Имя королевства",
        "Kingdom Size": "Размер мира", "Difficulty": "Сложность", "Normal": "Обычная",
        "Generate": "Создать", "Advanced Setup": "Настройки", "Stocks": "Запасы",
        "Population": "Население", "Military": "Армия", "Events": "События", "Help": "Помощь",
        "Sunset": "Закат", "Sunrise": "Рассвет", "Depth": "Глубина", "Food": "Еда",
        "Drink": "Питье", "Year": "Год", "Day": "День", "Spring": "Весна", "Summer": "Лето",
        "Autumn": "Осень", "Winter": "Зима", "Overview": "Сводка", "Rooms": "Комнаты",
        "Diplomacy": "Дипломатия", "Friendly": "Друзья", "Distance": "Дистанция",
        "Idle": "Бездельники", "Injured": "Раненые", "Deceased": "Погибшие",
        
        # --- ПРОФЕССИИ (Приоритет 3) ---
        "Miner": "Шахтер", "Mason": "Каменщик", "Stonecarver": "Резчик", "Woodcutter": "Дровосек",
        "Carpenter": "Плотник", "Woodcarver": "Резчик по дереву", "Smelter": "Плавильщик",
        "Blacksmith": "Кузнец", "Metalworker": "Металлург", "Weaponsmith": "Оружейник",
        "Armorer": "Бронник", "Gemcutter": "Огранщик", "Jeweler": "Ювелир",
        "Weaver": "Ткач", "Tailor": "Портной", "Potter": "Гончар", "Leatherworker": "Кожевник",
        "Bonecarver": "Резчик по кости", "Prospector": "Старатель", "Tinkerer": "Жестянщик",
        "Machinist": "Машинист", "Engineer": "Инженер", "Mechanic": "Механик",
        "Rancher": "Животновод", "Butcher": "Мясник", "Gardener": "Садовник", "Farmer": "Фермер",
        "Chef": "Повар", "Brewer": "Пивовар", "Medic": "Медик", "Caretaker": "Смотритель",
        "Builder": "Строитель", "Hauler": "Носильщик", "Soldier": "Солдат",

        # --- МАТЕРИАЛЫ И ПРЕДМЕТЫ (Строгие границы) ---
        "steel": "сталь", "iron": "железо", "lead": "свинец", "bronze": "бронза",
        "copper": "медь", "malachite": "малахит", "silver": "серебро", "gold": "золото",
        "platinum": "платина", "tin": "олово", "metal": "металл", "ore": "руда",
        "pine": "сосна", "orange wood": "апельсин", "apple": "яблоко", "strawberry": "земляника",
        "soil": "земля", "dirt": "грязь", "stone": "камень", "log": "бревно", "plank": "доска",
        "block": "блок", "wall": "стена", "floor": "пол", "tree": "дерево"
    }

def run():
    # Читаем исходный дамп
    with open('C:/Users/Lecoo/projects/GnomoriaTranslator/Gnomoria_raw_catch.json', 'r', encoding='utf-8', errors='ignore') as f:
        keys = re.findall(r'\"([^\"]+)\"\s*:', f.read())
    
    db = get_clean_db()
    sorted_pats = sorted(db.keys(), key=len, reverse=True)
    
    final = {}
    for k in set(keys):
        if not k.strip() or k == '?': continue
        val = k
        if k == "v1.0": val = "v0.0.2 | memasevich 2026"
        else:
            for p in sorted_pats:
                # Используем границы слов \b для коротких материалов
                if len(p) <= 5:
                    pattern = re.compile(r'\b' + re.escape(p) + r'\b', re.IGNORECASE)
                else:
                    pattern = re.compile(re.escape(p), re.IGNORECASE)
                
                def replace_func(m):
                    rus = db[p]
                    orig = m.group(0)
                    if orig.isupper(): return rus.upper()
                    if orig[0].isupper(): return rus.capitalize()
                    return rus
                
                val = pattern.sub(replace_func, val)
        
        final[k] = val.replace("  ", " ").strip()

    # Сохраняем в Obsidian и игру
    with open('D:/steam/steamapps/common/Gnomoria/Gnomoria_en_ru.json', 'w', encoding='utf-8') as f:
        json.dump(final, f, ensure_ascii=False, indent=2)
    
    with open('C:/Obsidian/obsidian-hesh/Проекты/GnomoriaTranslator/Словарь_перевода.md', 'w', encoding='utf-8') as f:
        f.write("# Финальный словарь Gnomoria\n\n| EN | RU |\n| --- | --- |\n" + "\n".join([f"| {k} | {v} |" for k, v in final.items()]))

    print(f"Final Gold Reconstructed: {len(final)} strings. No more internal corruption.")

run()
