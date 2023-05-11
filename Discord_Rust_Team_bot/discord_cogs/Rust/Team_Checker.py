"""Full Doku on: https://github.com/NapoII/Discord_Rust_Team_bot"
-----------------------------------------------
a send ebmbed to channel for the discord admin.
------------------------------------------------
"""

from discord.app_commands import Choice
from util.__funktion__ import *


# get the path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
bot_path = os.path.abspath(sys.argv[0])
bot_folder = os.path.dirname(bot_path)
# construct the path to the config.ini file relative to the current directory
config_dir = os.path.join(bot_folder, "cfg", "config.ini")
guild_id = int(read_config(config_dir, "Client", "guild_id"))
guild = discord.Object(id=guild_id)


class bot_team_checker(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    description = "detects teams in Rust"
    @app_commands.command(name="team_checker", description=description)
    @app_commands.describe(
        player_steam_url="The SteamID from a Player or his Steam URL",
    )
    async def choise_team(self, interaction: discord.Interaction, player_steam_url: str,):
        self.player_steam_url = player_steam_url


        if "https://steamcommunity.com" in player_steam_url:
            pass
        else:
            if "https://steamcommunity.com" not in player_steam_url:
                player_steam_url = "https://steamcommunity.com/profiles/{player_steam_url}/"

        battlemetrics_server_id = read_config(config_dir, "Rust", "battlemetrics_server_id")

        data_steam_name = team_cheacker(battlemetrics_server_id, player_steam_url)
        if data_steam_name == None:
            embed=discord.Embed(title="Team Cheacker", url=player_steam_url, description="No data found under this Steam URL.", color=0xff0006)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            data_battlemetrics_server_id_name = generate_list_of_online_players(battlemetrics_server_id)
            
            

            team_player_data = zip_data_steamname_and_bat_id (data_steam_name, data_battlemetrics_server_id_name)

            team_player_data_len = len(team_player_data)
            if team_player_data_len == 1:
                embed=discord.Embed(title="Team Cheacker", description="No info on a team maybe he's solo?", color=0x0080ff)
            else:
                embed=discord.Embed(title="Team Cheacker", description=f"The team consists of {team_player_data_len} players.", color=0x0080ff)


            x = -1
            offline = False
            team_player_data_only_name = list(team_player_data.keys())
            while True:
                x = x + 1
                if x == team_player_data_len:
                    break

                name = team_player_data_only_name[x]
                try:
                    ID = team_player_data[name]["ID"]
                    steam_url = team_player_data[name]["steam_url"]
                    Player_Bat_url= f"https://www.battlemetrics.com/players/{ID}"

                    value = f"Steam name: [`{name}`]({steam_url})\nBattlemetrics ID: [`{ID}`]({Player_Bat_url})"
                    embed.add_field(name=name, value=value, inline=True)
                except:
                    offline = True
                    break

            if offline == True:
                embed=discord.Embed(title="Team Cheacker", url=player_steam_url, description="Player not found. maybe it's not online on the server right now?", color=0xff0006)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message(embed=embed, ephemeral=False)


async def setup(bot: commands.Bot):
    await bot.add_cog(bot_team_checker(bot), guild=discord.Object(guild_id))
