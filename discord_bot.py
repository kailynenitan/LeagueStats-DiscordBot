import asyncio
import discord
import os
import sqlite3
from concurrent.futures import ProcessPoolExecutor
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path

import config
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
        self.db_handler = DatabaseHandler()

    async def close(self):
        self.executor.shutdown()
        await super().close()
    
    async def setup_hook(self):
        await self.add_cog(LeaderboardCog(self))
        await self.add_cog(ProfileCog(self))
        await self.add_cog(StatsCog(self))

        self.db_handler.initialize_db()

        print(f'Logged in as {self.user}')
'''
    async def on_ready(self):
        # Create directory and database files
        db_folder = Path(config.DB_FOLDER)
        db_file = db_folder / config.DB_FILE
        db_folder.mkdir(parents=True, exist_ok=True)

        # Create tables in database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        conn.execute('PRAGMA foreign_keys=ON;')

        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS game_table (
                    gameID INTEGER PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    mvp INTEGER,
                    ace INTEGER,
                    FOREIGN KEY(mvp) REFERENCES player_table(playerID),
                    FOREIGN KEY(ace) REFERENCES player_table(playerID)
            );""")
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS player_table (
                    playerID INTEGER PRIMARY KEY,
                    league_username TEXT NOT NULL UNIQUE,
                    discord_username TEXT,
                    nickname TEXT
            );""")
            
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
                    PRIMARY KEY(gameID, playerID),
                    FOREIGN KEY(gameID) REFERENCES game_table(gameID),
                    FOREIGN KEY(playerID) REFERENCES player_table(playerID)
            );""")
            conn.commit()
            print(f'Database initialized at: {db_file.resolve()}')
        except sqlite3.Error as e:
            print(f'Database init failed: {e}')
        finally:
            conn.close()
'''


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
