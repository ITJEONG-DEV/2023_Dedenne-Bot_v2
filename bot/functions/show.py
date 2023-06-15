import discord

from lostark.api import *
from .send import send_message


async def show_dobyss(message, auth, icon_url):
    response = get_dobyss_info(auth)

    embeds = []
    for item in response:
        embed = discord.Embed(
            title=f"{item['AreaName']} - {item['Name']}",
            color=discord.Color.blue()
        )

        embed.set_footer(icon_url=icon_url)
        embed.add_field(name="기간", value=f"{item['StartTime']} ~ {item['EndTime']}")

        embed.set_image(url=item['Image'])

        embeds.append(embed)

    if len(embeds) > 0:
        await send_message(message.channel, embeds=embeds)
    else:
        await send_message(message.channel, message="정보를 조회할 수 없습니다.")


async def show_doguard(message, auth, icon_url):
    response = get_doguard_info(auth)

    embeds = []
    for item in response["Raids"]:
        embed = discord.Embed(
            title=f"{item['Name']}",
            color=discord.Color.blue()
        )

        embed.set_footer(icon_url=icon_url)
        embed.add_field(name="기간", value=f"{item['StartTime']} ~ {item['EndTime']}")

        embed.set_image(url=item['Image'])

        embeds.append(embed)

    if len(embeds) > 0:
        await send_message(message.channel, embeds=embeds)
    else:
        await send_message(message.channel, message="정보를 조회할 수 없습니다.")


async def show_events(message, auth, icon_url):
    data = get_events(auth)

    if data is None:
        await send_message(channel=message.channel, message="이벤트 정보를 조회할 수 없어요.")

    else:
        embeds = []
        for news in data:
            embed = discord.Embed(
                title=news["Title"],
                url=news["Link"],
                color=discord.Color.blue()
            )

            start_date = news["StartDate"].split("T")[0]
            end_date = news["EndDate"].split("T")[0]

            embed.set_image(url=news["Thumbnail"])
            embed.set_footer(text=f"이벤트 기간: {start_date} ~ {end_date}", icon_url=icon_url)

            embeds.append(embed)

            if len(embeds) == 10:
                await send_message(message.channel, embeds=embeds)
                embeds.clear()

        if len(embeds) > 0:
            await send_message(message.channel, embeds=embeds)


async def show_notices(message, auth, icon_url):
    max_count = 5
    data = get_notices('', auth)

    if data is None:
        await send_message(channel=message.channel, message="공지 정보를 조회할 수 없어요.")

    else:
        embeds = []
        for i in range(max_count if max_count < len(data) else len(data)):
            news = data[i]

            embed = discord.Embed(
                title=news["Type"] + news["Title"],
                url=news["Link"],
                color=discord.Color.blue()
            )

            embed.set_footer(text=f"{news['Date']}", icon_url=icon_url)

            embeds.append(embed)

        await send_message(message.channel, embeds=embeds)


async def show_adventure_island(message, auth, icon_url):
    link = get_adventure_island(auth)

    if link == "":
        embed = discord.Embed(
            title="모험섬",
            url="https://lostark.game.onstove.com/Library/Tip/Views/138208?page=1&libraryStatusType=0&librarySearchCategory=0&searchtype=0&searchtext=&ordertype=latest&LibraryQaAnswerType=None&UserPageType=0",
            color=discord.Color.blue()
        )

        embed.set_footer(text="2021. 7. 10 기준", icon_url=icon_url)
        embed.add_field(name="평일", value="11:00 / 13:00 / 19:00 / 21:00 / 23:00")
        embed.add_field(name="주말", value="(오전) 09:00 / 11:00 / 13:00\n(오후) 19:00 / 21:00 / 23:00")

        await send_message(message.channel, embed=embed)

    else:
        await send_message(message.channel, file=discord.File(link))
