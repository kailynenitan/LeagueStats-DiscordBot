import asyncio
import cv2
import discord
import os
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from discord.ext import commands

import config
import reader


def mask_region(img, region):
    # Cover an area of img specified by region with a black rectangle
    img_height, img_width = img.shape[:2]
    (x, y, w, h) = config.REGIONS[region]
    mask_start = (int(img_width * x), int(img_height * y))
    mask_end = (int(img_width * (x + w)), int(img_height * (y + h)))
    cv2.rectangle(img, mask_start, mask_end, (0, 0, 0), -1)
    
# WIP
def get_stats(arg):    
    if not os.path.exists(config.IMG_PATH):
        return None

    # Create a resized threshold image with black text on a white background
    img = cv2.imread(config.IMG_NAME)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    mask_region(resized, 'mask_items')
    mask_region(resized, 'mask_slash1')
    mask_region(resized, 'mask_slash2')

    bitwise_not = cv2.bitwise_not(resized)

    '''
    cv2.imshow('processed img', bitwise_not)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
    
    text_reader = reader.ImageReader()
    result = text_reader.read_region(bitwise_not, arg)

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
