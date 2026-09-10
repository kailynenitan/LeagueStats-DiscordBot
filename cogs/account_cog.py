from cogs.views.player_ui import *
from discord.ext import commands

class AccountCommands(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot
