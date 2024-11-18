import csv
import os
import time

request_file = 'microservices/season_microservice/season_request.csv'
response_file = 'microservices/season_microservice/recommendations.csv'
filename = 'microservices/season_microservice/fragrance_data.csv'

def get_frags(filename):
    perfume_database = []
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                perfume_database.append({
                    "name": row["Name"],
                    "brand": row["Brand"],
                    "scent_note": row["Notes"].strip(),
                })
    except FileNotFoundError:
        print(f"Error: '{filename}' not found.")
    return perfume_database

def get_recommendations(season):
    seasonal_notes = {
        "spring": "floral",
        "summer": "citrus",
        "autumn": "woody",
        "winter": "spicy"
    }
    fragrances = get_frags(filename)
    note = seasonal_notes.get(season.lower(), "")
    matching_fragrances = [f for f in fragrances if note in f["scent_note"].lower()]
    return matching_fragrances

def process_request():
    while True:
        if os.path.exists(request_file) and os.stat(request_file).st_size > 0:
            try:
                with open(request_file, mode='r', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    season = next(reader)[0].strip().lower()
                    print(f"Processing request for season: '{season}'")

                recommendations = get_recommendations(season)

                with open(response_file, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    if recommendations:
                        writer.writerow(["Name", "Brand", "Notes"])
                        for fragrance in recommendations[:5]:
                            writer.writerow([fragrance["name"], fragrance["brand"], fragrance["scent_note"]])
                        print(f"{len(recommendations[:5])} recommendation(s) written to '{response_file}'.")
                    else:
                        writer.writerow(["Message"])
                        writer.writerow(["No recommendations found for this season."])
                        print("No recommendations found for this season.")
            except FileNotFoundError:
                print(f"Error: '{request_file}' not found. Please ensure the request file exists.")

            time.sleep(5)
        else:
            time.sleep(5)

if __name__ == "__main__":
    process_request()
