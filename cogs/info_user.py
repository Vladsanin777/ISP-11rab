import disnake
from disnake.ext import commands
from disnake import Colour

from PIL import Image, ImageDraw, ImageFont

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
        if user.avatar is None:
            image_url = user.default_avatar.url
        else:
            image_url = user.avatar.url

        with Image.open(BytesIO(requests.get(image_url).content)) as f:
            mean_color = np.mean(np.array(f), axis=(0,1))
            if isinstance(mean_color, np.ndarray) and len(mean_color) >= 3:
                embed_colour = Colour.from_rgb(*(tuple(map(int, mean_color[:3]))))
            else:
                # Handle case where mean_color is not an array or doesn't have enough values
                embed_colour = Colour.blurple()
        await ctx.send(embed=disnake.Embed(description=f'Аватарка пользователя {user.mention}', colour=embed_colour).set_image(url=image_url), ephemeral=True if ui == "Только я" else False, view=disnake.ui.View().add_item(disnake.ui.Button(label="Прямая ссылка на аватар", emoji="👍", url=image_url)))

    @commands.slash_command(name='банер', description='Отправляет банер участника')
    async def get_user_banner(self, ctx, user: disnake.User = commands.Param(default=None, name="участник"), ui: str = commands.Param(default="Только я", name="видимость", choices=["Только я", "Все участники чата"])):
        if user is None:
            user = ctx.author

        # Get user's avatar
        try:
            banner_url = user.banner.url
        except AttributeError:
            print("В разработке!")

        # Download user's avatar
        avatar_image = Image.open(BytesIO(requests.get(avatar_url).content)).convert("RGBA")

        # Create a blank image for the banner
        banner_image = Image.new("RGBA", (600, 200), (255, 255, 255, 255))

        # Paste the avatar onto the banner
        avatar_image = avatar_image.resize((100, 100))
        banner_image.paste(avatar_image, (20, 50))

        # Draw text onto the banner
        draw = ImageDraw.Draw(banner_image)
        font = ImageFont.truetype("arial.ttf", 24)
        draw.text((150, 80), f"Привет, {user.display_name}!", fill=(0, 0, 0), font=font)
        draw.text((150, 120), text, fill=(0, 0, 0), font=font)

        # Convert the banner image to bytes
        with BytesIO() as image_binary:
            banner_image.save(image_binary, format='PNG')
            image_binary.seek(0)
            file = disnake.File(image_binary, filename="banner.png")

        await ctx.send(file=file)

def setup(bot):
    bot.add_cog(InfoUser (bot))
