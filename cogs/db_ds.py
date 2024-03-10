import disnake
from disnake.ext import commands
from disnake import TextInputStyle
import random
from icecream import ic
import element
from datab.ORM import DS_Users





class DB_DS(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot



    
    @commands.Cog.listener() 
    async def on_ready (self): 
        print(f"Бот {self.bot.user} использует ког {__name__}")

    @commands.command(
        name = 'n'
    )
    async def n(self, ctx):
        await ctx.message.delete()
        view_1 = disnake.ui.View()
        view_1.add_item(disnake.ui.Button(label = "Закрыть", custom_id = "esc"))
        if ctx.author.id == 997495611978960957:
            await DS_Users().user_null(user_id = ctx.author.id)
            await ctx.send("Ваш акаунт обнулён!", view = view_1)
        else: await ctx.send("Снос акаунта не возможен!\nПотому что вы не являетесь тестировщиком и разработчиком бота!",  view = view_1)

    @commands.slash_command(name = "promo")
    async def promo(self, ctx, pashword):
        view_1 = disnake.ui.View()
        view_1.add_item(disnake.ui.Button(label = "Закрыть", custom_id = "esc"))
        if pashword == element.dover_isp.DoverISP().tg_enter_class_pashword:
            await ctx.send(f"Вы активировали перемиум на всё и {await DS_Users().promo_all_ds_bd(ctx.author.id)}", view = view_1)
        else:
            await ctx.send(f"Вы ввели не существующий промокод!", view = view_1)

    @commands.slash_command(name = "name")
    async def name(self, inter, new_name = None, display_names = commands.Param(choices = ["Обращаться по профилю discord", "Нет, называй меня так как я скажу"], default = "Нет, называй меня так как я скажу")):
        if display_names == "Нет, называй меня так как я скажу":
            if new_name is None:
                # Детали модального окна и его компонентов
                components = [
                    disnake.ui.TextInput(
                        label="Новое имя",
                        placeholder="Введите как к вам обращаться! Или 0.",
                        custom_id="Новое имя:",
                        style=disnake.TextInputStyle.short,
                        max_length=50,
                    ),
                ]
                await inter.response.send_modal(modal=disnake.ui.Modal(
                    title="Переименование",
                    custom_id="new_name",
                    components=components,
                ))
            else:
                await self.new_name(inter = inter, new_name = new_name, old_name = await DS_Users().ds_users_proba_name(user_id = inter.author.id))
        else:
            await self.new_name(inter = inter, new_name = None, old_name = await DS_Users().ds_users_proba_name(user_id = inter.author.id))
    

    @commands.Cog.listener()
    async def on_modal_submit(self, modal: disnake.ui.Modal):
        if modal.custom_id == "new_name":
            await self.new_name(inter = modal, new_name = modal.text_values['Новое имя:'], old_name = await DS_Users().ds_users_proba_name(user_id = modal.user.id))
            
    async def new_name(self, inter, new_name, old_name):
        await DS_Users().ds_users_edit_name(user_id = inter.author.id, new_name = new_name if new_name != "0" else None)
        embed = disnake.Embed(title="Переименование", colour = disnake.Colour(int("0x3498db", 16)))
        embed.add_field(
            name = "Новое имя",
            value = "Я буду обращаться к тебе по профилю" if new_name is None or new_name == "0" else new_name,
            inline = True,
        )
        embed.add_field(
            name = "Старое имя",
            value = inter.author.display_name if old_name is None else old_name,
            inline = True,
        )
        await inter.response.send_message(embed=embed, ephemeral=True)



def setup(bot: commands.Bot):
    bot.add_cog(DB_DS(bot))