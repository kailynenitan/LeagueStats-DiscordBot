import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

'''@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if len(message.attachments) > 0:
        await message.channel.send('Attachment detected')

'''


bot = commands.Bot(command_prefix='$', intents=intents)

@bot.command()
async def test(ctx):
    await ctx.send('bot command works')

client.run(os.getenv("BOT_TOKEN"))

