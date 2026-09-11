from cogs.views.player_view import *
from discord.ext import commands
from typing import Any


class PlayerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.columns = ['playerID', 'discord_username', 'nickname']

    async def _validate_input(self, **kwargs) -> dict[str, Any]:
        invalid_input = {}
        for key, value in kwargs.items():
            if (key in self.columns) and ((await self.bot.player_dao.select_player(value)) is not None):
                continue
            else:
                invalid_input[key] = value

        return invalid_input

    '''
    Assign a Discord user within the server to an account in account_table.
    Produce a user select menu where the author of the interaction assigns a Discord user
    to an account saved within the database.

    Args: 
        account_name (str): The name of the account to be assigned to a member of the Discord server
            - correlates to 'league_username' in account_table
    '''
    @commands.command(name='assign')
    async def insert_player(self, ctx):
        #TODO call playerView for user selection to assign an account to a player
        pass

    '''
    @commands.command(name='names')
    async def select_all_names(self, ctx, discord_username: str):
        invalid_input = await self._validate_input(discord_username=discord_username)
        for key, value in invalid_input.items():
            await ctx.send(f'ERR: User \'{value}\' was not found in the database.')
            return

        row = await self.bot.player_dao.select_player(discord_username)
        if (not row):
            await ctx.send(f'ERR: Account \'{discord_username}\' was not found in the database.')
            return

        player_dict = {
            'playerID':         row[0],
            'discord_username': row[1],
            'nickname':         row[2]
        }
        view = PlayerView(player_dict.copy())
        embed = view.create_embed()
        await ctx.send(embed=embed, view=view)
        return
    '''
