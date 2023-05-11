"""Full Doku on: https://github.com/NapoII/Discord_Rust_Team_bot"
-----------------------------------------------
a send ebmbed to channel for the discord admin.
------------------------------------------------
"""

from discord.app_commands import Choice
from util.__funktion__ import *

from discord.ui import Select, View
import json

# get the path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
bot_path = os.path.abspath(sys.argv[0])
bot_folder = os.path.dirname(bot_path)
# construct the path to the config.ini file relative to the current directory
config_dir = os.path.join(bot_folder, "cfg", "config.ini")
guild_id = int(read_config(config_dir, "Client", "guild_id"))
guild = discord.Object(id=guild_id)

file_path = os.path.dirname(sys.argv[0])
file_path_Team_Checker = os.path.dirname(os.path.realpath(__file__))

file_path_temp = os.path.join(file_path_Team_Checker, "temp")
file_path_temp = Folder_gen("temp", file_path_temp)

file_path_Team_data = os.path.join(bot_folder, "cfg", "Team_data.json")

team_cheack_data_temp_dir = file_path_temp + "/" + \
    ((File_name_with_time("Team_cheack_data"))+".temp")


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
        global team_cheack_data_temp_dir

        if "https://steamcommunity.com" in player_steam_url:
            pass
        else:
            if "https://steamcommunity.com" not in player_steam_url:
                player_steam_url = "https://steamcommunity.com/profiles/{player_steam_url}/"

        battlemetrics_server_id = read_config(
            config_dir, "Rust", "battlemetrics_server_id")

        data_steam_name = team_cheacker(
            battlemetrics_server_id, player_steam_url)
        if data_steam_name == None:
            embed = discord.Embed(title="Team Cheacker", url=player_steam_url,
                                  description="No data found under this Steam URL.", color=0xff0006)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            data_battlemetrics_server_id_name = generate_list_of_online_players(
                battlemetrics_server_id)

            team_player_data = zip_data_steamname_and_bat_id(
                data_steam_name, data_battlemetrics_server_id_name)
            json_string = json.dumps(team_player_data)

            team_cheack_data_temp_dir = create_and_fill_temp_bridge(
                json_string, team_cheack_data_temp_dir)

            team_player_data_len = len(team_player_data)
            if team_player_data_len == 1:
                embed = discord.Embed(
                    title="Team Cheacker", description="No info on a team maybe he's solo?", color=0x0080ff)
            else:
                embed = discord.Embed(
                    title="Team Cheacker", description=f"The team consists of {team_player_data_len} players.", color=0x0080ff)

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
                    Player_Bat_url = f"https://www.battlemetrics.com/players/{ID}"

                    value = f"Steam name: [`{name}`]({steam_url})\nBattlemetrics ID: [`{ID}`]({Player_Bat_url})"
                    embed.add_field(name=name, value=value, inline=True)
                except:
                    offline = True
                    break

            if offline == True:
                embed = discord.Embed(title="Team Cheack", url=player_steam_url,
                                      description="Player not found. maybe it's not online on the server right now?", color=0xff0006)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                view = Confirm_say()
                c_embed = await interaction.channel.send(embed=embed, view=view)

                await view.wait()

                if view.value is None:
                    self.confirm_Button = False
                    log(
                        f'Timed out... self.confirm_Button = {self.confirm_Button}')

                elif view.value:
                    self.confirm_Button = True
                    await c_embed.delete()
                    Team_list = Team_choice(file_path_Team_data)

                    # replace with your thinking emoji ID
                    thinking = self.bot.get_emoji(123456789)
                    embed = discord.Embed(
                        title="Select a team or create a new one", description=f"{thinking} Thinking...", color=discord.Color.blurple())
                    msg = await interaction.channel.send(embed=embed, delete_after=10, )

                    Team_list = Team_choice(file_path_Team_data)
                    Team_list_len = len(Team_list)

                    x = -1
                    options = [discord.SelectOption(
                        label=f"🆕Create a new team.🆕", description=f"Add a new team for players."),]
                    while True:
                        x = x + 1
                        if x == Team_list_len:
                            break
                        try:
                            team_name,  team_note = Team_list[x]

                            options.append(discord.SelectOption(
                                label=f"{team_name}", description=f"{team_note}"))
                        except:
                            pass
                    select = Select(options=options)

                    async def my_callback(interaction):

                        if f"{select.values[0]}" == f"🆕Create a new team.🆕":
                            await interaction.response.send_modal(modal_New_team())

                        else:

                            embed = discord.Embed(
                                title=f"Team Cheack", description="added to team watchlist", color=0xff8040)
                            await interaction.response.send_message(embed=embed, ephemeral=True,)

                    select.callback = my_callback
                    view = View()
                    view.add_item(select)

                    if msg is not None:
                        await msg.edit(embed=embed, view=view)
                    else:
                        await interaction.channel.send(embed=embed, delete_after=10, view=view)

                else:
                    self.confirm_Button = False
                    log(
                        f'Cancelled... self.confirm_Button = {self.confirm_Button}')
                    # return self.confirm_Button, self.say_channel_id, self.say_title, self.say_text


