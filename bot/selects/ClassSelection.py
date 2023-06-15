import discord
from .DefaultSelection import DefaultSelection


class ClassSelection(DefaultSelection):
    def __init__(self):
        self.codes = [
            "버서커",
            "디스트로이어",
            "워로드",
            "홀리나이트",
            "슬레이어",
            "아르카나",
            "서머너",
            "바드",
            "소서리스",
            "배틀마스터",
            "인파이터",
            "기공사",
            "창술사",
            "스트라이커",
            "블레이드",
            "데모닉",
            "리퍼",
            "호크아이",
            "데빌헌터",
            "블래스터",
            "스카우터",
            "건슬링어",
            "도화가",
            "기상술사"
        ]

        options = self.make_options()
        self.default = ""
        placeholder = "(선택)클래스"

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
