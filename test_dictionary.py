import json
import os

def test_dictionary_integrity():
    path = 'D:/steam/steamapps/common/Gnomoria/Gnomoria_en_ru.json'
    
    if not os.path.exists(path):
        print("FAIL: Dictionary file missing")
        return False
        
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"FAIL: JSON is invalid or has encoding issues: {e}")
        return False
    
    # Check for garbage characters (typical for OEM 866 vs UTF-8)
    for k, v in data.items():
        if "╨" in v or "╤" in v or "┬" in v:
            print(f"FAIL: Garbage characters found in key '{k}': {v}")
            return False
            
    # Check for specific "Load Game" translation reported by user
    if data.get("Load Game") != "Загрузить игру":
        print(f"FAIL: 'Load Game' is not correctly translated. Got: {data.get('Load Game')}")
        return False

    # Check for "Loading" reported as "загрузитьing"
    if data.get("Loading") == "загрузитьing":
        print("FAIL: 'Loading' has suffix corruption ('загрузитьing')")
        return False

    # Check for Year/Depth/Food/Drink
    if data.get("Food") != "Еда":
        print(f"FAIL: 'Food' is missing translation. Got: {data.get('Food')}")
        return False

    print("PASS: Dictionary integrity verified.")
    return True

if __name__ == "__main__":
    test_dictionary_integrity()
