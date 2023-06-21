import datetime
import discord

from .functions import *
from util import parse_json

KOREA = datetime.timezone(datetime.timedelta(hours=9))
time = datetime.time(hour=15, minute=38, tzinfo=KOREA)


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

    @tasks.loop(time=time)
    async def on_alarm(self):
        print("on_alarm")

        data = parse_json("./private/alarm.json")

        link = get_adventure_island(self.lostark["apikeyauth"])

        alarm_type = "adventure_island"

        for guild in self.guilds:
            # if guild not in data.keys():
            #     data[guild.id][type] = True

            id = str(guild.id)

            if id not in data.keys():
                continue

            elif data[id][alarm_type]:
                if alarm_type == "adventure_island":
                    for channel in guild.text_channels:
                        if (id == "957221859953352725" and "봇" in channel.name) or "데덴네" in channel.name:
                            await channel.send(file=discord.File(link))
                            await channel.send(f"알림을 끄고 싶다면 '알림 해제'를 입력해 주세요. 서버 단위로 적용됩니다.")

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
                await show_notices(message, self.lostark["apikeyauth"], self.icon)

            elif command == "guild":
                # await show_guilds(message, self.lostark["apikeyauth"], self.icon
                await send_message(message.channel, "현재 준비중인 기능입니당")

            elif command == "alarm":
                await set_alarm(message)

            elif command == "gif":
                await make_gif(message)

    def get_return_words(self, message):
        for item in self.words:
            for word in item["trigger"]:
                if word in message:
                    return item["return"]

        return None
