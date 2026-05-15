import json
import re

def phase_2_repair():
    path = 'D:/steam/steamapps/common/Gnomoria/Gnomoria_en_ru.json'
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Расширенный словарь для вкладки Population и профессий
    updates = {
        "Population": "Население",
        "Population:": "Население:",
        "Population Cap": "Лимит гномов",
        "Deceased": "Погибшие",
        "Injured:": "Раненые:",
        "Idle:": "Бездельники:",
        "Professions": "Профессии",
        "Assign": "Назначить",
        "Overview": "Сводка",
        "Status:": "Статус:",
        "Name:": "Имя:",
        "Skills": "Навыки",
        "Attributes": "Характеристики",
        "Health": "Здоровье",
        "Equipment": "Экипировка",
        "Uniform": "Униформа",
        "Job Type Priority": "Приоритет задач",
        "Move Up": "Выше",
        "Move Down": "Ниже",
        "Ban": "Запретить",
        "New": "Создать",
        "Remove": "Удалить",
        
        # Навыки с цифрами (поддержка шаблонов)
        "Mining:": "Шахтерство:",
        "Masonry:": "Каменное дело:",
        "Woodcutting:": "Лесозаготовка:",
        "Carpentry:": "Плотницкое дело:",
        "Metalworking:": "Металлургия:",
        "Construction:": "Строительство:",
        "Hauling:": "Переноска:",
        "Tailoring:": "Шитье:",
        "Brewing:": "Пивоварение:",
        "Cooking:": "Кулинария:",
        "Farming:": "Земледелие:",
        "Medic:": "Медицина:",

        # Длинные описания
        "The Population menu provides detailed ": "В меню Население представлена детальная ",
        "information about your gnomes and their ": "информация о ваших гномах и их ",
        "activities. ": "занятиях. ",
        "The Overview tab displays your total ": "На вкладке Сводка показано общее число ",
        "population as well as number of gnomes who are ": "гномов и количество тех, кто ",
        "currently idle. The right side of this window ": "сейчас бездельничает. ",
        "shows how many gnomes have been selected for ": "Справа показано распределение ",
        "each job type. ": "по типам задач. "
    }

    # Массовый подхват строк типа "(20) Mining" -> "(20) Шахтерство"
    skills_map = {
        "Mining": "Шахтерство", "Masonry": "Каменное дело", "Stonecarving": "Резьба по камню",
        "Woodcutting": "Лесозаготовка", "Carpentry": "Плотницкое дело", "Woodcarver": "Резчик по дереву",
        "Smelting": "Плавка", "Blacksmithing": "Кузнечное дело", "Metalworking": "Металлургия",
        "Weapon Crafting": "Оружейное дело", "Armor Crafting": "Броня", "Gemcutting": "Огранка",
        "Jewelry Making": "Ювелирное дело", "Weaving": "Ткачество", "Tailoring": "Шитье",
        "Pottery": "Гончарное дело", "Leatherworking": "Кожевенное дело", "Bonecarver": "Резьба по кости",
        "Prospecting": "Поиск руды", "Animal Husbandry": "Животноводство", "Butchery": "Мясное дело",
        "Medic": "Медицина", "Caretaking": "Уход", "Construction": "Строительство", "Hauling": "Переноска"
    }

    # Берем текущий дамп ключей из игры, чтобы найти динамические строки
    with open('C:/Users/Lecoo/projects/GnomoriaTranslator/Gnomoria_raw_catch.json', 'r', encoding='utf-8', errors='ignore') as f:
        raw_content = f.read()
    all_keys = re.findall(r'\"([^\"]+)\"\s*:', raw_content)

    for k in set(all_keys):
        # 1. Паттерн "Population: X"
        if k.startswith("Population: "):
            updates[k] = k.replace("Population: ", "Население: ")
        
        # 2. Паттерн "(Цифра) Навык"
        match = re.match(r'\((\d+)\)\s+(.*)', k)
        if match:
            num = match.group(1)
            skill_eng = match.group(2)
            if skill_eng in skills_map:
                updates[k] = f"({num}) {skills_map[skill_eng]}"

    # Слияние
    data.update(updates)
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Phase 2 Repair complete: {len(updates)} strings fixed/added.")

if __name__ == "__main__":
    phase_2_repair()
