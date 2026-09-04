import asyncio
import discord
import os
import sqlite3
from concurrent.futures import ProcessPoolExecutor
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path

from db_handler.database_handler import DatabaseHandler
from db_handler.account_dao import AccountDAO
from db_handler.game_dao import GameDAO
from db_handler.performance_history_dao import PerformanceHistoryDAO
from db_handler.player_dao import PlayerDAO

from cogs.image_cog import ImageCog
from cogs.leaderboard_cog import LeaderboardCommands
from cogs.player_cog import PlayerCommands

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

        self.db_handler = DatabaseHandler()
        self.account_dao = AccountDAO(self.db_handler)
        self.game_dao = GameDAO(self.db_handler)
        self.perf_history_dao = PerformanceHistoryDAO(self.db_handler)
        self.player_dao = PlayerDAO(self.db_handler)

    async def close(self):
        self.executor.shutdown()
        self.db_handler.close()
        await super().close()
        
    
    async def setup_hook(self):
        await self.add_cog(ImageCog(self))
        await self.add_cog(PlayerCommands(self))
        await self.add_cog(LeaderboardCommands(self))

        self.db_handler.create_tables()
        await self.player_dao.insert_player('UNASSIGNED', 'UNASSIGNED')

        print(f'Logged in as {self.user}')

    async def on_command_error(self, ctx, error):
        await ctx.send(f'ERR: {type(error).__name__}:\n{error}')

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
