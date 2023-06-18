import datetime
import discord

from .DefaultView import DefaultView
from .MarketView import MarketView
from ..selects import *
from ..functions import send_message

from lostark.api import get_item


class MarketSearchView(DefaultView):
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

        self.search_button = discord.ui.Button()
        self.search_button.label = "검색"
        self.search_button.style = discord.ButtonStyle.grey
        self.search_button.callback = self.on_click_search_button

        self.add_item(self.category)
        self.add_item(self.grade)
        self.add_item(self.tier)
        self.add_item(self.character_class)
        self.add_item(self.search_button)

    async def on_click_search_button(self, interaction):
        if self.category.selection == self.category.default:
            await self.message.edit(content="```css\n[카테고리 지정은 필수입니다.]\n```")
            await interaction.response.defer()

        else:
            category = self.category.selection
            grade = self.grade.selection
            tier = self.tier.selection
            character_class = self.character_class.selection
            keyword = self.keyword

            result = get_item(category, character_class, tier, grade, keyword, self.auth)["Items"]

            self.clear_items()

            if result is None or len(result) == 0:
                embed = discord.Embed(
                    title="검색 결과 없음",
                    color=discord.Color.blue()
                )
                await self.message.edit(content="", embed=embed, view=None)

            else:
                market_view = MarketView(result, self.max_count, datetime.datetime.now())
                market_view.set_message(self.message)

                embeds = []

                for i in range(self.max_count if self.max_count < len(result) else len(result)):
                    item = result[i]

                    embed = discord.Embed(
                        title=f"{item['Name']}",
                        color=discord.Color.blue()
                    )
                    embed.set_thumbnail(url=item["Icon"])
                    embed.set_footer(text=f"{market_view.time} 기준", icon_url=self.icon_url)

                    embed.add_field(name="전날 평균 판매가", value=item["YDayAvgPrice"])
                    embed.add_field(name="최근 판매가", value=item["RecentPrice"])
                    embed.add_field(name="현재 최저가", value=item["CurrentMinPrice"])

                    if item["TradeRemainCount"] is not None:
                        embed.add_field(name="구매 시 거래 가능 횟수", value=item["TradeRemainCount"])

                    embeds.append(embed)

                market_view.embeds[0] = embeds

                await self.message.edit(content=f"page {market_view.page + 1}/{market_view.max_page}", embeds=embeds,
                                        view=market_view)

            await interaction.response.defer()
