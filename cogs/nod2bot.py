import asyncio
import math
import disnake
from disnake.ext import commands
import os


import element.tradidnod
import element.costomEVKnod
import element.EVKnod

class CMDUsers1 (commands.Cog):
  def __init__(self, bot): 
    self.bot = bot


  @commands.Cog.listener() 
  async def on_ready (self): 
    print(f"Бот {self.bot.user} использует ког {__name__}")



  @commands.slash_command(
    name = "нод",
    description = "Двух чисел"
  )
  async def nod (
    ctx,
    p:
    int = commands.Param(
      name = "первое_число",
      description = "Введите первое число"
    ),
    u:
    int = commands.Param(
      name = "второе_число",
      description = "Введите второе число"
    ),
    t:
    str = commands.Param(
      name = "обяснение",
      choices = [
        "Пошаговое",
        "Для галочки",
        "Только ответ"
      ]
    ),
    r:
    str = commands.Param(
      name = "способ",
      description = "Можно с разу двумя способами",
      choices = [
        "Все три",
        "Традиционный способ",
        "Способ Евклида",
        "Кастомный способ Евклида"
      ]
    ),
    f:
    str = commands.Param(
      default = "Нет, без формулы",
      name = "формула",
      description = "Нужнали формула?",
      choices = [
        "Да, с формулой",
        "Нет, без формулы"
      ]
    )
  ):
    match t:
      case "Только ответ":
        b = math.gcd(p, u)
        await ctx.send(f"Всё ответ готов {b}")
      case _:
        tyo = [p, u, f, t]
        match r:
          case "Все три":
            #Традиционный
            c = await element.tradidnod.tradid(tyo)
            try:
              await ctx.send(f"{c}")
            except BaseException:
              await ctx.send("Результат получился слишком большой для отправки, попробуйте выбрать менее подробное обЪяснение.")
            #Кастомный способ ЕВК
            n = await element.costomEVKnod.costomEVK(tyo)
            try:
              await ctx.send(f"{n}")
            except BaseException:
              await ctx.send("Результат получился слишком большой для отправки, попробуйте выбрать менее подробное обЪяснение.")
            #Способ Евклида обыч.
            g = await element.EVKnod.EVK(tyo)
            try:
              await ctx.send(f"{g}")
            except BaseException:
              await ctx.send("Результат получился слишком большой для отправки, попробуйте выбрать менее подробное обЪяснение.")
          case "Традиционный способ":
            c = await element.tradidnod.tradid(tyo)
            try:
              await ctx.send(f"{c}")
            except BaseException:
              await ctx.send("Результат получился слишком большой для отправки, попробуйте выбрать менее подробное обЪяснение.")
          case "Кастомный способ Евклида":
            n = await element.costomEVKnod.costomEVK(tyo)
            try:
              await ctx.send(f"{n}")
            except BaseException:
              await ctx.send("Результат получился слишком большой для отправки, попробуйте выбрать менее подробное обЪяснение.")
          case "Способ Евклида":
            g = await element.EVKnod.EVK(tyo)
            try:
              await ctx.send(f"{g}")
            except BaseException:
              await ctx.send("Результат получился слишком большой для отправки, попробуйте выбрать менее подробное обЪяснение.")



def setup(bot):
  bot.add_cog(CMDUsers1 (bot))