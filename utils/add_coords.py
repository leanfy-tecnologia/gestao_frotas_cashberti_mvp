import json
import random

def add_coordinates_to_abastecimentos():
    file_path = 'data/abastecimentos.json'
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            abastecimentos = json.load(f)
            
        # Bounding box roughly for São José dos Pinhais, PR
        # Central area
        LAT_MIN = -25.5600
        LAT_MAX = -25.5000
        LON_MIN = -49.2200
        LON_MAX = -49.1600
        
        for abastecimento in abastecimentos:
            if 'latitude' not in abastecimento or 'longitude' not in abastecimento:
                abastecimento['latitude'] = round(random.uniform(LAT_MIN, LAT_MAX), 6)
                abastecimento['longitude'] = round(random.uniform(LON_MIN, LON_MAX), 6)
                
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(abastecimentos, f, indent=4, ensure_ascii=False)
            
        print(f"Successfully added coordinates to {len(abastecimentos)} records.")
        
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    add_coordinates_to_abastecimentos()
