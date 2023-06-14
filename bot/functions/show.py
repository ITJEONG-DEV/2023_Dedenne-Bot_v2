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

async def show_news(message, auth, icon_url):
    data = get_news(auth)

    if data is None:
        await send_message(channel=message.channel, message="로스트아크 소식 정보를 조회할 수 없어요.")

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