import disnake
from disnake.ext import commands
from disnake import Colour

from PIL import Image, ImageDraw, ImageFont

import requests
import numpy as np
from io import BytesIO


from element.colour import colour_f


class InfoUser(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready (self):
        print(f"Бот {self.bot.user} использует ког {__name__}")


    @commands.slash_command(name='аватар', description='Отправляет аватар участника')
    async def get_user_avatar(self, ctx, user: disnake.User = commands.Param(default=None, name="участник"), ui: str = commands.Param(default="Только я", name="видимость", choices=["Только я", "Все участники чата"])):
        if user is None:
            user = ctx.author
        if (user_avatar := user.avatar) is not None: user_avater_url = user_avatar.url
        else: user_avater_url = user.default_avatar.url
        await ctx.send(embed=disnake.Embed(description=f'Аватарка пользователя {user.mention}', colour = Colour.from_rgb(*await colour_f(user_avater_url))).set_image(url=user_avater_url), ephemeral=True if ui == "Только я" else False, view=disnake.ui.View().add_item(disnake.ui.Button(label="Прямая ссылка на аватар", emoji="👍", url=user_avater_url)))


def setup(bot):
    bot.add_cog(InfoUser (bot))
