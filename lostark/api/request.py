import requests
import json

main_url = "https://developer-lostark.game.onstove.com"


def get_GET_headers(auth):
    return {'accept': 'application/json', 'authorization': auth}


def get_POST_headers(auth):
    return {'accept': 'application/json', 'authorization': auth, 'Content-Type': 'application/json'}


def get_news(auth):
    request_url = main_url + "/news/events"

    response = requests.get(request_url, headers=get_GET_headers(auth), verify=False)

    return response.json()


def get_dobyss_info(auth):
    request_url = main_url + "/gamecontents/challenge-abyss-dungeons"

    response = requests.get(request_url, headers=get_GET_headers(auth), verify=False)

    return response.json()


def get_doguard_info(auth):
    request_url = main_url + "/gamecontents/challenge-guardian-raids"

    response = requests.get(request_url, headers=get_GET_headers(auth), verify=False)

    return response.json()


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

    return response.json()


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

    return response.json()


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

    return response.json()


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

    return response.json()
