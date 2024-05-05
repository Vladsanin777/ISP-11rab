import disnake
from disnake.ext import commands
from disnake import Colour

from PIL import Image, ImageDraw, ImageFont

import requests
import numpy as np
from io import BytesIO

import datetime
import pytz
from babel.dates import format_date

from element.colour import colour_f


class InfoServer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready (self):
        print(f"Бот {self.bot.user} использует ког {__name__}")



    @commands.slash_command(name = "сервер", description = "Выдаёт информацию о сервере!")
    async def get_server_info(self, ctx, ui: str = commands.Param(default="Только я", name="видимость", choices=["Только я", "Все участники чата"])):
        guild = ctx.guild

        # Определение участников
        bot_count = human_count = online = offline = idle = dnd = streaming = invisible = do_not_disturb = 0
        for member in guild.members:
            match member.status:
                case disnake.Status.online: online += 1
                case disnake.Status.idle: idle += 1
                case disnake.Status.dnd: dnd += 1
                case disnake.Status.invisible: invisible += 1
                case disnake.Status.do_not_disturb: do_not_disturb += 1
                case disnake.Status.offline: offline += 1
            if any(activity.type == disnake.ActivityType.streaming for activity in member.activities): streaming += 1
            if member.bot: bot_count += 1
            else: human_count += 1
        online -= streaming
        # Определение каналов
        category_channels = sum(1 for channel in guild.channels if isinstance(channel, disnake.CategoryChannel))
        total_channels = len(guild.channels) - category_channels
        voice_channels = len(guild.voice_channels)
        text_channels = len(guild.text_channels)
        rules_channel = guild.rules_channel.mention if guild.rules_channel else "Отсутствует"
        forum_channels = len(guild.forum_channels)
        announcement_channels = sum(1 for channel in guild.text_channels if channel.is_news())

        # Определение уровня верификации сервера
        verification_levels = {disnake.VerificationLevel.none.value: "Нет", disnake.VerificationLevel.low.value: "Низкий", disnake.VerificationLevel.medium.value: "Средний", disnake.VerificationLevel.high.value: "Высокий", disnake.VerificationLevel.highest.value: "Максимальный"}
        level = verification_levels.get(guild.verification_level.value, "Неизвестный")

        em = disnake.Embed(title = f"Информация о сервере {guild.name}", colour = Colour.blurple() if guild.icon is None else Colour.from_rgb(*k) if (k := tuple(await colour_f(guild.icon.url))) else Colour.blurple()).add_field(name = "ID сервера:", value = f"```{guild.id}```", inline = False).add_field(name = "Участники:", value = f"👥 Всего участников: {guild.member_count}\n🧑 Людей: {human_count}\n🤖 Ботов: {bot_count}\n", inline = True).add_field(name = "Статус участников", value = f"💚 Онлайн: {online}\n🌙 Неактивен: {idle}\n❌ Оффлайн: {offline}\n⛔ Небеспокоить: {dnd}", inline = True).add_field(name = "Какналы", value = f"✏️ Всего каналов: {total_channels}\n📝 Текстовых каналов: {voice_channels}\n🔊 Голосовых каналов: {voice_channels}", inline = True).add_field(name = "Дополнительные статусы:", value = f"🔴 Стримит: {streaming}\n👻 Невидимый: {invisible}\n🤚 Прозба не беспокоить: {do_not_disturb}", inline = True).add_field(name = "Другая информация", value = f"📁 Всего категорий: {category_channels}\n📜 Канал с правилами: {rules_channel}\n", inline = True).add_field(name = "Другая информация", value = f"💬 Канлов-форумов: {forum_channels}\n📢 Каналов с объявлениями: {announcement_channels}").add_field(name = "Создатель сервера:", value = guild.owner.mention, inline = True).add_field(name = "Уровень верификации сервера:", value = level, inline = True).add_field(name = "Сервер создан:", value = format_date(guild.created_at, format='d MMMM yyyy г.', locale='ru_RU'))
        if (guild_icon := guild.icon) is not None: em.set_thumbnail(url=guild_icon.url)
        await ctx.send(embed = em, ephemeral=True if ui == "Только я" else False)




def setup(bot):
    bot.add_cog(InfoServer (bot))
