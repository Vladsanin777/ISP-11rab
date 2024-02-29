import disnake
from disnake.ext import commands 
import asyncio
import numexpr
import os

import disnake
from disnake.ext import commands


class PingCommand(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot



  
  @commands.Cog.listener() 
  async def on_ready (self): 
    print(f"Бот {self.bot.user} использует ког {__name__}")


  @commands.slash_command()
  async def ping(self, inter):
    """Получить текущую задержку бота."""
    await inter.response.send_message(f"Понг! {round(self.bot.latency * 1000)}мс")
  
  @commands.slash_command(
    name = "калькулятор",
    description = "Считает выражения"
  )
  async def calc (
    self,
    ctx, 
    gh:
    str = commands.Param(
      name = "выражение",
      description = "Считает выражения любой сложности"
    )
  ):
    await ctx.response.send_message(f"{gh} = {numexpr.evaluate(gh)}")

def setup(bot: commands.Bot):
  bot.add_cog(PingCommand(bot))