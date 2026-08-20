import asyncio
import discord
from discord.ext import commands

class LeaderboardCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def select_player_stat(self, ctx):
        pass
        # get avg of a specified stat per game for a specified player

    async def select_stat_leaderboard(self, ctx):
        pass
        # get leaderboard of all players for their avgs of a specified stat

    async def select_player_winstreak(self, ctx):
        pass
        # get winstreak of a specified player

    async def select_winstreak_leaderboard(self, ctx):
        pass
        # get leaderboard of all current winstreaks in desc order
