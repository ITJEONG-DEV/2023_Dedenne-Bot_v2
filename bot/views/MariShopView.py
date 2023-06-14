import discord

from .View import DefaultView
from lostark.crawling.data import *


class MariShopView(DefaultView):
    def __init__(self, data: MariShop):
        super().__init__(data)

    @discord.ui.button(label="성장 추천", style=discord.ButtonStyle.grey, emoji="🔝")
    async def on_click_tab1(self, interaction: discord.Interaction, button: discord.ui.Button):
        if "성장 추천" not in self.embeds.keys():
            embed = discord.Embed(
                title=self.data.title,
                url=self.data.url,
                color=discord.Color.blue()
            )

            # embed.set_footer(text=self.data.name, icon_url=self.data.emblem)
            embed.set_footer(text=self.data.time + " 기준", icon_url=self.icon_url)

            m = ""
            for i in range(len(self.data.tab1)):
                item = self.data.tab1[i]
                m += f"```diff\n+{item[0]}\n-크리스탈 {item[1]}\n```"
            if m == "":
                m = "현재 판매 상품이 없습니다"
            embed.add_field(name="현재 판매 상품", value=m)

            pre_num = int(len(self.data.tab1_pre) / 6)

            for i in range(pre_num):
                m = ""
                for j in range(6):
                    item = self.data.tab1_pre[i * 6 + j]
                    m += f"```diff\n+{item[0]}\n-크리스탈 {item[1]}\n```"
                if m == "":
                    m = "이전 판매 상품이 없습니다"
                embed.add_field(name=self.data.tab1_pre_name[i], value=m)

            self.embeds["성장 추천"] = embed

        await self.message.edit(embed=self.embeds["성장 추천"])
        await interaction.response.defer()

    @discord.ui.button(label="전투ㆍ생활 추천", style=discord.ButtonStyle.grey, emoji="⚔")
    async def on_click_tab2(self, interaction: discord.Interaction, button: discord.ui.Button):
        if "전투 생활 추천" not in self.embeds.keys():
            embed = discord.Embed(
                title=self.data.title,
                url=self.data.url,
                color=discord.Color.blue()
            )

            embed.set_footer(text=self.data.time + " 기준", icon_url=self.icon_url)

            m = ""
            for i in range(len(self.data.tab2)):
                item = self.data.tab2[i]
                m += f"```diff\n+{item[0]}\n-크리스탈 {item[1]}\n```"
            if m == "":
                m = "현재 판매 상품이 없습니다"
            embed.add_field(name="현재 판매 상품", value=m)

            pre_num = int(len(self.data.tab2_pre) / 6)

            for i in range(pre_num):
                m = ""
                for j in range(6):
                    item = self.data.tab2_pre[i * 6 + j]
                    m += f"```diff\n+{item[0]}\n-크리스탈 {item[1]}\n```"
                if m == "":
                    m = "이전 판매 상품이 없습니다"
                embed.add_field(name=self.data.tab2_pre_name[i], value=m)

            self.embeds["전투 생활 추천"] = embed

        await self.message.edit(embed=self.embeds["전투 생활 추천"])
        await interaction.response.defer()
