import discord


class DefaultSelection(discord.ui.Select):
    def __init__(self, options, default, placeholder):
        self.selection = default

        super().__init__(options=options, placeholder=placeholder)

    async def callback(self, interaction):
        await interaction.response.defer()
