import discord
import sqlite3
from discord.ext import commands


class PlayerDAO(commands.Cog):
    ''' 
    Holds commands to handle individual player data
    '''
    
    def __init__(self, bot):
        self.bot = bot

    async def insert_player(self, league_username: str, discord_username: str=None, nickname: str=None) -> int:
        if ((discord_username is not None) and (nickname is not None)):
            sql_statement = (
                'INSERT OR IGNORE INTO player_table (league_username, discord_username, nickname) '
                'VALUES (?, ?, ?);'
            )
            params = (league_username, discord_username, nickname)

        elif (discord_username is not None):
            sql_statement = (
                'INSERT OR IGNORE INTO player_table (league_username, discord_username) '
                'VALUES (?, ?);'
            )
            params = (league_username, discord_username)

        elif (nickname is not None):
            sql_statement = (
                'INSERT OR IGNORE INTO player_table (league_username, nickname) '
                'VALUES (?, ?);'
            )
            params = (league_username, nickname)

        else:
            sql_statement = (
                'INSERT OR IGNORE INTO player_table (league_username) '
                'VALUES (?);'
            )
            params = (league_username,)

        return self.bot.get_cog('DatabaseHandler').execute_insert(sql_statement, params)

    async def select_player(
        self,
        league_username: str=None,
        discord_username:str=None,
        nickname: str=None
    ):
        if not any(v for v in [league_username, discord_username, nickname] if v and v.strip()):
            raise ValueError('Must enter at least one: league_username, discord_username, nickname')
            return None

        if (league_username and league_username.strip()):
            sql_statement = (
                'SELECT * FROM player_table WHERE league_username = ?;'
            )
            params = (league_username.strip(),)

        elif (discord_username and discord_username.strip()):
            sql_statement = (
                'SELECT * FROM player_table WHERE discord_username = ?;'
            )
            params = (discord_username.strip(),)

        else:
            sql_statement = (
                'SELECT * FROM player_table WHERE nickname = ?;'
            )
            params = (nickname.strip(),)

        return self.bot.get_cog('DatabaseHandler').execute_select(sql_statement, params, 1)

    async def select_playerID(
        self,
        league_username: str=None,
        discord_username:str=None,
        nickname: str=None
    ):
        if not any(v for v in [league_username, discord_username, nickname] if v and v.strip()):
            raise ValueError('Must enter at least one: league_username, discord_username, nickname')
            return None

        if (league_username and league_username.strip()):
            sql_statement = (
                'SELECT playerID FROM player_table WHERE league_username = ?;'
            )
            params = (league_username.strip(),)

        elif (discord_username and discord_username.strip()):
            sql_statement = (
                'SELECT playerID FROM player_table WHERE discord_username = ?;'
            )
            params = (discord_username.strip(),)

        else:
            sql_statement = (
                'SELECT playerID FROM player_table WHERE nickname = ?;'
            )
            params = (nickname.strip(),)

        return self.bot.get_cog('DatabaseHandler').execute_select(sql_statement, params, 1)

