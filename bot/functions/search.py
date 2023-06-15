import discord
import datetime

from lostark.crawling import get_character_data, get_mari_shop
from lostark.api import *
from .send import send_message
from ..views import CharacterView, MariShopView, MarketView


async def search_lostark(message):
    keyword = message.content.split()[-1]
    data = get_character_data(character_name=keyword)

    if data is None:
        return await send_message(channel=message.channel, message=f"{keyword}의 정보를 조회할 수 없어요.")

    options = CharacterView(data=data)

    embed = discord.Embed(
        title=data.name + "@" + data.server + " " + data.lv,
        url="https://lostark.game.onstove.com/Profile/Character/" + data.name,
        color=discord.Color.blue()
    )

    embed.set_image(url=data.profile_ingame.profile_equipment.src)
    embed.set_footer(text=data.name + "\t\t\t" + data.time + " 기준", icon_url=data.emblem)

    embed.add_field(name="원정대 레벨", value=f"`{data.profile_ingame.profile_info.expedition_lv}`")
    embed.add_field(name="아이템 레벨", value=f"`{data.profile_ingame.profile_info.equip_item_lv}`")
    embed.add_field(name="영지",
                    value=f"`{data.profile_ingame.profile_info.estate_name} {data.profile_ingame.profile_info.estate_lv}`")

    m = "```diff\n"
    for slot in data.profile_ingame.profile_equipment.ability_engrave_slot.ability:
        if "감소" in str(slot):
            m += "-" + str(slot) + "\n"
        else:
            m += "+" + str(slot) + "\n"
    if m == "```diff\n":
        m = "-"
    else:
        m += "```"
    embed.add_field(name="각인 효과", value=m)

    m = f" 공격력 `{data.state.attack}`\n최대 생명력 `{data.state.hp}`"
    embed.add_field(name="기본 특성", value=m)

    options.embeds["기본 정보"] = embed

    message = await send_message(message.channel, embed=options.embeds["기본 정보"], view=options)
    options.set_message(message)


async def search_mari_shop(message):
    data = get_mari_shop()
    options = MariShopView(data=data)

    if data is None:
        return await send_message(channel=message.channel, message=f"마리샵 정보를 조회할 수 없어요.")

    embed = discord.Embed(
        title=data.title,
        url=data.url,
        color=discord.Color.blue()
    )

    embed.set_footer(text=data.time + " 기준", icon_url=options.icon_url)

    m = ""
    for i in range(len(data.tab1)):
        item = data.tab1[i]
        m += f"```diff\n+{item[0]}\n-크리스탈 {item[1]}\n```"
    if m == "":
        m = "현재 판매 상품이 없습니다"
    embed.add_field(name="현재 판매 상품", value=m)

    pre_num = int(len(data.tab1_pre) / 6)

    for i in range(pre_num):
        m = ""
        for j in range(6):
            item = data.tab1_pre[i * 6 + j]
            m += f"```diff\n+{item[0]}\n-크리스탈 {item[1]}\n```"
        if m == "":
            m = "이전 판매 상품이 없습니다"
        embed.add_field(name=data.tab1_pre_name[i], value=m)

    options.embeds["성장 추천"] = embed
    message = await send_message(message.channel, embed=options.embeds["성장 추천"], view=options)
    options.set_message(message)


async def search_gem(message, auth, icon_url):
    words = message.content.split()

    item_name = ""

    if len(words) >= 2:
        item_name = words[1]

        if "홍" in item_name:
            item_name = item_name[:-1] + "레벨 홍염의 보석"
            # item_name.replace("홍", "레벨 홍염의 보석")
        elif "멸" in item_name:
            item_name = item_name[:-1] + "레벨 멸화의 보석"
            # item_name.replace("멸", "레벨 멸화의 보석")
        else:
            if "레벨" not in item_name:
                item_name += "레벨"

    result_items = get_gems(item_name, auth)["Items"]

    if result_items:
        image_url = result_items[0]["Icon"]

        embed = discord.Embed(
            title=f"{result_items[0]['Name']} 검색 결과",
            color=discord.Color.blue()
        )
        embed.set_footer(text=f"{datetime.datetime.now()} 기준", icon_url=icon_url)
        embed.set_thumbnail(url=image_url)

        str_field = ""
        for item in result_items:
            str_field += f'{item["Name"]} {item["AuctionInfo"]["BuyPrice"]}골드\n'

        embed.add_field(name="매물", value=str_field)

        await send_message(message.channel, embed=embed)

    else:
        await send_message(message.channel, message=f"{' '.join(words[1:])}에 해당하는 매물이 없어요")


async def search_leaf_stone(message, auth, icon_url):
    result_items = get_leaf_stone(auth)["Items"]

    if result_items:
        time = datetime.datetime.now()
        embeds = []

        for i in range(2):
            item = result_items[i]
            embed = discord.Embed(
                title=item["Name"],
                color=discord.Color.blue()
            )
            embed.set_footer(text=f"{time} 기준", icon_url=icon_url)
            embed.set_thumbnail(url=item["Icon"])

            embed.add_field(name="전날 평균 판매가", value=item["YDayAvgPrice"])
            embed.add_field(name="최근 판매가", value=item["RecentPrice"])
            embed.add_field(name="현재 최저가", value=item["CurrentMinPrice"])

            embeds.append(embed)

        await send_message(message.channel, embeds=embeds)

    else:
        await send_message(message.channel, message=f"돌파석 시세를 검색할 수 없어요.")


