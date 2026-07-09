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

    # Create a resized threshold image with black text on a white background
    img = cv2.imread(config.IMG_NAME)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Cover the in-game item icons in the pre-processed image
    resized_height, resized_width = resized.shape[:2]
    (mask_x, mask_y, mask_w, mask_h) = config.DATA_REGIONS['mask_items']
    mask_start = (int(resized_width * mask_x), int(resized_height * mask_y))
    mask_end = (int(resized_width * (mask_x + mask_w)), int(resized_height * (mask_y + mask_h)))
    cv2.rectangle(resized, mask_start, mask_end, (0, 0, 0), -1)
    
    '''
    cv2.imshow('processed img', resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
    
    text_reader = reader.ImageReader()
    result = text_reader.read_region(resized, arg)

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
    async def updateImage(self, ctx, attachment: discord.Attachment,  arg='No arg given'):
        # Update the SQL database from a screenshot provided by the user

        '''
        (async)img = attachment from Discord

        retrieve stats for each user using ocr

        send stats to Discord for confirmation

        update database
        '''

        
        await attachment.save(config.IMG_PATH)
        await ctx.send('Testing easyocr image reading...\n')

        loop = asyncio.get_running_loop()
        img_text = await loop.run_in_executor(self.bot.executor, get_stats, arg)

        await ctx.send(img_text)
        await ctx.send('Test complete!')

        os.remove(config.IMG_NAME)
