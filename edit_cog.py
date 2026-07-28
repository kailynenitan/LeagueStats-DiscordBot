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


class EditCog(commands.Cog):
    '''
    Holds commands that will edit the information in SQL database
    '''
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='read_image')
    async def editFromImage(self, ctx, arg):
        '''Update the SQL database from a screenshot provided by the user

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
        
        # Save and edit an image to make it easier for the OCR to read the text
        await attachment_list[0].save(config.IMG_PATH)
        text_reader = reader.ImageReadfer()
        processed = text_reader.process_image()
        
        img_text = text_reader.read_region(processed, arg)
    
        if len(img_text) == 0:
            await ctx.send('No text read')
        else:
            await ctx.send(img_text)

        os.remove(config.IMG_NAME)
        return


    @commands.command()
    async def insert_db(self, ctx, arg):
        db_folder = Path(config.DB_FOLDER)
        db_file = db_folder / config.DB_FILE
        await ctx.send(f'path: {db_file}')
        
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        try:
            # Add a new player to the database
            conn.execute(
                'INSERT INTO player_table (league_username) VALUES (?);',
                (arg,)
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f'Database insert failed: {e}')
        finally:   
            conn.close()

        return
