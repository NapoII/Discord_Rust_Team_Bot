"""Full Doku on: https://github.com/NapoII/Discord_Rust_Team_bot"
-----------------------------------------------
This COG is for player cards to see the latest activiti.
Team note: ?
updated 7 minutes ago
FRED
🔴 one month ago
ServerZeit: 223.61h
note: Close by
Player ID: 244928103
------------------------------------------------
"""

import discord
import requests
from discord.ext import commands, tasks
from discord.ui import Select, View
from numpy import append
import asyncio
from util.__my_imge_path__ import *
img_url = my_image_url()
from util.__funktion__ import *
from discord_cogs.rust.player_observation.__funktion__player_observation import *
from util.__Mydiscord_funktions__ import *

#    Prevents the code from being executed when the file is imported as a module.
if __name__ == "player_observation":
    print("__function should not be executed when the file is imported as a module.\nThis was not the case!", "r")
else:
    pass

img_url = my_image_url()
# get the path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
bot_path = os.path.abspath(sys.argv[0])
bot_folder = os.path.dirname(bot_path)
# construct the path to the config.ini file relative to the current directory
config_dir = os.path.join(bot_folder, "config", "config.ini")


json_rust_observation_commands_data_dir = os.path.join(bot_folder, "config", "json", "observation_commands.json")
json_rust_observation_commands_data = read_json_file(json_rust_observation_commands_data_dir)
observation_commands = [re.sub(r'\{.*?\}', '', entry["command"].replace("```", "").replace(" ", ""))
            for entry in json_rust_observation_commands_data]


guild_id = read_config(config_dir, "client", "guild_id", "int")
if guild_id == None:
    guild_id = 1
guild_id = int(guild_id)

guild = discord.Object(id=guild_id)

file_path = os.path.dirname(sys.argv[0])
file_path_player_observation = os.path.dirname(os.path.realpath(__file__))

#file_path_temp = os.path.join(file_path_player_observation, "temp")
file_path_temp = Folder_gen("temp", file_path_player_observation)

player_observation_data_dir = os.path.join(bot_folder, "config", "json", "player_observation_data.json")
player_observation_data_dir = os.path.normpath(player_observation_data_dir)
content = {}
player_observation_data_dir = if_json_file_404(player_observation_data_dir, content)


f_name = File_name_with_time("player_id")
player_id_temp_dir = f"{file_path_temp}/{f_name}.temp"
player_id_temp_dir = os.path.normpath(player_id_temp_dir)
f_name = File_name_with_time("player_note")
player_note_temp_dir = f"{file_path_temp}/{f_name}.temp"
player_note_temp_dir = os.path.normpath(player_note_temp_dir)
f_name = File_name_with_time("player_name")
player_name_temp_dir = f"{file_path_temp}/{f_name}.temp"
player_name_temp_dir = os.path.normpath(player_name_temp_dir)


guild = discord.Object(id=guild_id)
player_observation_channel_id = int(read_config(config_dir, "channels", "player_observation_channel_id"))

Rust_Bot_Channel_ID = read_config(config_dir, "channels", "player_observation_channel_id")
if Rust_Bot_Channel_ID == None:
    Rust_Bot_Channel_ID = 1
Rust_Bot_Channel_ID = int(Rust_Bot_Channel_ID)


