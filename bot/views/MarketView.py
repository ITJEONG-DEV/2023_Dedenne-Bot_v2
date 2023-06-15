import datetime
import discord

from .View import DefaultView
from ..selects import *
from ..functions import send_message

from lostark.api import get_item


class SearchButton(discord.ui.Button):
    def __init__(self, view):
        super().__init__()

        self.label = "검색"
        self.style = discord.ButtonStyle.grey

        self.__view = view

    async def callback(self, interaction):
        if self.__view.category.selection == self.__view.category.default:
            return await interaction.response.defer()

        category = self.__view.category.selection
        grade = self.__view.grade.selection
        tier = self.__view.tier.selection
        character_class = self.__view.character_class.selection
        keyword = self.__view.keyword

        print(category, grade, tier, character_class, keyword)

        result = get_item(category, character_class, tier, grade, keyword, self.__view.auth)["Items"]

        if result is None:
            embed = discord.Embed(
                title="검색 결과",
                color=discord.Color.blue()
            )
            await self.__view.message.edit(embed=embed)

        else:
            embeds = []

            now = datetime.datetime.now()
            for i in range(self.__view.max_count if self.__view.max_count < len(result) else len(result)):
                item = result[i]

                embed = discord.Embed(
                    title=f"{item['Name']}",
                    color=discord.Color.blue()
                )
                embed.set_thumbnail(url=item["Icon"])
                embed.set_footer(text=f"{now} 기준", icon_url=self.__view.icon_url)

                embed.add_field(name="전날 평균 판매가", value=item["YDayAvgPrice"])
                embed.add_field(name="최근 판매가", value=item["RecentPrice"])
                embed.add_field(name="현재 최저가", value=item["CurrentMinPrice"])
                embed.add_field(name="구매 시 거래 가능 횟수", value=item["TradeRemainCount"])

                embeds.append(embed)

                self.__view.clear_items()

            await self.__view.message.edit(content='검색 결과', embeds=embeds, view=None)

        await interaction.response.defer()


class MarketView(DefaultView):
    def __init__(self, data):
        super().__init__(data)

        self.keyword = ""
        self.auth = ""
        self.icon_url = ""

        self.max_count = 4

        self.category = CategorySelection()
        self.grade = GradeSelection()
        self.tier = TierSelection()
        self.character_class = ClassSelection()
        self.button = SearchButton(self)

        self.add_item(self.category)
        self.add_item(self.grade)
        self.add_item(self.tier)
        self.add_item(self.character_class)
        self.add_item(self.button)
