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