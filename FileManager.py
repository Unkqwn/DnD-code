import json
from pathlib import Path

script_dir = Path(__file__).resolve().parent
folder_path = script_dir / "Stat sheets"
folder_path.mkdir(exist_ok=True)

def check_folder(type=".json"):
    files = [f for f in folder_path.iterdir() if f.is_file() and f.suffix == type]

    if not files:
        print("No stat files found. Please create your first stats file.")
        create_new_file()
        return [f for f in folder_path.iterdir() if f.is_file()]
    else:
        return files

def create_new_file(file_type=".json"):
    '''
    Creates a new stats file in the designated folder.
    '''

    new_filename = input("Enter new filename: ").strip()

    if not new_filename.lower().endswith(".json"):
        new_filename += file_type

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

def search_files(file, search_term):
    '''
    Searches the given file for a term and returns matching stats.
    '''
    data = load_file(file)
    search_term = search_term.lower()
    results = {}

    if not data:
        print(f"No data found in '{file.name}'.")
        return None
    
    for category, stats in data.items():
        category_match = category.lower() == search_term
        stats_match = {}

        for stat, value in stats.items():
            if (search_term in stat.lower()) or (str(value).lower() == search_term):
                stats_match[stat] = value

        if category_match or stats_match:
            results[category] = stats_match if stats_match else stats

    if results:
        print(f"Search results for '{search_term}' in '{file.name}':")
        for cat, stats in results.items():
            print(f"\n[{cat}]")
            for stat, value in stats.items():
                print(f"  {stat}: {value}")
    else:
        print(f"No matches found for '{search_term}' in '{file.name}'.")

    return value

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