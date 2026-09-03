import discord

class LeaderboardView(discord.ui.View):
    def __init__(self, asc: bool=False):
        super().__init__(timeout=300)
        self.asc = asc
        self.current_index = 0

    def avg_leaderboard_embed(self, data_category: str, user_data: list[tuple], size: int=3) -> discord.Embed:
        embed = discord.Embed(
            title=f'{data_category} Leaderboard',
            color=discord.Color.red()
        )

        for i in range(size):
            (name, stat_avg) = user_data[i]
            embed.add_field(name=name, value=str(stat_avg), inline=False)

        return embed


