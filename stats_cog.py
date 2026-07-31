import asyncio
import discord
import os
import numpy as np
import sqlite3
from concurrent.futures import ProcessPoolExecutor
from discord.ext import commands
from pathlib import Path

import config
import reader


class StatsCog(commands.Cog):
    '''
    Holds commands that will edit the information in SQL database
    '''
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='read_image')
    async def editFromImage(self, ctx, arg):
        '''
        Update the SQL database from a screenshot provided by the user

        Args:
            ctx: Text command from the user
            attachment: Screenshot image of entire window of League of Legends game match history
        '''
        attachment_list = ctx.message.attachments
        if not attachment_list:
            await ctx.send('ERR: No attachment.')
            return

        for attachment in attachment_list:
            if not attachment.content_type.startswith('image'):
                await ctx.send('ERR: Wrong attachment type.')
                return
        
        # Read text from a specific region in image
        image_bytes = await attachment_list[0].read()
        text_reader = reader.ImageReader(image_bytes)
        img_text = text_reader.read_region(arg)
    
        if len(img_text) == 0:
            await ctx.send('No text read')
        else:
            await ctx.send(img_text)

        return


    @commands.command(name='add_player')
    async def insert_player(self, league_username, discord_username=None, name=None):
        db_folder = Path(config.DB_FOLDER)
        db_file = db_folder / config.DB_FILE
        
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        try:
            # Add a new player to the database
            sql_statement = (f'INSERT INTO player_table'
                             f'VALUES {league_username}')
            conn.execute(sql_statement)

            if (discord_username is not None):
                sql_statement = (f'UPDATE player_table'
                                 f'SET discord_username={discord_username}')
                conn.execute(sql_statement)

            if (name is not None):
                sql_statement = (f'UPDATE player_table'
                                 f'SET alt_name={name}')
                conn.execute(sql_statement
                             )
            conn.commit()
        except sqlite3.Error as e:
            print(f'Database insert failed: {e}')
        finally:   
            conn.close()

        return
