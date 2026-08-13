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

        profile_cog = self.bot.get_cog('ProfileCog')
        if (profile_cog is None):
            await ctx.send('ERR: Could not load profile_cog')
            return

        '''
        game_cog = self.bot.get_cog('GameCog')
        if (game_cog is None):
            await ctx.send('ERR: Could not load game_cog')
            return
        '''

        # Read bytes from screenshot so ImageReader can interact
        # with the photo wihtout an open connection to the image.
        image_bytes = await attachment_list[0].read()
        img_reader = ImageReader(image_bytes)

        game_result = img_reader.read_region('game_result')[0].lower()
        if ((game_result == 'victory') or (game_result.startswith('v'))):
            game_result = 'win'
        else:
            game_result = 'loss'

        # gameID = await game_cog.insert_game()
        # await ctx.send(str(gameID))

        # Insert stats for each player into game_player_table
        for player_num in range(1, 11):
            
            # The value of game_result corresponds to the status of the players
            # shown in the team listed in the top half of the screenshot. So, all
            # players in the bottom half must be the opposite game_result
            player_result = game_result if player_num <= 5 else ('loss' if game_result == 'win' else 'win')

            stats = img_reader.read_region(f'p{player_num}')
            if (not stats):
                await ctx.send('ERR: Unable to read stats')
                continue
            '''
            if ((not stats) or (not stats[0]) or (not stats[0].strip())):
                continue
            '''

            league_username = stats[0]
            kills, deaths, assists, cs, gold = stats[1:6]

            player_rowID = await profile_cog.insert_player(league_username)
            playerID = (await profile_cog.select_player(league_username=league_username))[0]
            
        return
