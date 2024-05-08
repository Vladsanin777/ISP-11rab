import disnake
from disnake.ext import commands
from disnake import Colour


class Game(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready (self):
        print(f"Бот {self.bot.user} использует ког {__name__}")


    @commands.slash_command(name = "монетка", description = "Игра в Орёл и Решку")
    async def coin(self, ctx, coin: str = commands.Param(name = "сторона", description = "Выбери сторону монеты", choices = ["Орёл", "Решка"]), ui: str = commands.Param(default="Только я", name="видимость", choices=["Только я", "Все участники чата"])):
        print(random(2))




def setup(bot):
    bot.add_cog(Game(bot))
