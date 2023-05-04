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
config_dir = os.path.join(bot_folder,"cfg", "config.ini")
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
                text_clear = f"`/clear_watchlist`\n Attention removes all players and all teams irrevocably."

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
                await interaction.response.edit_message(embed=embed)

        select.callback = my_callback
        view = View()
        view.add_item(select)
        embed = discord.Embed(
            title="Delete player", description="Select a player!", color=0xff8040)
        await interaction.response.send_message(embed=embed, ephemeral=True, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(help(bot), guild=discord.Object(guild_id))
