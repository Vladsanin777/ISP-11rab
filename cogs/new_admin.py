import disnake
from disnake.ext import commands
from datab.ORM import DS_Servers

class NewAdmin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready (self):
        print(f"Бот {self.bot.user} использует ког {__name__}")


    @commands.slash_command(name = "выдача_админки", description = "Отправка заявки на администрирования этого сервера")
    async def new_admin(self, ctx):
        if (cha := await DS_Servers().admin_channel(guild_id = ctx.guild.id)) != 0:
            if self.bot.get_guild(ctx.guild.id).get_channel(cha) is not None:
                view = disnake.ui.View()
                view.add_item(disnake.ui.Button(label="Подать заявку", custom_id="new_admin", style=disnake.ButtonStyle.green))
                await ctx.send(embed=disnake.Embed(description='Привет, нажми кнопку чтобы стать админом!', colour=555555), view=view, ephemeral=True)
            else:
                await ctx.send(embed=disnake.Embed(description='Привет, Мне очень жаль но я не смогу отправить заявку на выдачу вам прав администратора так как на этом сервере был удалён канал администрации следовательно я немогу отправить вашу заявку на рассмотрение админам и владельцу сервера если у вас есть связь с админами или с владельцем сервера обратитесь к ним путь установят канал для админов спомошью комманды\n/канал_администрации', colour=111111),  ephemeral=True)
        else:
            await ctx.send(embed=disnake.Embed(description='Привет, Мне очень жаль но я не смогу отправить заявку на выдачу вам прав администратора так как на этом сервере не назначен канал администрации следовательно я немогу отправить вашу заявку на рассмотрение админам и владельцу сервера если у вас есть связь с админами или с владельцем сервера обратитесь к ним путь установят канал для админов спомошью комманды\n/канал_администрации', colour=111111), ephemeral=True)

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
        custID = inter.component.custom_id
        match custID:
            case "new_admin":
                # Детали модального окна и его компонентов
                components = [
                    disnake.ui.TextInput(
                        label="Имя",
                        placeholder="Введите ваше имя!",
                        custom_id="Имя",
                        style=disnake.TextInputStyle.short,
                        max_length=50,
                    ),
                    disnake.ui.TextInput(
                        label="Фамилия",
                        placeholder="Введите вашу фамилию!",
                        custom_id="Фамилия",
                        style=disnake.TextInputStyle.short,
                        max_length=50,
                    ),
                    disnake.ui.TextInput(
                        label="Возраст",
                        placeholder="Введите ваш возраст!",
                        custom_id="Возраст",
                        style=disnake.TextInputStyle.short,
                        max_length=50,
                    ),
                    disnake.ui.TextInput(
                        label="О себе",
                        placeholder="Напишите о себе!",
                        custom_id="О себе",
                        style=disnake.TextInputStyle.paragraph,
                        max_length=4000,
                    )
                ]
                await inter.response.send_modal(modal=disnake.ui.Modal(
                    title="Заявление на админку!",
                    custom_id="new_admin",
                    components=components,
                ))
            case _:
                if inter.author.guild_permissions.administrator:
                    #user_n = inter.guild.get_member(custID[14:])
                    user_n = inter.guild.get_member(int(custID[14:]))
                    role_admin = inter.guild.get_role(await DS_Servers().admin_role(guild_id=inter.guild.id))
                    match custID[:14]:
                        case "new_admin_yes_":
                            try:
                                await user_n.add_roles(role_admin)
                                await inter.message.delete()
                                await user_n.send(f"Вам одобренно в администрировании!\nНа сервере ({inter.guild.name})\nАдминистратором ({inter.author.mention})", embed=inter.message.embeds[0])
                                await inter.send(embed=disnake.Embed(description=f"Вы одобрили выдачу роли администратора ({role_admin.name}) пользователю ({user_n.mention})", colour=555555), ephemeral=True)
                                await inter.channel.send(embed=disnake.Embed(description=f"Администратор ({inter.author.mention}) одобрил выдачу роли администратора ({role_admin.name}) пользователю ({user_n.mention})"))
                            except disnake.errors.Forbidden:
                                await inter.send(embed=disnake.Embed(description=f"""{inter.user.mention} ```ansi
[2;31m[2;31m[0;31m[0;31mВнимательно прочитай![0m[0;31m[0m[2;31m[0m[2;31m[0m
``` \nЯ не могу выдать {user_n.mention} роль потому что она ({role_admin.name}) стоит выше в списке ролей чем моя\nЧто бы это исправить либо опустите роль ({role_admin.name}) ниже моей либо на оборот поднимите мою роль выше роли ({role_admin.name})""", colour=555555), ephemeral=True)
                        case "new_admin_not_":
                            await inter.message.delete()
                            await user_n.send(f"Вам отказано в администрировании!\nНа сервере ({inter.guild.name})\nАдминистратором ({inter.author.mention})", embed=inter.message.embeds[0])
                            await inter.send(embed=disnake.Embed(description=f"Вы не одобрили выдачу роли администратора ({role_admin.name}) пользователю ({user_n.mention})", colour=555555), ephemeral=True)
                            await inter.channel.send(embed=disnake.Embed(description=f"Администратор ({inter.author.mention}) не одобрил выдачу роли администратора ({role_admin.name}) пользователю ({user_n.mention})"))
                else:
                    await inter.send(embed=disnake.Embed(description="У вас нет прав для того чтобы принимать решения о принятии администратора на пост!", colour=888888), ephemeral=True)



    @commands.Cog.listener()
    async def on_modal_submit(self, modal: disnake.ui.Modal):
        match modal.custom_id:
            case "new_admin":
                embed = disnake.Embed(description=f"{modal.user.mention} хочет получить админку на этом сервере ({modal.guild}) вот его заявка:", colour = 666666)
                for component in modal.data.components:
                    embed.add_field(
                        name=component['components'][0]['custom_id'],
                        value=component['components'][0]['value'],
                        inline=False,
                    )
                view = disnake.ui.View()
                view.add_item(disnake.ui.Button(label="Назначить", custom_id=f"new_admin_yes_{modal.user.id}", style=disnake.ButtonStyle.green))
                view.add_item(disnake.ui.Button(label="Отклонить", custom_id=f"new_admin_not_{modal.user.id}", style=disnake.ButtonStyle.red))
                await self.bot.get_channel(await DS_Servers().admin_channel(guild_id=modal.guild.id)).send(embed=embed, view = view)
                await modal.response.send_message(f"Ваша заявка отправлена админам этого сервера ({modal.guild}) на рассмотрение", embed = embed, ephemeral=True)


    #@commands.Cog.listene


def setup(bot):
    bot.add_cog(NewAdmin (bot))
