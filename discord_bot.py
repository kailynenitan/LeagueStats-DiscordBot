import asyncio
import discord
import os
import sqlite3
from concurrent.futures import ProcessPoolExecutor
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path

from cogs.database_handler import DatabaseHandler
from cogs.game_dao import GameDAO
from cogs.match_dao import MatchDAO
from cogs.player_dao import PlayerDAO
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

    async def close(self):
        self.executor.shutdown()
        self.get_cog('DatabaseHandler').close()
        await super().close()
        
    
    async def setup_hook(self):
        await self.add_cog(DatabaseHandler(self))
        self.get_cog('DatabaseHandler').create_tables() 

        await self.add_cog(GameDAO(self))
        await self.add_cog(MatchDAO(self))
        await self.add_cog(PlayerDAO(self))
        await self.add_cog(StatsCog(self))

        print(f'Logged in as {self.user}')

    async def on_command_error(self, ctx, error):
        await ctx.send(f'ERR: {type(error).__name__}: {error}')

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
