import discord
from discord.ext import commands

# WIP
class GetCog(commands.Cog):
    '''  
    Holds commands to fetch information from SQL database
    '''
    
    def __init__(self, bot):
        self.bot = bot
