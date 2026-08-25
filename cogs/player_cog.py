from discord.ext import commands
from cogs.player_data_view import PlayerDataView


class PlayerCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='all_names')
    async def select_all_names(self, ctx, league_username: str):
        if (league_username is None) or (not league_username.strip()):
            await ctx.send('Please enter a valid league_username.')
            return

        player_dao = self.bot.get_cog('PlayerDAO')
        if not (player_dao):
            await ctx.send('PlayerDAO cog is not loaded.')
            return

        row = await player_dao.select_player(league_username=league_username)
        if (not row):
            await ctx.send(f'No player found with league username: \'{league_username}\'')
            return

        db_id, db_league, db_discord, db_nickname = row

        # TODO: make embed to show player names

        return

    async def update_player(self):
        pass
