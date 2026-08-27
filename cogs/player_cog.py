from cogs.player_ui import *
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
        invalid_input = await self._validate_input(league_username=league_username)
        for key, value in invalid_input.items():
            await ctx.send(f':warning: User "{value}" was not found in the database.')
            return

        row = await self.player_dao.select_player(league_username=league_username)
        if (not row):
            await ctx.send(f'No player found with league username: \'{league_username}\'')
            return

        player_dict = {
            'playerID': row[0],
            'league_username': row[1],
            'discord_username': row[2],
            'nickname': row[3]
        }
        view = PlayerView(player_dict, ctx.author.id)
        embed = view.player_names_embed()
        await ctx.send(embed=embed, view=view)
        return
