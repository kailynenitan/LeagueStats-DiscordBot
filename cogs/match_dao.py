import asyncio
import discord
from discord.ext import commands

class MatchDAO(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def insert_player_match(self, gameID: int, playerID: int, player_data: dict):
        # Insert an entry into game_player_table in the database
        # This should only be called after verifying that the data is correct
        sql_statement = (
            'INSERT INTO game_player_table (gameID, playerID, kills, deaths, assists, cs, gold, result) '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?);'
        )
        params = (
                gameID,
                playerID,
                player_data['kills'],
                player_data['deaths'],
                player_data['assists'],
                player_data['cs'],
                player_data['gold'],
                player_data['result']
        )
        return self.bot.get_cog('DatabaseHandler').execute_insert(sql_statement, params)

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
