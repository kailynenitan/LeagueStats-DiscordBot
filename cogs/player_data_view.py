import discord

class PlayerDataView(discord.ui.LayoutView):
    '''
    Produce a Discord embed to the Discord channel where the command was called.
    The embed is formatted to show data retrieved from league_stats.db.

    Args:
        title (str): Title of the embed
        description (str): Description of the contents of the embed
        return_data (list[str]): List of the columns in player_table to retrieve
        return_size (int): Number of entries from player_table to retrieve
    '''
    def __init__(self, title: str, description: str, return_data: list[str], return_size: int=None):
        super().__init__()
        self.title = title
        self.description = description
        self.return_data = return_data
        self.return_size = return_size

        container = discord.ui.Container(discord.ui.TextDisplay('Testing the text display'))
