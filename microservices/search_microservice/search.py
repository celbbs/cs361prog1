import csv
import time
import os

SEND_FILE = 'microservices/search_microservice/send.csv'
RESPONSE_FILE = 'microservices/search_microservice/response_search.csv'
FRAGDATA_FILE = 'microservices/search_microservice/fragdata.csv'

def read_fragrance_data():
    """get info from fragdata csv"""
    fragrances = []
    if os.path.exists(FRAGDATA_FILE):
        with open(FRAGDATA_FILE, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                fragrances.append({
                    'name': row[0],
                    'brand': row[1],
                    'notes': row[2]
                })
    return fragrances

def write_results(results):
    """write the results to the response csv"""
    with open(RESPONSE_FILE, mode='w', newline='', encoding='utf-8') as response_file:
        writer = csv.writer(response_file)
        writer.writerow(["Name", "Brand", "Notes"])
        for result in results:
            writer.writerow([result['name'], result['brand'], result['notes']])

def search_service():
    """read from the send file and write results"""
    while True:
        if os.path.exists(SEND_FILE):
            with open(SEND_FILE, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    search_type = row[0]
                    query = row[1]
                    fragrances = read_fragrance_data()

                    if search_type == "name":
                        results = [fragrance for fragrance in fragrances if query.lower() in fragrance['name'].lower()]
                    elif search_type == "note":
                        results = [fragrance for fragrance in fragrances if query.lower() in fragrance['notes'].lower()]
                    else:
                        results = []

                    if results:
                        print(f"Found {len(results)} results for '{query}'.")
                        for fragrance in results:
                            print(f"- {fragrance['name']} by {fragrance['brand']} (Notes: {fragrance['notes']})")
                        write_results(results)
                    else:
                        print(f"No results found for '{query}'.")
                        write_results([])

        time.sleep(6)

if __name__ == "__main__":
    search_service()
