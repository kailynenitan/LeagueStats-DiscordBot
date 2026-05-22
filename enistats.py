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

# SEND ONE WORD FOLLOWING COMMAND BACK TO CHANNEL
@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)

# SAVE AN ATTACHMENT TO THE CURRENT WORKING DIRECTORY
@bot.command()
async def upload(ctx, attachment: discord.Attachment):
    path = os.path.join(os.getcwd(), 'stats.jpg')
    await attachment.save(path)
    print('Successfully saved attachment')

bot.run(os.getenv("BOT_TOKEN"))
