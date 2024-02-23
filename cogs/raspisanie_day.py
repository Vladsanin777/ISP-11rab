import disnake
from disnake.ext import commands

import datetime

import asyncio

import element.chetnost_nedeli

class Raspisanie (commands.Cog):
  def __init__(self, bot): 
    self.bot = bot



  @commands.Cog.listener() 
  async def on_ready (self): 
    print(f"Бот {self.bot.user} использует ког {__name__}")


"""
  async def raspisanie_commands(self):
    last_message = self.bot.get_channel(1180576414479695903).fetch_message(1)
    print(last_message)
    if datetime.datetime.now() - last_message.created_at < timedelta(hours=1) or last_message.author.id != 1151110889492185118:
      today = datetime.datetime.now() + datetime.timedelta(hours = 4)
      day_of_week = today.weekday()
      if today.hour > 15:
        if day_of_week == 6:
          day_of_week = 0
        else:
          day_of_week += 1
      match day_of_week:
        case 0 | 6: picture = disnake.File(fp = "raspisanie/raspis_days/Понедельник.png", spoiler = False, description = "На понедельник")
        case 1: 
          print(f"{((await element.chetnost_nedeli.ChetnostNedeli().is_even_week())[0])}")
          if ((await element.chetnost_nedeli.ChetnostNedeli().is_even_week())[0]): picture = disnake.File(fp = "raspisanie/raspis_days/Вторник числитель.png", spoiler = False, description = "На вторник Числитель")
          else: picture = disnake.File(fp = "raspisanie/raspis_days/Вторник знаменатель.png", spoiler = False, description = "На вторник Знаменатель")
        case 2: picture = disnake.File(fp = "raspisanie/raspis_days/Среда.png", spoiler = False, description = "На среду")
        case 3: picture = disnake.File(fp = "raspisanie/raspis_days/Четверг.png", spoiler = False, description = "На четверг")
        case 4: picture = disnake.File(fp = "raspisanie/raspis_days/Пятница.png", spoiler = False, description = "На пятницу")
        case 5: picture = disnake.File(fp = "raspisanie/raspis_days/Суббота.png", spoiler = False, description = "На субботу")
        case _: picture = None
      channel = self.bot.get_channel(1180576414479695903)
      messages = await channel.history().flatten()
      await channel.delete_messages(messages)
      await channel.send(content="", file=picture)


  async def raspisanie_loop(self):
    while True:
      await self.raspisanie_commands()
      await asyncio.sleep(3600)


  @commands.slash_command(
    name="обновление_расписание_дня",
    description="Обновляет расписание дня"
  )
  async def raspisanie_loop_command(self, ctx):
    await self.raspisanie_commands()
    await ctx.send(content = "Расписание дня обновлено!", ephemeral = True)

"""
def setup(bot):
  bot.add_cog(Raspisanie (bot))