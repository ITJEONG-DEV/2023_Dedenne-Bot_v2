import requests
import json

main_url = "https://developer-lostark.game.onstove.com"


def get_GET_headers(auth):
    return {'accept': 'application/json', 'authorization': auth}


def get_POST_headers(auth):
    return {'accept': 'application/json', 'authorization': auth, 'Content-Type': 'application/json'}


def get_events(auth):
    request_url = main_url + "/news/events"

    response = requests.get(request_url, headers=get_GET_headers(auth), verify=False)

    try:
        data = response.json()
        return data
    except:
        return None


def get_notices(type, auth):
    request_url = main_url + f"/news/notices/"

    response = requests.get(request_url, headers=get_GET_headers(auth), verify=False)

    try:
        data = response.json()
        return data
    except:
        return None


def get_dobyss_info(auth):
    request_url = main_url + "/gamecontents/challenge-abyss-dungeons"

    response = requests.get(request_url, headers=get_GET_headers(auth), verify=False)

    try:
        data = response.json()
        return data
    except:
        return None


def get_doguard_info(auth):
    request_url = main_url + "/gamecontents/challenge-guardian-raids"

    response = requests.get(request_url, headers=get_GET_headers(auth), verify=False)

    try:
        data = response.json()
        return data
    except:
        return None


def get_siblings(name, auth):
    request_url = main_url + f"/characters/{name}/siblings"

    response = requests.get(request_url, headers=get_GET_headers(auth), verify=False)

    try:
        data = response.json()
        return data
    except:
        return None


def get_gems(name, auth):
    data_dict = {}

    data_dict["ItemLevelMin"] = 0
    data_dict["ItemLevelMax"] = 0
    data_dict["ItemGradeQuality"] = 0

    data_dict["SkillOptions"] = [{}]
    data_dict["SkillOptions"][0]["FirstOption"] = None
    data_dict["SkillOptions"][0]["SecondOption"] = None
    data_dict["SkillOptions"][0]["MinValue"] = None
    data_dict["SkillOptions"][0]["MaxValue"] = None

    data_dict["EtcOptions"] = [{}]
    data_dict["EtcOptions"][0]["FirstOption"] = None
    data_dict["EtcOptions"][0]["SecondOption"] = None
    data_dict["EtcOptions"][0]["MinValue"] = None
    data_dict["EtcOptions"][0]["MaxValue"] = None

    data_dict["Sort"] = "BUY_PRICE"
    data_dict["CategoryCode"] = 210000
    data_dict["CharacterClass"] = ""
    data_dict["ItemTier"] = 3
    data_dict["ItemGrade"] = ""
    data_dict["ItemName"] = name
    data_dict["PageNo"] = 0
    data_dict["SortCondition"] = "ASC"

    data = json.dumps(data_dict)

    request_url = main_url + "/auctions/items"

    response = requests.post(request_url, headers=get_POST_headers(auth), data=data, verify=False)

    try:
        data = response.json()

        if "Error" in data.keys():
            return {"Items": None}
        else:
            return data
    except:
        return {"Items": None}


def get_leaf_stone(auth):
    data_dict = {}

    data_dict["Sort"] = "RECENT_PRICE"
    data_dict["CategoryCode"] = 50010
    data_dict["CharacterClass"] = ""
    data_dict["ItemTier"] = 3
    data_dict["ItemGrade"] = "희귀"
    data_dict["ItemName"] = "돌파석"
    data_dict["PageNo"] = 0
    data_dict["SortCondition"] = "DESC"

    data = json.dumps(data_dict)

    request_url = main_url + "/markets/items"

    response = requests.post(request_url, headers=get_POST_headers(auth), data=data, verify=False)

    try:
        data = response.json()

        if "Error" in data.keys():
            return {"Items": None}
        else:
            return data
    except:
        return {"Items": None}


def get_engrave(name, auth):
    data_dict = {}

    data_dict["Sort"] = "RECENT_PRICE"
    data_dict["CategoryCode"] = 40000
    data_dict["CharacterClass"] = ""
    data_dict["ItemTier"] = None
    data_dict["ItemGrade"] = "전설"
    data_dict["ItemName"] = name
    data_dict["PageNo"] = 0
    data_dict["SortCondition"] = "DESC"

    data = json.dumps(data_dict)

    request_url = main_url + "/markets/items"

    response = requests.post(request_url, headers=get_POST_headers(auth), data=data, verify=False)

    try:
        data = response.json()

        if "Error" in data.keys():
            return {"Items": None}
        else:
            return data
    except:
        return {"Items": None}


