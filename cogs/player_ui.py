import discord
import traceback

'''
Produce a Discord embed that shows the names of a player and allows the user to change any of the names.
Args:
    player_data tuple[str]: One row of all columns in player_table for one specific player.
                            The tuple should match the tuple that is a result of a SELECT query
Returns:
    A Discord embed showing all names that are associated with a player along with buttons that produce a modal
    to change any of the names that are associated with the player.
'''
class PlayerView(discord.ui.View):

    def __init__(self, player_data: dict, authorID: int):
        super().__init__(timeout=300)
        self.player_data = player_data
        self.authorID = authorID
        self.saveID = 1

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.authorID:
            await interaction.response.send_message('You cannot edit this session.', ephemeral=True)
            return False
        return True

    def create_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title=f'Names Associated with {self.player_data['league_username']}',
            color=discord.Color.blurple()
        )
        embed.add_field(
            name='League of Legends Username',
            value=str(self.player_data['league_username']),
            inline=True
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

    @discord.ui.button(label='Change League Username', style=discord.ButtonStyle.primary, row=0)
    async def league_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = RenameModal('league_username', self.player_data, self)
        await interaction.response.send_modal(modal)
        
    @discord.ui.button(label='Change Discord Username', style=discord.ButtonStyle.primary, row=0)
    async def discord_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = RenameModal('discord_username', self.player_data, self)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label='Change Nickname', style=discord.ButtonStyle.primary, row=0)
    async def nickname_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = RenameModal('nickname', self.player_data, self)
        await interaction.response.send_modal(modal)

        # A new nickname was entered -> enable save button
        save_item = self.find_item(self.saveID)
        save_item.disabled = False

    @discord.ui.button(label='Save New Names', id=1, disabled=True, style=discord.ButtonStyle.success, row=1)
    async def save_button(self, interaction: discord.Interaction, button: discord.ui.button):
        player_dao = interaction.client.get_cog('PlayerDAO')
        if (player_dao is None):
            await interaction.response.send_message('Player table data access object not found.', ephemeral=True)
            return

        try:
            # TODO write below 3 lines as a for loop for simplicity
            await player_dao.update_player(self.player_data['playerID'], 'league_username', self.player_data['league_username'])
            await player_dao.update_player(self.player_data['playerID'], 'discord_username', self.player_data['discord_username'])
            await player_dao.update_player(self.player_data['playerID'], 'nickname', self.player_data['nickname'])

            save_item = self.find_item(self.saveID)
            save_item.disabled = True

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
