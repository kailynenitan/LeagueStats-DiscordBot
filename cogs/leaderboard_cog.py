import asyncio
import discord
from discord.ext import commands

class LeaderboardCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

