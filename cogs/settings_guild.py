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
            await ctx.send(embed = disnake.Embed(description = "У вас нет прав на выполнение этой команды."), ephemeral = True)
            return False
    return commands.check(predicate)



class SettingsGuild(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready (self):
        print(f"Бот {self.bot.user} использует ког {__name__}")


    # Метод который изменяет канал для администрации и роль администрации
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

            admin_roles = [role for role in ctx.guild.roles if role.permissions.administrator and not is_bot_role(role)]

            if len(admin_roles) != 0:
                top_admin_role = max(admin_roles, key=lambda r: r.position)
                await ds_server.edit_admin_role(guild_id = ctx.guild.id, admin_role_id = top_admin_role.id)
                view = disnake.ui.View()
                for admin_role in admin_roles:
                    view.add_item(disnake.ui.Button(label=admin_role.name, custom_id=f"admin_role_id_{admin_role.id}", style=disnake.ButtonStyle.red)
                await admin_channel.send(embed = disnake.Embed(description = f"Выберите роль для администраторов по умолчанию она будет ({top_admin_role.name}) если вы не видите нужной роли то воспользуйтесь командой:\n/роль_админа\nВажное примечание роль администратора должна иметь права администратора!", colour = 666666), view = view)
            else:
                guild = ctx.guild
                admin_perms = discord.Permissions(administrator=True)
                admin_role = await guild.create_role(name='Admin', permissions=admin_perms)
                await ds_server.edit_admin_role(guild_id = ctx.guild.id, admin_role_id = admin_role.id)
                await admin_channel.send(embed = disnake.Embed(description = f"Роль для администрации {admin_role.name}, если вас неустраивает эта роль то создайте свою и воспользуйтесь командой:\n/роль_админа\nВажное примечание роль администратора должна иметь права администратора!", colour = 666666))



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

    async def admin_role_list(self, guild):
        return [role for role in guild.roles if role.permissions.administrator and not is_bot_role(role)]


    @commands.slash_command(name = "роль_админа", description = "Установить роль для администраторов")
    @admin_only()
    async def new_admin_role(self, ctx, admin_role = commands.Param(choise = await self.admin_role_list(ctx.guild))):
        await ds_server.edit_admin_role(guild_id = ctx.guild.id, admin_role_id = admin_role.id)
        await ctx.send(embed=disnake.Embed(description=f"Теперь роль администратора будет {admin.name}, если хотите хотите изменить роль то создайте роль с правами администратора и воспользуйтесь командой\n/роль_админа"), ephemeral=True)

def setup(bot):
    bot.add_cog(SettingsGuild (bot))