class New_player(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="add_player", description="Adds players to the observationlist.")
    @app_commands.describe(
        player_name="Rust Player_name or Steam_id",
        player_note="Note for the player.",
    )
    async def choise_team(self, interaction: discord.Interaction, player_name: str, player_note: str):
        self.player_name = player_name
        self.player_note = player_note

        # replace with your thinking emoji ID
        thinking = self.bot.get_emoji(123456789)
        # Send the embed with the thinking animation
        embed = discord.Embed(title="Adding player...", description=f"{thinking} Thinking...", color=discord.Color.blurple())
        defer_msg = await interaction.response.defer(ephemeral=True)

        battlemetrics_server_id = read_config(config_dir, "rust", "battlemetrics_server_id")

        if contains_only_numbers(player_name) == True:
            player_id = player_name
   
        else:
            player_id = get_player_id_from_name(player_name, battlemetrics_server_id)

        if player_id == None:
            sec_to_delta = 20
            delt_str = delt_str_time(sec_to_delta)
            
            s_url = f"https://www.battlemetrics.com/players?filter%5Bsearch%5D={player_name}&filter%5BplayerFlags%5D=&filter%5Bservers%5D={battlemetrics_server_id}&sort=-lastSeen"
            embed = discord.Embed(title=f"No search results with {player_name}", url=s_url, description="Try to find the player by yourself and add the ID to the next request with `id:{battlemetrics_player_id}`."+f"\n{delt_str}", color=0xff0000)
            await interaction.channel.send(embed=embed, delete_after= sec_to_delta)
        else:
            player_id = int(player_id)
            create_and_fill_temp_bridge(player_id, player_id_temp_dir)
            create_and_fill_temp_bridge(player_note, player_note_temp_dir)

            url = f"https://api.battlemetrics.com/players/{player_id}"
            response = requests.get(url)
            response_json = response.json()
            status_code = response.status_code

            Player_name = response_json["data"]["attributes"]["name"]
            create_and_fill_temp_bridge(Player_name, player_name_temp_dir)

            battlemetrics_server_id = read_config(config_dir, "rust", "battlemetrics_server_id")
            url = f"https://api.battlemetrics.com/players/{player_id}/servers/{battlemetrics_server_id}"
            response = requests.get(url)
            response_json = response.json()
            status_code = response.status_code

            try:
                player_online_status = response_json["data"]["attributes"]["online"]
                player_lastSeen = response_json["data"]["attributes"]["lastSeen"]
                time_convert = ISO_Time_to_Milisec(player_lastSeen)
                player_lastSeen = discord_time_convert(time_convert)
                played_on_server = True
            except:
                Player_server_data = Player_Server_info(player_id, battlemetrics_server_id)
                if Player_server_data == "Rate Limit Exceeded":
                    while True:
                        Player_server_data = Player_Server_info(player_id, battlemetrics_server_id)
                        if Player_server_data != "Rate Limit Exceeded":
                            break
                if Player_server_data == "400":
                    player_online_status = "never_played"

            if player_online_status == False or player_online_status == "never_played":
                if player_online_status == "never_played":

                    
                    embed = discord.Embed(title=f"{Player_name}", url=f"https://www.battlemetrics.com/players/{player_id}", description=("❌ | ID: "+str(player_id)), color=0xff0000)
                    value = f"❌ `Never played on that Server` ❌ | note: `{player_note}`"
                    embed.add_field(name=Player_name, value=value, inline=True)
                else:
                    embed = discord.Embed(title=f"{Player_name}", url=f"https://www.battlemetrics.com/players/{player_id}",description=("🔴 | ID: "+str(player_id)), color=0xff0000)
                    embed.add_field(name="Last Seen",value=f"{player_lastSeen}", inline=True)
                    embed.add_field(name="Note", value=f"{player_note}", inline=True)
                    embed.set_footer(text=f"Select team:")
            else:
                embed = discord.Embed(title=f"{Player_name}", url=f"https://www.battlemetrics.com/players/{player_id}",description=f"🟢 | ID: {player_id}", color=0xff8040)
                embed.add_field(name="Online since", value=f"{player_lastSeen}", inline=True)
                embed.add_field(name="Note", value=f"{player_note}", inline=True)
                embed.set_footer(text=f"Select team:")

            Team_list, Team_Note_list = Team_choice(player_observation_data_dir)
            Team_list_len = len(Team_list)

            x = -1
            options = [discord.SelectOption(label=f"🆕Create a new team.🆕", description=f"Add a new team for players."),]
            while True:
                x = x + 1
                if x == Team_list_len:
                    break
                try:
                    team_name = Team_list[x]
                    team_note = Team_Note_list[x]
                    options.append(discord.SelectOption(label=f"{team_name}", description=f"{team_note}"))
                except:
                    pass
            select = Select(options=options)

            async def my_callback(interaction):

                if f"{select.values[0]}" == f"🆕Create a new team.🆕":
                    await interaction.response.send_modal(modal_New_team())

                else:
                    player_id_int = int(read_and_delt_temp_bridge(player_id_temp_dir))
                    player_note_str = (read_and_delt_temp_bridge(player_note_temp_dir))
                    player_name_str = (read_and_delt_temp_bridge(player_name_temp_dir))
                    JSOn_data = read_json_file(player_observation_data_dir)
                    JSOn_data = add_player(JSOn_data, f"{select.values[0]}", Player_name, player_id, player_note)
                    fill_json_file(player_observation_data_dir, JSOn_data)         

                    embed = discord.Embed(
                        title=f"{Player_name}", description="added to team", color=0xff8040)
                    await interaction.response.send_message(embed=embed, ephemeral=True,)

            select.callback = my_callback
            view = View()
            view.add_item(select)
            sec_to_delta = 30
            delt_str = delt_str_time(sec_to_delta)
            embed.add_field(name="Time to delt", value=f"{delt_str}", inline=False)
            await interaction.channel.send(embed=embed, delete_after=sec_to_delta, view=view)


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
        print(f"Send Confrim / Cancel query.")

        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Cancelling', ephemeral=True)
        self.value = False
        self.stop()


