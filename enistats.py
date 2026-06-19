import asyncio
import cv2
import discord
import numpy as np
import os
import pytesseract
from concurrent.futures import ProcessPoolExecutor
from discord.ext import commands
from dotenv import load_dotenv
from PIL import Image

IMG_NAME = 'stats.jpg'
IMG_PATH = os.path.join(os.getcwd(), IMG_NAME)
REGIONS = {
    't1_unames': (326, 619, 360, 380),
    't1_levels': (176, 620, 65, 390),
    't1_kda': (1186, 625, 275, 390),
    't1_cs': (1494, 619, 120, 390),
    't1_gold': (1635, 619, 200, 400),
    
    't2_unames': (327, 1110, 360, 380),
    't2_levels': (178, 1110, 65, 390),
    't2_kda': (1188, 1115, 275, 390),
    't2_cs': (1491, 1109, 120, 390),
    't2_gold': (1634, 1111, 200, 400),
    
    'game_result': (203, 220, 248, 74)
}

load_dotenv()
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract'



# WIP
def read_image():
    # Return a string of text from IMG_PATH

    if not os.path.exists(IMG_PATH):
        return None

    # Create a resized threshold image with black text on a white background
    img = cv2.imread(IMG_NAME)
    gray = cv2.bitwise_not(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
    resized = cv2.resize(gray, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    
    cv2.imshow('current image', resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    text = pytesseract.image_to_string(resized)
    return text




# WIP
class GetCog(commands.Cog):
    '''
    Holds commands to fetch information from SQL database
    '''
    
    def __init__(self, bot):
        self.bot = bot

    # SEND ONE WORD FOLLOWING COMMAND CAll BACK TO CHANNEL
    @commands.command()
    async def test(self, ctx, arg="No arg given"):
        await ctx.send(arg)


# WIP
class EditCog(commands.Cog):
    '''
    Holds commands that will update/change the information in SQL database
    '''
    def __init__(self, bot):
        self.bot = bot

    # SAVE AN ATTACHMENT TO THE CURRENT WORKING DIRECTORY
    # DELETE LATER
    @commands.command()
    async def upload(self, ctx, attachment: discord.Attachment):
        await attachment.save(IMG_PATH)
        print('Successfully saved attachment')

    @commands.command()
    async def update(self, ctx, attachment: discord.Attachment):
        # Update the SQL database from a screenshot provided by the user

        await attachment.save(IMG_PATH)

        await ctx.send('Testing pytesseract image reading...\n\n')
        #await ctx.send(pytesseract.image_to_string(Image.open(IMG_NAME)))
        loop = asyncio.get_running_loop()
        img_text = await loop.run_in_executor(self.bot.executor, read_image)
        await ctx.send(img_text)
        await ctx.send('Complete!')


# WIP
class StatsBot(commands.Bot):
    '''
    A Discord bot that uses screenshots to maintain a local SQL database that holds League of Legends stats

    StatsBot is a subclass of the discord.ext.commands.Bot class
    All commands for this bot are handled by the GetCog and EditCog classes

    All commands for StatsBot begin with '$'
    '''
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='$', intents=intents)
        self.executor = ProcessPoolExecutor()

    async def setup_hook(self):
        await self.add_cog(GetCog(self))
        await self.add_cog(EditCog(self))
        print(f'Logged in as {self.user}')

    async def close(self):
        self.executor.shutdown()
        await super().close()




async def main():
    bot = StatsBot()
    async with bot:
        try:
            await bot.start(os.getenv("BOT_TOKEN"))
        except KeyboardInterrupt:
            print('Shutting down...')
        finally:
            if not bot.is_closed():
                await bot.close()

if __name__== "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
