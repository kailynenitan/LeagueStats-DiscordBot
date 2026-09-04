class PlayerRecord():
    def __init__(self, discord_username: str=None, nickname: str=None):
        self.id = None
        self.discord_username = discord_username
        self.nickname = nickname

'''
Holds SQL commands to handle Discord user data
'''
class PlayerDAO():
    def __init__(self, db_handler):
        self.db_handler = db_handler

    async def insert_player(self, discord_username: str, nickname: str=None):
        sql_statement = 'INSERT OR IGNORE INTO player_table (discord_username) VALUES (?);'
        params = (discord_username,)
        if (nickname is not None):
            sql_statement = 'INSERT OR IGNORE INTO player_table (discord_username, nickname) VALUES (?, ?);'
            params = (discord_username, nickname)
        return self.db_handler.execute_insert(sql_statement, params)

    async def select_player(self, discord_username: str=None):
        if (discord_username is None):
            raise ValueError('ERR: Discord username not found in database.')
            return
        sql_statement = 'SELECT * FROM player_table WHERE discord_username = ?;'
        params = (discord_username,)
        return self.db_handler.execute_select(sql_statement, params, 1)

    async def update_player(self, playerID: int, change_data: str, new_value: str) -> bool:
        sql_statement = 'UPDATE player_table SET {change_data} = ? WHERE playerID = ?;'
        params = (new_value, playerID)
        return self.db_handler.execute_update(sql_statement, params)

