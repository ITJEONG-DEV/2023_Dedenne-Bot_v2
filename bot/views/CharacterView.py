import discord

from .DefaultView import DefaultView
from lostark.crawling.data import *


class CharacterView(DefaultView):
    def __init__(self, data: Profile):
        super().__init__(data)

    @discord.ui.button(label="기본 정보", style=discord.ButtonStyle.grey, emoji="ℹ")
    async def on_click_default_info(self, interaction: discord.Interaction, button: discord.ui.Button):
        if "기본 정보" not in self.embeds.keys():
            embed = discord.Embed(
                title=self.data.name + "@" + self.data.server + " " + self.data.lv,
                url="https://lostark.game.onstove.com/Profile/Character/" + self.data.name,
                color=discord.Color.blue()
            )

            embed.set_image(url=self.data.profile_ingame.profile_equipment.src)
            embed.set_footer(text=self.data.name + "\t\t\t" + self.data.time + " 기준", icon_url=self.data.emblem)

            embed.add_field(name="원정대 레벨", value=f"`{self.data.profile_ingame.profile_info.expedition_lv}`")
            embed.add_field(name="아이템 레벨", value=f"`{self.data.profile_ingame.profile_info.equip_item_lv}`")
            embed.add_field(name="영지",
                            value=f"`{self.data.profile_ingame.profile_info.estate_name} {self.data.profile_ingame.profile_info.estate_lv}`")

            m = "```diff\n"
            for slot in self.data.profile_ingame.profile_equipment.ability_engrave_slot.ability:
                if "감소" in str(slot):
                    m += "-" + str(slot) + "\n"
                else:
                    m += "+" + str(slot) + "\n"
            if m == "```diff\n":
                m = "-"
            else:
                m += "```"
            embed.add_field(name="각인 효과", value=m)

            m = f"공격력 `{self.data.state.attack}\n`최대 생명력 `{self.data.state.hp}`\n"
            embed.add_field(name="기본 특성", value=m)

            self.embeds["기본 정보"] = embed

            elixir = self.data.profile_ingame.profile_equipment.elixir
            if elixir is not None:
                m = f"`{elixir.name}`"
                embed.add_field(name="엘릭서", value=m)

        await self.message.edit(embed=self.embeds["기본 정보"])
        await interaction.response.defer()

    @discord.ui.button(label="장비/ 카드 세트 정보", style=discord.ButtonStyle.grey, emoji="📄")
    async def on_click_set_effect(self, interaction: discord.Interaction, button: discord.ui.Button):
        if "세트 정보" not in self.embeds.keys():
            embed = discord.Embed(
                title=self.data.name + "@" + self.data.server + " " + self.data.lv,
                url="https://lostark.game.onstove.com/Profile/Character/" + self.data.name,
                color=discord.Color.blue()
            )

            embed.set_footer(text=self.data.name + "\t\t\t\t\t\t" + self.data.time + " 기준", icon_url=self.data.emblem)
            embed.set_thumbnail(url=self.data.profile_ingame.profile_equipment.src)

            m = "```"
            for effect in self.data.profile_ingame.profile_equipment.card_slot.effect:
                m += f"{effect.title}\n"
            if m == "```":
                m = "-"
            else:
                m += "```"
            embed.add_field(name="카드 세트 효과", value=m)

            m = "```"
            effect_list = list(self.data.profile_ingame.profile_equipment.equipment_effect_slot)
            effect_list.sort()
            for effect in effect_list:
                m += " ".join(effect.split("\t")[:-1]) + "\n"
            if m == "```":
                m = "-"
            else:
                m += "```"
            embed.add_field(name="장비 세트 효과", value=m)

            self.embeds["세트 정보"] = embed

        await self.message.edit(embed=self.embeds["세트 정보"])
        await interaction.response.defer()

    @discord.ui.button(label="특성 정보", style=discord.ButtonStyle.grey, emoji="📊")
    async def on_click_ability_info(self, interaction: discord.Interaction, button: discord.ui.Button):
        if "특성 정보" not in self.embeds.keys():
            embed = discord.Embed(
                title=self.data.name + "@" + self.data.server + " " + self.data.lv,
                url="https://lostark.game.onstove.com/Profile/Character/" + self.data.name,
                color=discord.Color.blue()
            )

            embed.set_thumbnail(url=self.data.profile_ingame.profile_equipment.src)
            embed.set_footer(text=self.data.name + "\t\t" + self.data.time + " 기준", icon_url=self.data.emblem)

            m = f"\n치명 `{self.data.state.fatal}`\n특화 `{self.data.state.specialization}`\n제압 `{self.data.state.overpowering}`\n신속 `{self.data.state.swiftness}`\n인내 `{self.data.state.patience}`\n숙련 `{self.data.state.skilled}`"
            embed.add_field(name="전투 특성", value=m)

            state = self.data.profile_state
            m = f"\n지성 `{state.intellect}`\n담력 `{state.courage}`\n매력 `{state.charm}`\n친절 `{state.kindness}`"
            embed.add_field(name="성향", value=m)

            self.embeds["특성 정보"] = embed

        await self.message.edit(embed=self.embeds["특성 정보"])
        await interaction.response.defer()

    @discord.ui.button(label="보석 정보", style=discord.ButtonStyle.grey, emoji="💎")
    async def on_click_jewel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if "보석 정보" not in self.embeds.keys():

            embed = discord.Embed(
                title=self.data.name + "@" + self.data.server + " " + self.data.lv,
                url="https://lostark.game.onstove.com/Profile/Character/" + self.data.name,
                color=discord.Color.blue()
            )

            embed.set_thumbnail(url=self.data.profile_ingame.profile_equipment.src)
            embed.set_footer(text=self.data.name + "\t\t\t\t\t\t\t\t\t\t" + self.data.time + " 기준",
                             icon_url=self.data.emblem)

            m = "```ini\n"
            for jewel in self.data.profile_ingame.profile_equipment.jewel_slot:
                effect = jewel.effect.replace("재사용 대기시간 ", "[쿨타임 -")
                effect = effect.replace(" 감소", "")
                effect = effect.replace("피해 ", "[피해 +")
                effect = effect.replace(" 증가", "")
                effect = effect.replace(".00", "")
                m += f"[{' '.join(jewel.name.split(' ')[:-1])[:-1]}] {jewel.skill_name} {effect}]\n"
            if m == "```md\n":
                m = "-"
            else:
                m += "```"
            embed.add_field(name="보석 정보", value=m)

            self.embeds["보석 정보"] = embed

        await self.message.edit(embed=self.embeds["보석 정보"])
        await interaction.response.defer()

    @discord.ui.button(label="보유 캐릭터", style=discord.ButtonStyle.grey, emoji="👥")
    async def on_click_character_list(self, interaction: discord.Interaction, button: discord.ui.Button):
        if "보유 캐릭터" not in self.embeds.keys():

            embed = discord.Embed(
                title=self.data.name + "@" + self.data.server + " " + self.data.lv,
                url="https://lostark.game.onstove.com/Profile/Character/" + self.data.name,
                color=discord.Color.blue()
            )

            embed.set_footer(text=self.data.name + "\t\t" + self.data.time + " 기준", icon_url=self.data.emblem)
            embed.set_thumbnail(url=self.data.profile_ingame.profile_equipment.src)

            character_list = self.data.profile_character_list.character_list
            msg = "\n"
            for server in character_list:
                msg += "**" + server.server + "**\n```"
                for character in server.characters:
                    msg += character.name + " " + character.item_lv + " " + character.job + "\n"
                msg += "```\n"

            embed.add_field(name="보유 캐릭터 목록", value=msg)

            self.embeds["보유 캐릭터"] = embed

        await self.message.edit(embed=self.embeds["보유 캐릭터"])
        await interaction.response.defer()

    @discord.ui.button(label="내실", style=discord.ButtonStyle.grey, emoji="🌱")
    async def on_click_stability(self, interaction: discord.Interaction, button: discord.ui.Button):
        if "내실" not in self.embeds.keys():
            embed = discord.Embed(
                title=self.data.name + "@" + self.data.server + " " + self.data.lv,
                url="https://lostark.game.onstove.com/Profile/Character/" + self.data.name,
                color=discord.Color.blue()
            )

            embed.set_thumbnail(url=self.data.profile_ingame.profile_equipment.src)
            embed.set_footer(text=self.data.name + "\t\t\t\t\t" + self.data.time + " 기준", icon_url=self.data.emblem)

            stability = self.data.profile_stability

            life_skill = stability.profile_skill_life
            embed.add_field(name="생활 스킬", value="\n".join(life_skill.skill))

            collection = stability.profile_collection
            embed.add_field(name="수집형 포인트", value=str(collection))

            self.embeds["내실"] = embed

        await self.message.edit(embed=self.embeds["내실"])
        await interaction.response.defer()
