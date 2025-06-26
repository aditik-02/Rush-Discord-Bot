import json

def load_cafes():
    with open("data/yelp_academic_dataset_business.json", "r", encoding="utf-8") as f:
        cafes = []
        for line in f:
            data = json.loads(line)
            
            if data.get("categories") and "Cafe" in data["categories"] and data.get("is_open", 0) == 1:
                attributes = data.get("attributes") or {}

                # Parse Ambience
                ambience_raw = attributes.get("Ambience")
                try:
                    raw_dict = eval(ambience_raw) if ambience_raw else {}
                    ambience = {
                        k: v is True
                        for k, v in raw_dict.items()
                        if isinstance(v, (bool, type(None)))
                    }
                except:
                    ambience = {}

                # Extract Price
                price = attributes.get("RestaurantsPriceRange2")
                try:
                    price = int(price) if price and price.isdigit() else None
                except:
                    price = None

                # Get hours
                hours = data.get("hours") or {}


                cafes.append({
                    "name": data["name"],
                    "city": data["city"],
                    "stars": data["stars"],
                    "address": data["address"],
                    "ambience": ambience,
                    "latitude": data["latitude"],
                    "longitude": data["longitude"],
                    "price": price,
                    "hours":hours
                })

        return cafes