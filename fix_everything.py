import json
import re
import os

def get_db():
    return {
        "New Game": "Новая игра", "Options": "Настройки", "Steam Workshop": "Мастерская Steam",
        "Exit": "Выход", "v1.0": "v0.0.2 | memasevich 2026", "Controls": "Управление",
        "Gameplay": "Геймплей", "Audio": "Аудио", "Video": "Видео", "Display:": "Дисплей:",
        "Windowed": "Оконный режим", "Resolution:": "Разрешение:", "Custom:": "Свое:",
        "Vertical Sync": "Верт. синхронизация", "Back": "Назад", "Apply": "Применить",
        "Load Game": "Загрузить игру", "Delete": "Удалить", "Load": "Загрузить",
        "Save": "Сохранить", "Cancel": "Отмена", "Suspend": "Пауза", "Resume": "Продолжить",
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
        "pine": "сосна", "orange wood": "апельсин", "wild strawberry": "земляника",
        "apple": "яблоко", "orange": "апельсин", "grape": "виноград", "strawberry": "земляника",
        "soil": "земля", "dirt": "грязь", "stone": "камень", "log": "бревно", "plank": "доска",
        "Wall": "Стена", "Floor": "Пол", "Stairs": "Лестница", "Ramp": "Скат", "Hole": "Яма",
        "Spring": "Весна", "Summer": "Лето", "Autumn": "Осень", "Winter": "Зима",
        "day of": "день", "Year": "Год", "Depth": "Глубина", "Worth": "Ценность",
        "Food": "Еда", "Drink": "Питье", "Sunrise": "Рассвет", "Sunset": "Закат",
        "Overview": "Сводка", "Rooms": "Комнаты", "Population": "Население", "Military": "Армия",
        "Friendly": "Друзья", "Distance": "Дистанция", "Idle": "Бездельники", "Loading": "Загрузка"
    }

def run_fix():
    # Читаем дамп для получения всех 1334 ключей
    with open('C:/Users/Lecoo/projects/GnomoriaTranslator/Gnomoria_raw_catch.json', 'r', encoding='utf-8', errors='ignore') as f:
        keys = re.findall(r'\"([^\"]+)\"\s*:', f.read())
    
    db = get_db()
    sorted_pats = sorted(db.keys(), key=len, reverse=True)
    
    final = {}
    for k in set(keys):
        if not k.strip() or k == '?': continue
        val = k
        if k == "v1.0": val = "v0.0.2 | memasevich 2026"
        else:
            for p in sorted_pats:
                if p.lower() in val.lower():
                    r = db[p]
                    val = val.replace(p, r).replace(p.capitalize(), r.capitalize()).replace(p.lower(), r)
        final[k] = val

    # Пишем в UTF-8 без BOM (самый чистый формат)
    with open('D:/steam/steamapps/common/Gnomoria/Gnomoria_en_ru.json', 'w', encoding='utf-8') as f:
        json.dump(final, f, ensure_ascii=False, indent=2)
    
    print(f"Fix complete: {len(final)} strings written safely.")

run_fix()
