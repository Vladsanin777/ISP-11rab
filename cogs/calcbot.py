import disnake
from disnake.ext import commands 
import asyncio
import numexpr
import os

class CMDUsers2 (commands.Cog):
  def __init__(self, bot): 
    self.bot = bot


  @commands.Cog.listener() 
  async def on_ready (self): 
    print(f"Бот {self.bot.user} использует ког {__name__}")

  @commands.slash_command(
    name = "калькулятор",
    description = "Считает выражения"
  )
  async def calc (
    ctx, 
    gh1:
    str = commands.Param(
      name = "выражение_1",
      description = "Считает выражения любой сложности"
    ),
    gh2:
    str = commands.Param(
      default = None,
      name = "выражение_2",
      description = "Считает выражения любой сложности"
    ),
    gh3:
    str = commands.Param(
      default = None,
      name = "выражение_3",
      description = "Считает выражения любой сложности"
    ),
    gh4:
    str = commands.Param(
      default = None,
      name = "выражение_4",
      description = "Считает выражения любой сложности"
    ),
    gh5:
    str = commands.Param(
      default = None,
      name = "выражение_5",
      description = "Считает выражения любой сложности"
    ),
    gh6:
    str = commands.Param(
      default = None,
      name = "выражение_6",
      description = "Считает выражения любой сложности"
    ),
    gh7:
    str = commands.Param(
      default = None,
      name = "выражение_7",
      description = "Считает выражения любой сложности"
    ),
    gh8:
    str = commands.Param(
      default = None,
      name = "выражение_8",
      description = "Считает выражения любой сложности"
    ),
    gh9:
    str = commands.Param(
      default = None,
      name = "выражение_9",
      description = "Считает выражения любой сложности"
    ),
    gh10:
    str = commands.Param(
      default = None,
      name = "выражение_10",
      description = "Считает выражения любой сложности"
    ),
    gh11:
    str = commands.Param(
      default = None,
      name = "выражение_11",
      description = "Считает выражения любой сложности"
    ),
    gh12:
    str = commands.Param(
      default = None,
      name = "выражение_12",
      description = "Считает выражения любой сложности"
    ),
    gh13:
    str = commands.Param(
      default = None,
      name = "выражение_13",
      description = "Считает выражения любой сложности"
    ),
    gh14:
    str = commands.Param(
      default = None,
      name = "выражение_14",
      description = "Считает выражения любой сложности"
    ),
    gh15:
    str = commands.Param(
      default = None,
      name = "выражение_15",
      description = "Считает выражения любой сложности"
    ),
    gh16:
    str = commands.Param(
      default = None,
      name = "выражение_16",
      description = "Считает выражения любой сложности"
    ),
    gh17:
    str = commands.Param(
      default = None,
      name = "выражение_17",
      description = "Считает выражения любой сложности"
    ),
    gh18:
    str = commands.Param(
      default = None,
      name = "выражение_18",
      description = "Считает выражения любой сложности"
    ),
    gh19:
    str = commands.Param(
      default = None,
      name = "выражение_19",
      description = "Считает выражения любой сложности"
    ),
    gh20:
    str = commands.Param(
      default = None,
      name = "выражение_20",
      description = "Считает выражения любой сложности"
    ),
    gh21:
    str = commands.Param(
      default = None,
      name = "выражение_21",
      description = "Считает выражения любой сложности"
    ),
    gh22:
    str = commands.Param(
      default = None,
      name = "выражение_22",
      description = "Считает выражения любой сложности"
    ),
    gh23:
    str = commands.Param(
      default = None,
      name = "выражение_23",
      description = "Считает выражения любой сложности"
    ),
    gh24:
    str = commands.Param(
      default = None,
      name = "выражение_24",
      description = "Считает выражения любой сложности"
    ),
    gh25:
    str = commands.Param(
      default = None,
      name = "выражение_25",
      description = "Считает выражения любой сложности"
    ),
  ):

    kl = [gh1, gh2, gh3, gh4, gh5,
      gh6, gh7, gh8, gh9, gh10,
      gh11, gh12, gh13, gh14, gh15,
      gh16, gh17, gh18, gh19, gh20,
      gh21, gh22, gh23, gh24, gh25
    ]
    res = ""
    k = 0
    tyu = (f"")
    for i in kl:
      match i:
        case None:
          pass
        case _:
          try:
            r = numexpr.evaluate(i)
          except BaseException:
            tyu = i
            i = i[:-1]
            try:
              r = numexpr.evaluate(i)
            except BaseException:
              r = None
          k += 1
          match r:
            case None:
              res += (f"{k}) {tyu}   Данное выражение написанно не корректно\n")
            case _:
              res += (f"{k}) {i} = {r}\n")

    await ctx.send(f"{res}")

def setup(bot):
  bot.add_cog(CMDUsers2 (bot))