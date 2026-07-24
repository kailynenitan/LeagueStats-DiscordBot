import asyncio
import discord
import os
import sqlite3
from concurrent.futures import ProcessPoolExecutor
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path

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

    async def close(self):
        self.executor.shutdown()
        await super().close()
    
    async def setup_hook(self):
        await self.add_cog(get_cog.GetCog(self))
        await self.add_cog(edit_cog.EditCog(self))

        print(f'Logged in as {self.user}')

    async def on_ready(self):
        # Create directory and database files
        db_folder = Path('data')
        db_file = db_folder / 'league_stats.db'
        db_folder.mkdir(parents=True, exist_ok=True)

        # Create tables in database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        conn.execute("""
            CREATE TABLE IF NOT EXISTS game_player_table (
                gameID INTEGER,
                playerID INTEGER,
                kills INTEGER NOT NULL,
                deaths INTEGER NOT NULL,
                assists INTEGER NOT NULL,
                cs INTEGER NOT NULL,
                gold INTEGER NOT NULL,
                result INTEGER NOT NULL,
                PRIMARY KEY(gameID, playerID)
        );""")
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS game_table (
                gameID INTEGER PRIMARY KEY,
                timestamp TEXT,
                mvp INTEGER,
                ace INTEGER
        );""")
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS player_table (
                playerID INTEGER PRIMARY KEY,
                league_username TEXT NOT NULL UNIQUE,
                discord_username TEXT,
                alt_name TEXT
        );""")

        conn.commit()
        conn.close()
        print(f'Database initialized at: {db_file.resolve()}')
        



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
