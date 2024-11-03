# CSV file by: Nandini Bansal, Public Domain, via Kaggle.com 
# https://www.kaggle.com/datasets/nandini1999/perfume-recommendation-dataset?resource=download

import csv

filename = 'fragrance_data.csv'
fragrances = []

def get_frags(filename):
    perfume_database = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            perfume_database.append({
                "name": row["Name"],
                "brand": row["Brand"],
                "scent_note": row["Notes"].strip(),
            })
    return perfume_database

fragrances = get_frags(filename)

def get_fragrance_by_name(fragrances, name):
    matching_fragrances = []
    for fragrance in fragrances:
        if name.strip().lower() in fragrance["name"].strip().lower():
            matching_fragrances.append(fragrance)
    return matching_fragrances

def get_fragrance_by_note(fragrances, note):
    matching_fragrances = []
    for fragrance in fragrances:
        if note.strip().lower() in fragrance["scent_note"].strip().lower():
            matching_fragrances.append(fragrance)
    return matching_fragrances

def display_fragrance(fragrance):
    if fragrance:
        print()
        print(f"Fragrance: {fragrance['name']}")
        print(f"Brand: {fragrance['brand']}")
        print(f"Notes: {fragrance['scent_note']}")
        print()

def print_welcome():
    print("=" * 50)
    print(" WELCOME TO THE PERFUME RECOMMENDATION PROGRAM ".center(50, "-"))
    print("=" * 50)
    print("\nDiscover your next signature scent!\n")
    print("This program helps you find note and brand information for fragrances.")

def print_help():
    print("=" * 50)
    print(" ABOUT US ".center(50, "-"))
    print("=" * 50)
    print("\nYou can search for fragrances by name or by scent notes.")
    print("The program displays up to five matching fragrances at a time.")
    print("If no matches are found, try different keywords.\n")
    print("Note: This program uses a dataset, so the results are limited, and may take time to load.")

def main():
    print_welcome()

    while True:
        action = input("Type 'go' to start searching for fragrances, 'help' for assistance, or 'exit' to quit the program: ").strip().lower()
        if action == 'exit':
            print("Thank you for using the perfume recommendation program!")
            break
        if action == 'help':
            print_help()
            continue
        if action != 'go':
            print("Invalid input. Please type 'go' to start, 'help' for more info, or 'exit' to quit.")
            continue

        while True:
            search_type = input("\nType '1' to search by note, '2' for name, or type 'exit' to quit): ").strip().lower()
            if search_type == 'exit':
                print("Thank you for using the perfume recommendation program!")
                return

            if search_type == '2':
                perfume_name = input("Enter the perfume name (or type 'back' to go to main menu): ")
                if perfume_name.lower() == 'back':
                    break
                matching_fragrances = get_fragrance_by_name(fragrances, perfume_name)
            elif search_type == '1':
                note_option = input("Enter a scent note to see available options (or type 'back' to go to main menu): ").strip().lower()
                if note_option == 'back':
                    break
                matching_fragrances = get_fragrance_by_note(fragrances, note_option)
            else:
                print("Invalid input. Please type '1' for note, or '2' for name.")
                continue

            if matching_fragrances:
                for i in range(0, len(matching_fragrances), 5):
                    batch = matching_fragrances[i:i + 5]
                    for selected_fragrance in batch:
                        display_fragrance(selected_fragrance)
                    if i + 5 < len(matching_fragrances):
                        more = input("Do you want to see more results? (yes/no or type 'back' to main menu): ").strip().lower()
                        if more == 'back':
                            break
                        elif more != 'yes':
                            break
                else:
                    print("No more results to display.")
            else:
                print("No fragrances found with that input. Please try again.")

            look_again = input("Do you want to look up another perfume? (yes/no): ").strip().lower()
            if look_again != 'yes':
                print("Thank you for using the perfume recommendation program!")
                return


if __name__ == "__main__":
    main()
