# CSV file by: Nandini Bansal, Public Domain, via Kaggle.com 
# https://www.kaggle.com/datasets/nandini1999/perfume-recommendation-dataset?resource=download

import csv
import time
import os

SEARCH_SEND_FILE = 'microservices/search_microservice/send.csv'
SEARCH_RESPONSE_FILE = 'microservices/search_microservice/response_search.csv'

IMAGE_DESC_SEND_FILE = 'microservices/image_desc_microservice/send.csv'
IMAGE_DESC_RESPONSE_FILE = 'microservices/image_desc_microservice/response_image_desc.csv'

COMPARE_SEND_FILE = 'microservices/compare_microservice/send.csv'
COMPARE_RESPONSE_FILE = 'microservices/compare_microservice/response_compare.csv'

SEASON_SEND_FILE = 'microservices/season_microservice/season_request.csv'
SEASON_RESPONSE_FILE = 'microservices/season_microservice/recommendations.csv'

def write_to_send_csv(send_file, data):
    """write data to csv"""
    with open(send_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(data) 

def read_from_response_csv(response_file):
    """get response from csv"""
    result = []
    with open(response_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            result.append(row)
    return result

def search_service(query, search_type):
    """search microservice, by frag notes or by name"""
    write_to_send_csv(SEARCH_SEND_FILE, [search_type, query])
    time.sleep(6)
    return read_from_response_csv(SEARCH_RESPONSE_FILE)

def image_desc_service(fragrance_name):
    """run image/description microservice"""
    write_to_send_csv(IMAGE_DESC_SEND_FILE, ["image_desc", fragrance_name])
    time.sleep(8)
    return read_from_response_csv(IMAGE_DESC_RESPONSE_FILE)

def compare_service(name1, name2):
    """run the comparison microservice"""
    write_to_send_csv(COMPARE_SEND_FILE, ["compare", name1, name2])
    time.sleep(6)
    return read_from_response_csv(COMPARE_RESPONSE_FILE)

def season_service(season_selected):
    """run the season recommendation microservice"""
    write_to_send_csv(SEASON_SEND_FILE, [season_selected])
    time.sleep(6)
    return read_from_response_csv(SEASON_RESPONSE_FILE)

def main():
    print("Welcome to the Fragrance Program!")
    while True:
        print("\nChoose an option:")
        print("1: Search by name or scent note")
        print("2: Get image and description for a fragrance")
        print("3: Compare two fragrances")
        print("4: Get a fragrance reccomendation for a specific season")
        print("5: Exit the program")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            search_type = input("Search by (1) Name or (2) Scent Note: ").strip()
            if search_type == "1":
                search_query = input("Enter fragrance name: ").strip()
                results = search_service(search_query, "name")
            elif search_type == "2":
                search_query = input("Enter scent note: ").strip()
                results = search_service(search_query, "note")
            else:
                print("Invalid choice! Please try again.")
                continue

            if results:
                print(f"\nFound {len(results)} matching fragrance(s):")

                batch_size = 5
                start_index = 0

                while start_index < len(results):
                    for i in range(start_index, min(start_index + batch_size, len(results))):
                        print(f"- {results[i][0]} by {results[i][1]} (Notes: {results[i][2]})")
                    
                    start_index += batch_size
                    if start_index < len(results):
                        user_input = input("\nWould you like to see more results? (yes/no): ").strip().lower()
                        if user_input != "yes":
                            print("Ending search")
                            break
            else:
                print(f"No results found for your query: '{search_query}'.")

        elif choice == "2":
            fragrance_name = input("Enter fragrance name to get details: ").strip()
            image_desc = image_desc_service(fragrance_name)
            if image_desc:
                print(f"\nImage: {image_desc[0][1]}")
                print(f"Description: {image_desc[0][2]}")
            else:
                print(f"No image or description found for '{fragrance_name}'.")

        elif choice == "3":
            name1 = input("Enter first fragrance name: ").strip()
            name2 = input("Enter second fragrance name: ").strip()
            comparison_result = compare_service(name1, name2)
            if comparison_result:
                print(f"\nComparison result: {comparison_result[0]}")
            else:
                print("No comparison data found for the given fragrances.")

        elif choice == "4":
            season_name = input("Which season would you like to get a fragrance for? (e.g., spring, summer, autumn, winter): ").strip().lower()
            season_result = season_service(season_name)
            if season_result:
                print(f"\nFound {len(season_result)} fragrance(s) for '{season_name}':")
                for frag in season_result:
                    print(f"- {frag[0]} by {frag[1]} (Notes: {frag[2]})")
            else:
                print(f"No recommendations found for '{season_name}'.")

        elif choice == "5":
            print("\nExiting the program. Goodbye!")
            break

        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
