import json

with open("config.json") as f:
    config = json.load(f)

def is_admin(user_id):
    return str(user_id) in config["ADMIN_IDS"]
