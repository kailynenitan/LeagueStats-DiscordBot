import asyncio
import discord
from discord.ext import commands

'''
The commands in this cog are used to test commands and features of other cogs.
All commands in this cog are experimental and not meant for regular bot use.
'''
class TestCog(commands.Cog):
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
