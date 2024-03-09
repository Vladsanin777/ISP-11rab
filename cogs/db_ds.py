import disnake
from disnake.ext import commands
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
        


def setup(bot: commands.Bot):
    bot.add_cog(DB_DS(bot))