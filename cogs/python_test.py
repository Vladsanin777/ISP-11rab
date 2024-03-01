import disnake
from disnake.ext import commands





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



class PingCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot



    
    @commands.Cog.listener() 
    async def on_ready (self): 
        print(f"Бот {self.bot.user} использует ког {__name__}")



    @commands.slash_command(
        name = 'тест_по_python'
    )
    async def python_test_setup_ds()




def setup(bot: commands.Bot):
    bot.add_cog(PingCommand(bot))