class modal_New_team(ui.Modal, title="New Team",):

    New_Team_name = ui.TextInput(
        label="Name of the new team",
        style=discord.TextStyle.short,
        placeholder="Team name",
        required=True,
        max_length=None)
    
    New_team_note = ui.TextInput(
        label="Embed Titel:",
        style=discord.TextStyle.short,
        placeholder="Team note",
        required=True,
        max_length=None)

    print("modal_New_team: New_Team_name | New_team_note |")

    async def on_submit(self, interaction: discord.Interaction):

        embed = discord.Embed(title=self.New_Team_name, description=self.New_team_note, color=0xc0c0c0)
        view = Confirm_say()
        await interaction.response.send_message(embed=embed, ephemeral=True, view=view)

        print(f"Output modal_New_team: New_Team_name={self.New_Team_name} | New_team_note={self.New_team_note}")
        print(f"Send Confrim / Cancel query.")

        print("Send Discordembed: Test Result")
        await view.wait()
        if view.value is None:
            self.confirm_Button = False
            print(f'Timed out... self.confirm_Button = {self.confirm_Button}')

        elif view.value:
            self.confirm_Button = True

            embed = discord.Embed(title=self.New_Team_name, description=self.New_team_note, color=0xc0c0c0)

            Team_Card_embed_id = 0
            print(f'Confirmed... self.confirm_Button = {self.confirm_Button}')

            JSOn_data = read_json_file(player_observation_data_dir)
            JSOn_data = add_Team(JSOn_data, self.New_Team_name,
                                 self.New_team_note, Team_Card_embed_id)

            player_id_int = int(read_and_delt_temp_bridge(player_id_temp_dir))
            player_note_str = (read_and_delt_temp_bridge(player_note_temp_dir))
            player_name_str = (read_and_delt_temp_bridge(player_name_temp_dir))

            # add_player(dict, team, name, id, note):

            JSOn_data = add_player(
                JSOn_data, self.New_Team_name, player_name_str, player_id_int, player_note_str)

            fill_json_file(player_observation_data_dir, JSOn_data)

        else:
            self.confirm_Button = False
            print(f'Cancelled... self.confirm_Button = {self.confirm_Button}')
            # return self.confirm_Button, self.say_channel_id, self.say_title, self.say_text


class clear_observationlist(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="clear_observationlist", description="Deletes the Playerwatch list.")
    async def clear_data(
            self,
            interaction: discord.Integration):
        await interaction.response.send_modal(modal_confrim_delt())


class modal_confrim_delt(ui.Modal, title="Clear observationlist"):

    confirm_delt = ui.TextInput(label="Confirm with Yes", style=discord.TextStyle.short, placeholder="Confirm with Yes", required=True,)

    print("Send modal_confrim_delt: Confirm with Yes ")

    async def on_submit(self, interaction: discord.Interaction):
        confirm_delt = (str(self.confirm_delt)).lower()
        if str(confirm_delt) == "yes":

            JSOn_data = read_json_file(player_observation_data_dir)
            player_observation_data_dir_old = file_path_temp + "/" + \
                ((File_name_with_time("Team_data_old"))+".json")
            fill_json_file(player_observation_data_dir_old, JSOn_data)

            embed_ID_list = get_all_embed_IDs(JSOn_data)
            embed_ID_list_len = len(embed_ID_list)
            x = -1
            while True:
                x = x + 1
                if x == embed_ID_list_len or embed_ID_list_len == 0:
                    break
                #player_observation_channel_id = int(read_config(config_dir, "channels", "player_observation_channel_id"))
                try:
                    player_observation_channel = interaction.client.get_channel(
                        player_observation_channel_id)
                    msg = await player_observation_channel.fetch_message(embed_ID_list[x])
                    await msg.delete()
                    print(f"No msg delt", "blue")
                except:
                    print(f"No msg to delt", "blue")

            dictionary = {}
            fill_json_file(player_observation_data_dir, dictionary)
            embed = discord.Embed(
                title="observationlist", description="Watch list was cleared.", color=0xc0c0c0)
            await interaction.response.send_message(embed=embed, ephemeral=True)


