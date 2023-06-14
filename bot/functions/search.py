import discord
import datetime

from lostark.crawling import get_character_data, get_mari_shop
from lostark.api import *
from .send import send_message
from ..views import CharacterView, MariShopView


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
            item_name += "레벨"

    result_items = get_gems(item_name, auth)["Items"]

    if result_items:
        image_url = result_items[0]["Icon"]

        embed = discord.Embed(
            title=f"{item_name} 검색 결과",
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
