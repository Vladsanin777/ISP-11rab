import disnake
from disnake.ext import commands
from disnake import Colour

from PIL import Image
import requests
import numpy as np
from io import BytesIO


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
        try:
            image_url = user.avatar.url
        except AttributeError:
            image_url = user.default_avatar.url
        with Image.open(BytesIO(requests.get(image_url).content)) as f:
            mean_color = np.mean(np.array(f), axis=(0,1))
            if isinstance(mean_color, np.ndarray) and len(mean_color) >= 3:
                embed_colour = Colour.from_rgb(*(tuple(map(int, mean_color[:3]))))
            else:
                # Handle case where mean_color is not an array or doesn't have enough values
                embed_colour = Colour.blurple()
        await ctx.send(embed=disnake.Embed(description=f'Аватарка пользователя {user.mention}', colour=embed_colour).set_image(url=image_url), ephemeral=True if ui == "Только я" else False, view=disnake.ui.View().add_item(disnake.ui.Button(label="Прямая ссылка на аватар", emoji="👍", url=image_url)))



def setup(bot):
    bot.add_cog(InfoUser (bot))
