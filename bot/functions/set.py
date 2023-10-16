import json

from util import parse_json, overwrite_json
from . import send_message


async def set_alarm(message):
    keyword = message.content.split()[1]

    data = parse_json("./private/alarm.json")

    guild = str(message.guild.id)

    if keyword == "설정":
        if guild not in data.keys():
            data[guild] = dict()

        if "adventure_island" not in data[guild].keys():
            data[guild]["adventure_island"] = True
        elif not data[guild]["adventure_island"]:
            data[guild]["adventure_island"] = True
        else:
            return await send_message(message.channel, f"알림이 이미 {keyword}되어 있습니다.")

    elif keyword == "해제":
        if guild not in data.keys():
            data[guild] = dict()

        if "adventure_island" not in data[guild].keys():
            data[guild]["adventure_island"] = False
        elif data[guild]["adventure_island"]:
            data[guild]["adventure_island"] = False
        else:
            return await send_message(message.channel, f"알림이 이미 {keyword}되어 있습니다.")

    else:
        return await send_message(message.channel, f"올바른 명령이 아닙니다.")

    overwrite_json("./private/alarm.json", data)

    await send_message(message.channel, f"알림이 {keyword} 되었습니다.")
