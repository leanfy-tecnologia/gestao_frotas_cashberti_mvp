import json
import random

def redistribute_coordinates():
    file_path = 'data/abastecimentos.json'
    
    # 10 Hotspots in São José dos Pinhais
    hotspots = [
        {"lat": -25.534500, "lon": -49.206200, "weight": 0.50}, # Main Station (50%)
        {"lat": -25.520000, "lon": -49.190000, "weight": 0.055},
        {"lat": -25.550000, "lon": -49.220000, "weight": 0.055},
        {"lat": -25.510000, "lon": -49.170000, "weight": 0.055},
        {"lat": -25.540000, "lon": -49.230000, "weight": 0.055},
        {"lat": -25.500000, "lon": -49.200000, "weight": 0.055},
        {"lat": -25.560000, "lon": -49.180000, "weight": 0.055},
        {"lat": -25.530000, "lon": -49.160000, "weight": 0.055},
        {"lat": -25.570000, "lon": -49.210000, "weight": 0.055},
        {"lat": -25.515000, "lon": -49.225000, "weight": 0.060}, # Slightly more to fill the rest
    ]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            abastecimentos = json.load(f)
            
        random.shuffle(abastecimentos) # Shuffle to distribute randomly across time
        
        current_idx = 0
        total_records = len(abastecimentos)
        
        for hotspot in hotspots:
            # Calculate how many records for this hotspot
            count = int(total_records * hotspot['weight'])
            # Ensure we don't go out of bounds on the last one
            if hotspot == hotspots[-1]:
                end_idx = total_records
            else:
                end_idx = min(current_idx + count, total_records)
            
            for i in range(current_idx, end_idx):
                # Add location with small jitter (approx 100-200 meters)
                jitter_lat = random.uniform(-0.0015, 0.0015)
                jitter_lon = random.uniform(-0.0015, 0.0015)
                
                abastecimentos[i]['latitude'] = round(hotspot['lat'] + jitter_lat, 6)
                abastecimentos[i]['longitude'] = round(hotspot['lon'] + jitter_lon, 6)
            
            current_idx = end_idx
                
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(abastecimentos, f, indent=4, ensure_ascii=False)
            
        print(f"Successfully redistributed {total_records} records into 10 hotspots.")
        
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    redistribute_coordinates()
