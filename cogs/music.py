import asyncio
import math
import disnake
from disnake.ext import commands
import os

from youtube_dl import YoutubeDL


class CMDUsers7 (commands.Cog):
  def __init__(self, bot): 
    self.bot = bot


  @commands.Cog.listener() 
  async def on_ready (self): 
    print(f"Бот {self.bot.user} использует ког {__name__}")
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