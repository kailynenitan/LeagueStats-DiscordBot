from discord.ext import commands

''' 
Holds commands to handle League account data
'''
class AccountDAO():
    def __init__(self, db_handler):
        self.db_handler = db_handler
        self.UNASSIGNED_PLAYERID = 1
        self.COLUMNS = ['accountID', 'playerID', 'account_username']

    async def insert_account(self, account_username: str) -> int:
        sql_statement = 'INSERT OR IGNORE INTO account_table (playerID, account_username) VALUES (?, ?);'
        params = (self.UNASSIGNED_PLAYERID, account_username)
        return self.db_handler.execute_insert(sql_statement, params)

    async def select_account(self, account_username: str=None) -> (tuple) | None:
        sql_statement = 'SELECT * FROM account_table WHERE account_username = ?;'
        params = (account_username.strip(),)
        return self.db_handler.execute_select(sql_statement, params, 1)

    async def select_accountID(self, account_username: str=None) -> int | None:
        sql_statement = 'SELECT accountID FROM account_table WHERE account_username = ?;'
        params = (account_username,)
        row = self.db_handler.execute_select(sql_statement, params, 1)
        return row[0] if row else None 
