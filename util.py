import json


def parse_json(url):
    with open(url, "r", encoding="UTF-8") as json_txt:
        json_contents = json.load(json_txt)

        return json_contents
