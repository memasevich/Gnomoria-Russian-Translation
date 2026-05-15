import json

def force_professions():
    path = 'D:/steam/steamapps/common/Gnomoria/Gnomoria_en_ru.json'
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # ПРЯМАЯ ФОРСИРОВАННАЯ ЗАПИСЬ ВСЕХ ПРОФЕССИЙ
    # Я взял этот список из официальной вики игры
    p_map = {
        "Rancher": "Животновод", "Butcher": "Мясник", "Gardener": "Садовник",
        "Farmer": "Фермер", "Chef": "Повар", "Brewer": "Пивовар",
        "Medic": "Медик", "Caretaker": "Смотритель", "Builder": "Строитель",
        "Miner": "Шахтер", "Mason": "Каменщик", "Stonecarver": "Резчик по камню",
        "Woodcutter": "Дровосек", "Carpenter": "Плотник", "Woodcarver": "Резчик по дереву",
        "Smelter": "Плавильщик", "Blacksmith": "Кузнец", "Metalworker": "Металлург",
        "Weaponsmith": "Оружейник", "Armorer": "Бронник", "Gemcutter": "Огранщик",
        "Jeweler": "Ювелир", "Weaver": "Ткач", "Tailor": "Портной", "Potter": "Гончар",
        "Leatherworker": "Кожевник", "Bonecarver": "Резчик по кости", "Prospector": "Старатель",
        "Tinkerer": "Жестянщик", "Machinist": "Машинист", "Engineer": "Инженер",
        "Mechanic": "Механик", "Hauler": "Носильщик", "Soldier": "Солдат",
        "Guard": "Стражник", "Merchant": "Торговец", "Ambassador": "Посол"
    }

    # Добавляем варианты с двоеточиями (Rancher: -> Животновод:)
    final_updates = {}
    for eng, rus in p_map.items():
        final_updates[eng] = rus
        final_updates[eng + ":"] = rus + ":"

    data.update(final_updates)
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Force Update: {len(final_updates)} profession variants applied.")

if __name__ == "__main__":
    force_professions()
