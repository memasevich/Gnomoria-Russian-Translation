import json
import os

def fix_help_topics():
    path = 'D:/steam/steamapps/common/Gnomoria/Gnomoria_en_ru.json'
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # КРИТИЧЕСКИЕ ЗАГОЛОВКИ И СТРОКИ
    topics = {
        "User Interface": "Интерфейс",
        "Gnomes": "Гномы",
        "Designations": "Разметка зон",
        "Constructions": "Постройки",
        "Combat": "Бой",
        "Movement": "Движение",
        "Needs": "Нужды",
        "Skills and Professions": "Навыки и Профессии",
        "Rooms": "Комнаты",
        "Research": "Исследования",
        "Links": "Связи",
        "Power Sources": "Энергия",
        "Devices": "Устройства",
        "Traps": "Ловушки",
        "Squad": "Отряд",
        "Position": "Позиция",
        
        # Дикие растения и земля
        "wild cotton plant": "дикий хлопок",
        "wild wheat plant": "дикая пшеница",
        "wild strawberry plant": "дикая земляника",
        "cotton": "хлопок",
        "wheat": "пшеница",
        
        # Другие фразы в обучении
        "Movement": "Передвижение",
        "Mouse Controls": "Управление мышью",
        "HUD": "Экраны",
        "General": "Общее",
        "Kingdom": "Королевство",
        "Stocks": "Запасы",
        "Population": "Население",
        "Military": "Армия",
        "Events": "События",
        "Help": "Помощь"
    }

    # Массово применяем
    data.update(topics)
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Help Topics fixed: {len(topics)} entries updated.")

if __name__ == "__main__":
    fix_help_topics()
