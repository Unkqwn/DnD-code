import json
from pathlib import Path

folder_path = Path("C:/users/Unkqw/DnD Code/Stat sheets")

def check_folder():
    files = [f for f in folder_path.iterdir() if f.is_file() and f.suffix == ".json"]

    if not files:
        print("No stat files found. Please create your first stats file.")
        create_new_file()
        return [f for f in folder_path.iterdir() if f.is_file()]
    else:
        return files

def create_new_file():
    '''
    Creates a new stats file in the designated folder.
    '''

    new_filename = input("Enter new filename: ").strip()

    if not new_filename.lower().endswith(".json"):
        new_filename += ".json"

    new_file = folder_path / new_filename

    if not new_file.exists():
        new_file.touch()
        with new_file.open("w", encoding="utf-8") as f:
            json.dump({}, f, indent=4)
        print(f"File '{new_file.name}' created in the {folder_path.stem} folder.")
    else:
        print(f"File '{new_file.name}' already exists.")
    return new_file

def create_new_category(file):
    '''
    Creates a new category in an existing stats file.
    '''

    categories = load_file(file)

    new_category = input("Enter new category name: ").strip()

    if new_category in categories:
        print(f"Category '{new_category}' already exists in '{file.name}'.")
        return

    categories[new_category] = {}

    with file.open("w", encoding="utf-8") as f:
        json.dump(categories, f, indent=4)

    print(f"Category '{new_category}' added to '{file.name}'.")
    return new_category

def create_new_stat(file, category):
    '''
    Creates a new stat in an existing category of a stats file.
    '''
    stats = load_file(file)

    new_stat = input("Enter new stat name: ").strip()

    if new_stat in stats[category]:
        print(f"Stat '{new_stat}' already exists in category '{category}'.")
        return
    
    stat_value = input("Enter stat value: ").strip()

    if stat_value.isdigit():
        stats[category][new_stat] = int(stat_value)
    else:
        stats[category][new_stat] = stat_value

    with file.open("w", encoding="utf-8") as f:
        json.dump(stats, f, indent=4)

    print(f"Stat '{new_stat}' with value {stat_value} added to category '{category}' in '{file.name}'.")
    return new_stat

def load_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: '{filename}' contains invalid JSON.")
        return {}
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return {}