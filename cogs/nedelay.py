import disnake
from disnake.ext import commands

import asyncio

import datetime

import element.chetnost_nedeli


class Nedelay (commands.Cog):
  def __init__(self, bot): 
    self.bot = bot



  @commands.Cog.listener() 
  async def on_ready (self): 
    print(f"Бот {self.bot.user} использует ког {__name__}")






  async def nedelay_commands(self):
    result = (await asyncio.gather( element.chetnost_nedeli.ChetnostNedeli().is_even_week()))[0]

    for id_channel in [1181006630721179691, 1180156712150376488]:
      channel = self.bot.get_channel(id_channel)
      last_message = await channel.history(limit=1).flatten()
      print(last_message)
      print(await last_message.created_at())
      if datetime.datetime.now() - last_message.created_at() < datetime.timedelta(hours=1) or last_message.author.id != 1151110889492185118:
        match id_channel:
          case 1181006630721179691:
            if result[0] and not(result[1]): picture = disnake.File(fp="raspisanie/raspisanie_on_nedelay/Расписание числитель.png", spoiler=False, description="Эта неделя числитель!")
            elif result[0] and result[1]: picture = disnake.File(fp="raspisanie/raspisanie_on_nedelay/Расписание знаменатель.png", spoiler=False, description="Следующая неделя знаменатель!")
            elif not(result[0]) and result[1]: picture = disnake.File(fp="raspisanie/raspisanie_on_nedelay/Расписание числитель.png", spoiler=False, description="Следующая неделя числитель!")
            elif not(result[0]) and not(result[1]): picture = disnake.File(fp="raspisanie/raspisanie_on_nedelay/Расписание знаменатель.png", spoiler=False, description="Эта неделя знаменатель!")
            else: picture = None
          case 1180156712150376488:
            if result[0] and not(result[1]): picture = disnake.File(fp="raspisanie/chetnost_nedelay/Числитель.png", spoiler=False, description="Эта неделя числитель!")
            elif result[0] and result[1]: picture = disnake.File(fp="raspisanie/chetnost_nedelay/Знаменатель.png", spoiler=False, description="Следующая неделя знаменатель!")
            elif not(result[0]) and result[1]: picture = disnake.File(fp="raspisanie/chetnost_nedelay/Числитель.png", spoiler=False, description="Следующая неделя числитель!")
            elif not(result[0]) and not(result[1]): picture = disnake.File(fp="raspisanie/chetnost_nedelay/Знаменатель.png", spoiler=False, description="Эта неделя знаменатель!")
            else: picture = None

        channel = self.bot.get_channel(id_channel)
        messages = await channel.history().flatten()
        await channel.delete_messages(messages)
        await channel.send(content="", file=picture)

  async def nedelay_loop(self):
    while True:
      await self.nedelay_commands()
      await asyncio.sleep(3600)

  @commands.slash_command(
    name="обновление_чётности_недели",
    description="Обновляет данные о чётности недели"
  )
  async def nedelay_loop_command(self, ctx):
    if ctx.guild.id == 1147074522328084545:
      await self.nedelay_commands()
      await ctx.send(content="Чётность недели обновлена!", ephemeral=True)
    else: await ctx.send(content = "Данная команда даступна только на сервере ИСП-11!")





def setup(bot):
  bot.add_cog(Nedelay (bot))