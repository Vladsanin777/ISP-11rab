import disnake
from disnake.ext import commands
from datab.ORM import DS_Servers

def admin_only():
    async def predicate(ctx):
        # Проверяем, есть ли у пользователя права администратора
        if ctx.author.guild_permissions.administrator:
            return True
        else:
            # Если у пользователя нет прав администратора, отправляем сообщение об ошибке
            await ctx.send("У вас нет прав на выполнение этой команды.")
            return False
    return commands.check(predicate)



class SettingsGuild(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready (self):
        print(f"Бот {self.bot.user} использует ког {__name__}")


    # Метод который изменяет канал для администрации
    @commands.slash_command(name="канал_администрации", description="Установить канал администрации")
    @admin_only()
    async def admin_channel(self, ctx, admin_channel: disnake.TextChannel):
        ds_server = DS_Servers()
        guild_id = ctx.guild.id
        cha_id = await ds_server.admin_channel(guild_id=guild_id)

        if cha_id == 0:
            await ds_server.edit_admin_channel(guild_id=guild_id, admin_channel=admin_channel.id)
            await ctx.send(embed=disnake.Embed(description=f"Вы ({ctx.author.display_name}) установили канал администрации ({admin_channel})!"), ephemeral=True)
            await admin_channel.send(embed=disnake.Embed(description=f"Администратор ({ctx.author.display_name}) установил этот канал ({admin_channel}) как канал администрации!"))

        elif cha_id == admin_channel.id:
            await ctx.send(embed=disnake.Embed(description=f"Извините ({ctx.author.display_name}) вы пытаетесь установить канал новый канал администрации, но он уже является каналом администрации ({admin_channel})!"), ephemeral=True)

        else:
            cha = ctx.guild.get_channel(await ds_server.edit_admin_channel(guild_id=guild_id, admin_channel=admin_channel.id))
            if cha is None:
                await ctx.send(embed=disnake.Embed(description=f"Вы ({ctx.author.display_name}) установили канал новый канал администрации ({admin_channel}) на смену не существующему на данный момент каналу!"), ephemeral=True)
                await admin_channel.send(embed=disnake.Embed(description=f"Администратор ({ctx.author.display_name}) установил этот канал ({admin_channel}) как канал администрации на смену не существующему на данный момент каналу!"))
            else:
                await ctx.send(embed=disnake.Embed(description=f"Вы ({ctx.author.display_name}) установили канал новый канал администрации ({admin_channel}) на смену канала ({cha})!"), ephemeral=True)
                await admin_channel.send(embed=disnake.Embed(description=f"Администратор ({ctx.author.display_name}) установил этот канал ({admin_channel}) как канал администрации на смену канала ({cha})!"))

    # Метод который изменяет канал для ивентов
    @commands.slash_command(name = "канал_ивентов", description = "Установить канал для ивентов")
    @admin_only()
    async def event_channel(self, ctx, event_channel: disnake.TextChannel):
        ds_server = DS_Servers()
        guild_id = ctx.guild.id
        cha_id = await ds_server.event_channel(guild_id=guild_id)

        if cha_id == event_channel.id:
            await ctx.send(embed=disnake.Embed(description=f"Извините ({ctx.author.display_name}) вы пытаетесь установить канал новый канал для ивентов, но он уже является каналом для ивентов ({event_channel})!"), ephemeral=True)
        else:
            cha = ctx.guild.get_channel(await ds_server.edit_event_channel(guild_id=guild_id, event_channel=event_channel.id))
            if cha is None:
                await ctx.send(embed=disnake.Embed(description=f"Вы ({ctx.author.display_name}) установили канал новый канал для ивентов ({event_channel}) на смену не существующему на данный момент каналу!"), ephemeral=True)
                await event_channel.send(embed=disnake.Embed(description=f"Администратор ({ctx.author.display_name}) установил этот канал ({event_channel}) как канал для ивентов на смену не существующему на данный момент каналу!"))
            else:
                await ctx.send(embed=disnake.Embed(description=f"Вы ({ctx.author.display_name}) установили канал новый канал для ивентов ({event_channel}) на смену канала ({cha})!"), ephemeral=True)
                await event_channel.send(embed=disnake.Embed(description=f"Администратор ({ctx.author.display_name}) установил этот канал ({event_channel}) как канал для ивентов на смену канала ({cha})!"))


def setup(bot):
    bot.add_cog(SettingsGuild (bot))
