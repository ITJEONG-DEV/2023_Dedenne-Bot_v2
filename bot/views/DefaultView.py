import discord


class DefaultView(discord.ui.View):
    def __init__(self, data):
        super().__init__(timeout=None)

        self.message = None
        self.data = data
        self.icon_url = "https://cdn-lostark.game.onstove.com/2018/obt/assets/images/common/icon/favicon-192.png"
        self.embeds = {}

    def set_message(self, message):
        self.message = message
