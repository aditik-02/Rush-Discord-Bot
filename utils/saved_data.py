import json
import os

SAVE_PATH = "data/saved_cafes.json"

def load_saved_data():
    if not os.path.exists(SAVE_PATH):
        return {}
    with open(SAVE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def save_cafe_for_user(user_id, cafe):
    data = load_saved_data()
    uid = str(user_id)
    if uid not in data:
        data[uid] = []
    if cafe not in data[uid]:
        data[uid].append(cafe)
    save_data(data)

def get_saved_cafes(user_id):
    data = load_saved_data()
    return data.get(str(user_id), [])