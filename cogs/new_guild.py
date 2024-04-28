import disnake
from disnake.ext import commands
from datab.ORM import DS_Servers

class NewGuild(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Бот {self.bot.user} использует ког {__name__}")

    @commands.slash_command(name="регистрация_сервера", description="Если бот некорректно работает на вашем сервере")
    async def server_registration(self, ctx):
        await ctx.send(embed = disnake.Embed(description = await self.on_guild_join(ctx.guild), colour=555555), ephemeral=True)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        top_channel = guild.text_channels[0]  # получаем самый верхний текстовый канал
        if await DS_Servers().new_guild(guild_id=guild.id, guild_name=guild.name, guild_event_channel=top_channel.id):
            greetings = 'Привет всем! Я первый раз на этом сервере вот команды для первоначальной настройки:\n   /channel_admin\n    /channel_event'
        else:
            try:
                event_channel = DS_Servers().event_channel(guild.id)
                greetings = 'Привет всем! Я вернулся и помню предыдущие настройки, но на всякий случай вот команды для моей настройки:\n /channel_admin\n    /channel_event'
                await event_channel.send(embed=disnake.Embed(description=greetings, colour=555555))
            except:
                await DS_Servers().edit_event_channel(guild_id=guild.id, new_event_channel=top_channel.id)
                greetings = 'Привет всем! Я вернулся и помню предыдущие настройки, но на всякий случай вот команды для моей настройки:\n /channel_admin\n    /channel_event'
                await top_channel.send(embed=disnake.Embed(description=greetings, colour=555555))
        return greetings

def setup(bot):
    bot.add_cog(NewGuild(bot))