class Delt_player(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="delt_player", description="Deletes players from the observationlist.")
    async def choise_player_to_delt(self, interaction: discord.Interaction):

        dict = read_json_file(player_observation_data_dir)
        Full_player_list = Get_all_player_list(dict)
        Full_player_list_len = len(Full_player_list)
        x = -1
        options = []
        while True:
            x = x + 1
            if x == Full_player_list_len:
                break
            name = Full_player_list[x]

            Team_name_from_player = Team_name_from_Player(dict, name)
            note = dict[Team_name_from_player][name]["note"]
            options.append(discord.SelectOption(
                label=f"{name}", description=f"{Team_name_from_player}"))
        select = Select(options=options)

        async def my_callback(interaction: discord.Interaction):

            name = select.values[0]

            dict = read_json_file(player_observation_data_dir)
            Team_name_from_player = Team_name_from_Player(dict, name)

            ID = dict[Team_name_from_player][name]["ID"]
            note = dict[Team_name_from_player][name]["note"]

            embed = discord.Embed(title=f"🚮 Should the {name} be deleted? 🚮")
            embed.add_field(name="Team", value=Team_name_from_player, inline=True)
            embed.add_field(name="Battlemetrics ID", value=ID, inline=True)
            embed.add_field(name="Note", value=note, inline=True)

            view = Confirm_say()
            await interaction.response.send_message(embed=embed, ephemeral=True, view=view)

            print(f"Send Confrim / Cancel query.")

            print("Send Discordembed: Test Result")
            await view.wait()
            if view.value is None:
                self.confirm_Button = False
                print(f'Timed out... self.confirm_Button = {self.confirm_Button}')
                # return self.confirm_Button, self.say_channel_id, self.say_title, self.say_text

            elif view.value:
                self.confirm_Button = True

                print(f'Confirmed... self.confirm_Button = {self.confirm_Button}')
                JSOn_data = read_json_file(player_observation_data_dir)
                Team = Team_name_from_Player(JSOn_data, name)
                JSOn_data = delt_player(dict, Team, name)
                fill_json_file(player_observation_data_dir, JSOn_data)

            else:
                self.confirm_Button = False
                print(f'Cancelled... self.confirm_Button = {self.confirm_Button}')
                # return self.confirm_Button, self.say_channel_id, self.say_title, self.say_text

        select.callback = my_callback
        view = View()
        view.add_item(select)
        embed = discord.Embed(title="Delete player", description="Select a player!", color=0xff8040)
        await interaction.response.send_message(embed=embed, ephemeral=True, view=view)


class Delt_Team(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="delt_team", description="Delete team from observationlist.")
    async def choise_Team_to_delt(self, interaction: discord.Interaction):

        dict = read_json_file(player_observation_data_dir)
        Team_list = list(dict.keys())
        Team_list_len = len(Team_list)
        x = -1
        options = []
        while True:
            x = x + 1
            if x == Team_list_len:
                break
            Team_name = Team_list[x]

            note = dict[Team_name]["note"]
            options.append(discord.SelectOption(
                label=f"{Team_name}", description=f"{note}"))
        select = Select(options=options)

        async def my_callback(interaction: discord.Interaction):

            Team_name = select.values[0]

            dict = read_json_file(player_observation_data_dir)
            # ad team names

            note = dict[Team_name]["note"]

            embed = discord.Embed(title=f"🚮 Should the team {Team_name} be deleted? 🚮")
            embed.add_field(name="Note", value=note, inline=True)

            view = Confirm_say()
            await interaction.response.send_message(embed=embed, ephemeral=True, view=view)

            print(f"Send Confrim / Cancel query.")

            print("Send Discordembed: Test Result")
            await view.wait()
            if view.value is None:
                self.confirm_Button = False
                print(f'Timed out... self.confirm_Button = {self.confirm_Button}')
                # return self.confirm_Button, self.say_channel_id, self.say_title, self.say_text

            elif view.value:
                self.confirm_Button = True

                print(f'Confirmed... self.confirm_Button = {self.confirm_Button}')

                JSOn_data = read_json_file(player_observation_data_dir)
                embed_id = JSOn_data[Team_name]["embed_id"]

                JSOn_data = delt_Team(JSOn_data, Team_name)
                fill_json_file(player_observation_data_dir, JSOn_data)

                player_observation_channel = interaction.client.get_channel(player_observation_channel_id)
                print(f"msg delt: {embed_id}: Team embed ({Team_name})")
                msg = await player_observation_channel.fetch_message(embed_id)
                await msg.delete()

            else:
                self.confirm_Button = False
                print(f'Cancelled... self.confirm_Button = {self.confirm_Button}')
                # return self.confirm_Button, self.say_channel_id, self.say_title, self.say_text

        select.callback = my_callback
        view = View()
        view.add_item(select)
        embed = discord.Embed(title="Delete player", description="Select a player!", color=0xff8040)
        await interaction.response.send_message(embed=embed, ephemeral=True, view=view)


