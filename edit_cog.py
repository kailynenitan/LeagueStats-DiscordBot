import asyncio
import cv2
import discord
import os
import numpy as np
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
    Holds commands that will update/change the information in SQL database
    '''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='read_image')
    async def editFromImage(self, ctx, attachment: discord.Attachment, arg='No arg given'):
        # Update the SQL database from a screenshot provided by the user
        
        await attachment.save(config.IMG_PATH)
        await ctx.send('Testing easyocr image reading...\n')

        loop = asyncio.get_running_loop()
        img_text = await loop.run_in_executor(self.bot.executor, get_stats, arg)

        if img_text == '':
            await ctx.send('No text read')
        else:
            await ctx.send(img_text)
        await ctx.send('Test complete!')

        os.remove(config.IMG_NAME)
