import asyncio
import math
import disnake
from disnake.ext import commands
import os
import collection


import element.razloz


class CMDUsers6 (commands.Cog):
  def __init__(self, bot): 
    self.bot = bot

  @commands.Cog.listener() 
  async def on_ready (self): 
    print(f"Бот {self.bot.user} использует ког {__name__}")


  @commands.slash_command(
    name = "нод_эксп"
  )
  async def nodm(
    ctx,
    f1:
    int = commands.Param(
      name = "число_1"
    ),
    f2:
    int = commands.Param(
      name = "число_2"
    ),
    f3:
    int = commands.Param(
      default = None,
      name = "число_3"
    ),
    f4:
    int = commands.Param(
      default = None,
      name = "число_4"
    ),
    f5:
    int = commands.Param(
      default = None,
      name = "число_5"
    ),
    f6:
    int = commands.Param(
      default = None,
      name = "число_6"
    ),
    f7:
    int = commands.Param(
      default = None,
      name = "число_7"
    ),
    f8:
    int = commands.Param(
      default = None,
      name = "число_8"
    ),
    f9:
    int = commands.Param(
      default = None,
      name = "число_9"
    ),
    f10:
    int = commands.Param(
      default = None,
      name = "число_10"
    )
  ):


    fg = [
      f1, f2, f3, f4, f5,
      f6, f7, f8, f9, f10
    ]


    ii = ""
    ip = []
    for i in fg:
      match i:
        case None:
          pass
        case _:
          i = await element.razloz.rapk(i)
          ii += (f"{i[0]}\n")
          ip.append(i[1])


    async def srav(tu ,tp):
      a = []
      ly = ""
      mhj = -1
      kgh = 0
      pt = tp
      tp = max(tp, tu)
      tu = min(tu, pt)
      for i in tp:
        fgh = -1
        mhj += 1
        for j in tu:
          fgh += 1
          if i == j:
            tp.insert(mhj, j)
            tu.insert(fgh, j)
            a.append(i)
            if kgh == 0:
              kgh += 1
              ly += (f"{i}")
              break
            else:
              ly += (f" + {i}")
              break
      return a

    print(ip)
    sd = []
    for n1 in :
      print(n1)
      ip -= n1
      for n2 in max(ip):
        ip -= n2
        sd = await asyncio.gather(srav(n2, n1))
        break



    await ctx.send(f"{sd}")

def setup(bot):
  bot.add_cog(CMDUsers6 (bot))