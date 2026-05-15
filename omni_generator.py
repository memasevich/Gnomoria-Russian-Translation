import json
import re

def get_db():
    return {
        "New Game": "Новая игра", "Options": "Настройки", "Steam Workshop": "Мастерская Steam",
        "Exit": "Выход", "v1.0": "v0.0.2 | memasevich 2026", "Controls": "Управление",
        "Gameplay": "Геймплей", "Audio": "Аудио", "Video": "Видео", "Display:": "Дисплей:",
        "Windowed": "Оконный режим", "Resolution:": "Разрешение:", "Custom:": "Свое:",
        "Vertical Sync": "Верт. синхронизация", "Back": "Назад", "Apply": "Применить",
        "Music Volume:": "Громкость музыки:", "Effects Volume:": "Громкость эффектов:",
        "Save every": "Автосохранение каждые", "days": "дня", "Pause": "Пауза",
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
        "steel": "сталь", "iron": "железо", "lead": "свинец", "bronze": "бронза", "copper": "медь",
        "malachite": "малахит", "silver": "серебро", "gold": "золото", "platinum": "платина",
        "tin": "олово", "metal": "металл", "ore": "руда", "bar": "слиток", "coal": "уголь",
        "pine": "сосна", "orange wood": "апельсин", "apple": "яблоко", "strawberry": "земляника",
        "soil": "земля", "dirt": "грязь", "stone": "камень", "log": "бревно", "plank": "доска",
        "Wall": "Стена", "Floor": "Пол", "Stairs": "Лестница", "Ramp": "Скат", "Hole": "Яма",
        "Spring": "Весна", "Summer": "Лето", "Autumn": "Осень", "Winter": "Зима",
        "Year": "Год", "Depth": "Глубина", "Food": "Еда", "Drink": "Питье", "Loading": "Загрузка",
        "Load Game": "Загрузить игру", "Delete": "Удалить", "Load": "Загрузить",
        "Overview": "Сводка", "Rooms": "Комнаты", "Population": "Население", "Military": "Армия",
        "Events": "События", "Help": "Помощь", "Nothing": "Ничего"
    }

def run():
    # 1. Читаем все наловленные ключи
    with open('C:/Users/Lecoo/projects/GnomoriaTranslator/Gnomoria_raw_catch.json', 'r', encoding='utf-8', errors='ignore') as f:
        keys = re.findall(r'\"([^\"]+)\"\s*:', f.read())
    
    db = get_db()
    sorted_pats = sorted(db.keys(), key=len, reverse=True)
    
    final = {}
    obsidian_md = "# База перевода Gnomoria (v3.6)\n\n| English | Russian |\n| --- | --- |\n"
    
    for k in sorted(list(set(keys))):
        if not k.strip() or k == '?': continue
        
        val = k
        if k == "v1.0": val = "v0.0.2 | memasevich 2026"
        else:
            for p in sorted_pats:
                if p.lower() in val.lower():
                    r = db[p]
                    # Умная замена
                    val = val.replace(p, r).replace(p.capitalize(), r.capitalize()).replace(p.lower(), r)
        
        final[k] = val
        obsidian_md += f"| {k} | {val} |\n"

    # 2. Запись в игру
    with open('D:/steam/steamapps/common/Gnomoria/Gnomoria_en_ru.json', 'w', encoding='utf-8') as f:
        json.dump(final, f, ensure_ascii=False, indent=2)
    
    # 3. Запись в Obsidian
    obs_path = 'C:/Obsidian/obsidian-hesh/Проекты/GnomoriaTranslator/Словарь_перевода.md'
    with open(obs_path, 'w', encoding='utf-8') as f:
        f.write(obsidian_md)
    
    print(f"OMNI-DICT generated: {len(final)} strings. Obsidian sync complete.")

run()
