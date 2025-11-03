import random
import FileManager as FM

def creation_flow():
    new_file = FM.create_new_file()
    while True:
        new_category = FM.create_new_category(new_file)
        while True:
            FM.create_new_stat(new_file, new_category)
            if not handle_yes_no("Create another stat?"):
                break
        if not handle_yes_no("Create another category?"):
            break

def load_options(options):
    '''
    Displays a list of options to the user.
    '''
    
    print("C. Create new stats file")
    print("0. Exit")
    
    if all(isinstance(opt, str) for opt in options):
        for i, opt in enumerate(options, start=1):
            print(f"{i}. {opt}")
    else:
        for i, opt in enumerate(options, start=1):
            print(f"{i}. {opt.stem}")

def handle_yes_no(prompt):
    '''
    Handles yes/no user input.
    '''
    while True:
        choice = input(prompt + " (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def handle_choice(options, create_option=False):
    '''
    Gets a users choice from a list of options and handles
    '''
    
    while True:
        choice = input("Please enter your choice (Either name or number): ").strip().lower()

        if create_option and choice == "c":
            creation_flow()
            return None
        if choice == "0" or choice == "exit":
            print("Exiting program. Goodbye!")
            exit()

        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(options):
                return options[index]
            print("Invalid selection. Please try again.")
        else:
            matches = []
            if all(isinstance(opt, str) for opt in options):
                matches = [opt for opt in options if opt.lower() == choice]
            else:
                matches = [opt for opt in options if opt.stem.lower() == choice]

            if matches:
                return matches[0]
            print("Not found. Please try again.")

def roll_dice(stat_value, sides=20):
    roll = random.randint(1, sides)
    total = roll + stat_value
    print(f"You rolled a {roll} + {stat_value} = {total}")
    return total

def main():
    print("Welcome to the DnD sheet manager/roller!")

    while True:
        files = FM.check_folder()

        print("\nChoose a stat file to load:")
        load_options(files)
        selected_file = handle_choice(files, create_option=True)
        if selected_file is None:
            continue

        stats = FM.load_file(selected_file)
        if not stats:
            print("This file has no categories yet.")
            continue

        print("\nChoose a category:")
        categories = list(stats.keys())
        load_options(categories)
        selected_category = handle_choice(categories)
        if selected_category is None:
            continue

        stat_names = list(stats[selected_category].keys())
        print(f"\nChoose a stat from '{selected_category}':")
        load_options(stat_names)
        selected_stat = handle_choice(stat_names)
        if selected_stat is None:
            continue

        if not isinstance(stats[selected_category][selected_stat], int):
            print(f"Your selected option is {stats[selected_category][selected_stat]}.")
            continue
        roll_dice(stats[selected_category][selected_stat])

if __name__ == "__main__":
    main()