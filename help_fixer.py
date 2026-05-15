import json
import os

def fix_help_text():
    path = 'D:/steam/steamapps/common/Gnomoria/Gnomoria_en_ru.json'
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # ПОЛНЫЕ СТРОКИ ОБУЧЕНИЯ (без фрагментации)
    help_map = {
        "Gnomoria is a sandbox management game and is ": "Gnomoria — это песочница и симулятор управления, ",
        "played by indirectly controlling your gnomes ": "где вы косвенно руководите своими гномами, ",
        "by creating jobs for them, designating areas ": "создавая для них задачи, размечая зоны мира ",
        "of the world as specific places and adjusting ": "как особые места и настраивая различные ",
        "settings. You can pause and unpause the game ": "параметры. Вы можете ставить игру на паузу ",
        "at anytime to manage your kingdom and watch ": "в любое время, чтобы управлять королевством и ",
        "your gnomes get to work. ": "наблюдать за тем, как гномы трудятся. ",
        "Each gnome needs to eat, drink and sleep and ": "Каждому гному нужно есть, пить и спать, ",
        "it's your job to help provide for them. As you ": "и ваша задача — обеспечить их этим. По мере ",
        "build your kingdom, your overall worth will ": "роста поселения его общая ценность будет ",
        "increase, attracting more gnomes to join you as ": "расти, привлекая новых гномадов и, увы, ",
        "well as enemies who threaten your gnomes. ": "врагов, которые угрожают вашим гномам. ",
        "Your only objective is to help your gnomes ": "Ваша единственная цель — помочь гномам ",
        "survive in this harsh world for as long as ": "выжить в этом суровом мире так долго, ",
        "possible. ": "как это только возможно. ",
        "Gnomoria takes place in a randomly generated ": "Действие игры происходит в случайно созданном ",
        "3D world with many resources to discover and ": "3D-мире со множеством ресурсов для поиска и ",
        "harvest. ": "сбора. ",
        "The world is split into a 3D grid of cells and is ": "Мир разбит на 3D-сетку клеток и полностью ",
        "fully deformable. Each cell can be harvested ": "изменяем. Каждую клетку можно раскопать ",
        "for its resource and used to be rebuilt ": "ради ресурсов, чтобы затем построить что-то ",
        "elsewhere or crafted into new items. ": "в другом месте или создать новые предметы. ",
        "Normally, 1 item can be placed in each square ": "Обычно 1 предмет занимает 1 клетку, ",
        "until the Stockpile is full. Storage items, such ": "пока склад не заполнится. Предметы хранения, ",
        "as crates, barrels and bags, can be built on ": "такие как ящики, бочки и мешки, можно ставить ",
        "Stockpiles so that each square can hold ": "на склады, чтобы увеличить вместимость клеток ",
        "additional items. ": "дополнительными предметами. "
    }

    # Принудительно перезаписываем эти ключи
    for k, v in help_map.items():
        data[k] = v
        
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Help text fixed: {len(help_map)} blocks updated.")

if __name__ == "__main__":
    fix_help_text()
