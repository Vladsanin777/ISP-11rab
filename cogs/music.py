import asyncio
import math
import disnake
from disnake.ext import commands, tasks
from asyncio import Queue
import os
import logging

from icecream import ic

import yt_dlp

from dataclasses import dataclass




class CMDUsers7 (commands.Cog):
  def __init__(self, bot): 
    self.bot = bot


  @commands.Cog.listener() 
  async def on_ready (self): 
    print(f"Бот {self.bot.user} использует ког {__name__}")
    self.queue = dict()



  @commands.slash_command()
  async def add(self, ctx, url: str):
    await ctx.response.defer()
    """Добавляет трек в очередь."""
    if not url.startswith('http'):
      return await ctx.send('Неверная ссылка.')
    
    # Получение информации о треке
    try:
      ydl_opts = {
        'format': 'bestaudio',
        'age_limit': 120,  # Указываем возрастной лимит (можно указать любой, включая 18+)
      }
      with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info['title']
        url_audio = info['url']
    except Exception as e:
      title = "Об этом треке нет информации"
      print(f"Ошибка при получении информации о треке: {e}")
    
    # Добавление трека в очередь
    if str(ctx.author.voice.channel.id) not in self.queue:
      self.queue[str(ctx.author.voice.channel.id)] = [(title, url_audio)]
      print("Первый")
    else:
      self.queue[str(ctx.author.voice.channel.id)].append((title, url_audio))
    await ctx.send(f'Трек **{title}** добавлен в очередь.')
    print(self.queue)
    print(url_audio)


  # Функция для воспроизведения следующего трека
  async def play_next_track(self, ctx):
    voice_client = disnake.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    if str(ctx.author.voice.channel.id) in self.queue and self.queue[str(ctx.author.voice.channel.id)]:
      next_title, next_url = self.queue[str(ctx.author.voice.channel.id)].pop(0)
      next_source = await disnake.FFmpegOpusAudio.from_probe(next_url)
      voice_client.play(next_source)
      await ctx.send(f'Воспроизводится **{next_title}**.')
    else:
      await voice_client.disconnect()



  # Команда для воспроизведения очереди
  @commands.slash_command()
  async def play(self, ctx):


    ic(self.queue)
    ic(ctx.author.voice.channel.id)
    # Проверка очереди
    if str(ctx.author.voice.channel.id) not in self.queue:
      return await ctx.send('Очередь пуста.')
    voice_client = disnake.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    """Воспроизводит очередь треков."""
    if not disnake.utils.get(ctx.bot.voice_clients, guild=ctx.guild):
      await ctx.author.voice.channel.connect()
      await ctx.send('Бот подключился к голосовому каналу.')
      while True:
        while voice_client.is_playing():
          await asyncio.sleep(3)
        if len(self.queue and self.queue[str(ctx.author.voice.channel.id)]) != 0:
          await self.play_next_track()
        else:
          await ctx.author.voice.channel.disconnect()
          break

    
    
    # Воспроизведение первого трека
    title, url = self.queue[str(ctx.author.voice.channel.id)].pop(0)
    source = await disnake.FFmpegOpusAudio.from_probe(url)
    disnake.utils.get(ctx.bot.voice_clients, guild=ctx.guild).play(source)
    await ctx.send(f'Воспроизводится **{title}**.')

  # Команда для пропуска трека
  @commands.slash_command()
  async def skip(self, ctx):
    """Пропускает текущий трек."""
    if not ctx.voice_client:
      return await ctx.send('Бот не подключен к голосовому каналу.')
    
    # Проверка очереди
    if not Queue().queue:
      return await ctx.send('Очередь пуста.')
    
    # Остановка текущего трека
    ctx.voice_client.stop()
    
    # Воспроизведение следующего трека
    title, url = Queue().queue.pop(0)
    source = await disnake.FFmpegOpusAudio.from_probe(url)
    ctx.voice_client.play(source)
    await ctx.send(f'Воспроизводится **{title}**.')


  #Перемотка вперёд
  @commands.slash_command()
  async def forward(self, ctx, count: int):
    """Перематывает очередь на заданное количество треков вперёд."""
    if not ctx.voice_client:
      return await ctx.send('Бот не подключен к голосовому каналу.')
    
    # Проверка очереди
    if not Queue().queue:
      return await ctx.send('Очередь пуста.')
    
    # Проверка количества треков
    if count > len(Queue().queue):
      return await ctx.send(f'В очереди недостаточно треков.')
    
    # Перемотка очереди
    for _ in range(count):
      Queue().queue.pop(0)
    
    # Воспроизведение следующего трека
    title, url = Queue().queue.pop(0)
    source = await disnake.FFmpegOpusAudio.from_probe(url)
    ctx.voice_client.play(source)
    await ctx.send(f'Воспроизводится **{title}**.')



  #Перемотка назад
  @commands.slash_command()
  async def backward(self, ctx, count: int):
    """Перематывает очередь на заданное количество треков назад."""
    if not ctx.voice_client:
      return await ctx.send('Бот не подключен к голосовому каналу.')
    
    # Проверка очереди
    if not Queue().queue:
      return await ctx.send('Очередь пуста.')
    
    # Проверка количества треков
    if count > len(Queue().queue):
      return await ctx.send(f'В очереди недостаточно треков.')
    
    # Перемотка очереди
    for _ in range(count):
      Queue().queue.append(Queue().queue.pop(0))
    
    # Воспроизведение текущего трека
    title, url = Queue().queue[-1]
    source = await disnake.FFmpegOpusAudio.from_probe(url)
    ctx.voice_client.play(source)
    await ctx.send(f'Воспроизводится **{title}**.')


  """
  @commands.slash_command(
    name = "плей",
    description = "Включает очередь"
  )
  async def play(
    ctx,
    *,
    ok:
    str = commands.Param(
      name = "очередь",
      description = "Ссылка на очередь"
    ),
    voice_channel: 
    disnake.VoiceChannel = commands.Param(
      default = None,
      name = "голосовой_канал"
    )
  ):
    YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'True', 'simulate': 'True', 'preferredquality': '192', 'preferredcodec': 'mp3', 'key': 'FFmpegExtractAudio'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    #global user

    match voice_channel:
      case None:
        try:
          voice_channel = ctx.author.voice.channel
        except:
          voice_channel = None
        match voice_channel:
          case None:
            await ctx.send(f"Вы не находитесь в голосовом канале и не выброли канал к которому хотите подключить бота.")
          case _:
            vc = await voice_channel.connect()
      case _:
        vc = await voice_channel.connect()

    if ctx.is_playing():
      await ctx.send(f'{ctx.cog_after_slash_command_invoke.mention}, музыка уже проигрывается.')

    else:
      with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(ok, download = False)

      URL = info['formats'][0]['url']

      vc.play (discord.FFmpegPCMAudio(executable="ffmpeg\\ffmpeg.exe", source = URL, **FFMPEG_OPTIONS))

      if not vc.is_paused():
        await vc.disconnect()
        """

def setup(bot):
  bot.add_cog(CMDUsers7 (bot))