import asyncio
import discord
import os
import numpy as np
import sqlite3
from concurrent.futures import ProcessPoolExecutor
from discord.ext import commands

import config
from cogs.ocr_handler import ImageReader

class StatsCog(commands.Cog):
    """
    Holds commands that will insert match history data into the SQL database
    """
    
    def __init__(self, bot):
        self.bot = bot
    

    def insert_match(
        self,
        username: str,
        kills: int, deaths: int, assists: int,
        cs: int,
        gold: int,
        result: str
    ):
        pass
        '''
        purpose: insert all data from screenshot

        gameID = new row in game_table

        for every player in screenshot:
            IF player is not in player_table:
                add player to player_table
            
            make new row in game_player_table
        '''


    @commands.command(name='read_image')
    async def insert_screenshot(self, ctx):
        '''
        Update the SQL database from a screenshot provided by the user

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
        
        image_bytes = await attachment_list[0].read()
        text_reader = ImageReader(image_bytes)
       
        '''
        text = text_reader.read_region('p1')
        for stat in text:
            await ctx.send(stat)
        '''

        profile_cog = self.bot.get_cog('ProfileCog')
        if (profile_cog is None):
            await ctx.send('ERR: Could not load profile_cog')
            return

        game_cog = self.bot.get_cog('GameCog')
        if (game_cog is None):
            await ctx.send('ERR: Could not load game_cog')
            return

        await game_cog.insert_game()
        for x in range(1, 11):
            text = text_reader.read_region(f'p{x}')
            if text:
                # await ctx.send(text)
                league_username = text[0]
                kills = text[1]
                deaths = text[2]
                assists = text[3]
                cs = text[4]
                gold = text[5]

                await profile_cog.insert_player(league_username)
        return
