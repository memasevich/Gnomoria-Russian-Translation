import json

def phase_1():
    data = {
        "New Game": "Новая игра",
        "Options": "Настройки",
        "Steam Workshop": "Мастерская Steam",
        "Exit": "Выход",
        "v1.0": "v0.0.2 | memasevich 2026",
        "Load Game": "Загрузить игру",
        "Delete": "Удалить",
        "Load": "Загрузить",
        "Back": "Назад",
        "Apply": "Применить",
        "Save": "Сохранить",
        "Controls": "Управление",
        "Gameplay": "Геймплей",
        "Audio": "Аудио",
        "Video": "Видео",
        "Display:": "Дисплей:",
        "Windowed": "Оконный режим",
        "Resolution:": "Разрешение:",
        "Custom:": "Свое:",
        "Vertical Sync": "Верт. синхронизация",
        "Music Volume:": "Громкость музыки:",
        "Effects Volume:": "Громкость эффектов:",
        "Music Style:": "Стиль музыки:",
        "Classic": "Классика",
        "Save every": "Автосохранение каждые",
        "days": "дня",
        "Pause and show enemies when spotted": "Пауза при обнаружении врага",
        "Pause and show arriving gnomads": "Пауза при прибытии гномов",
        "Pause and show arriving merchants": "Пауза при прибытии торговцев",
        "Generate craft item jobs by default": "Автозадачи на крафт",
        "Kingdom Name": "Имя королевства",
        "Kingdom Size": "Размер мира",
        "Difficulty": "Сложность",
        "Standard": "Стандарт",
        "Normal": "Обычная",
        "Generate": "Создать",
        "Advanced Setup": "Настройки",
        "Food": "Еда",
        "Drink": "Питье",
        "Depth": "Глубина",
        "Sunrise": "Рассвет",
        "Sunset": "Закат",
        "Year": "Год",
        "Spring": "Весна",
        "Summer": "Лето",
        "Autumn": "Осень",
        "Winter": "Зима"
    }
    
    target = 'D:/steam/steamapps/common/Gnomoria/Gnomoria_en_ru.json'
    with open(target, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Phase 1 complete: {len(data)} strings applied.")

if __name__ == "__main__":
    phase_1()
