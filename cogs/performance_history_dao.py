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
        # Get the average of a specific stat for a specific player
        sql_statement = (
            f'SELECT AVG({stat}) as avg_value '
            f'FROM game_player_table '
            f'WHERE playerID = ?;'
        )
        params = (playerID, )
        return self.bot.db_handler.execute_select(sql_statement, params, 1)

    async def select_avg_list(self, stat: str):
        # Get a descending list of averages of all players for a specific stat
        sql_statement = (
            f'SELECT playerID, AVG({stat}) as avg_value '
            f'FROM game_player_table '
            f'GROUP BY playerID '
            f'ORDER BY avg_value DESC;'
        )
        return self.bot.db_handler.execute_select(sql_statement, fetch_size=-1)
