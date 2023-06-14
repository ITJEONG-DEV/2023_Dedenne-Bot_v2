import requests

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
