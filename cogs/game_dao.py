import discord
import sqlite3
from datetime import datetime
from discord.ext import commands


# WIP
class GameDAO(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def insert_game(self):
        sql_statement = (
            'INSERT OR IGNORE INTO game_table (timestamp) '
            'VALUES (?);'
        )
        params = (datetime.now(),)
        return self.bot.get_cog('DatabaseHandler').execute_insert(sql_statement, params)

    @commands.command()
    async def select_top_mvp(self, ctx):
        pass
        '''
        sql_statement = get player with highest count of mvps in game_table
        '''

    @commands.command()
    async def select_mvp_list(self, ctx):
        pass
        '''
        sql_statement = get list of all players in descending order of number of mvps
        '''

    @commands.command()
    async def select_mvp_count(self, ctx, arg: str):
        pass
        '''
        sql_statement = get number of mvps of a specified player
        '''

    @commands.command()
    async def select_top_ace(self, ctx):
        pass
        '''
        sql_statement = get player with highest count of aces in game_table
        '''

    @commands.command()
    async def select_ace_list(self, ctx):
        pass
        '''
        sql_statement = get list of all players in descending order of number of aces
        '''

    @commands.command()
    async def select_ace_count(self, ctx, arg: str):
        pass
        '''
        sql_statement = get number of aces of a specified player
        '''

    @commands.command()
    async def select_games(self, ctx, arg='None'):
        pass
        '''
        sql_statement = get games on a specified date
        '''

