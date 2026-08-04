import asyncio
import discord
import os
import sqlite3
from concurrent.futures import ProcessPoolExecutor
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path

import config
from databasehandler import Databasehandler
from cogs.leaderboard_cog import LeaderboardCog
from cogs.profile_cog import ProfileCog
from cogs.stats_cog import StatsCog


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
        self.db_handler = None

    async def close(self):
        self.executor.shutdown()
        self.db_handler.close()
        await super().close()
        
    
    async def setup_hook(self):
        await self.add_cog(LeaderboardCog(self))
        await self.add_cog(ProfileCog(self))
        await self.add_cog(StatsCog(self))

        self.db_handler = Databasehandler()
        self.db_handler.create_tables()        

        print(f'Logged in as {self.user}')


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
