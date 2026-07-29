import discord
import sqlite3
from discord.ext import commands
from pathlib import Path

import config

# WIP
class GetCog(commands.Cog):
    '''  
    Holds commands to fetch information from SQL database
    '''
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def get_player_names(self, ctx, arg):
        # Print all names associated with a player
        
        db_folder = Path(config.DB_FOLDER)
        db_file = db_folder / config.DB_FILE
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()

        try:
            cur.execute(
                'SELECT * FROM player_table WHERE league_username = ?;',
                (arg,)
            )

            output = cur.fetchall()
            for row in output:
                await ctx.send(row)
            
            conn.commit()
        except sqlite3.Error as e:
            print(f'Database SELECT failed: {e}')
        finally:
            conn.close()

        return
