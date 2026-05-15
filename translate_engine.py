import json
import os

source_path = 'C:/Users/Lecoo/projects/GnomoriaTranslator/Gnomoria_raw_catch.json'
output_path = 'C:/Users/Lecoo/projects/GnomoriaTranslator/Gnomoria_final_translated.json'

def translate_str(k):
    # Металлы и материалы
    mats = {
        "steel": "сталь", "iron": "железо", "lead": "свинец", "bronze": "бронза", 
        "copper": "медь", "malachite": "малахит", "silver": "серебро", "gold": "золото", 
        "rose gold": "розовое золото", "platinum": "платина", "tin": "олово",
        "pine": "сосна", "orange wood": "апельсиновое дерево", "wild strawberry": "дикая земляника",
        "apple": "яблоко", "strawberry": "земляника", "orange": "апельсин", "grape": "виноград"
    }
    
    # Рецепты и предметы
    items = {
        "pickaxe": "кирка", "felling axe": "топор лесоруба", "crate": "ящик", 
        "bin": "контейнер", "barrel": "бочка", "bag": "мешок",
        "Contents": "Содержимое", "Job": "Задача", "Mine": "Копать"
    }

    # Интерфейс и HUD
    ui = {
        "The Military window shows information about ": "Окно Армия показывает информацию о ",
        "your Squads and their current assignments. ": "ваших отрядах и их текущих приказах. ",
        "The Events window provides of log of various ": "Окно События содержит журнал различных ",
        "events that can be viewed by date. There is ": "событий, которые можно смотреть по датам. ",
        "Load Game": "Загрузить игру", "Delete": "Удалить", "Load": "Загрузить",
        "Depth:": "Глубина:", "Worth:": "Ценность:", "Total": "Всего",
        "Squads:": "Отряды:", "Soldiers:": "Солдаты:", "Assigned:": "Назначено:",
        "Joined:": "Вступил:", "Profession:": "Профессия:", "Race:": "Раса:", "Gender:": "Пол:"
    }

    # Навыки (в скобках)
    skills = {
        "Mining": "Шахтерство", "Masonry": "Каменное дело", "Stonecarving": "Резьба по камню",
        "Woodcutting": "Лесозаготовка", "Carpentry": "Плотницкое дело", "Woodcarving": "Резьба по дереву",
        "Smelting": "Плавка", "Blacksmithing": "Кузнечное дело", "Metalworking": "Металлообработка",
        "Weapon Crafting": "Оружейное дело", "Armor Crafting": "Броня", "Gemcutting": "Огранка",
        "Jewelry Making": "Ювелирное дело", "Weaving": "Ткачество", "Tailoring": "Шитье",
        "Pottery": "Гончарное дело", "Leatherworking": "Кожевенное дело", "Bonecarving": "Резьба по кости",
        "Prospecting": "Поиск руды", "Animal Husbandry": "Животноводство", "Butchery": "Мясное дело",
        "Medic": "Медицина", "Caretaking": "Уход", "Construction": "Строительство", "Hauling": "Переноска"
    }

    res = k
    # Пытаемся перевести по частям для сложных строк типа "pine crate (32/32)"
    for eng, rus in mats.items(): res = res.replace(eng, rus)
    for eng, rus in items.items(): res = res.replace(eng, rus)
    for eng, rus in ui.items(): res = res.replace(eng, rus)
    for eng, rus in skills.items(): res = res.replace(eng, rus)
    
    # Специфические замены для HUD
    if res.startswith("Depth:"): res = res.replace("Depth:", "Глубина:")
    if "is in good health" in res: res = res.replace("is in good health", "в добром здравии")
    if "1st day of Spring, Year 1" in res: res = "1-й день Весны, Год 1"
    
    return res

with open(source_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

translated = {}
for k, v in data.items():
    if k == v or v == "": # Если строка не переведена или пустая
        translated[k] = translate_str(k)
    else:
        translated[k] = v # Сохраняем уже существующий перевод

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(translated, f, ensure_ascii=False, indent=2)

print(f"Translation processed: {len(translated)} strings.")
