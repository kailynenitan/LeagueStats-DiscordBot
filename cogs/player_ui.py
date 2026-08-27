import discord

'''
Produce a Discord embed that shows the names of a player
Args:
    player_data tuple[str]: One row of all columns in player_table for one specific player.
                            The tuple should match the tuple that is a result of a SELECT query
Returns:
    A Discord embed showing all names that are associated with a player.
'''
def player_names_embed(player_data: tuple[str]) -> discord.Embed:
    _, league_username, discord_username, nickname = player_data
    embed = discord.Embed(title=f'Names Associated with {league_username}', color=discord.Color.blurple())
    embed.add_field(name='League of Legends Username', value=str(league_username), inline=True)
    embed.add_field(name='Discord Username', value=str(discord_username), inline=True)
    embed.add_field(name='Nickname', value=str(nickname), inline=True)
    return embed
