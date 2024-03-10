import asyncio
import math
import disnake
from disnake.ext import commands, tasks
from asyncio import Queue
import os
import logging

from icecream import ic

from youtube_dl import YoutubeDL

from dataclasses import dataclass




class CMDUsers7 (commands.Cog):
  def __init__(self, bot): 
    self.bot = bot
    self.queue: dict


  @commands.Cog.listener() 
  async def on_ready (self): 
    print(f"Бот {self.bot.user} использует ког {__name__}")



  # Команда для добавления трека в очередь
  @commands.slash_command()
  async def add(self, ctx, url: str):
    """Добавляет трек в очередь."""
    if not url.startswith('http'):
      return await ctx.send('Неверная ссылка.')
    
    # Получение информации о треке
    with YoutubeDL() as ydl:
      info = ydl.extract_info(url, download=False)
    
    # Добавление трека в очередь
    ic(ctx.author.voice.channel.id)
    if self.queue[ctx.author.voice.channel.id] is None:
      self.queue[ctx.author.voice.channel.id] = [(info['title'], url)]
    else:
      self.queue[ctx.author.voice.channel.id].append((info['title'], url))
    await ctx.send(f'Трек **{info["title"]}** добавлен в очередь.')
    ic(self.queue[ctx.author.voice.channel.id])

  # Команда для воспроизведения очереди
  @commands.slash_command()
  async def play(self, ctx):
    """Воспроизводит очередь треков."""
    if not ctx.voice_client:
      return await ctx.send('Бот не подключен к голосовому каналу.')
    
    # Проверка очереди
    if not Queue().queue:
      return await ctx.send('Очередь пуста.')
    
    # Воспроизведение первого трека
    title, url = Queue().queue.pop(0)
    source = await disnake.FFmpegOpusAudio.from_probe(url)
    ctx.voice_client.play(source)
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