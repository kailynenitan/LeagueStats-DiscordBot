import sqlite3
from pathlib import Path

class DatabaseHandler:
    def __init__(self):
        self.DB_FOLDER = Path('data')
        self.DB_FOLDER.mkdir(parents=True, exist_ok=True)
        self.DB_FILE = self.DB_FOLDER / 'league_stats.db'

        self.conn = None
        self.cursor = None

    def close(self):
        self.conn.close()

    def execute_query(self, sql_statement: str, params: tuple=(), fetch_size: int=0):
        '''
        Execute a sql query on the league_stats database
       
        Args:
            sql_statement: A string of the sql statement to be executed
            params: A tuple of the dynamic variables to be used
                  in sql_statement
            fetch: An int describing how many rows to select and return
                  -1 -> fetch all
                  0 -> fetch none
                  1 -> fetch one
                  x -> fetch x number of rows
        '''
        if ((not self.cursor) or (not self.conn)):
            print('[ERR] Query execution failed: Database connection or cursor not intialized.')

        rows = None

        try:
            self.cursor.execute(sql_statement, params)

            if (fetch_size == -1):
                rows = self.cursor.fetchall()
            elif (fetch_size == 1):
                rows = self.cursor.fetchone()
            elif (fetch_size > 0):
                rows = self.cursor.fetchmany(fetch_size)

            self.conn.commit()

        except sqlite3.Error as e:
            print(f'Query execution failed: {e}')
 
        else:
            print('Query execution successful')
            return rows


    def get_lastrowid(self):
        return self.cursor.lastrowid

    def create_tables(self):
        self.conn = sqlite3.connect(self.DB_FILE)
        self.cursor = self.conn.cursor()

        try:
            self.conn.execute('PRAGMA foreign_keys=ON;')

            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS game_table (
                    gameID INTEGER PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    mvp INTEGER,
                    ace INTEGER,
                    FOREIGN KEY(mvp) REFERENCES player_table(playerID),
                    FOREIGN KEY(ace) REFERENCES player_table(playerID)
            );''')
 
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS player_table (
                    playerID INTEGER PRIMARY KEY,
                    league_username TEXT NOT NULL UNIQUE,
                    discord_username TEXT,
                    nickname TEXT
            );''')
 
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS game_player_table (
                    gameID INTEGER,
                    playerID INTEGER,
                    kills INTEGER NOT NULL,
                    deaths INTEGER NOT NULL,
                    assists INTEGER NOT NULL,
                    cs INTEGER NOT NULL,
                    gold INTEGER NOT NULL,
                    result TEXT NOT NULL,
                    PRIMARY KEY(gameID, playerID),
                    FOREIGN KEY(gameID) REFERENCES game_table(gameID),
                    FOREIGN KEY(playerID) REFERENCES player_table(playerID)
            );''')

            self.conn.commit()

        except sqlite3.Error as e:
            print(f'Database initialization failed: {e}')

        finally:
            print(f'Database initialized at: {self.DB_FILE.resolve()}')

