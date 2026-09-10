import discord
import traceback

'''
The purpose of VerifyDataView is to double check the text
that the OCR read before inserting data into the database. Data
for each player is read in line-by-line and a view is produced
for each line of data. Each stat to be validated is sent to a
text channel as a button that, when pressed, will produce a 
modal where the user can edit the information.
'''
class VerifyDataView(discord.ui.View):

    def __init__(self, bot, players_data: list[dict], authorID: int):
        super().__init__(timeout=300)
        self.bot = bot
        self.players_data = players_data
        self.authorID = authorID
        self.current_index = 0

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.authorID:
            await interaction.response.send_message('You cannot edit this session.', ephemeral=True)
            return False
        return True

    def create_embed(self) -> discord.Embed:
        player = self.players_data[self.current_index]
        embed = discord.Embed(
            title=f'Verify Stats - Player {self.current_index + 1} of {len(self.players_data)}',
            description=f'Reviewing stats for **{player['league_username']}**',
            color=discord.Color.blurple()
        )
        embed.add_field(name='Kills', value=str(player['kills']), inline=True)
        embed.add_field(name='Deaths', value=str(player['deaths']), inline=True)
        embed.add_field(name='Assists', value=str(player['assists']), inline=True)
        embed.add_field(name='CS', value=str(player['cs']), inline=True)
        embed.add_field(name='Gold', value=str(player['gold']), inline=True)
        embed.set_footer(text='Click \'Edit Core\' or \'Edit Extra\' to adjust values before saving.')
        return embed

    def create_overview_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title='Match Summary Overview',
            description='Check all players below. Select a player to edit or confirm directly.',
            color=discord.Color.gold()
        )

        overview_lines=[]
        for p in self.players_data:
            overview_lines.append(
                f'**{p['league_username']}**: {p['kills']}/{p['deaths']}/{p['assists']} | {p['cs']} CS | {p['gold']}g'
            )

        embed.add_field(
            name='Roster',
            value='\n'.join(overview_lines),
            inline=False
        )
        embed.set_footer(text='Click \'Confirm and Save to Database\' to save.\nUse the next and previous buttons to edit specific players.')
        return embed

    @discord.ui.button(label='Overview All', style=discord.ButtonStyle.secondary, row=0)
    async def overview_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.create_overview_embed()
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='Previous', style=discord.ButtonStyle.secondary, row=0)
    async def prev_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_index = (self.current_index - 1) % len(self.players_data)
        await interaction.response.edit_message(embed=self.create_embed(), view=self)

    @discord.ui.button(label='Next', style=discord.ButtonStyle.secondary, row=0)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_index = (self.current_index + 1) % len(self.players_data)
        await interaction.response.edit_message(embed=self.create_embed(), view=self)

    @discord.ui.button(label='Edit Core Stats', style=discord.ButtonStyle.primary, row=1)
    async def edit_core(self, interaction: discord.Interaction, button: discord.ui.Button):
        player = self.players_data[self.current_index]
        modal = CoreStatsModal(player, self)
        await interaction.response.send_modal(modal)

    @discord.ui.button(label='Edit Extra Stats', style=discord.ButtonStyle.primary, row=1)
    async def edit_extra(self, interaction: discord.Interaction, button: discord.ui.Button):
        player = self.players_data[self.current_index]
        modal = ExtraStatsModal(player, self)
        await interaction.response.send_modal(modal)
 
    @discord.ui.button(label='Confirm and Save to Database', style=discord.ButtonStyle.success, row=2)
    async def save_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            gameID = await self.bot.game_dao.insert_game()
            for player_dict in self.players_data:
                await self.bot.account_dao.insert_account(player_dict['league_username'])
                accountID = await self.bot.account_dao.select_accountID(player_dict['league_username'])
                await self.bot.perf_history_dao.insert_player_match(gameID, accountID, player_dict)
        except Exception as e:
            await interaction.response.send_message(f'Failed to save player match data: {e}', ephemeral=True)
            return

        for item in self.children:
            item.disabled=True

        embed = discord.Embed(
            title='Data Saved Successfully.',
            description=f'Verified data for **{len(self.players_data)} players** has been added to the database.',
            color=discord.Color.green()
        )
        await interaction.response.edit_message(embed=embed, view=self)
        self.stop()
     
    async def on_error(
            self, interaction: discord.Interaction[discord.Client], error: Exceptionj, item: discord.ui.Item[typing.Any]) -> None:
        tb = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
        message = f'An error occurred while processing the interaction for {str(item)}:\n```py\n{tb}\n```'
        await interaction.response.send_message(message)


class CoreStatsModal(discord.ui.Modal):
    def __init__(self, player_data: dict, parent_view: 'VerifyDataView'):
        super().__init__(title=f'Core Stats: {player_data['league_username']}')
        self.player_data = player_data
        self.parent_view = parent_view

        init_kills = str(player_data['kills'])[:5]
        init_deaths = str(player_data['deaths'])[:5]
        init_assists = str(player_data['assists'])[:5]
        init_cs = str(player_data['cs'])[:5]

        self.kills = discord.ui.TextInput(label='Kills', default=init_kills, max_length=5)
        self.deaths = discord.ui.TextInput(label='Deaths', default=init_deaths, max_length=5)
        self.assists = discord.ui.TextInput(label='Assists', default=init_assists, max_length=5)
        self.cs = discord.ui.TextInput(label='CS (Creep Score)', default=init_cs, max_length=5)

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
    def __init__(self, player_data: dict, parent_view: 'VerifyDataView'):
        super().__init__(title=f'Extra Stats: {player_data['league_username']}')
        self.player_data = player_data
        self.parent_view = parent_view

        init_gold = str(player_data['gold'])[:5]

        self.league_username = discord.ui.TextInput(label='Username', default=str(player_data['league_username']))
        self.gold = discord.ui.TextInput(label='Gold', default=init_gold)

        for item in [self.league_username, self.gold]:
            self.add_item(item)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            self.player_data['gold'] = int(self.gold.value)
        except ValueError:
            await interaction.response.send_message('Stats must be integers')
            return

        try:
            self.player_data['league_username'] = str(self.league_username.value)
        except ValueError:
            await interaction.response.send_message('Must enter a username')
            return

        embed = self.parent_view.create_embed()
        await interaction.response.edit_message(embed=embed, view=self.parent_view)
