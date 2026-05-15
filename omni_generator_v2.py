import json
import re

def get_db():
    # Мы расширяем базу максимально простыми словами, чтобы они ловились внутри фраз
    return {
        # Базовые сущности
        "Kingdom": "Королевство",
        "Stocks": "Запасы",
        "Sunset": "Закат",
        "Sunrise": "Рассвет",
        "Tree": "дерево",
        "Wall": "стена",
        "Floor": "пол",
        "Food": "Еда",
        "Drink": "Питье",
        "Year": "Год",
        "Day": "День",
        "Spring": "Весна",
        "Summer": "Лето",
        "Autumn": "Осень",
        "Winter": "Зима",
        "Loading": "Загрузка",
        "Load": "Загрузить",
        
        # Меню и кнопки
        "New Game": "Новая игра",
        "Options": "Настройки",
        "Steam Workshop": "Мастерская Steam",
        "Exit": "Выход",
        "Back": "Назад",
        "Apply": "Применить",
        "Save": "Сохранить",
        "Cancel": "Отмена",
        "Delete": "Удалить",
        
        # Материалы
        "steel": "сталь", "iron": "железо", "lead": "свинец", "bronze": "бронза", "copper": "медь",
        "silver": "серебро", "gold": "золото", "platinum": "платина", "tin": "олово",
        "pine": "сосна", "orange wood": "апельсин", "wild strawberry": "земляника",
        "apple": "яблоко", "orange": "апельсин", "grape": "виноград", "strawberry": "земляника",
        
        # Профессии
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

        # Инструменты/Предметы
        "pickaxe": "кирка", "felling axe": "топор", "sword": "меч", "hammer": "молот",
        "crate": "ящик", "barrel": "бочка", "bag": "мешок", "bin": "контейнер"
    }

def run():
    with open('C:/Users/Lecoo/projects/GnomoriaTranslator/Gnomoria_raw_catch.json', 'r', encoding='utf-8', errors='ignore') as f:
        keys = re.findall(r'\"([^\"]+)\"\s*:', f.read())
    
    db = get_db()
    # Сортируем от самых длинных к самым коротким
    sorted_pats = sorted(db.keys(), key=len, reverse=True)
    
    final = {}
    obsidian_md = "# Финальная база перевода Gnomoria (v3.7)\n\n| English | Russian |\n| --- | --- |\n"
    
    for k in set(keys):
        if not k.strip() or k == '?': continue
        
        val = k
        if k == "v1.0": 
            val = "v0.0.2 | memasevich 2026"
        else:
            # Умный регистронезависимый перевод фрагментов
            for p in sorted_pats:
                # Используем регулярку для замены с сохранением контекста
                pattern = re.compile(re.escape(p), re.IGNORECASE)
                
                def replace_func(match):
                    rus = db[p]
                    original = match.group(0)
                    if original.isupper(): return rus.upper()
                    if original[0].isupper(): return rus.capitalize()
                    return rus
                
                val = pattern.sub(replace_func, val)
        
        final[k] = val
        obsidian_md += f"| {k} | {val} |\n"

    # Запись в игру
    with open('D:/steam/steamapps/common/Gnomoria/Gnomoria_en_ru.json', 'w', encoding='utf-8') as f:
        json.dump(final, f, ensure_ascii=False, indent=2)
    
    # Синхронизация Obsidian
    with open('C:/Obsidian/obsidian-hesh/Проекты/GnomoriaTranslator/Словарь_перевода.md', 'w', encoding='utf-8') as f:
        f.write(obsidian_md)
    
    print(f"OMNI-DICT v3.7 generated: {len(final)} strings. Logic: Case-insensitive fragment replacement.")

run()