async def search_engrave(message, auth, icon_url):
    def get_item_id(name):
        keyword_dict = {
            "스커": "스트라이커",
            "디트": "디스트로이어",
            "배마": "배틀마스터",
            "알카": "아르카나",
            "데헌": "데빌헌터",
            "가짜건슬": "데빌헌터",
            "홀나": "홀리나이트",

            "구동": "구슬동자",
            "강무": "강화 무기",
            "결대": "결투의 대가",
            "극의체술": "극의:",
            "급타": "급소타격",
            "고기": "고독한 기사",
            "기대": "기습의 대가",
            "달소": "달의 소리",
            "달저": "달인의 저력",
            "돌대": "돌격대장",
            "마효증": "마나 효율 증가",
            "마흐": "마나의 흐름",
            "부뼈": "부러진 뼈",
            "분망": "분노의 망치",
            "번분": "번개의 분노",
            "사시": "사냥의 시간",
            "상소": "상급 소환사",
            "선필": "선수필승",
            "시집": "시선 집중",
            "아기": "아르데타인의 기술",
            "안상": "안정된 상태",
            "약무": "약자 무시",
            "예둔": "예리한 둔기",
            "저받": "저주받은",
            "전태": "전투 태세",
            "절구": "절실한 구원",
            "정단": "정밀 단도",
            "정흡": "정기 흡수",
            "중수": "중력 수련",
            "중착": "중갑 착용",
            "진용": "진실된 용맹",
            "질증": "질량 증가",
            "최마증": "최대 마나 증가",
            "충단": "충격 단련",
            "타대": "타격의 대가",
            "폭전": "폭발물 전문가",
            "피메": "피스메이커",
            "핸건": "핸드거너"
        }

        if name in keyword_dict.keys():
            name = keyword_dict[name]

        return name

    keyword = get_item_id(message.content.split()[-1])

    if keyword == "순위":
        data = get_engrave_rank(auth)["Items"]

    else:
        data = get_engrave(keyword, auth)["Items"]

    if len(data) == 0:
        return await send_message(message.channel, f"{keyword} 각인서를 찾을 수 없습니다")

    embeds = []

    if keyword == "순위":
        for i in range(5):
            item = data[i]

            embed = discord.Embed(
                title=f"{item['Name']} 시세",
                color=discord.Color.blue()
            )
            embed.set_footer(icon_url=icon_url)

            embed.add_field(name="전날 평균 판매가", value=item["YDayAvgPrice"])
            embed.add_field(name="최근 판매가", value=item["RecentPrice"])
            embed.add_field(name="현재 최저가", value=item["CurrentMinPrice"])
            embed.set_thumbnail(url=item["Icon"])

            embeds.append(embed)

        await send_message(message.channel, message="전설 각인서 순위 TOP 5", embeds=embeds)

    else:
        for item in data:
            embed = discord.Embed(
                title=f"{item['Name']} 시세",
                color=discord.Color.blue()
            )
            embed.set_footer(icon_url=icon_url)

            embed.add_field(name="전날 평균 판매가", value=item["YDayAvgPrice"])
            embed.add_field(name="최근 판매가", value=item["RecentPrice"])
            embed.add_field(name="현재 최저가", value=item["CurrentMinPrice"])
            embed.set_thumbnail(url=item["Icon"])

            embeds.append(embed)

        await send_message(message.channel, embeds=embeds)


async def search_avatar(message, auth, icon_url):
    max_count = 4
    content = message.content.split()[1:]

    if "직업" in message.content:
        name = ' '.join(content[:-1])
        character_class = content[-1].split("=")[1]
    else:
        name = ' '.join(content[:])
        character_class = ''

    print(name, character_class)

    avatar_info = get_avatar(name, character_class, auth)["Items"]

    if avatar_info is None:
        if character_class == "":
            return await send_message(message.channel, message=f"{name} 아바타를 검색할 수 없어요")
        else:
            return await send_message(message.channel, message=f"{character_class} 직업의 {name} 아바타를 검색할 수 없어요")

    embeds = []
    now = datetime.datetime.now()
    for i in range(max_count if max_count < len(avatar_info) else len(avatar_info)):
        item = avatar_info[i]

        embed = discord.Embed(
            title=f"{item['Name']}",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=item["Icon"])
        embed.set_footer(text=f"{now} 기준", icon_url=icon_url)

        embed.add_field(name="전날 평균 판매가", value=item["YDayAvgPrice"])
        embed.add_field(name="최근 판매가", value=item["RecentPrice"])
        embed.add_field(name="현재 최저가", value=item["CurrentMinPrice"])
        embed.add_field(name="구매 시 거래 가능 횟수", value=item["TradeRemainCount"])

        embeds.append(embed)

    await send_message(message.channel, embeds=embeds)


async def search_market(message, auth, icon_url):
    if not message.content == "아이템":
        words = message.content.split()
        keyword = " ".join(words[1:])
    else:
        keyword = ""

    options = MarketView(data=None)
    message = await send_message(message.channel, message="검색 옵션을 설정합니다.", view=options)
    options.set_message(message)
    options.keyword = keyword
    options.auth = auth
    options.icon_url = icon_url
