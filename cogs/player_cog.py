from cogs.player_ui import player_names_embed
from discord.ext import commands
from typing import Any


class PlayerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.columns = ['league_username', 'discord_username', 'nickname']
        self.player_dao = self.bot.get_cog('PlayerDAO')
        if not (self.player_dao):
            raise ConnectionError('PlayerDAO failed to load.')
            return

    async def _validate_input(self, **kwargs) -> dict[str, Any]:
        invalid_input = {}
        for key, value in kwargs.items():
            if (key in self.columns) and ((await self.player_dao.select_player(value)) is not None):
                continue
            else:
                invalid_input[key] = value

        return invalid_input


    @commands.command(name='names')
    async def select_all_names(self, ctx, league_username: str):
        invalid_input = self._validate_input(league_username=league_username)
        if len(invalid_input) > 0:
            for key, value in invalid_input.items():
                if (key in ['league_username', 'discord_username', 'nickname']):
                    await ctx.send(f'{key}: {value} was not found in the database')
                else:
                    await ctx.send(f'{key} is not a valid category for names in the database.')
            return

        row = await self.player_dao.select_player(league_username=league_username)
        if (not row):
            await ctx.send(f'No player found with league username: \'{league_username}\'')
            return

        embed = player_names_embed(row)
        await ctx.send(embed=embed)
        return

'''
    @commands.command(name='change_names')
    async def update_player_names(self, ctx, league_username; str):
        invalid_input = _validate_input(kwargs)
        if len(invalid_input) > 0:
            for key, value in invalid_input.items():
                if (key in ['league_username', 'discord_username', 'nickname']):
                    await ctx.send(f'{key}: {value} was not found in the database')
                else:
                    await ctx.send(f'{key} is not a valid category for names in the database.')
            return

        #TODO: make a modal pop-up to change a name of a player

        return 
'''
