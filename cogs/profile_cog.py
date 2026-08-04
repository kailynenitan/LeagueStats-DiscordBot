import discord
import sqlite3
from discord.ext import commands

import config

# WIP
class ProfileCog(commands.Cog):
    """ 
    Holds commands to handle individual player data
    """
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='add_player')
    async def insert_player(self, league_username, discord_username=None, nickname=None):
        
        sql_statement = (
            'INSERT INTO player_table (league_username)'
            'VALUES (?);'
        )
        params = (league_username,)

        if (discord_username is not None):
            sql_statement = (
                'INSERT INTO player_table (league_username, discord_username);'
                'VALUES (?, ?);'
            )
            params = (league_username, discord_username)

        if (nickname is not None):
            sql_statement = (
                'INSERT INTO player_table (league_username, nickname);'
                'VALUES (?, ?);'
            )
            params = (league_username, nickname)


        if (discord_username is not None and nickname is not None):
            sql_statement = (
                'INSERT INTO player_table (league_username, discord_username, nickname);'
                'VALUES (?, ?, ?);'
            )
            params = (league_username, discord_username, nickname)

        self.db_handler.execute_query(sql_statement, params)

        return


    @commands.command(name='print_names')
    async def select_all_names(self, ctx, arg):
        # Print all names associated with a player
        
        sql_statement = (
            'SELECT * FROM player_table WHERE league_username = ?;'
        )
        params = (arg,)

        row = self.db_handler.execute_query(sql_statement, params, 1)
        await ctx.send(f'All names associated with {arg}:\n')
        await ctx.send(
            f'League username: {row[0]}\n'
            f'Discord username: {row[1]}\n'
            f'Nickname: {row[2]}'
        )
        return
