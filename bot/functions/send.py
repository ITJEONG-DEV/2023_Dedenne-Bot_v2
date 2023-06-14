import discord

ad_title = ""
ad_url = ""
ad_filename = ""
ad_text = ""


# 기본 send_message
async def send_message(channel, message=None, file=None, embeds=None, embed=None, view=None, ads=False):
    _ = await channel.send(content=message, file=file, embeds=embeds, embed=embed, view=view)

    return _


# help message
async def send_help_message(message):
    with open("./private/help.txt", "r", encoding="utf-8") as txt:
        content = txt.read()

        await send_message(channel=message.channel, message=content)


# 점령전
async def send_occup_message(message, icon_url):
    embed = discord.Embed(
        title="점령전 시간",
        url="https://m-lostark.game.onstove.com/News/Notice/Views/1907?page=1&searchtype=0&searchtext=&noticetype=all",
        color=discord.Color.blue()
    )

    embed.set_footer(text="2022. 3. 30 기준", icon_url=icon_url)

    embed.add_field(name="개최 가능 요일", value="목, 금, 토, 일")
    embed.add_field(name="참여 가능 시간", value="12:30 / 16:30 / 18:30 / 19:30 / 22:30 / 23:30")

    await send_message(message.channel, embed=embed)
