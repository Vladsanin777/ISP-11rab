from disnake.ext import commands
import asyncio

from dataclasses import dataclass


@dataclass
class Stabil_data:
  message = []



class Stabil(commands.Cog):
  def __init__ (self, bot): 
    self.bot = bot


  @commands.Cog.listener() 
  async def on_ready (self): 
    print(f"Бот {self.bot.user} использует ког {__name__}")

  async def stabil_command(self, stabil_time):
        try:
          message = await self.bot.get_channel(1180109793168461864).fetch_message(Stabil_data().message[0])
          await message.edit(content=f"Bot {self.bot.user} работает стабильно {stabil_time} минут!")
        except: 
          channel = self.bot.get_channel(1180109793168461864)
          messages = await channel.history().flatten()
          await channel.delete_messages(messages)
          await channel.send(content=f"Bot {self.bot.user} работает стабильно {stabil_time} минут!")
          message = await channel.history(limit = 1).flatten()
          Stabil_data().message.clear()
          Stabil_data().message.append(message[0].id)


  async def stabil(self):
    a = 0
    while True:
      await asyncio.gather(Stabil(self.bot).stabil_command(float(a/4)))
      await asyncio.sleep(15)
      a += 1


def setup(bot):
  bot.add_cog(Stabil (bot))