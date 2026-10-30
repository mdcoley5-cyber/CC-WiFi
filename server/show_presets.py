import json
from app import app, get_presets

with app.app_context():
    resp = get_presets()
    presets = [p for p in resp.json if p['name'] != '[Empty]']
    print(json.dumps(presets, indent=2))
