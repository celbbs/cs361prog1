import csv
import time
import os

SEND_FILE = 'microservices/image_desc_microservice/send.csv'
RESPONSE_FILE = 'microservices/image_desc_microservice/response_image_desc.csv'
FRAGDATA_FILE = 'microservices/image_desc_microservice/fragdata.csv'

def read_fragrance_data():
    """read fragdata csv"""
    fragrances = []
    if os.path.exists(FRAGDATA_FILE):
        with open(FRAGDATA_FILE, mode='r', encoding='ISO-8859-1') as file:
            reader = csv.reader(file)
            next(reader) 
            for row in reader:
                if len(row) >= 5:
                    fragrances.append({
                        'name': row[0],
                        'description': row[2],
                        'notes': row[3],
                        'image_url': row[4]
                    })
                else:
                    print(f"Skipping incomplete row: {row}")
    return fragrances

def image_desc_service():
    """return image and desc for fragrance"""
    while True:
        if os.path.exists(SEND_FILE):
            with open(SEND_FILE, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == "image_desc":
                        fragrance_name = row[1]
                        fragrances = read_fragrance_data()
                        
                        result = next((fragrance for fragrance in fragrances if fragrance['name'].lower() == fragrance_name.lower()), None)

                        with open(RESPONSE_FILE, mode='w', newline='', encoding='utf-8') as response_file:
                            writer = csv.writer(response_file)
                            if result:
                                writer.writerow(["Name", "Image URL", "Description", "Notes"])
                                writer.writerow([result['name'], result['image_url'], result['description'], result['notes']])
                            else:
                                writer.writerow(["Name", "Image URL", "Description", "Notes"])
                                writer.writerow([fragrance_name, "", "No description found", ""])

                        print(f"Details for '{fragrance_name}' written to {RESPONSE_FILE}")

            time.sleep(1)
        else:
            time.sleep(1)

if __name__ == "__main__":
    image_desc_service()
