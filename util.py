import json


def parse_json(url):
    with open(url, "r", encoding="UTF-8") as json_txt:
        json_contents = json.load(json_txt)

        return json_contents


def overwrite_json(url, data):
    with open(url, "w", encoding="UTF-8") as json_txt:
        json.dump(data, json_txt)