def get_engrave_rank(auth):
    data_dict = {}

    data_dict["Sort"] = "RECENT_PRICE"
    data_dict["CategoryCode"] = 40000
    data_dict["CharacterClass"] = ""
    data_dict["ItemTier"] = None
    data_dict["ItemGrade"] = "전설"
    data_dict["ItemName"] = ""
    data_dict["PageNo"] = 0
    data_dict["SortCondition"] = "DESC"

    data = json.dumps(data_dict)

    request_url = main_url + "/markets/items"

    response = requests.post(request_url, headers=get_POST_headers(auth), data=data, verify=False)

    try:
        data = response.json()

        if "Error" in data.keys():
            return {"Items": None}
        else:
            return data
    except:
        return {"Items": None}


def get_avatar(name, character_class, auth):
    data_dict = {}

    data_dict["Sort"] = "GRADE"
    data_dict["CategoryCode"] = 20000
    data_dict["CharacterClass"] = character_class
    data_dict["ItemTier"] = None
    data_dict["ItemGrade"] = ""
    data_dict["ItemName"] = name
    data_dict["PageNo"] = 0
    data_dict["SortCondition"] = "DESC"

    data = json.dumps(data_dict)

    request_url = main_url + "/markets/items"

    response = requests.post(request_url, headers=get_POST_headers(auth), data=data, verify=False)

    try:
        data = response.json()

        if "Error" in data.keys():
            return {"Items": None}
        else:
            return data

    except:
        return {"Items": None}


def get_item(category, character_class, tier, grade, name, auth):
    data_dict = {}

    data_dict["Sort"] = "GRADE"
    data_dict["CategoryCode"] = category
    data_dict["CharacterClass"] = character_class
    data_dict["ItemTier"] = tier
    data_dict["ItemGrade"] = grade
    data_dict["ItemName"] = name
    data_dict["PageNo"] = 0
    data_dict["SortCondition"] = "DESC"

    data = json.dumps(data_dict)

    request_url = main_url + "/markets/items"

    response = requests.post(request_url, headers=get_POST_headers(auth), data=data, verify=False)
    try:
        data = response.json()

        if "Error" in data.keys():
            return {"Items": None}
        else:
            return data
    except:
        return {"Items": None}


def get_island_info(auth):
    request_url = main_url + "/gamecontents/calendar"

    response = requests.get(request_url, headers=get_GET_headers(auth), verify=False)

    island = []

    try:
        data = response.json()

        if "Error" in data.keys():
            return None

        for item in data:
            if "모험" in item["CategoryName"]:
                island.append(item)
    except:
        return None

    return island


if __name__ == "__main__":
    result = get_item("", "", None, None, "",
                      "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IktYMk40TkRDSTJ5NTA5NWpjTWk5TllqY2lyZyIsImtpZCI6IktYMk40TkRDSTJ5NTA5NWpjTWk5TllqY2lyZyJ9.eyJpc3MiOiJodHRwczovL2x1ZHkuZ2FtZS5vbnN0b3ZlLmNvbSIsImF1ZCI6Imh0dHBzOi8vbHVkeS5nYW1lLm9uc3RvdmUuY29tL3Jlc291cmNlcyIsImNsaWVudF9pZCI6IjEwMDAwMDAwMDAwMDA1MTMifQ.KJSweBbQpwz7OcYwY_Fc9FJDmSBL_8y0KqNXKq3KMC6vIgy-Cmsfzi7klAyjIJLGRB2SeW9sq--QbafkIHBeWUVD7jROy8mhLvKlr8vLnGJ5IePGriBtC6IB-Ma6Wr1w4Upa0jwBDE7eRwk6FPX21wrXnalqk-MpYpTBmPp1MmcaNVCoxZliMRsNtfrFrQE0RnceerNsBAoj6blyIt7wH9IB5dHTzLYEDVXBA6rQeS8gBzYzcKC4yWDcHSas6es_JqCykp-w9HdaT20YXZW0te3knRl2VZ3oOsVmCmCoPk3cSHaqaleesmabKnuWPd7sT6FCvdKeuhfCNvMNAze9nA")

    print(result)
