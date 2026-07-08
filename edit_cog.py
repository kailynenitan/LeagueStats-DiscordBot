import asyncio
import cv2
import discord
import os
from concurrent.futures import ProcessPoolExecutor
from discord.ext import commands

import config
import reader


# WIP
def update_database(arg):
    if not os.path.exists(config.IMG_PATH):
        return None

    # Create a resized threshold image with black text on a white background
    img = cv2.imread(config.IMG_NAME)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    '''    
    denoised = cv2.GaussianBlur(resized, (3, 3), 0)
    _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    inverted = cv2.bitwise_not(thresh)
    
    kernel = np.ones((2, 2), np.uint8)
    cleaned = cv2.morphologyEx(inverted, cv2.MORPH_CLOSE, kernel, iterations=1)
    '''
    
    '''
    cv2.imshow('processed img', cleaned)
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

    @commands.command()
    async def update(self, ctx, attachment: discord.Attachment,  arg='No arg given'):
        # Update the SQL database from a screenshot provided by the user
        
        await attachment.save(config.IMG_PATH)
        await ctx.send('Testing easyocr image reading...\n')

        loop = asyncio.get_running_loop()
        img_text = await loop.run_in_executor(self.bot.executor, update_database, arg)

        await ctx.send(img_text)
        await ctx.send('Test complete!')

        os.remove(config.IMG_NAME)
