import datetime
import discord

from .functions import *
from util import parse_json

KOREA = datetime.timezone(datetime.timedelta(hours=9))


class DedenneBot(discord.Client):

    def __init__(self, *, intents, **options):
        super().__init__(intents=intents, **options)

        self.words = parse_json("private/command.json")
        self.lostark = parse_json("private/lostark.json")

        self.icon = "https://cdn-lostark.game.onstove.com/2018/obt/assets/images/common/icon/favicon-192.png"

    def check_update_available(self):
        content = ""
        with open("./private/update.txt", "r", encoding="utf-8") as txt:
            content = txt.read()

        open("./private/update.txt", "w").close()

        if len(content) > 10:
            return content
        else:
            return None

    async def on_ready(self):

        update_content = self.check_update_available()

        if update_content:
            for guild in self.guilds:
                if guild.id == 957221859953352725:
                    for channel in guild.text_channels:
                        if "봇" in channel.name:
                            await channel.send(update_content)

                else:
                    for channel in guild.text_channels:
                        if "데덴네" in channel.name:
                            await channel.send(update_content)
                            
        else:
            print("업데이트 내용이 없음")

    async def on_message(self, message):
        await self.wait_until_ready()

        # 데덴네봇을 위한 채널이 아닌 경우 응답하지 않음

        # 957221859953352725 여기가 어디죠?
        # 1021645719528022077 디스코드봇 테스트용 서버

        if message.guild is None:
            return

        if message.guild.id == 957221859953352725:
            if str(message.channel) != '봇':
                return

        else:
            if not str(message.channel).__contains__("데덴네"):
                return

        # 본인인 경우 응답하지 않음
        if message.author == self.user:
            return

        command = self.get_return_words(message.content)

        if command is not None:
            if command == "help":
                await send_help_message(message)

            elif command == "search":
                await search_lostark(message)

            elif command == "item":
                # await send_message(channel=message.channel, message="준비 중인 기능")
                await search_market(message, self.lostark["apikeyauth"], self.icon)

            elif command == "avatar":
                await search_avatar(message, self.lostark["apikeyauth"], self.icon)

            elif command == "mari":
                await search_mari_shop(message)

            elif command == "engrave":
                await search_engrave(message, self.lostark["apikeyauth"], self.icon)

            elif command == "gem":
                await search_gem(message, self.lostark["apikeyauth"], self.icon)

            elif command == "leafstone":
                await search_leaf_stone(message, self.lostark["apikeyauth"], self.icon)

            elif command == "occup":
                await send_occup_message(message, self.icon)

            elif command == "island":
                await show_adventure_island(message, self.lostark["apikeyauth"], self.icon)

            elif command == "dobyss":
                await show_dobyss(message, self.lostark["apikeyauth"], self.icon)

            elif command == "doguard":
                await show_doguard(message, self.lostark["apikeyauth"], self.icon)

            elif command == "events":
                await show_events(message, self.lostark["apikeyauth"], self.icon)

            elif command == "notices":
                # await send_message(message.channel, "현재 준비중인 기능입니당")
                await show_notices(message, self.lostark["apikeyauth"], self.icon)

            elif command == "gif":
                await make_gif(message)

    def get_return_words(self, message):
        for item in self.words:
            for word in item["trigger"]:
                if word in message:
                    return item["return"]

        return None
