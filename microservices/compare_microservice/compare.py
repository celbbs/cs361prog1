import csv
import time
import os

SEND_FILE = 'microservices/compare_microservice/send.csv'
RESPONSE_FILE = 'microservices/compare_microservice/response_compare.csv'
FRAGDATA_FILE = 'microservices/compare_microservice/fragdata.csv'

def read_fragrance_data():
    """read fragdata from csv"""
    fragrances = []
    if os.path.exists(FRAGDATA_FILE):
        with open(FRAGDATA_FILE, mode='r', encoding='ISO-8859-1') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                fragrances.append({
                    'name': row[0],
                    'notes': row[3]
                })
    return fragrances

def compare_service():
    """run the comparison service"""
    while True:
        if os.path.exists(SEND_FILE):
            with open(SEND_FILE, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == "compare":
                        name1, name2 = row[1], row[2]
                        fragrances = read_fragrance_data()
                        fragrance1 = next((fragrance for fragrance in fragrances if fragrance['name'].lower() == name1.lower()), None)
                        fragrance2 = next((fragrance for fragrance in fragrances if fragrance['name'].lower() == name2.lower()), None)

                        comparison_result = f"Comparison between {name1} and {name2}"
                        if fragrance1 and fragrance2:
                            comparison_result += f": Notes are, {fragrance1['notes']} vs {fragrance2['notes']}"
                        else:
                            comparison_result += ": One or both fragrances not found."

                        with open(RESPONSE_FILE, mode='w', newline='', encoding='utf-8') as response_file:
                            writer = csv.writer(response_file)
                            writer.writerow(["Comparison Result"])
                            writer.writerow([comparison_result])

                        print(f"Comparison between '{name1}' and '{name2}' written to {RESPONSE_FILE}")
            
            time.sleep(1) 
        else:
            time.sleep(1)

if __name__ == "__main__":
    compare_service()
