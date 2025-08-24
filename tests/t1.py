import json

with open('mock_hotels.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    for i in data:
        print(type(i))
print(data)