import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

@bot.command()
async def upload(ctx, attachment: discord.Attachment):
    #await attachment.save('C:/Users/Kailyn/Desktop/LeagueStats-DiscordBot{stats.jpg}')
    path = os.path.join(os.getcwd(), 'stats.jpg')
    await attachment.save(path)
    await ctx.send(f'You uploaded <{attachment.url}>')

bot.run(os.getenv("BOT_TOKEN"))
