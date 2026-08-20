import discord
import traceback

'''
The purpose of GameDataView is to double check the text
that the OCR read before inserting data into the database. Data
for each player is read in line-by-line and a view is produced
for each line of data. Each stat to be validated is sent to a
text channel as a button that, when pressed, will produce a 
modal where the user can edit the information.
'''
class GameDataView(discord.ui.View):

    def __init__(self, players_data: list[dict], authorID: int):
        super().__init__(timeout=300)
        self.players = players_data
        self.authorID = authorID
        self.current_index = 0

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.authorID:
            await interaction.response.send_message('You cannot edit this session.', ephemeral=True)
            return False
        return True

    def create_embed(self) -> discord.Embed:
        player = self.players[self.current_index]
        embed = discord.Embed(
            title=f'Verify Stats - Player {self.current_index + 1} of {len(self.players)}',
            description=f'Reviewing stats for **{player['username']**}',
            color=discord.Color.blurple()
        )
        embed.add_field(name="Kills", value=str(player['kills']), inline=True)
        embed.add_field(name="Deaths", value=str(player['deaths']), inline=True)
        embed.add_field(name="Assists", value=str(player['assists']), inline=True)
        embed.add_field(name="CS", value=str(player['cs']), inline=True)
        embed.add_field(name="Gold", value=str(player['gold']), inline=True)
        embed.add_field(name="Vision", value=str(player['vision']), inline=True)
        embed.add_field(name="Damage", value=str(player['damage']), inline=True)
        embed.set_footer(text="Click 'Edit Core' or 'Edit Extra' to adjust values before saving.")
        return embed
     
    async def on_error(
            self, interaction: discord.Interaction[discord.Client], error: Exceptionj, item: discord.ui.Item[typing.Any]) -> None:
        tb = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
        message = f'An error occurred while processing the interaction for {str(item)}:\n```py\n{tb}\n```'
        await interaction.response.send_message(message)

    def _disable_all(self) -> None:
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

class CoreStatsModal(discord.ui.Modal):
    def __init__(self, player_data: dict, parent_view: 'GameDataView'):
        super().__init__(title=f'Core Stats: {player_data['username']}')
        self.player_data = player_data
        self.parent_view = parent_view

        self.kills = discord.ui.TextInput(label='Kills')
        self.deaths = discord.ui.TextInput(label='Deaths')
        self.assists = discord.ui.TextInput(label='Assists')
        self.cs = discord.ui.TextInput(label='CS (Creep Score)')

        for item in [self.kills, self.deaths, self.assists, self.cs]:
            self.add_item(item)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            self.player_data['kills'] = int(self.kills.value)
            self.player_data['deaths'] = int(self.deaths.value)
            self.player_data['assists'] = int(self.assists.value)
            self.player_data['cs'] = int(self.cs.value)
        except ValueError:
            await interaction.response.send_message('Stats must be integers.', ephemeral=True)
            return

        embed = self.parent_view.create_embed()
        await interaction.response.edit_message(embed=embed, view=self.parent_view)


class ExtraStatsModal(discord.ui.Modal):
    def __init__(self, player_data: dict, parent_view: 'GameDataView'):
        super().__init__(title=f'Extra Stats: {player_data['name']}')
        self.player_data = player_data
        self.parent_view = parent_view

        self.username = discord.ui.TextInput(label='Username')
        self.gold = discord.ui.TextInput(label='Gold')

        for item in [self.username, self.gold]:
            self.add_item(item)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            self.player_data['gold'] = int(self.gold.value)
        except ValueError:
            await interaction.response.send_message('Stats must be integers')
            return

        try:
            self.player_data['username'] = str(self.username.value)
        except ValueError:
            await interaction.response.send_message('Must enter a username')
            return

        embed = self.parent_view.create_embed()
        await interaction.response.edit_message(embed=embed, view=self.parent_view)