class player_observation_loops(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):

        self.bot = bot
        self.myLoop.start(bot)

    Time_wait = 60


    @tasks.loop(seconds=Time_wait)  # repeat after every 10 seconds
    async def myLoop(self, bot,):

        await self.bot.wait_until_ready()

        battlemetrics_server_id = read_config(config_dir, "rust", "battlemetrics_server_id")
        JSOn_data = read_json_file(player_observation_data_dir)
        Team_list = list(JSOn_data.keys())
        Team_list_len = len(Team_list)

        print(f"Loop Start")
        x = -1
        while True:

            x = x + 1
            if x == Team_list_len:
                break
            
            JSOn_data = read_json_file(player_observation_data_dir)
    	    
            Team_Name = Team_list[x]
            team_exist = if_team_in_json(player_observation_data_dir,Team_Name)
            if team_exist:
                try:
                    Team_note = JSOn_data[f"{Team_list[x]}"]["note"]
                    Team_embed_id = JSOn_data[f"{Team_list[x]}"]["embed_id"]
                    Last_Status = JSOn_data[f"{Team_list[x]}"]["Last_Status"]

                    Never_played = False

                    online = Team_online_status(JSOn_data, Team_Name, battlemetrics_server_id)
                except:
                    print (f"--> No {Team_list[x]} anymore.")
                    pass

                if online == "Rate Limit Exceeded":
                    print_x = -1
                    while True:
                        print_x = print_x + 1
                        online = Team_online_status(
                            JSOn_data, Team_Name, battlemetrics_server_id)
                        if online != "Rate Limit Exceeded":
                            print(
                                f"print_x:{print_x} Team_online_status = Rate Limit Exceeded")
                            break

                time_stemp = time.time()
                Discord_time_stemp = discord_time_convert(int(time_stemp))
                description = f"Team note: `{Team_note}` \n updated {Discord_time_stemp}"
                Sub_alert = False

                if online == True:
                    embed = discord.Embed(title=Team_Name, description=description, color=0x808040)
                    if Last_Status == False:
                        Sub_alert = True

                        JSOn_data = read_json_file(player_observation_data_dir)
                        JSOn_data[f"{Team_list[x]}"]["Last_Status"] = True
                        fill_json_file(player_observation_data_dir, JSOn_data)

                else:

                    embed = discord.Embed(title=Team_Name, description=description, color=0xff0000)
                    if Last_Status == True:
                        Sub_alert = True

                    JSOn_data = read_json_file(player_observation_data_dir)
                    try:
                        JSOn_data[f"{Team_list[x]}"]["Last_Status"] = False
                        fill_json_file(player_observation_data_dir, JSOn_data)
                    except:
                        print(f"--> no team: {Team_list[x]} no more in data")
                        

                # JSOn_data = read_json_file(player_observation_data_dir)

                Player_list = get_all_Player_from_a_Team(JSOn_data, Team_Name)
                Player_list_len = len(Player_list)
                y = -1
                while True:
                    y = y + 1
                    if y == Player_list_len:
                        break
                    
                    #JSOn_data = read_json_file(player_observation_data_dir)
                    Player = Player_list[y]
                    do_player_exist = player_exists(player_observation_data_dir, Player)
                    if do_player_exist:
                        Player_id = JSOn_data[Team_Name][Player]["ID"]
                        Player_note = JSOn_data[Team_Name][Player]["note"]
                        Plyer_first_name = Player
                        name_cange = Player_name_cange(JSOn_data, Team_Name, Player)
                        Player_Bat_url = f"https://www.battlemetrics.com/players/{Player_id}"
                        await asyncio.sleep(10)
                        Player_server_data = Player_Server_info(Player_id, battlemetrics_server_id)
                        if Player_server_data == "Rate Limit Exceeded":
                            x = x - 1
                            break
                        if Player_server_data == "400":
                            Never_played = True
                            value = f"❌ `Never played on that Server` ❌ \n note: `{Player_note}` \n Player ID: [{Player_id}]({Player_Bat_url})"
                            embed.add_field(name=Player, value=value, inline=True)

                        else:

                            Online_ico = Player_server_data[0]
                            lastSeen = Player_server_data[1]
                            timePlayed = Player_server_data[2]
                            Player_Server_url = Player_server_data[3]
                            if "[Steam URL]" in Player_note:
                                value = f" {Online_ico}  {lastSeen} \n ServerTime: `{timePlayed}h` \n note: {Player_note} \n Player ID: [{Player_id}]({Player_Bat_url})"
                            else:
                                value = f" {Online_ico}  {lastSeen} \n ServerTime: `{timePlayed}h` \n note: `{Player_note}` \n Player ID: [{Player_id}]({Player_Bat_url})"

                            if str(name_cange[0]) == str(True):
                                embed.add_field(name=f"Oldname: {Player}\n🆕: {name_cange[1]}", value=value, inline=True)
                            else:
                                embed.add_field(name=f"{Player}", value=value, inline=True)
                    else:
                        print (f"--> {Player} not anymore in data")

                if Sub_alert == True:
                    JSOn_data = read_json_file(player_observation_data_dir)
                    Sub_Discord_ID_list = list(JSOn_data[f"{Team_list[x]}"]["Sub_Discord_ID_list"])
                    Sub_Discord_ID_list_len = len(Sub_Discord_ID_list)
                    if Sub_Discord_ID_list_len == 0:
                        pass
                    else:
                        z = -1
                        while True:
                            z = z + 1
                            if z == Sub_Discord_ID_list_len:
                                break
                            Player_ID = Sub_Discord_ID_list[z]
                            User = await self.bot.fetch_user(int(Player_ID))
                            embed_list = []
                            if online == True:
                                embed_New_Status = discord.Embed(
                                    title="🟢 New Online Status 🟢", description=f"Team `{Team_Name}` is now online! <#{player_observation_channel_id}>", color=0xff8000)
                                embed_list.append(embed_New_Status)
                                embed_list.append(embed)
                                await User.send(embeds=embed_list)
                            else:
                                embed_New_Status = discord.Embed(
                                    title="🔴 New Online Status 🔴", description=f"Team `{Team_Name}` is now offline! <#{player_observation_channel_id}>", color=0xff0000)
                                embed_list.append(embed_New_Status)
                                embed_list.append(embed)
                                await User.send(embeds=embed_list)

                try:
                    player_observation_channel = self.bot.get_channel(
                        player_observation_channel_id)
                    msg = await player_observation_channel.fetch_message(Team_embed_id)
                    await msg.edit(embed=embed)
                    print(
                        f"Discord: Edit Embed from Team [{Team_Name}] msg.id: [{msg.id}]")
                except:

                    try:
                        is_team_in_data = if_team_in_json(player_observation_data_dir, Team_Name)
                        if is_team_in_data:
                         
                            JSOn_data = read_json_file(player_observation_data_dir)
                            player_observation_channel = self.bot.get_channel(player_observation_channel_id)
                            Team_Card_embed = await player_observation_channel.send(embed=embed, view=Sub_button())
                            Team_Card_embed_id = (Team_Card_embed.id)
                            JSOn_data[Team_Name]["embed_id"] = Team_Card_embed_id
                            fill_json_file(player_observation_data_dir, JSOn_data)
                            print(f"Discord: send new Embed from Team [{Team_Name}] msg.id: [{Team_Card_embed_id}]")
                        else:
                            print(f"--> {Team_Name} no more in data")
                    except:
                        pass
            else:
                print(f"--> {Team_Name} no more in data")

