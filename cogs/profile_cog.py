import discord
import sqlite3
from discord.ext import commands
from pathlib import Path

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
        db_folder = Path(config.DB_FOLDER)
        db_file = db_folder / config.DB_FILE
        
        sql_statement = (
                'INSERT INTO player_table (league_username)'
                'VALUES (?);',
                (league_username,)
        )

        if (discord_username is not None):
            sql_statement = (
                'INSERT INTO player_table (league_username, discord_username);'
                'VALUES (?, ?);',
                (league_username, discord_username)
            )

        if (name is not None):
            sql_statement = (
                'INSERT INTO player_table (league_username, discord_username, nickname);'
                'VALUES (?, ?, ?);',
                (league_username, discord_username, nickname)
            )

        try:
            conn = sqlite3.connect(db_file)
            cur = conn.cursor()
            conn.execute(sql_statement)
            conn.commit()
        except sqlite3.Error as e:
            print(f'Database insert failed: {e}')
        finally:   
            conn.close()

        return

    @commands.command()
    async def get_player_names(self, ctx, arg):
        # Print all names associated with a player
        
        db_folder = Path(config.DB_FOLDER)
        db_file = db_folder / config.DB_FILE
        
        sql_statement = (
            'SELECT * FROM player_table WHERE league_username = ?;',
            (arg,)
        )

        try:
            conn = sqlite3.connect(db_file)
            cur = conn.cursor()
            cur.execute(sql_statement)
            
            output = cur.fetchall()
            for row in output:
                await ctx.send(row)
            
            conn.commit()
        except sqlite3.Error as e:
            print(f'Database SELECT failed: {e}')
        finally:
            conn.close()

        return
