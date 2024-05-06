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
        bot_count = sum(1 for member in guild.members if member.bot)
        human_count = guild.member_count - bot_count

        # Определение статуса участников
        status_counts = {status: sum(1 for member in guild.members if member.status == status) for status in disnake.Status}
        streaming = sum(1 for member in guild.members if any(activity.type == disnake.ActivityType.streaming for activity in member.activities))
        online = status_counts.get(disnake.Status.online, 0) - streaming
        offline = status_counts.get(disnake.Status.offline, 0)
        idle = status_counts.get(disnake.Status.idle, 0)
        dnd = status_counts.get(disnake.Status.dnd, 0)
        invisible = status_counts.get(disnake.Status.invisible, 0)
        do_not_disturb = status_counts.get(disnake.Status.do_not_disturb, 0)

        # Определение каналов
        category_channels = sum(1 for channel in guild.channels if isinstance(channel, disnake.CategoryChannel))
        text_channels = sum(1 for channel in guild.text_channels if not isinstance(channel, disnake.CategoryChannel))
        voice_channels = sum(1 for channel in guild.voice_channels)
        total_channels = len(guild.channels) - category_channels
        forum_channels = len(guild.forum_channels)
        announcement_channels = sum(1 for channel in guild.text_channels if channel.is_news())
        rules_channel = guild.rules_channel.mention if guild.rules_channel else "Отсутствует"

        # Определение уровня верификации сервера
        verification_level = {"none": "Нет", "low": "Низкий", "medium": "Средний", "high": "Высокий", "highest": "Максимальный"}.get(guild.verification_level.name, "Неизвестный")

        guild_icon = guild.icon
        em = disnake.Embed(title = f"Информация о сервере {guild.name}", colour = Colour.blurple() if guild_icon is None else Colour.from_rgb(*k) if (k := await colour_f(guild_icon.url)) else Colour.blurple()).add_field(name = "ID сервера:", value = f"```{guild.id}```", inline = False).add_field(name = "Участники:", value = f"👥 Всего участников: {guild.member_count}\n🧑 Людей: {human_count}\n🤖 Ботов: {bot_count}\n", inline = True).add_field(name = "Статус участников", value = f"💚 Онлайн: {online}\n🌙 Неактивен: {idle}\n❌ Оффлайн: {offline}\n⛔ Небеспокоить: {dnd}", inline = True).add_field(name = "Какналы", value = f"✏️ Всего каналов: {total_channels}\n📝 Текстовых каналов: {voice_channels}\n🔊 Голосовых каналов: {voice_channels}", inline = True).add_field(name = "Дополнительные статусы:", value = f"🔴 Стримит: {streaming}\n👻 Невидимый: {invisible}\n🤚 Прозба не беспокоить: {do_not_disturb}", inline = True).add_field(name = "Другая информация", value = f"📁 Всего категорий: {category_channels}\n📜 Канал с правилами: {rules_channel}\n", inline = True).add_field(name = "Другая информация", value = f"💬 Канлов-форумов: {forum_channels}\n📢 Каналов с объявлениями: {announcement_channels}").add_field(name = "Создатель сервера:", value = guild.owner.mention, inline = True).add_field(name = "Уровень верификации сервера:", value = verification_level, inline = True).add_field(name = "Сервер создан:", value = format_date(guild.created_at, format='d MMMM yyyy г.', locale='ru_RU'))
        if guild_icon: em.set_thumbnail(url=(guild_icon_url := guild_icon.url))
        else: guild_icon_url = None
        await ctx.send(embed = em, ephemeral=True if ui == "Только я" else False, view = disnake.ui.View() if guild_icon_url is None else disnake.ui.View().add_item(disnake.ui.Button(label="Прямая ссылка на аватар сервера", emoji="👍", url=guild_icon_url)))

def setup(bot):
    bot.add_cog(InfoServer (bot))
