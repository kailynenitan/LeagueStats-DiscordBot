import discord
import traceback

'''
The purpose of ValidateStatsView is to double check the text
that the OCR read before inserting data into the database. Data
for each player is read in line-by-line and a view is produced
for each line of data. Each stat to be validated is sent to a
text channel as a button that, when pressed, will produce a 
modal where the user can edit the information.
'''
class ValidateStatsView(discord.ui.View):

    def __init__(self, timeout: float = 300.0):
        super().__init__(timeout=timeout)
        self.count=0

    def _disable_all(self) -> None:
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

    @discord.ui.button(label='Test', style=discord.ButtonStyle.green)
    async def counter(self, inter: discord.Interaction, button: discord.ui.Button[ValidateStatsView]) -> None:
        button.label = 'Disabled!'
        self._disable_all()
        await inter.response.edit_message(view=self)
        
    async def on_error(
            self, interaction: discord.Interaction[discord.Client], error: Exceptionj, item: discord.ui.Item[typing.Any]) -> None:
        tb = ''.join(traceback.format_exception(type(error), error, error.__traceback__))
        message = f'An error occurred while processing the interaction for {str(item)}:\n```py\n{tb}\n```'
        await interaction.response.send_message(message)
