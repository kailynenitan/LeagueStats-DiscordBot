from cogs.leaderboard_view import LeaderboardView
from discord.ext import commands
from typing import Any

'''
All commands in this cog produce an embed with a leaderboard of a stat that
can be derived from the information saved in performance_history_table.
'''
class LeaderboardCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.perf_history_dao = self.bot.get_cog('PerformanceHistoryDAO')
        if not (self.perf_history_dao):
            raise ConnectionError('Performance history data access object failed to load.')
            return
        

    @commands.command()
    async def kills(self, ctx, size: int=3):
        kill_list = await self.perf_history_dao.select_avg_list('kills') 
        view = LeaderboardView()
        embed = view.avg_leaderboard_embed('kills', kill_list, size)
        await ctx.send(embed=embed)

    @commands.command()
    async def kills_share(self, ctx):
        # avg share of total kills in a game
        pass

    @commands.command()
    async def deaths(self, ctx):
        death_list = await self.perf_history_dao.select_avg_list('deaths') 
        view = LeaderboardView()
        embed = view.avg_leaderboard_embed('deaths', death_list, size)
        await ctx.send(embed=embed)

    @commands.command()
    async def deaths_share(self, ctx):
        # avg share of total deaths in a game
        pass

    @commands.command()
    async def assists(self, ctx):
        assist_list = await self.perf_history_dao.select_avg_list('assists') 
        view = LeaderboardView()
        embed = view.avg_leaderboard_embed('assists', assist_list, size)
        await ctx.send(embed=embed)

    @commands.command()
    async def assists_share(self, ctx):
        # avg share of total assists in a game
        pass

    @commands.command()
    async def kda(self, ctx):
        pass

    @commands.command()
    async def kill_participation(self, ctx):
        pass

    @commands.command()
    async def cs(self, ctx):
        cs_list = await self.perf_history_dao.select_avg_list('cs') 
        view = LeaderboardView()
        embed = view.avg_leaderboard_embed('cs', cs_list, size)
        await ctx.send(embed=embed)

    @commands.command()
    async def cs_per_minute(self, ctx):
        pass

    @commands.command()
    async def gold(self, ctx):
        gold_list = await self.perf_history_dao.select_avg_list('gold') 
        view = LeaderboardView()
        embed = view.avg_leaderboard_embed('gold', gold, size)
        await ctx.send(embed=embed)

    @commands.command()
    async def gold_per_minute(self, ctx):
        pass

    @commands.command()
    async def gold_share(self, ctx):
        # avg of player's total gold relative to the team's total gold
        pass

    @commands.command()
    async def winstreak(self, ctx):
        pass
    
    @commands.command()
    async def losestreak(self, ctx):
        pass
