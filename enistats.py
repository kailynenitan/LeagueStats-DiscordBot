import asyncio
import discord
import os
from concurrent.futures import ProcessPoolExecutor
from discord.ext import commands
from dotenv import load_dotenv

import config
import edit_cog
import get_cog
import test_cog

    
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
        self.executor = ProcessPoolExecutor()

    async def setup_hook(self):
        await self.add_cog(get_cog.GetCog(self))
        await self.add_cog(edit_cog.EditCog(self))
        # await self.add_cog(test_cog.TestCog(self))
        print(f'Logged in as {self.user}')
    
    async def close(self):
        self.executor.shutdown()
        await super().close()



async def main():
    load_dotenv()
    
    bot = StatsBot()
    async with bot:
        try:
            await bot.start(os.getenv("BOT_TOKEN"))
        except KeyboardInterrupt:
            print('\n[Ctrl+C] detected. Shutting down...')
        finally:
            if not bot.is_closed():
                await bot.close()

if __name__== "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
