import asyncio
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# WIP
class GetCog(commands.Cog):
    '''
    Holds commands to fetch information from SQL database
    '''
    
    def __init__(self, bot):
        self.bot = bot

    # SEND ONE WORD FOLLOWING COMMAND CAll BACK TO CHANNEL
    @commands.command()
    async def test(self, ctx, arg="No arg given"):
        await ctx.send(arg)


# WIP
class EditCog(commands.Cog):
    '''
    Holds commands that will update/change the information in SQL database
    '''
    def __init__(self, bot):
        self.bot = bot

    # SAVE AN ATTACHMENT TO THE CURRENT WORKING DIRECTORY
    @commands.command()
    async def upload(self, ctx, attachment: discord.Attachment):
        path = os.path.join(os.getcwd(), 'stats.jpg')
        await attachment.save(path)
        print('Successfully saved attachment')


# WIP
class StatsBot(commands.Bot):
    '''
    A Discord bot that uses screenshots to maintain a local SQL database that holds League of Legends stats

    StatsBot is a subclass of the discord.ext.commands.Bot class
    All commands for this bot are handled by the GetCog and EditCog classes

    All commands for StatsBot begin with '$'
    '''
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='$', intents=intents)

    async def setup_hook(self):
        await self.add_cog(GetCog(self))
        await self.add_cog(EditCog(self))
        print(f'Logged in as {self.user}')



async def main():
    bot = StatsBot()
    async with bot:
        await bot.start(os.getenv("BOT_TOKEN"))

if __name__== "__main__":
    asyncio.run(main())
