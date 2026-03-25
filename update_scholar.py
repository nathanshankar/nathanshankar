import json
import os

def generate_shields_json():
    if not os.path.exists('google_scholar_nathan.json'):
        print("Error: google_scholar_nathan.json not found.")
        return

    with open('google_scholar_nathan.json', 'r') as f:
        data = json.load(f)

    # Extract stats from the SerpApi structure
    stats = data.get('cited_by', {}).get('table', [])
    
    # Defaults
    citations = "0"
    h_index = "0"
    i10_index = "0"

    if len(stats) > 0:
        citations = str(stats[0].get('citations', {}).get('all', 0))
    if len(stats) > 1:
        h_index = str(stats[1].get('h_index', {}).get('all', 0))
    if len(stats) > 2:
        i10_index = str(stats[2].get('i10_index', {}).get('all', 0))

    # Helper to create Shields.io compatible JSON
    def create_badge_json(label, message, color):
        return {
            "schemaVersion": 1,
            "label": label,
            "message": message,
            "color": color
        }

    # Save individual badge JSONs
    with open('citations.json', 'w') as f:
        json.dump(create_badge_json("Citations", citations, "blue"), f, indent=2)
    
    with open('h_index.json', 'w') as f:
        json.dump(create_badge_json("h-index", h_index, "orange"), f, indent=2)
        
    with open('i10_index.json', 'w') as f:
        json.dump(create_badge_json("i10-index", i10_index, "brightgreen"), f, indent=2)

    print("Generated citations.json, h_index.json, and i10_index.json")

if __name__ == "__main__":
    generate_shields_json()
