import discord
from .DefaultSelection import DefaultSelection

class GradeSelection(DefaultSelection):
    def __init__(self):
        self.codes = [
            "일반", "고급", "희귀", "영웅", "전설", "유물", "고대", "에스더"
        ]
        options = self.make_options()
        self.default = ""
        placeholder = "(선택)등급"

        super().__init__(options, self.default, placeholder)

    def make_options(self):
        options = []

        for item in self.codes:
            options.append(
                discord.SelectOption(label=item, description=item)
            )
        return options

    async def callback(self, interaction):
        self.selection = self.values[0]
        await interaction.response.defer()