class Sub_button(discord.ui.View,):
    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label="🔔", style=discord.ButtonStyle.green, custom_id="Sub")
    async def New_Sub(self, interaction: discord.Interaction, Button: discord.ui.Button):

        User = interaction.user
        User_ID = interaction.user.id

        embed_ID = interaction.message.id
        JSOn_data = read_json_file(player_observation_data_dir)
        Team_data = from_embed_ID_to_data(JSOn_data, embed_ID)
        Team_name = Team_data[0]
        Sub_Discord_ID_list = list(Team_data[1])
        Sub_Discord_ID_list.append

        Team_data = from_embed_ID_to_data(JSOn_data, embed_ID)
        Team_name = Team_data[0]
        Sub_Discord_ID_list = list(Team_data[1])

        #json_object = json.dumps(JSOn_data, indent = 4)

        if User_ID in Sub_Discord_ID_list:
            await interaction.response.send_message(f"You already subscribe the team: {Team_name}", ephemeral=True)
        else:
            Sub_Discord_ID_list.append(User_ID)
            JSOn_data[f"{Team_name}"]["Sub_Discord_ID_list"] = Sub_Discord_ID_list
            fill_json_file(player_observation_data_dir, JSOn_data)

            text = f"I will inform you here via Direct Message when the online status of {Team_name} has changed."
            embed = discord.Embed(title=f"🔔 You are now subscribing the team: {Team_name} 🔔", description=text, color=0xff8040)
            await User.send(embed=embed)

            text = f"I will inform you via Direct Message when the online status of {Team_name} changedt."
            embed = discord.Embed(title=f"🔔 You are now subscribing the team: {Team_name} 🔔", description=text, color=0xff8040)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="🔕", style=discord.ButtonStyle.grey, custom_id="UnSub")
    async def deltSub(self, interaction: discord.Interaction, Button: discord.ui.Button):
        User = interaction.user
        User_ID = interaction.user.id

        embed_ID = interaction.message.id
        JSOn_data = read_json_file(player_observation_data_dir)
        Team_data = from_embed_ID_to_data(JSOn_data, embed_ID)
        Team_name = Team_data[0]
        Sub_Discord_ID_list = list(Team_data[1])
        if User_ID in Sub_Discord_ID_list:
            Sub_Discord_ID_list.remove(User_ID)
            JSOn_data[f"{Team_name}"]["Sub_Discord_ID_list"] = Sub_Discord_ID_list
            fill_json_file(player_observation_data_dir, JSOn_data)

            text = f"I will no longer inform you here via Direct Message if the online status ofn {Team_name} has changed."
            embed = discord.Embed(title=f"🔕 You are now unsubscribing to the team: {Team_name} 🔕", description=text, color=0xff0000)
            await User.send(embed=embed)

            text = f"I will no longer inform you via Direct Message when the online status of {Team_name} changedt."
            embed = discord.Embed(title=f"🔕 You are now unsubscribing to the team: {Team_name} 🔕", description=text, color=0xff0000)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(f"You currently subscribe to the team {Team_name} not.", ephemeral=True)

    @discord.ui.button(label="Delete all subscriptions", style=discord.ButtonStyle.red, custom_id="UnSubAll")
    async def deltAllSubs(self, interaction: discord.Interaction, Button: discord.ui.Button):
        User = interaction.user
        User_ID = interaction.user.id

        embed_ID = interaction.message.id
        JSOn_data = read_json_file(player_observation_data_dir)
        JSOn_data = delt_all_Player_subs(JSOn_data, User_ID)
        fill_json_file(player_observation_data_dir, JSOn_data)

        text = f" You no longer subscribe to a team."
        embed = discord.Embed(title=f"🔕", description=text, color=0xff0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)



