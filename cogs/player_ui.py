import discord

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

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.authorID:
            await interaction.response.send_message('You cannot edit this session.', ephemeral=True)
            return False
        return True

    def player_names_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title=f'Names Associated with {self.player_data[league_username]}',
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

    @discord.ui.button(label='Change Name', style=discord.ButtonStyle.primary, row=0)
    async def change_name_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = ChangeNameModal(self)
        await interaction.response.send_modal(modal)

class ChangeNameModal(discord.ui.Modal):

    def __init__(self, player_data: dict, parent_view: 'PlayerView'):
        super().__init__(title=f'Change Names')
        self.player_data = player_data
        self.parent_view = parent_view

        '''
        league_option = discord.SelectOption(label='League of Legends Username', emoji='nerd', default=True)
        discord_option = discord.SelectOption(label='Discord Username', emoji='smiling_imp')
        nickname_option = discord.SelectOption(label='Nickname', emoji='bust_in_silhouette')
        option_list = [league_option, discord_option, nickname_option]
        '''
        self.select_column = discord.ui.Select(placeholder='Select name category to change')
        self.select_column.add_option(
            label='League of Legends Username', value='league_username',
            emoji='nerd', default=True)
        self.select_column.add_option(label='Discord Username', value='discord_username', emoji='smiling_imp')
        self.select_column.add_option(label='Nickname', value='nickname', emoji='bust_in_silhouette')

        self.input_name = discord.ui.TextInput(label='New Name')

        for item in [self.select_column, self.input_name]:
            self.add_item(item)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            self.player_data[self.select_column.value] = self.input_name.value
        except Exception as e:
            await interaction.response.send_message(f'ERR: {e}')
            return

        embed = self.parent_view.create_embed()
        await interaction.response.edit_message(embed=embed, view=self.parent_view)
