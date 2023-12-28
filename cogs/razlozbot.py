import asyncio

import os

import disnake
from disnake.ext import commands

import element.razloz



class CMDUsers4 (commands.Cog):
  def __init__(self, bot): 
    self.bot = bot


  @commands.Cog.listener() 
  async def on_ready (self): 
    print(f"Бот {self.bot.user} использует ког {__name__}")

  @commands.slash_command(
    name = "разложение_чисел",
    description = "Раскладывает числа на простые множители"
  )
  async def razloz (
    ctx, 
    p1:
    int = commands.Param(
      name = "число_1",
      description = "Чисто для разложения"
    ),
    p2:
    int = commands.Param(
      default = None,
      name = "число_2",
      description = "Чисто для разложения"
    ),
    p3:
    int = commands.Param(
      default = None,
      name = "число_3",
      description = "Чисто для разложения"
    ),
    p4:
    int = commands.Param(
      default = None,
      name = "число_4",
      description = "Чисто для разложения"
    ),
    p5:
    int = commands.Param(
      default = None,
      name = "число_5",
      description = "Чисто для разложения"
    ),
    p6:
    int = commands.Param(
      default = None,
      name = "число_6",
      description = "Чисто для разложения"
    ),
    p7:
    int = commands.Param(
      default = None,
      name = "число_7",
      description = "Чисто для разложения"
    ),
    p8:
    int = commands.Param(
      default = None,
      name = "число_8",
      description = "Чисто для разложения"
    ),
    p9:
    int = commands.Param(
      default = None,
      name = "число_9",
      description = "Чисто для разложения"
    ),
    p10:
    int = commands.Param(
      default = None,
      name = "число_10",
      description = "Чисто для разложения"
    ),
    p11:
    int = commands.Param(
      default = None,
      name = "число_11",
      description = "Чисто для разложения"
    ),
    p12:
    int = commands.Param(
      default = None,
      name = "число_12",
      description = "Чисто для разложения"
    ),
    p13:
    int = commands.Param(
      default = None,
      name = "число_13",
      description = "Чисто для разложения"
    ),
    p14:
    int = commands.Param(
      default = None,
      name = "число_14",
      description = "Чисто для разложения"
    ),
    p15:
    int = commands.Param(
      default = None,
      name = "число_15",
      description = "Чисто для разложения"
    ),
    p16:
    int = commands.Param(
      default = None,
      name = "число_16",
      description = "Чисто для разложения"
    ),
    p17:
    int = commands.Param(
      default = None,
      name = "число_17",
      description = "Чисто для разложения"
    ),
    p18:
    int = commands.Param(
      default = None,
      name = "число_18",
      description = "Чисто для разложения"
    ),
    p19:
    int = commands.Param(
      default = None,
      name = "число_19",
      description = "Чисто для разложения"
    ),
    p20:
    int = commands.Param(
      default = None,
      name = "число_20",
      description = "Чисто для разложения"
    ),
    p21:
    int = commands.Param(
      default = None,
      name = "число_21",
      description = "Чисто для разложения"
    ),
    p22:
    int = commands.Param(
      default = None,
      name = "число_22",
      description = "Чисто для разложения"
    ),
    p23:
    int = commands.Param(
      default = None,
      name = "число_23",
      description = "Чисто для разложения"
    ),
    p24:
    int = commands.Param(
      default = None,
      name = "число_24",
      description = "Чисто для разложения"
    ),
    p25:
    int = commands.Param(
      default = None,
      name = "число_25",
      description = "Чисто для разложения"
    )
  ):
    rt = [ p1, p2, p3, p4, p5, 
      p6, p7, p8, p9, p10, 
      p11, p12, p13, p14, p15, 
      p16, p17, p18, p19, p20, 
      p21, p22, p23, p24, p25
    ]
    tyr = ""
    ut = 0
    for i in rt:
      match i:
        case None:
          pass
        case _:
          ut += 1
          lk = None
          lk = await element.razloz.rapk(i, "kl")
          tyr += (f"{ut}) {lk}\n")
    await ctx.send(f"{tyr}")


def setup(bot):
  bot.add_cog(CMDUsers4 (bot))