import disnake
from disnake.ext import commands
from disnake import Colour
import random


class Game(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready (self):
        print(f"Бот {self.bot.user} использует ког {__name__}")


    @commands.slash_command(name = "монетка", description = "Игра в Орёл и Решку")
    async def coin(self, ctx, coin: str = commands.Param(name = "сторона", description = "Выбери сторону монеты", choices = ["Орёл", "Решка"]), ui: str = commands.Param(default="Только я", name="видимость", choices=["Только я", "Все участники чата"])):
        if (rand := bool(random.randint(0,1))) and coin == "Орёл" or (not rand) and coin == "Решка":
            result = "**Ты угодал!!!**"
            colour = 0x33FF18
            computer = coin
        else:
            result = "**Ты не угодал!!!**"
            colour = 0xFF1B18
            computer = ["Орёл", "Решка"][int(not bool(["Орёл", "Решка"].index(coin)))]
        await ctx.send(embed = disnake.Embed(description = result, colour = colour).add_field(name = "Ты загодал:", value = coin, inline = False).add_field(name = "Компьютер загодал:", value = computer), ephemeral=True if ui == "Только я" else False)


def setup(bot):
    bot.add_cog(Game(bot))
