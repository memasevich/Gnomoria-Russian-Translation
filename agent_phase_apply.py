import json
import re

def get_agent_data():
    return {
        "iron": "железо", "steel": "сталь", "pine": "сосна", "stone": "камень",
        "copper": "медь", "silver": "серебро", "gold": "золото", "leather": "кожа",
        "bone": "кость", "pickaxe": "кирка", "axe": "топор", "sword": "меч",
        "crate": "ящик", "barrel": "бочка", "helmet": "шлем", "felling axe": "топор лесоруба",
        "raw stone": "необр. камень", "worn sword": "поношенный меч", "chisel": "долото",
        "pickaxe head": "головка кирки", "sausage omelette": "омлет с колбасой", "sack": "мешок",
        "coal": "уголь", "hand axe": "ручной топор", "windmill blade": "лопасть ветряка",
        "cheese omelette": "сырный омлет", "pet rock": "ручной камень", "worn warhammer": "поношенный боевой молот",
        "leather glove": "кожаная перчатка", "loaf of bread": "буханка хлеба", "wine": "вино",
        "warhammer head": "головка боевого молота", "warhammer": "боевой молот", "leather strap": "кожаный ремешок",
        "leather bracer": "кожаный наруч", "sandwich": "сэндвич", "leather cuirass": "кожаная кираса",
        "bandage": "бинт", "sawblade": "диск пилы", "ball-peen hammer": "молоток", "hammer": "молоток",
        "straw": "солома", "armor plate": "бронепластина", "leather panel": "кожаная панель",
        "armor": "броня", "claymore blade": "лезвие клеймора", "worn claymore": "поношенный клеймор",
        "claymore": "клеймор", "beer": "пиво", "mushroom omelette": "грибной омлет",
        "leather helm": "кожаный шлем", "battle axe": "боевой топор", "battle axe head": "головка боевого топора",
        "sword blade": "лезвие меча", "worn hammer": "поношенный молоток", "hand axe head": "головка ручного топора",
        "blade trap": "ловушка с лезвиями", "loom": "ткацкий станок", "strawberry": "клубника",
        "worn battle axe": "поношенный боевой топор", "hammer head": "головка молотка",
        "felling axe head": "головка топора лесоруба", "wool": "шерсть", "birch": "береза",
        "cedar": "кедр", "apple": "яблоко", "cherry": "вишня", "walnut": "орех", "rock": "порода",
        "dirt": "грязь", "clay": "глина", "bronze": "бронза", "lead": "свинец", "tin": "олово",
        "malachite": "малахит", "lapis": "лазурит", "cotton": "хлопок", "silk": "шелк",
        "chest": "сундук", "gauntlet": "перчатка", "boot": "сапог", "blade": "лезвие",
        "saw": "пила", "needle": "игла", "bag": "сумка", "potion": "зелье", "bread": "хлеб",
        "pie": "пирог", "omelette": "омлет"
    }

def process():
    # Читаем наш текущий рабочий JSON
    path = 'D:/steam/steamapps/common/Gnomoria/Gnomoria_en_ru.json'
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Новые данные от агента
    m = get_agent_data()
    sorted_keys = sorted(m.keys(), key=len, reverse=True)
    
    # Обновляем все непереведенные строки
    updated_count = 0
    for k in data:
        if data[k] == k or data[k] == "":
            val = k
            # Проход по словарю фрагментов
            for eng in sorted_keys:
                if eng.lower() in val.lower():
                    rus = m[eng]
                    val = val.replace(eng, rus)
                    val = val.replace(eng.capitalize(), rus.capitalize())
                    val = val.replace(eng.lower(), rus)
            
            if val != k:
                data[k] = val
                updated_count += 1
                
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Agent Phase complete: {updated_count} strings translated via fragments.")

process()
