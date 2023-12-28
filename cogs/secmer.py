import asyncio
import math
import disnake
from disnake.ext import commands
import os
import time

class Secmer (commands.Cog):
  def __init__(self, bot): 
    self.bot = bot


  @commands.Cog.listener() 
  async def on_ready (self): 
    print(f"Бот {self.bot.user} использует ког {__name__}")



  @commands.slash_command(name = "секундомер")
  #sd кол-во секунд
  async def secmer(self, ctx, ui: str = commands.Param(name = "видимость_секундомера", choices = ["Только для меня", "Для всех"])):
    start = time.time()
    match ui:
      case "Для всех":
        await ctx.send(content = f" {ctx.author.display_name} включил секундомер")
      case "Только для меня":
        await ctx.send(content = f"Вы запустили сеундомер", ephemeral = True)
    while True:
      #message = ((await ctx.channel.history(limit = 1).flatten())[0]).id
      try:
        await message.edit(content=f"Прошло {math.floor(time.time() - start)} секунд")
      except IndexError:
        await ctx.send(content=f"Прошло {math.floor(time.time() - start)} секунд")
        message1 = await ctx.channel.history(limit=1).flatten()
        message = self.bot.get_channel( ctx.channel.id).fetch_message(message1[0])


      await asyncio.sleep(1)







def setup(bot):
  bot.add_cog(Secmer (bot))