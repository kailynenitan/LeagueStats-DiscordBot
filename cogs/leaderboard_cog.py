import asyncio
import discord
from discord.ext import commands

class LeaderboardCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def insert_game(self, ctx):
        sql_statement = (
            'INSERT INTO game_table (timestamp)'
            'VALUES (?);'
        )
        params = (sqlite3.datetime('now', 'localtime'),)
        self.db_handler.execute_query(sql_statement, params)