class all_players(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="all_players", description="Show a list of all players who are online")
    async def all_players_list_send(self, interaction: discord.Interaction):
        battlemetrics_server_id = read_config(config_dir, "rust", "battlemetrics_server_id")
        data = get_all_online_player(battlemetrics_server_id)
        data_len = len(data)

        player_observation_channel = await self.bot.fetch_channel(player_observation_channel_id)
        str_list = []
        for name, player_id in data.items():
            player_id = int(player_id.pop())
            player_bat_url = f"https://www.battlemetrics.com/players/{player_id}"
            id_str = f"[{player_id}]({player_bat_url})"
            str_list.append(f"{name} | `{player_id}`")

        str = "\n".join(str_list)

        sec_to_delta = 60
        delt_msg_str = delt_str_time(sec_to_delta)

        all_player_embeds = []
        embed_delt = discord.Embed(title=f"{delt_msg_str}", colour=0xffffff)
        
        all_player_embeds.append(embed_delt)
        # await interaction.response.send_message(f"<#{player_observation_channel_id}> The list will be automatically deleted in 60 sec.", ephemeral=True)
        
        # Überprüfen, ob die Länge des Strings größer als 1000 ist
        players = str.split('\n')
        chunks = []
        current_chunk = players[0]
        
        for player in players[1:]:
            if len(current_chunk) + len(player) < 1000:
                current_chunk += '\n' + player
            else:
                chunks.append(current_chunk)
                current_chunk = player
        
        if current_chunk:
            chunks.append(current_chunk)
        
        for i, chunk in enumerate(chunks):
            chunk_embed = discord.Embed(title=f"{data_len} Player Online (Teil {i+1})", description=chunk)
            all_player_embeds.append(chunk_embed)
            #await player_observation_channel.send(embed=chunk_embed, delete_after=60)
        await interaction.response.send_message(embeds=all_player_embeds, delete_after=sec_to_delta)

