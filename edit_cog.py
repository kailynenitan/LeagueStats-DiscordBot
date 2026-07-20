import asyncio
import cv2
import discord
import os
import numpy as np
import sqlite3
from concurrent.futures import ProcessPoolExecutor
from discord.ext import commands

import config
import reader

    
    
# WIP
def get_stats(arg):    
    if not os.path.exists(config.IMG_PATH):
        return None

    # Create a resized image with black text on a white background
    img = cv2.imread(config.IMG_NAME)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    processed = cv2.bitwise_not(resized)
    
    text_reader = reader.ImageReader()
    result = text_reader.read_region(processed, arg)
    
    text = ''
    for r in result:
        text = text + r + '\n'
    
    return text


# WIP
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

        await attachment_list[0].save(config.IMG_PATH)
        
        loop = asyncio.get_running_loop()
        img_text = await loop.run_in_executor(self.bot.executor, get_stats, arg)

        if img_text == '':
            await ctx.send('No text read')
        else:
            await ctx.send(img_text)

        os.remove(config.IMG_NAME)
        return


    @commands.command()
    async def insert_db(self, ctx):
        conn = sqlite3.connect('test_database.db')
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS test_table.')
