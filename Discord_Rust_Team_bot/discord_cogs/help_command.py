"""Full Doku on: https://github.com/NapoII/Discord_Rust_Team_bot"
-----------------------------------------------
this cog is for gen help info embeds.
------------------------------------------------
"""

import os

from discord.ui import Select, View
from util.__funktion__ import *

#    Prevents the code from being executed when the file is imported as a module.
if __name__ == "help_command":
    log("__function should not be executed when the file is imported as a module.\nThis was not the case!", "r")
else:
    pass


# get the path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
bot_path = os.path.abspath(sys.argv[0])
bot_folder = os.path.dirname(bot_path)
# construct the path to the config.ini file relative to the current directory
config_dir = os.path.join(bot_folder, "cfg", "config.ini")
guild_id = int(read_config(config_dir, "Client", "guild_id"))
guild = discord.Object(id=guild_id)


class help(commands.Cog, ):

    def __init__(self, bot: commands.Bot,) -> None:
        self.bot = bot

    @app_commands.command(name="help", description="Questions about the Discord Bot")
    async def help_list(self,
                        interaction: discord.Interaction,):
        options = []
        options.append(discord.SelectOption(
            label=f"Rust", description="Alles Infos zu den Rust-Botcommands"))
        select = Select(options=options)

        async def my_callback(interaction: discord.Interaction):

            auswahl = select.values[0]

            if auswahl == "Rust":
                embed = discord.Embed(
                    title="Help / Rust Bot", description="Listing of all Comands", color=0x8080ff)
                embed.set_thumbnail(url="https://i.imgur.com/Twekn9L.png")

                text_serveraendern = f"`/change_server`\nUse Battlemetrics.com to determine the server ID and /change_server register."
                text_addplayer = f"`/add_player`\nUse Battlemetrics.com to find out the player ID andt /change_server enter. Add a note to the player. Now, if necessary, create a new team or assign it to the new player in an existing team via the menu.."
                text_deltplayer = f"`/delt_player`\nSelecting a player from the list to remove him/her."
                text_deltteam = f"`/delt_team`\nSelect team from the list to remove it."
                text_clear = f"`/clear_watchlist`\nAttention removes all players and all teams irrevocably."
                text_team_check = f"`/team_check`\nChecks a player for possible team members on the server using their steam ID"

                embed.add_field(name="Rust Server ändern",
                                value=text_serveraendern, inline=False)
                embed.add_field(name="Neuen Spieler anlegen",
                                value=text_addplayer, inline=False)
                embed.add_field(name="Spieler entfernen",
                                value=text_deltplayer, inline=False)
                embed.add_field(name="Team entfernen",
                                value=text_deltteam, inline=False)
                embed.add_field(name="Watchlist leeren",
                                value=text_clear, inline=False)
                embed.add_field(name="Team Check",
                                value=text_team_check, inline=False)
                await interaction.response.edit_message(embed=embed)

        select.callback = my_callback
        view = View()
        view.add_item(select)
        embed = discord.Embed(
            title="Delete player", description="Select a player!", color=0xff8040)
        await interaction.response.send_message(embed=embed, ephemeral=True, view=view)


class HelpBox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = self.CustomHelp()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

    class CustomHelp(commands.HelpCommand):
        def __init__(self):
            super().__init__()
            self.command_attrs['help'] = 'Show help about the bot, a command, or a category'

        async def send_bot_help(self, mapping):
            embed = discord.Embed(
                title="Help", description="Here's a list of commands:")
            embed.add_field(
                name="/change_server", value="Use Battlemetrics.com to determine the server ID and /change_server register.")
            embed.add_field(name="/add_player", value="Use Battlemetrics.com to find out the player ID andt /change_server enter. Add a note to the player. Now, if necessary, create a new team or assign it to the new player in an existing team via the menu.")
            embed.add_field(
                name="/delt_player", value="Selecting a player from the list to remove him/her.")
            embed.add_field(name="/delt_team",
                            value="Select team from the list to remove it.")
            embed.add_field(name="/clear_watchlist",
                            value="Attention removes all players and all teams irrevocably.")
            embed.add_field(
                name="/team_check", value="Checks a player for possible team members on the server using their steam ID.")
            await self.get_destination().send(embed=embed)

        async def send_command_help(self, command):
            embed = discord.Embed(
                title=f"Help with `{command.name}`", description=command.help)
            embed.add_field(
                name="Usage", value=f"`{self.get_command_signature(command)}`")
            await self.get_destination().send(embed=embed)

        async def send_group_help(self, group):
            embed = discord.Embed(
                title=f"Help with `{group.name}`", description=group.help)
            embed.add_field(
                name="Usage", value=f"`{self.get_command_signature(group)}`")
            await self.get_destination().send(embed=embed)

        async def send_cog_help(self, cog):
            embed = discord.Embed(
                title=f"Help with `{cog.qualified_name}`", description=cog.description)
            for command in cog.get_commands():
                if command.hidden:
                    continue
                embed.add_field(name=command.name,
                                value=command.help, inline=False)
            await self.get_destination().send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(help(bot), guild=discord.Object(guild_id))
    await bot.add_cog(HelpBox(bot), guild=discord.Object(guild_id))