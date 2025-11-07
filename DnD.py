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

def load_options(options, type):
    '''
    Displays a list of options to the user.
    '''
    
    print(f"C. Create {type}")
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

def handle_choice(options, type):
    '''
    Gets a user's choice from a list of options and handles creation logic.
    '''
    while True:
        load_options(options, type)
        choice = input("Please enter your choice (Either name or number): ").strip().lower()

        if choice == "c":
            if type == "file":
                creation_flow()
                return None

            elif type == "category":
                while True:
                    new_category = FM.create_new_category(open_file)
                    print(f"Category '{new_category}' created.")

                    if handle_yes_no("Would you like to add a stat to this new category?"):
                        while True:
                            FM.create_new_stat(open_file, new_category)
                            if not handle_yes_no("Create another stat?"):
                                break

                    if not handle_yes_no("Would you like to create another category?"):
                        break
                return None

            elif type == "stat":
                while True:
                    FM.create_new_stat(open_file, open_category)
                    if not handle_yes_no("Create another stat?"):
                        break
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
    global open_file, open_category
    print("Welcome to the DnD sheet manager/roller!")

    while True:
        open_file = FM.check_folder()

        print("\nChoose a stat file to load:")
        selected_file = handle_choice(open_file, "file")
        if selected_file is None:
            continue
        
        open_file = selected_file
        file_contents = FM.load_file(selected_file)
        if not file_contents:
            print("This file has no categories yet.")
            continue

        print("\nChoose a category:")
        categories = list(file_contents.keys())
        selected_category = handle_choice(categories, "category")
        if selected_category is None:
            continue
        
        open_category = selected_category
        stat_names = list(file_contents[selected_category].keys())
        print(f"\nChoose what to do from '{selected_category}':")
        selected_stat = handle_choice(stat_names, "stat")
        if selected_stat is None:
            continue

        if not isinstance(file_contents[selected_category][selected_stat], int):
            print(f"Your selected option is {file_contents[selected_category][selected_stat]}.")
            continue
        roll_dice(file_contents[selected_category][selected_stat])

if __name__ == "__main__":
    main()