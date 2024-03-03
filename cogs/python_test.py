import disnake
from disnake.ext import commands
import random
from icecream import ic

from datab.ORM import DS_Users



class podtverzhd(disnake.ui.View):
    def __init__(self):
        super().__init__()
    @disnake.ui.button(label='Подтвердить отправку', style=disnake.ButtonStyle.green, emoji='✅')
    async def question_1(self, button: disnake.ui.Button, interaction: disnake.CmdInteraction):
        await interaction.response.send_message('Отправка подтверждена!', ephemeral=True)
        self.stop()
    @disnake.ui.button(label='Отменить отпрвку', style=disnake.ButtonStyle.red, emoji='❌')
    async def question_2(self, button: disnake.ui.Button, interaction: disnake.CmdInteraction):
        await interaction.response.send_message('Отправка отменена', ephemeral=True)
        self.stop()
    @disnake.ui.button(label='Отменить отпрвку', style=disnake.ButtonStyle.blurple, emoji='❌')
    async def question_3(self, button: disnake.ui.Button, interaction: disnake.CmdInteraction):
        await interaction.response.send_message('Отправка отменена', ephemeral=True)
        self.stop()

    @disnake.ui.button(label = "Закрыть", custom_id = "esc")
    async def esc_discord(self, ctx):
        print("Работает")
        await ctx.message.delete()



class Python_test(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot



    
    @commands.Cog.listener() 
    async def on_ready (self): 
        print(f"Бот {self.bot.user} использует ког {__name__}")



    @commands.slash_command(
        name = 'тест_по_python'
    )
    async def python_test_setup_ds(self, ctx):
        print(ctx.author)
        print(ctx.author.id)
        ic(ctx.author.display_name)
        if (await DS_Users().ds_user_poverka_new_user(id_ds = ctx.author.id)) is None:
            await DS_Users().ds_users_edit_all_newuser(id = ctx.author.id, pofil_name = await DS_Users().ds_users_name(ctx = ctx), user_name = ctx.author.name)
        warning, text, access = await DS_Users().ds_users_proba_and_premium_test_python(user_id = ctx.author.id)
        view_1 = disnake.ui.View()
        if access:
            if warning:
                view_1.add_item(disnake.ui.Button(label = "Да", custom_id = "python_test_yes")).add_item(disnake.ui.Button(label = "Закрыть", custom_id = "esc"))
                await ctx.response.send_message(f"{text}\nВы действительно хотите потратить одну попытку сейчас?", view = view_1, ephemeral=True)
            else:
                view_1.add_item(disnake.ui.Button(label = "Лёгкий", custom_id = "easy_python_test")).add_item(disnake.ui.Button(label = "Средний", custom_id = "medium_python_test")).add_item(disnake.ui.Button(label = "Сложный", custom_id = "hard_python_test")).add_item(disnake.ui.Button(label = "Закрыть", custom_id = "esc"))
                await ctx.response.send_message(f"Если хотите пройти тест по python, то выбирите уровень сложности или закрыть если передумали:", view = view_1, ephemeral=True)
        else:
            view_1.add_item(disnake.ui.Button(label = "Закрыть", custom_id = "esc"))
            await ctx.response.send_message("У вас закончились попытки и нет премиума!", view = view_1, ephemeral=True)


    @commands.Cog.listener()
    async def on_button_click(self, interaction: disnake.Interaction):
        if interaction.data.custom_id == 'esc':
            message = interaction.message
            print(message)
            try:
                await message.delete()
            except:
                channel = self.bot.get_channel(interaction.message.channel.id)
                message_1 = await channel.fetch_message(interaction.message.id)
                print(f"{message_1} удаление")
                await message_1.delete()








    """
    async def generator_question_python_ds(self, ctx):
        count_question = ...  # Calculate or retrieve question count
        used_questions = ...  # Get list of used question IDs

        while True:
            random_question = random.randint(0, count_question - 1)
            if count_question < len(used_questions) or str(random_question) not in used_questions:
                break

        # Replace with equivalent logic from `questions_on_test_python`
        answer_question = ...  # Get question content and answer choices

        answer = answer_question.copy()[1:]
        random.shuffle(answer)

        buttons = [
            disnake.ui.Button(label=p, custom_id=f"not_enter_questions_{python_test}_test_python" if p is i else f"enter_questions_{python_test}_test_python")
            for i, p in enumerate(answer)
        ]

        view = disnake.ui.View(children=buttons)
        view.add_item(disnake.ui.Button(label="Close", custom_id="esc"))

        # Track user progress and question number (replace with appropriate logic)
        progress = ...
        question_number = ...

        await ctx.send(f"{progress}\nQuestion #{question_number + 1}\n{answer_question[0]}", view=view)
    """



def setup(bot: commands.Bot):
    bot.add_cog(Python_test(bot))