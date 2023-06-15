import discord
from .DefaultSelection import DefaultSelection


class TierSelection(DefaultSelection):
    def __init__(self):
        self.codes = [
            1, 2, 3
        ]
        options = self.make_options()
        self.default = None
        placeholder = "(선택)아이템 티어"

        super().__init__(options, self.default, placeholder)

    def make_options(self):
        options = []

        for item in self.codes:
            options.append(
                discord.SelectOption(label=str(item), description=str(item))
            )
        return options

    async def callback(self, interaction):
        self.selection = int(self.values[0])
        await interaction.response.defer()
