import asyncio
import math
import disnake
from disnake.ext import commands
import os
from typing import Optional
import aiogram






class podtverzhd(disnake.ui.View):
  def __init__(self):
    super().__init__()
    self.value = Optional[bool]
  @disnake.ui.button(label='Подтвердить отправку', style=disnake.ButtonStyle.green, emoji='✅')
  async def yes(self, button: disnake.ui.Button, interaction: disnake.CmdInteraction):
    await interaction.response.send_message('Отправка подтверждена!', ephemeral=True)
    self.value = True
    self.stop()
  @disnake.ui.button(label='Отменить отпрвку', style=disnake.ButtonStyle.red, emoji='❌')
  async def no(self, button: disnake.ui.Button, interaction: disnake.CmdInteraction):
    await interaction.response.send_message('Отправка отменена', ephemeral=True)
    self.value = False
    self.stop()


class podtverzhd_dr_kan(disnake.ui.View):
  def __init__(self):
    super().__init__()
    self.value = Optional[bool]

  @disnake.ui.button(label='Отменить отпрвку', style=disnake.ButtonStyle.red, emoji='❌')
  async def no(self, button: disnake.ui.Button, interaction: disnake.CmdInteraction):
    await interaction.response.send_message('Отправка отменена', ephemeral=True)
    self.value = False
    self.stop()
  @disnake.ui.button(label='Подтвердить отправку', style=disnake.ButtonStyle.green, emoji='✅')
  async def yes(self, button: disnake.ui.Button, interaction: disnake.CmdInteraction):
    view = podtverzhd()
    await interaction.response.send_message(content = "Вы уверины что хотите переправить данное сообщение?", view = view, ephemeral=True)
    await view.wait()
    if view.value is True:
      self.value = True
    else:
      self.value = False
    self.stop()




class new (commands.Cog):
  def __init__(self, bot): 
    self.bot = bot


  @commands.Cog.listener() 
  async def on_ready (self): 
    print(f"Бот {self.bot.user} использует ког {__name__}")



  #tg
  async def is_tg_in_ds(self, message_tg):
    channel = self.bot.get_channel(1147225474444046507)
    await channel.send(message_tg)

  #discord
  async def podtverzhd_1(self, ctx, pered_massage_ds, message_ds):
    view = podtverzhd()
    await ctx.response.send_message(content = pered_massage_ds, view = view, ephemeral=True)
    await view.wait()
    if view.value is True:
      #await asyncio.gather(send_message_tg(message_ds))
      channel = self.bot.get_channel(1147225474444046507)
      await channel.send(message_ds)




  async def podtverzhd_2(self, ctx, pered_massage_ds, message_ds):
    view_dr_kan = podtverzhd_dr_kan()
    await ctx.response.send_message(content = pered_massage_ds, view = view_dr_kan, ephemeral=True)
    await view_dr_kan.wait()
    match view_dr_kan.value:
      case True:
        #$await asyncio.gather(send_message_tg(message_ds))
        channel = self.bot.get_channel(1147225474444046507)
        await channel.send(message_ds)







  #Пересылка новости в телеграм

  @commands.slash_command(name="новость")
  async def news_ds(self, ctx, message_ds: str = commands.Param(name="новость")):
    message_ds = f'Новость отпралена из Discord\nС сервера: {ctx.guild}\nИз канала: {ctx.channel}\nПользователем: {ctx.author.display_name}\nНовость:{message_ds}'
    pered_massage_ds = (f"Переслать это сообщение:\n{message_ds}")
    if ctx.channel.id == 1147225474444046507:
      await asyncio.gather(self.podtverzhd_1(ctx, pered_massage_ds, message_ds))
    else:
      await asyncio.gather(self.podtverzhd_2(ctx, pered_massage_ds, message_ds))




def setup(bot):
  bot.add_cog(new (bot))
