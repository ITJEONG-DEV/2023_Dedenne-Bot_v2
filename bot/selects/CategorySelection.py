import discord

from .DefaultSelection import DefaultSelection


class CategorySelection(DefaultSelection):
    def __init__(self):
        self.codes = [
            {"code": 20000, "name": "아바타"},
            {"code": 20005, "name": "무기 아바타"},
            {"code": 20010, "name": "머리 아바타"},
            {"code": 20020, "name": "얼굴1 아바타"},
            {"code": 20030, "name": "얼굴2 아바타"},
            {"code": 20050, "name": "상의 아바타"},
            {"code": 20060, "name": "하의 아바타"},
            {"code": 20070, "name": "상하의 세트 아바타"},
            {"code": 21400, "name": "악기 아바타"},
            {"code": 21500, "name": "아바타 상자"},
            {"code": 21600, "name": "이동 효과"},
            {"code": 40000, "name": "각인서"},
            {"code": 50000, "name": "강화 재료"},
            {"code": 50010, "name": "재련 재료"},
            {"code": 50020, "name": "재련 추가 재료"},
            {"code": 51000, "name": "기타 재료"},
            {"code": 51100, "name": "무기 진화 재료"},
            {"code": 60000, "name": "배틀 아이템"},
            {"code": 70000, "name": "요리"},
            {"code": 90000, "name": "생활"},
            {"code": 100000, "name": "모험의 서"},
            {"code": 110000, "name": "항해"},
            {"code": 140000, "name": "펫"},
            {"code": 160000, "name": "탈 것"},
        ]
        options = self.make_options()
        self.default = 0
        placeholder = "(필수)카테고리"

        super().__init__(options=options, default=self.default, placeholder=placeholder)

    def make_options(self):
        options = []
        for item in self.codes:
            options.append(
                discord.SelectOption(label=item["name"], description=item["code"])
            )
        return options

    def get_code(self, selected_item):
        for item in self.codes:
            if item["name"] == selected_item:
                return item["code"]

        return None

    async def callback(self, interaction):
        self.selection = self.get_code(self.values[0])
        await interaction.response.defer()
