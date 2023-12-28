from openai import AsyncOpenAI

import disnake
from disnake.ext import commands

import os

import asyncio
from typing import Optional
from disnake.ui import TextInput

import element.gpt









class GPT(commands.Cog):
  def __init__(self, bot):
    self.bot = bot



  @commands.Cog.listener()
  async def on_ready(self):
    print(f"Бот {self.bot.user} использует ког {__name__}")

  async def _internal_pause(self, time):
    await asyncio.sleep(time)


  async def _gpt_eva(self, ctx, response_gpt, dm, ui, tts):
    popi = 0
    response_gpt = response_gpt[0]
    print(response_gpt)
    for i in response_gpt:
      if i != None or i != "":
        print(i)
        if dm == 1:
          await ctx.channel.send(content=i, tts = True)
        elif dm == 2:
          if ui is False:
            await ctx.channel.send(content=i, tts = tts)
            await ctx.author.dm_channel.send(content=i, tts = tts)
          elif ui is True:
            await ctx.send(content=i, ephemeral=True, tts = tts)
            await ctx.author.dm_channel.send(content=i, tts = tts)
        popi += 1
        if popi > 8:
          await self._internal_pause(2)
          popi = 0





  @commands.slash_command(name="общение_с_gpt")
  async def gpt(self, ctx, message_gpt, tts: str = commands.Param(name = "чтение_ответа", choices = ["Да, зачитать", "Нет, незачитывать"]), ui: str = commands.Param(name="видимость", default="Только для меня", choices=["Для всех", "Только для меня"])):
    await ctx.send(content=f"Братан {ctx.author.display_name} не кипетись ща отвечу на твой вопрос {message_gpt[:100]}",
      ephemeral=True)
    response_gpt = await asyncio.gather(element.gpt.gpt().gpt(message_gpt, 2000))
    print(response_gpt)


    respons_gpt = response_gpt[0]

    await ctx.author.create_dm()

    a = 1
    if ctx.author.dm_channel.id != ctx.channel.id:
      a += 1

    tts = bool(True if tts == "Да, зачитать" else False)
    if ui == "Для всех":
      await asyncio.gather(self._gpt_eva(ctx, response_gpt, a, False, tts))
    elif ui == "Только для меня":
      await asyncio.gather(self._gpt_eva(ctx, response_gpt, a, True, tts))


def setup(bot):
  bot.add_cog(GPT(bot))
