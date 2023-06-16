import math

import discord

from .DefaultView import DefaultView


class MarketView(DefaultView):
    def __init__(self, data, page_per_item, time):
        super().__init__(data)
        self.max = page_per_item
        self.time = time

        print(len(data))

        self.page = 0
        self.max_page = math.ceil(len(data) / page_per_item)

        self.left = discord.ui.Button()
        self.left.emoji = "◀"
        self.left.style = discord.ButtonStyle.grey
        self.left.callback = self.move_left_page
        self.add_item(self.left)

        self.right = discord.ui.Button()
        self.right.emoji = "▶"
        self.right.style = discord.ButtonStyle.grey
        self.right.callback = self.move_right_page
        self.add_item(self.right)

    async def move_left_page(self, interaction):
        if self.page > 0:
            self.page -= 1

        if self.page not in self.embeds.keys():
            embeds = []
            for i in range(self.max):
                if len(self.data) <= self.page * self.max + i:
                    break

                item = self.data[self.page * self.max + i]

                embed = discord.Embed(
                    title=f"{item['Name']}",
                    color=discord.Color.blue()
                )
                embed.set_thumbnail(url=item["Icon"])
                embed.set_footer(text=f"{self.time} 기준", icon_url=self.icon_url)

                embed.add_field(name="전날 평균 판매가", value=item["YDayAvgPrice"])
                embed.add_field(name="최근 판매가", value=item["RecentPrice"])
                embed.add_field(name="현재 최저가", value=item["CurrentMinPrice"])

                if item["TradeRemainCount"] is not None:
                    embed.add_field(name="구매 시 거래 가능 횟수", value=item["TradeRemainCount"])

                embeds.append(embed)

            self.embeds[self.page] = embeds

        await self.message.edit(content=f"page {self.page + 1}/{self.max_page}", embeds=self.embeds[self.page])
        await interaction.response.defer()

    async def move_right_page(self, interaction):
        if self.page < self.max_page - 1:
            self.page += 1

        if self.page not in self.embeds.keys():
            embeds = []
            for i in range(self.max):
                if len(self.data) <= self.page * self.max + i:
                    break

                item = self.data[self.page * self.max + i]

                embed = discord.Embed(
                    title=f"{item['Name']}",
                    color=discord.Color.blue()
                )
                embed.set_thumbnail(url=item["Icon"])
                embed.set_footer(text=f"{self.time} 기준", icon_url=self.icon_url)

                embed.add_field(name="전날 평균 판매가", value=item["YDayAvgPrice"])
                embed.add_field(name="최근 판매가", value=item["RecentPrice"])
                embed.add_field(name="현재 최저가", value=item["CurrentMinPrice"])
                if item["TradeRemainCount"] is not None:
                    embed.add_field(name="구매 시 거래 가능 횟수", value=item["TradeRemainCount"])

                embeds.append(embed)

            self.embeds[self.page] = embeds

        await self.message.edit(content=f"page {self.page + 1}/{self.max_page}", embeds=self.embeds[self.page])
        await interaction.response.defer()
