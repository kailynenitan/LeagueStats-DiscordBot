import asyncio
import discord
from discord.ext import commands

class PerformanceHistoryDAO(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.COLUMNS = [
            'gameID',
            'playerID',
            'kills',
            'deaths',
            'assists',
            'cs',
            'gold',
            'result'
        ]

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
        return self.bot.db_handler.execute_insert(sql_statement, params)

    async def select_avg(self, stat: str, playerID: int):
        sql_statement = (
            f'SELECT AVG({stat}) '
            f'FROM game_player_table '
            f'WHERE playerID = ?;'
        )
        params = (playerID, )
        return self.bot.db_handler.execute_insert(sql_statement, params)

    async def select_top(self, stat: str):
        pass

    async def select_bottom(self, stat: str):
        pass