class modal_New_team(ui.Modal, title="New Team", ):

    New_Team_name = ui.TextInput(label="Name of the new team", style=discord.TextStyle.short,
                                 placeholder="Team name", required=True, max_length=None)
    New_team_note = ui.TextInput(label="Embed Titel:", style=discord.TextStyle.short,
                                 placeholder="Team note", required=True, max_length=None)

    log("modal_New_team: New_Team_name | New_team_note |")

    async def on_submit(self, interaction: discord.Interaction):

        embed = discord.Embed(title=self.New_Team_name,
                              description=self.New_team_note, color=0xc0c0c0)
        view = Confirm_say()
        await interaction.response.send_message(embed=embed, ephemeral=True, view=view)

        log(
            f"Output modal_New_team: New_Team_name={self.New_Team_name} | New_team_note={self.New_team_note}")
        log(f"Send Confrim / Cancel query.")

        log("Send Discordembed: Test Result")
        await view.wait()
        if view.value is None:
            self.confirm_Button = False
            log(f'Timed out... self.confirm_Button = {self.confirm_Button}')

        elif view.value:
            self.confirm_Button = True
            
            embed = discord.Embed(title=self.New_Team_name,
                                  description=self.New_team_note, color=0xc0c0c0)

            Team_Card_embed_id = 0
            log(f'Confirmed... self.confirm_Button = {self.confirm_Button}')

            JSOn_data = open_JSOn_File(file_path_Team_data)
            JSOn_data = add_Team(JSOn_data, self.New_Team_name,
                                 self.New_team_note, Team_Card_embed_id)
            Fill_JSOn_File(file_path_Team_data, JSOn_data)
            team_player_data = read_and_delt_temp_bridge(
                team_cheack_data_temp_dir)
            team_player_data = json.loads(team_player_data)
            x = -1
            team_player_data_only_name = list(team_player_data.keys())
            while True:
                x = x + 1
                if x == len(team_player_data):
                    break

                name = team_player_data_only_name[x]
                ID = team_player_data[name]["ID"]
                steam_url = team_player_data[name]["steam_url"]

                JSOn_data = open_JSOn_File(file_path_Team_data)
                JSOn_data = add_player(
                    JSOn_data, self.New_Team_name, name, ID, steam_url)
                Fill_JSOn_File(file_path_Team_data, JSOn_data)

            # add_player(dict, team, name, id, note):

            Fill_JSOn_File(file_path_Team_data, JSOn_data)

        else:
            self.confirm_Button = False
            log(f'Cancelled... self.confirm_Button = {self.confirm_Button}')
            # return self.confirm_Button, self.say_channel_id, self.say_title, self.say_text


class Confirm_say(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button, ):
        await interaction.response.send_message('Confirming', ephemeral=True)
        log(f"Send Confrim / Cancel query.")

        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Cancelling', ephemeral=True)
        self.value = False
        self.stop()


async def setup(bot: commands.Bot):
    await bot.add_cog(bot_team_checker(bot), guild=discord.Object(guild_id))
