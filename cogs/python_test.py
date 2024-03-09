import disnake
from disnake.ext import commands
import random
from icecream import ic

from datab.ORM import DS_Users, PythonTest



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
                await ctx.response.send_message(f"{text}\nВы действительно хотите потратить одну попытку сейчас?", view = view_1)
            else:
                view_1.add_item(disnake.ui.Button(label = "Лёгкий", custom_id = "easy_python_test")).add_item(disnake.ui.Button(label = "Средний", custom_id = "medium_python_test")).add_item(disnake.ui.Button(label = "Сложный", custom_id = "hard_python_test")).add_item(disnake.ui.Button(label = "Закрыть", custom_id = "esc"))
                await ctx.response.send_message(f"Если хотите пройти тест по python, то выбирите уровень сложности или закрыть если передумали:", view = view_1)
        else:
            view_1.add_item(disnake.ui.Button(label = "Закрыть", custom_id = "esc"))
            await ctx.response.send_message("У вас закончились попытки и нет премиума!", view = view_1)


    @commands.Cog.listener()
    async def on_button_click(self, interaction: disnake.Interaction):
        d = interaction.data.custom_id
        match d:
            case 'esc':
                await interaction.message.delete()
            case 'python_test_yes':
                await self.python_test_yes(interaction = interaction)
            case 'easy_python_test' | 'medium_python_test' | 'hard_python_test':
                await self.python_test(interaction = interaction, python_test = d.split("_")[0])
            case 'test_python_pause_not_enter_easy' | 'test_python_pause_not_enter_medium' | 'test_python_pause_not_enter_hard':
                await self.test_python_pause_not_enter(interaction = interaction, python_test = d.split("_")[5])
            case 'test_python_pause_enter_easy' | 'test_python_pause_enter_medium' | 'test_python_pause_enter_hard':
                await self.test_python_pause_enter(interaction = interaction, python_test = d.split("_")[4])
            case 'enter_questions_easy_test_python' | 'enter_questions_medium_test_python' | 'enter_questions_hard_test_python':
                await self.enter_questions_test_python(interaction = interaction, python_test = d.split("_")[2])

    #Выдаёт пользователю результат прохождения лёгкого теста по python или задаёт следующий вопрос
    async def end_test_python(*, interaction, python_test):
        if (await DS_Users().progress_python_test_number(user_id = interaction.author.id, python_test = python_test)) < 10:
            await generator_question_python(interaction=interaction, python_test = python_test)
        else: 
            match python_test:
                case 'easy':
                    ru_python_test = 'ЛЁГКИЙ'
                case 'medium':
                    ru_python_test = 'СРЕДНИЙ'
                case 'hard':
                    ru_python_test = 'СЛОЖНЫЙ'
            print('Работает')
            python_result = f"Вы прошли {ru_python_test} ТЕСТ по Python:\nВаш результат {await DS_Users().enter_answer_python_test_number_chek(user_id = interaction.author.id, python_test = python_test)}/10"
            view_1 = disnake.ui.View()
            view_1.add_item(disnake.ui.Button(label = "Закрыть", custom_id = "esc"))
            await interaction.response.send_message(python_result, view = view_1)
            await DS_Users().all_python_test_delete_null(user_id = interaction.author.id, python_test = python_test)


    async def enter_questions_test_python(self, interaction, python_test):
        await interaction.message.delete()
        await DS_Users().enter_questions_test_python(user_id = interaction.author.id, python_test = python_test)
        await self.end_test_python(interaction = interaction, python_test = python_test)

    async def python_test_yes(interaction):
        await interaction.message.delete()
        view_1 = disnake.ui.View()
        view_1.add_item(disnake.ui.Button(label = "Лёгкий", custom_id = "easy_python_test")).add_item(disnake.ui.Button(label = "Средний", custom_id = "medium_python_test")).add_item(disnake.ui.Button(label = "Сложный", custom_id = "hard_python_test")).add_item(disnake.ui.Button(label = "Закрыть", custom_id = "esc"))
        await interaction.response.send_message(f"Если хотите пройти тест по python, то выбирите уровень сложности или закрыть если передумали:", view = view_1)
        
    async def test_python_pause_not_enter(self, interaction, python_test):
        try: await interaction.message.delete()
        except: pass
        await DS_Users().edit_proba_premium_test_python(user_id = interaction.author.id)
        await DS_Users().all_python_test_delete_null(user_id = interaction.author.id, python_test = python_test)
        await self.generator_question_python(interaction = interaction, python_test = python_test)

    async def test_python_pause_enter(self, interaction, python_test) -> None:
        try: await interaction.message.delete()
        except: pass
        await self.generator_question_python(interaction = interaction, python_test = python_test)

    async def python_test(self, interaction, python_test):
        await interaction.message.delete()
        ic(python_test)
        match python_test:
            case 'easy':
                ru_python_test_1 = 'лёгкое'
                ru_python_test_2 = 'лёгкий'
            case 'medium':
                ru_python_test_1 = 'среднее'
                ru_python_test_2 = 'средний'
            case 'hard':
                ru_python_test_1 = 'сложное'
                ru_python_test_2 = 'сложный'
        if (await DS_Users().testing_an_Python_test(user_id = interaction.author.id, python_test = python_test)) != 0:
            view_1 = disnake.ui.View()
            view_1.add_item(disnake.ui.Button(label = f"Нет, я хочу начать {ru_python_test_2} тест сначала", custom_id = f"test_python_pause_not_enter_{python_test}"))
            view_1.add_item(disnake.ui.Button(label = f"Да, хочу продолжить {ru_python_test_2} тест!", custom_id = f"test_python_pause_enter_{python_test}"))
            view_1.add_item(disnake.ui.Button(label = "Закрыть", custom_id = "esc"))
            await interaction.response.send_message(f"Хотите продолжить {ru_python_test_1} тестирование по Python с сохранением попытки или начать с начало!\n{await DS_Users().progress_python_test(user_id = interaction.author.id, python_test = python_test)}", view = view_1)
        else:
            await DS_Users().edit_proba_premium_test_python(user_id = interaction.author.id)
            await self.test_python_pause_not_enter(interaction = interaction, python_test = python_test)

 
    async def generator_question_python_ds(self, interaction, python_test):
        random_question = None
        count_question = await PythonTest().quantity_str(python_test = python_test)
        spisok_using_question = await DS_Users().spisok_list_answer_python_test_number(user_id = interaction.author.id, python_test = python_test)
        while True:
            random_question = random.randint(0, count_question - 1)
            if count_question < len(spisok_using_question) or str(random_question) not in spisok_using_question:
                break
        answer_question = await PythonTest().questions_on_test_python(number_of_questions = random_question, python_test = python_test)    

        answer = answer_question.copy()[1:]
        random.shuffle(answer)

        buttons = [
            disnake.ui.Button(label=p, custom_id=f"not_enter_questions_{python_test}_test_python" if p is i else f"enter_questions_{python_test}_test_python")
            for i, p in enumerate(answer)
        ]
        ic(buttons)
        view = disnake.ui.View(children=buttons)
        view.add_item(disnake.ui.Button(label="Close", custom_id="esc"))

        await DS_Users().list_answer_python_test_number(user_id = interaction.author.id, number = random_question, python_test = python_test)

        await interaction.response.send_message(f"{await DS_Users().progress_python_test(user_id = interaction.author.id, python_test = python_test)}\nВопрос №{(await DS_Users().answer_python_test_number_chek(user_id = interaction.author.id, python_test = python_test)) + 1}\n{answer_question[0]}", view = view)



def setup(bot: commands.Bot):
    bot.add_cog(Python_test(bot))