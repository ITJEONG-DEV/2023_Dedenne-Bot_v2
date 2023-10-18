import urllib.parse
from urllib.request import urlopen
from bs4 import BeautifulSoup

try:
    from .data import Profile, MariShop
except:
    from lostark.crawling.data import Profile, MariShop


def get_html_object(url="https://lostark.game.onstove.com/Profile/Character/허니퓨"):
    html = urlopen(url)
    return BeautifulSoup(html, "html.parser")


def get_html_object_korean(default_url="https://lostark.game.onstove.com/Profile/Character/", character_name="허니퓨"):
    character_name = urllib.parse.quote_plus(character_name)
    url = default_url + character_name

    return get_html_object(url)


def get_character_data(base_url="https://lostark.game.onstove.com/Profile/Character/", character_name="wpqlRhc"):
    character_name = urllib.parse.quote_plus(character_name)
    bs_object = get_html_object(base_url + character_name)

    if "캐릭터 정보가 없습니다." in bs_object.text or "서비스 점검" in bs_object.text:
        return None

    return Profile(bs_object)


def get_mari_shop(base_url="https://lostark.game.onstove.com/Shop"):
    bs_object = get_html_object(base_url)

    if "서비스 점검" in bs_object.text:
        return None

    return MariShop(bs_object, base_url)


if __name__ == "__main__":
    # bs_object = get_html_object_korean()

    data = get_character_data(character_name="거리의아이")
    # print(data.profile_ingame.profile_equipment)

    # import json

    # character_name = "바드는죽어서힐을"
    # with open(f"{character_name}.txt", "w") as t:
    #     data = get_html_object_korean(character_name=character_name)
    #
    #     t.write(data.prettify())

    # data = get_mari_shop()
    # data = get_gold_info()
