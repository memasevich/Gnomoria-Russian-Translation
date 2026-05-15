import json

def phase_2():
    path = 'D:/steam/steamapps/common/Gnomoria/Gnomoria_en_ru.json'
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Новые строки для Фазы 2
    professions = {
        "Miner": "Шахтер", "Mason": "Каменщик", "Stonecarver": "Резчик по камню",
        "Woodcutter": "Дровосек", "Carpenter": "Плотник", "Woodcarver": "Резчик по дереву",
        "Smelter": "Плавильщик", "Blacksmith": "Кузнец", "Metalworker": "Металлург",
        "Weaponsmith": "Оружейник", "Armorer": "Бронник", "Gemcutter": "Огранщик",
        "Jeweler": "Ювелир", "Weaver": "Ткач", "Tailor": "Портной", "Potter": "Гончар",
        "Leatherworker": "Кожевник", "Bonecarver": "Резчик по кости", "Prospector": "Старатель",
        "Tinkerer": "Жестянщик", "Machinist": "Машинист", "Engineer": "Инженер",
        "Mechanic": "Механик", "Rancher": "Животновод", "Butcher": "Мясник",
        "Gardener": "Садовник", "Farmer": "Фермер", "Chef": "Повар", "Brewer": "Пивовар",
        "Medic": "Медик", "Caretaker": "Смотритель", "Builder": "Строитель", "Hauler": "Носильщик",
        "Soldier": "Солдат", "Miner:": "Шахтер:", "Mason:": "Каменщик:", "Woodcutter:": "Дровосек:",
        "Mining": "Шахта", "Build": "Стройка", "Workshop": "Мастерская", "Grove": "Роща",
        "Hauling": "Переноска", "Professions": "Профессии", "Assign": "Назначить",
        "Squads": "Отряды", "Uniforms": "Экипировка", "Formations": "Построения"
    }
    
    # Слияние
    data.update(professions)
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Phase 2 complete: {len(professions)} strings added.")

if __name__ == "__main__":
    phase_2()
