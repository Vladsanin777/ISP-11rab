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
                await ctx.send(embed=disnake.Embed(description='Привет, Мне очень жаль но я не смогу отправить заявку на выдачу вам прав администратора так как на этом сервере был удалён канал администрации следовательно я немогу отправить вашу заявку на рассмотрение админам и владельцу сервера если у вас есть связь с админами или с владельцем сервера обратитесь к ним путь установят канал для админов спомошью комманды\n/admin_channel', colour=111111), view=view, ephemeral=True)
        else:
            await ctx.send(embed=disnake.Embed(description='Привет, Мне очень жаль но я не смогу отправить заявку на выдачу вам прав администратора так как на этом сервере не назначен канал администрации следовательно я немогу отправить вашу заявку на рассмотрение админам и владельцу сервера если у вас есть связь с админами или с владельцем сервера обратитесь к ним путь установят канал для админов спомошью комманды\n/admin_channel', colour=111111), view=view, ephemeral=True)

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
        match inter.component.custom_id:
            case "new_admin":
                # Детали модального окна и его компонентов
                components = [
                    disnake.ui.TextInput(
                        label="Имя",
                        placeholder="Введите ваше имя!",
                        custom_id="Имя:",
                        style=disnake.TextInputStyle.short,
                        max_length=50,
                    ),
                    disnake.ui.TextInput(
                        label="Фамилия",
                        placeholder="Введите вашу фамилию!",
                        custom_id="Фамилия:",
                        style=disnake.TextInputStyle.short,
                        max_length=50,
                    ),
                    disnake.ui.TextInput(
                        label="Возраст",
                        placeholder="Введите ваш возраст!",
                        custom_id="Возраст:",
                        style=disnake.TextInputStyle.short,
                        max_length=50,
                    ),
                    disnake.ui.TextInput(
                        label="О себе",
                        placeholder="Напишите о себе!",
                        custom_id="О себе:",
                        style=disnake.TextInputStyle.paragraph,
                        max_length=4000,
                    )
                ]
                await inter.response.send_modal(modal=disnake.ui.Modal(
                    title="Заявление на админку!",
                    custom_id="new_admin",
                    components=components,
                ))

    @commands.Cog.listener()
    async def on_modal_submit(self, modal: disnake.ui.Modal):
        match modal.custom_id:
            case "new_admin":
                embed = disnake.Embed(description = f"{modal.user} хочет получить админку на этом сервере ({modal.guild}) вот его заявка:")
                embed.add_field(
                    name = "Имя",
                    value = modal.components.custom_id["Имя:"],
                    inline = False,
                )
                embed.add_field(
                    name = "Фамилия",
                    value = modal.components.custom_id["Фамилия:"],
                    inline = False,
                )
                embed.add_field(
                    name = "Возраст",
                    value = modal.components.custom_id["Возраст:"],
                    inline = False,
                )
                embed.add_field(
                    name = "О себе",
                    value = modal.components.custom_id["О себе:"],
                    inline = False,
                )
                await (await DS_Servers().admin_channel(guild_id = modal.guild.id)).send(embed = embed)
                print(modal)




def setup(bot):
    bot.add_cog(NewAdmin (bot))
