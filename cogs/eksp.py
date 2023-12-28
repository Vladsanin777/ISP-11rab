import asyncio

import disnake
from disnake.ext import commands

import os


class CMDUsers5 (commands.Cog):
  def __init__(self, bot): 
    self.bot = bot


  @commands.Cog.listener() 
  async def on_ready (self): 
    print(f"Бот {self.bot.user} использует ког {__name__}")


  @commands.slash_command()
  async def eksp(ctx):
    print(f"{ctx}")
    await ctx.send(f"{await ctx}")


def setup(bot):
  bot.add_cog(CMDUsers5 (bot))
