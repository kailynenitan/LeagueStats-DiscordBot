import asyncio
import discord
import os
import numpy as np
import sqlite3
from concurrent.futures import ProcessPoolExecutor
from discord.ext import commands
from pathlib import Path

import config
from cogs.reader import ImageReader

class StatsCog(commands.Cog):
    """
    Holds commands that will insert match history data into the SQL database
    """
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='read_image')
    async def editFromImage(self, ctx):
        """
        Update the SQL database from a screenshot provided by the user

        Args:
            ctx: Text command from the user
            attachment: Screenshot image of entire window of League of Legends game match history
        """
        
        attachment_list = ctx.message.attachments
        if not attachment_list:
            await ctx.send('ERR: No attachment.')
            return

        for attachment in attachment_list:
            if not attachment.content_type.startswith('image'):
                await ctx.send('ERR: Wrong attachment type.')
                return
        
        image_bytes = await attachment_list[0].read()
        text_reader = ImageReader(image_bytes)

        text = text_reader.read_region('p1')
        for stat in text:
            await ctx.send(stat)

        return
