import json

#jprint to print the json in a readable way
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

#return python string of json
def get_text(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    return text