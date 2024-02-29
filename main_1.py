import disnake
from disnake.ext import commands
import asyncio

bot = commands.Bot()


@bot.event
async def on_ready():
    print("Бот готов!")


@bot.slash_command(name="user")
async def user(inter):
    await inter.response.send_message(f"Ваш тег: {inter.author}\nВаш ID: {inter.author.id}")

async def main():
    bot.run("MTIxMjg1NDQwODYxMDU4NjY1NA.Gpcedg.Z849AiQTWCRo-G9IrDV0FWWX4jZsSnZ3kPwIzQ")
asyncio.run(main())
