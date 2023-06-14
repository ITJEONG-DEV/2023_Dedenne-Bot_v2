import os
import datetime
import discord

import imageio as imageio

from .send import send_message


async def make_gif(message):
    if len(message.attachments) > 0:
        # parsed option
        option = message.content.split()

        duration = 500

        if len(option) > 1:
            for i in range(1, len(option)):
                word = option[i]

                if "duration" in word:
                    duration = float(word.split("=")[1]) * 1000

        dir_name = f'{message.author.id}_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}'

        os.makedirs(f'result/{dir_name}', exist_ok=True)

        images = []
        for attachment in message.attachments:
            filename = f'result/{dir_name}/' + attachment.filename
            await attachment.save(filename)

            images.append(imageio.imread(filename))

        imageio.mimsave(f'result/{dir_name}/result.gif', images, duration=duration, loop=0)

        await send_message(message.channel, file=discord.File(f'result/{dir_name}/result.gif'))
