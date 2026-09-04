import asyncio
import discord
import os
import numpy as np
import sqlite3
from concurrent.futures import ProcessPoolExecutor
from discord.ext import commands

from cogs.ocr_handler import ImageReader
from cogs.verify_data_view import VerifyDataView


"""
Holds commands that will insert match history data into the SQL database
"""
class ImageCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    

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

        gameID = await self.bot.game_dao.insert_game()

        # Read bytes from screenshot so ImageReader can interact
        # with the photo wihtout an open connection to the image.
        image_bytes = await attachment_list[0].read()
        img_reader = ImageReader(image_bytes)

        game_result = img_reader.read_region('game_result')[0].lower()
        if ((game_result == 'victory') or (game_result.startswith('v'))):
            game_result = 'win'
        else:
            game_result = 'loss'
        
        # Gather all the raw data from the OCR into match_data as a dictionary for each player
        match_data = []
        for player_num in range(1, 11):
            stats = img_reader.read_region(f'p{player_num}')
            if (not stats):
                await ctx.send('ERR: Unable to read stats')
                continue

            # The value of game_result corresponds to the status of the players
            # shown in the team listed in the top half of the screenshot. So, all
            # players in the bottom half must be the opposite game_result
            player_result = game_result if player_num <= 5 else ('loss' if game_result == 'win' else 'win')

            data_dict = {
                'league_username':  stats[0] if len(stats) > 0 else None,
                'kills':            stats[1] if len(stats) > 1 else None,
                'deaths':           stats[2] if len(stats) > 2 else None,
                'assists':          stats[3] if len(stats) > 3 else None,
                'cs':               stats[4] if len(stats) > 4 else None,
                'gold':             stats[5] if len(stats) > 5 else None,
                'result':           player_result
            }
            match_data.append(data_dict)

        match_data_copy = [dict(m) for m in match_data]
        view = VerifyDataView(self.bot, gameID, match_data_copy, authorID = ctx.author.id)
        embed = view.create_embed()
        await ctx.send(embed=embed, view=view)

        return