class auto_smg_delt_player_observation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_dir = config_dir

    @commands.Cog.listener()
    async def on_message(self, message):

        current_unix_time = int(time.time())
        delt_delay_sec = 60
        delt_msg_str = delt_str_time(delt_delay_sec)

        player_observation = message.channel
        # Check if the message is from a bot to avoid potential loops
        if message.author.bot:
            return
        if message.channel.id != player_observation_channel_id:
            return
        else:
            
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(f"\nplayer_observation - {current_time}:\n")
            print(f"Msg delt in 10s ec from: {message.author.name}:")
            print(f"msg:\n{message.content}\n")
            await message.delete(delay = delt_delay_sec)
            if message.content not in observation_commands:
                rust_team_text_channel_id = read_config(config_dir,"channels", "rust_team_text_channel_id", "int")
                embeds_list = []

                description = f"<@{message.author.id}>\nThe observation **channel is not a chat channel.**\nPlease utilize the channel designated for chatting, which is <#{rust_team_text_channel_id}>\n\n{delt_msg_str}\n\n**In this channel, you can use the following commands:**"
                embed_attention = discord.Embed(title="Please Note: Observation Channel Usage", description=description, colour=0x004000)
                embed_attention.set_thumbnail(url=img_url.piktogramm.attention())
                embeds_list.append(embed_attention)

                icon_url = message.author.display_avatar
                thumbnail_url = img_url.piktogramm.i
                embed = discord.Embed(title="#rust-player-observation", color=0x8080ff)
                embed.set_author(name=f"@{message.author.name}",icon_url=icon_url)
                embed.set_thumbnail(url=thumbnail_url)

                # Max number of fields per embed
                max_fields_per_embed = 25

                # Counter for fields
                field_count = 0

                for item in json_rust_observation_commands_data:
                    if field_count < max_fields_per_embed:
                        command = item["command"]
                        description = item["description"]
                        embed.add_field(name=command, value=description, inline=False)
                        field_count += 1
                    else:
                        # Reset field count
                        field_count = 0
                        # Append current embed to the list
                        embeds_list.append(embed)
                        # Create a new embed for the next set of fields
                        embed = discord.Embed(title="#rust-player-observation", color=0x8080ff)
                        embed.set_author(name=f"@{message.author.name}", icon_url=icon_url)
                        embed.set_thumbnail(url=thumbnail_url)
                        # Add the current field to the new embed
                        embed.add_field(name=command, value=description, inline=True)
                        # Increment field count for the new embed
                        field_count += 1

                # Append the last embed to the list
                embeds_list.append(embed)
                await player_observation.send(embeds=embeds_list, delete_after=delt_delay_sec)

                guild = message.guild
                rust_team_text_channel = discord.utils.get(guild.text_channels, id=rust_team_text_channel_id)
                content =f"Message from <@{message.author.id}>\n> {message.content}"
                await rust_team_text_channel.send(content=content)


async def setup(bot: commands.Bot):
    await bot.add_cog(New_player(bot), guild=discord.Object(guild_id))
    await bot.add_cog(clear_observationlist(bot), guild=discord.Object(guild_id))
    await bot.add_cog(player_observation_loops(bot), guild=discord.Object(guild_id))
    await bot.add_cog(Delt_player(bot), guild=discord.Object(guild_id))
    await bot.add_cog(Delt_Team(bot), guild=discord.Object(guild_id))
    await bot.add_cog(all_players(bot), guild=discord.Object(guild_id))
    await bot.add_cog(auto_smg_delt_player_observation(bot), guild=discord.Object(guild_id))
    bot.add_view(Sub_button())
