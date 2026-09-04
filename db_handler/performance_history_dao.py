import asyncio
import discord

class PerformanceHistoryDAO():
    def __init__(self, db_handler):
        self.db_handler = db_handler
        self.COLUMNS = [
            'gameID',
            'accountID',
            'kills',
            'deaths',
            'assists',
            'cs',
            'gold',
            'result'
        ]

    async def insert_player_match(self, gameID: int, accountID: int, player_data: dict):
        # Insert an entry into game_player_table in the database
        # This should only be called after verifying that the data is correct
        sql_statement = (
            'INSERT INTO performance_history_table (gameID, accountID, kills, deaths, assists, cs, gold, result) '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?);'
        )
        params = (
            gameID,
            accountID,
            player_data['kills'],
            player_data['deaths'],
            player_data['assists'],
            player_data['cs'],
            player_data['gold'],
            player_data['result']
        )
        return self.db_handler.execute_insert(sql_statement, params)

    async def select_avg(self, stat: str, accountID: int):
        # Get the average of a specific stat for a specific player
        sql_statement = ('SELECT AVG({stat}) as avg_value FROM performance_history_table WHERE accountID = ?;'
        )
        params = (accountID,)
        return self.db_handler.execute_select(sql_statement, params, 1)

    async def select_avg_list(self, stat: str):
        # Get a descending list of averages of all players for a specific stat
        sql_statement = (
            f'SELECT accountID, AVG({stat}) as avg_value '
            f'FROM performance_history_table '
            f'GROUP BY accountID '
            f'ORDER BY avg_value DESC;'
        )
        return self.db_handler.execute_select(sql_statement, fetch_size=-1)
