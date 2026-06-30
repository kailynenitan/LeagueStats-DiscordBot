import asyncio
import cv2
import discord
import easyocr
import numpy as np
import os
import string
from concurrent.futures import ProcessPoolExecutor
from discord.ext import commands
from dotenv import load_dotenv
from PIL import Image

IMG_NAME = 'stats.jpg'
IMG_PATH = os.path.join(os.getcwd(), IMG_NAME)

load_dotenv()
reader = easyocr.Reader(['en'], gpu=False)

# Areas of stats proportional to match history screenshots in pixels
# The format of each tuple is (x-coord, y-coord, width, height)
DATA_REGIONS = {
    'unames':       (0.11145, 0.37507, 0.12307, 0.53841),
    'levels':       (0.06017, 0.37507, 0.02222, 0.53841),
    'kills':        (0.41000, 0.37507, 0.02051, 0.53841),
    'deaths':       (0.44000, 0.37507, 0.02051, 0.53841),
    'assists':      (0.46871, 0.37507, 0.02051, 0.53841),
    'cs':           (0.51076, 0.37507, 0.04102, 0.53841),
    'gold':         (0.55897, 0.37507, 0.06837, 0.53841),
    'game_result':  (0.06940, 0.13309, 0.08547, 0.04537),

    't1_unames':    (0.11145, 0.37507, 0.12307, 0.24198),
    't1_levels':    (0.06017, 0.37507, 0.02222, 0.24198),
    't1_kills':     (0.41000, 0.37507, 0.02051, 0.24198),
    't1_deaths':    (0.44000, 0.37507, 0.02051, 0.24198),
    't1_assists':   (0.46871, 0.37507, 0.02051, 0.24198),
    't1_cs':        (0.51076, 0.37507, 0.04102, 0.24198),
    't1_gold':      (0.55897, 0.37507, 0.06837, 0.24198),

    't2_unames':    (0.11145, 0.67150, 0.12307, 0.24198),
    't2_levels':    (0.06017, 0.67150, 0.02222, 0.24198),
    't2_kills':     (0.41000, 0.67150, 0.02051, 0.24198),
    't2_deaths':    (0.44000, 0.67150, 0.02051, 0.24198),
    't2_assists':   (0.46871, 0.67150, 0.02051, 0.24198),
    't2_cs':        (0.51076, 0.67150, 0.04102, 0.24198),
    't2_gold':      (0.55897, 0.67150, 0.06837, 0.24198)
}


# WIP
def read_region(img, arg):
    # Read the text in a specified region of an image

    region = DATA_REGIONS[arg]
    img_height, img_width = img.shape[:2]
    x = int(region[0] * img_width)
    y = int(region[1] * img_height)
    w = int(region[2] * img_width)
    h = int(region[3] * img_height)

    crop = img[y:y + h, x:x + w]

    cv2.imshow(arg, crop)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return reader.readtext(crop, detail=0, paragraph=False)
    
    

# WIP
def update_database(arg):
    if not os.path.exists(IMG_PATH):
        return None

    # Create a resized threshold image with black text on a white background
    img = cv2.imread(IMG_NAME)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    
    
    denoised = cv2.GaussianBlur(resized, (3, 3), 0)
    _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    inverted = cv2.bitwise_not(thresh)
    
    kernel = np.ones((2, 2), np.uint8)
    cleaned = cv2.morphologyEx(inverted, cv2.MORPH_CLOSE, kernel, iterations=1)

    cv2.imshow('processed img', cleaned)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    result = read_region(cleaned, arg)

    text = ''
    for r in result:
        text = text + r + '\n'
        
    return text



class TestCog(commands.Cog):
    '''
    The commands in this cog are used to test commands and features of other cogs.
    All commands in this cog are experimental and not meant for regular bot use.
    '''

    def __init__(self, bot):
        self.bot = bot

    # SEND ONE WORD FOLLOWING COMMAND CAll BACK TO CHANNEL
    @commands.command()
    async def test(self, ctx, arg="No arg given"):
        await ctx.send(arg)

    @commands.command()
    async def getSize(self, ctx, attachment: discord.Attachment):
        await ctx.send('Getting image size...')
        # await ctx.send('height: ' + str(attachment.height) + '\twidth: ' + str(attachment.width))
        '''
        await attachment.save(IMG_PATH)
        img = Image.open(IMG_PATH).size
        w, h = img.size
        await ctx.send(f'width: {w}     height: {h}')
        await os.remove('stats.jpg')
        '''

# WIP
class GetCog(commands.Cog):
    '''  
    Holds commands to fetch information from SQL database
    '''
    
    def __init__(self, bot):
        self.bot = bot


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
        
        await attachment.save(IMG_PATH)
        await ctx.send('Testing easyocr image reading...\n')
        # await ctx.send('Arg provided is: ' + arg)

        loop = asyncio.get_running_loop()
        img_text = await loop.run_in_executor(self.bot.executor, update_database, arg)

        await ctx.send(img_text)
        await ctx.send('Test complete!')

        await os.remove('stats.jpg')


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
        # await self.add_cog(TestCog(self))
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
            print('\n[Ctrl+C] detected. Shutting down...')
        finally:
            if not bot.is_closed():
                await bot.close()

if __name__== "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
