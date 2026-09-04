import discord
import traceback

'''
Produce a Discord embed that shows the Discord username and nickname of a player and allows the user to change any of the names.
Args:
    player_data tuple[str]: One row of all columns in player_table for one specific player.
                            The tuple should match the tuple that is a result of a SELECT query
Returns:
    A Discord embed showing all names that are associated with a player along with buttons that produce a modal
    to change any of the names that are associated with the player.
'''
class PlayerView(discord.ui.View):

    def __init__(self, bot, player_data: dict):
        super().__init__(timeout=300)
        self.bot = bot
        self.player_data = player_data
        self.SAVEBUTTONID = 1

    def create_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title=f'Names Associated with {self.player_data['discord_username']}',
            color=discord.Color.blurple()
        )
        embed.add_field(
            name='Discord Username',
            value=str(self.player_data['discord_username']),
            inline=True
        )
        embed.add_field(
            name='Nickname',
            value=str(self.player_data['nickname']),
            inline=True
        )
        return embed

    @discord.ui.button(label='Change Discord Username', style=discord.ButtonStyle.primary, row=0)
    async def discord_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = RenameModal('discord_username', self.player_data, self)
        await interaction.response.send_modal(modal)
        self.find_item(self.SAVEBUTTONID).disabled = False

    @discord.ui.button(label='Change Nickname', style=discord.ButtonStyle.primary, row=0)
    async def nickname_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = RenameModal('nickname', self.player_data, self)
        await interaction.response.send_modal(modal)
        self.find_item(self.SAVEBUTTONID).disabled = False

    @discord.ui.button(label='Save New Names', id=1, disabled=True, style=discord.ButtonStyle.success, row=1)
    async def save_button(self, interaction: discord.Interaction, button: discord.ui.button):
        try:
            playerID = self.player_data['playerID']
            for category in ['discord_username', 'nickname']:
                await self.bot.player_dao.update_player(playerID, category, self.player_data[category])

            self.find_item(self.SAVEBUTTONID).disabled = True
            embed = self.create_embed()
            await interaction.response.edit_message(embed=embed, view=self)

        except Exception as e:
            await interaction.response.send_message(f'Failed to update player data: {e}', ephemeral=True)
            return

    async def on_error(
            self, interaction: discord.Interaction[discord.Client], error: Exceptionj, item: discord.ui.Item[typing.Any]) -> None:
        tb = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
        message = f'An error occurred while processing the interaction for {str(item)}:\n```py\n{tb}\n```'
        await interaction.response.send_message(message, ephemeral=True)


class RenameModal(discord.ui.Modal):

    def __init__(self, category: str, player_data: dict, parent_view: 'PlayerView'):
        super().__init__(title='Change Names')
        self.category = category
        self.player_data = player_data
        self.parent_view = parent_view

        self.name = discord.ui.TextInput(label='New Name', default=self.player_data[self.category])
        self.add_item(self.name)


    async def on_submit(self, interaction: discord.Interaction):
        try:
            self.player_data[self.category] = self.name.value
        except Exception as e:
            await interaction.response.send_message(f'ERR: {e}', ephemeral=True)
            return

        embed = self.parent_view.create_embed()
        await interaction.response.edit_message(embed=embed, view=self.parent_view)
