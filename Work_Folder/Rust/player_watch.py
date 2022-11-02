import discord
from discord.ui import Select
from discord.ui import View
from discord.ext import commands
from numpy import append
from Imports import*
import requests
from discord.ext import tasks

file_path = os.path.dirname(sys.argv[0])
file_path_player_watch = f"{file_path}/Work_Folder/Rust"

file_path_temp = f"{file_path_player_watch}/temp" 
file_path_temp = Folder_gen_all("temp", file_path_temp )
file_path_Team_data = f"{file_path_player_watch}/Team_data.json"


player_id_temp_dir = file_path_temp +"/"+((Datei_name_mit_Zeit("player_id"))+".temp")
player_note_temp_dir = file_path_temp +"/"+((Datei_name_mit_Zeit("player_note"))+".temp")
player_name_temp_dir = file_path_temp +"/"+((Datei_name_mit_Zeit("player_name"))+".temp")

guild_id = int(read_config(config_dir, "Client", "guild_id"))
guild = discord.Object(id=guild_id)
Rust_Bot_Channel_ID = int(read_config(config_dir, "Channel", "Rust_Bot_Channel_ID"))


class New_player(commands.Cog):
    def __init__(self, bot:commands.Bot)-> None:
        self.bot = bot
    @app_commands.command(name = "add_player", description="Fügt Spieler der Watchlist hinzu.")

    @app_commands.describe( 
        player_id = "Rust Player ID from Battlemetrics",
        player_note = "Notiz für den Spieler.",
        )


    async def choise_team(self, interaction: discord.Interaction, player_id: int, player_note: str):
        self.player_id = player_id
        self.player_note = player_note

        create_and_fill_temp_bridge(player_id ,player_id_temp_dir)
        create_and_fill_temp_bridge(player_note ,player_note_temp_dir)

        url = f"https://api.battlemetrics.com/players/{player_id}"
        response = requests.get(url)
        response_json = response.json()
        status_code = response.status_code

        Player_name = response_json["data"]["attributes"]["name"]
        create_and_fill_temp_bridge(Player_name , player_name_temp_dir)

        battlemetrics_Server_ID = read_config(config_dir, "Rust", "battlemetrics_Server_ID")
        url = f"https://api.battlemetrics.com/players/{player_id}/servers/{battlemetrics_Server_ID}"
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

            Player_server_data = Player_Server_info(player_id, battlemetrics_Server_ID)
            if Player_server_data == "Rate Limit Exceeded":
                while True:
                    Player_server_data = Player_Server_info(player_id, battlemetrics_Server_ID)
                    if Player_server_data != "Rate Limit Exceeded":
                        break
            if Player_server_data == "400":
                player_online_status = "never_played"

        if player_online_status == False or player_online_status == "never_played":
            if player_online_status == "never_played":
                embed=discord.Embed(title=f"{Player_name}", url=f"https://www.battlemetrics.com/players/{player_id}", description=("❌ | ID: "+str(player_id)), color=0xff0000)
                value = f"❌ `Never played on that Server` ❌ | note: `{player_note}`"
                embed.add_field(name=Player_name, value= value , inline=True)
            else:
                embed=discord.Embed(title=f"{Player_name}", url=f"https://www.battlemetrics.com/players/{player_id}", description=("🔴 | ID: "+str(player_id)), color=0xff0000)
                embed.add_field(name="Last Seen", value=f"{player_lastSeen}", inline=True)
                embed.add_field(name="Note", value=f"{player_note}", inline=True)
                embed.set_footer(text=f"Team auswählen:")
        else:
            embed=discord.Embed(title=f"{Player_name}", url=f"https://www.battlemetrics.com/players/{player_id}", description=f"🟢 | ID: {player_id}", color=0xff8040)
            embed.add_field(name="Online seit", value=f"{player_lastSeen}", inline=True)
            embed.add_field(name="Note", value=f"{player_note}", inline=True)
            embed.set_footer(text=f"Team auswählen:")

        Team_list = (Team_choice(file_path_Team_data)[0])
        Team_Note_list = (Team_choice(file_path_Team_data)[1])
        Team_list_len = len(Team_list)

        x = -1
        options =[discord.SelectOption(label=f"🆕Neues Team erstellen.🆕", description=f"Neues Team für Spieler hinzufügen."),]
        while True:
            x = x + 1
            if x == Team_list_len:
                break
            team_name = Team_list[x]
            team_note = Team_Note_list[x]
            options.append(discord.SelectOption(label=f"{team_name}", description=f"{team_note}"))
        select  = Select(options = options)

        async def my_callback(interaction):
            
            if f"{select.values[0]}" == f"🆕Neues Team erstellen.🆕":
                await interaction.response.send_modal(modal_New_team())
            
            else:
                player_id_int = int(read_and_delt_temp_bridge(player_id_temp_dir))
                player_note_str = (read_and_delt_temp_bridge(player_note_temp_dir))
                player_name_str = (read_and_delt_temp_bridge(player_name_temp_dir))
                JSOn_data = open_JSOn_File(file_path_Team_data)
                JSOn_data = add_player(JSOn_data,f"{select.values[0]}", Player_name, player_id, player_note)
                Fill_JSOn_File(file_path_Team_data, JSOn_data)
                embed=discord.Embed(title=f"{Player_name}", description="zu Team hinzugefügt", color=0xff8040)
                await interaction.response.send_message(embed=embed, ephemeral=True,)

        select.callback = my_callback
        view = View()
        view.add_item(select)
        await interaction.response.send_message(embed=embed, ephemeral=True, view=view)


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
        log(f"Send Confrim / Cancel abfrage.")


        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Cancelling', ephemeral=True)
        self.value = False
        self.stop()



class modal_New_team( ui.Modal, title="New Team",):
    
    New_Team_name = ui.TextInput(label ="Name des neuen Teams", style = discord.TextStyle.short, placeholder="Team name", required=True, max_length=None)
    New_team_note = ui.TextInput(label ="Embed Titel:", style = discord.TextStyle.short, placeholder="Team Notize", required=True, max_length=None)
    
    log("modal_New_team: New_Team_name | New_team_note |")
    async def on_submit(self, interaction: discord.Interaction):

        embed=discord.Embed(title=self.New_Team_name, description=self.New_team_note, color=0xc0c0c0)
        view = Confirm_say()
        await interaction.response.send_message(embed=embed, ephemeral=True, view=view)
        
        log(f"Output modal_New_team: New_Team_name={self.New_Team_name} | New_team_note={self.New_team_note}")
        log (f"Send Confrim / Cancel abfrage.")


        log("Send Discordembed: Test Result")
        await view.wait()
        if view.value is None:
            self.confirm_Button = False
            log(f'Timed out... self.confirm_Button = {self.confirm_Button}')
            #return self.confirm_Button, self.say_channel_id, self.say_title, self.say_text

        elif view.value:
            self.confirm_Button = True

            embed=discord.Embed(title=self.New_Team_name, description=self.New_team_note, color=0xc0c0c0)
            #Rust_Bot_Channel_ID = int(read_config(config_dir, "Channel", "Rust_Bot_Channel_ID"))
            #Channel = interaction.client.get_channel(Rust_Bot_Channel_ID)
            #Team_Card_embed = await Channel.send(embed=embed, view=Sub_button())
            #Team_Card_embed_id = (Team_Card_embed.id)
            Team_Card_embed_id = 0
            log(f'Confirmed... self.confirm_Button = {self.confirm_Button}')
            #return self.confirm_Button, self.say_channel_id, self.say_title, self.say_text

            JSOn_data = open_JSOn_File(file_path_Team_data)
            JSOn_data = add_Team(JSOn_data, self.New_Team_name, self.New_team_note, Team_Card_embed_id)

            player_id_int = int(read_and_delt_temp_bridge(player_id_temp_dir))
            player_note_str = (read_and_delt_temp_bridge(player_note_temp_dir))
            player_name_str = (read_and_delt_temp_bridge(player_name_temp_dir))


            #add_player(dict, team, name, id, note):

            JSOn_data = add_player(JSOn_data, self.New_Team_name,player_name_str, player_id_int, player_note_str)


            Fill_JSOn_File(file_path_Team_data,JSOn_data)

        else:
            self.confirm_Button = False
            log(f'Cancelled... self.confirm_Button = {self.confirm_Button}')
            #return self.confirm_Button, self.say_channel_id, self.say_title, self.say_text


class clear_watchlist(commands.Cog):
    def __init__(self, bot:commands.Bot)-> None:
        self.bot = bot

    @app_commands.command(name = "clear_watchlist", description="Löscht die Playerwatch list.")

    async def clear_data(
        self,
        interaction: discord.Integration):
        await interaction.response.send_modal(modal_confrim_delt())

class modal_confrim_delt(ui.Modal, title="Clear Watchlist"):

    confirm_delt = ui.TextInput(label ="Bestätige mit Ja", style = discord.TextStyle.short, placeholder="Bestätige mit Ja", required=True,)

    log("Send modal_confrim_delt: Bestätige mit Ja ")
    async def on_submit(self, interaction: discord.Interaction ):
        confirm_delt = (str(self.confirm_delt)).lower()
        if str(confirm_delt) == "ja":

            JSOn_data = open_JSOn_File(file_path_Team_data)
            file_path_Team_data_old = file_path_temp +"/"+ ((Datei_name_mit_Zeit("Team_data_old"))+".json")
            Fill_JSOn_File(file_path_Team_data_old ,JSOn_data)

            embed_ID_list = get_all_embed_IDs(JSOn_data)
            embed_ID_list_len = len(embed_ID_list)
            x = -1
            while True:
                x = x + 1
                if x == embed_ID_list_len:
                    break
                #Rust_Bot_Channel_ID = int(read_config(config_dir, "Channel", "Rust_Bot_Channel_ID"))
                Rust_Bot_Channel = interaction.client.get_channel(Rust_Bot_Channel_ID)
                msg = await Rust_Bot_Channel.fetch_message(embed_ID_list[x])
                await msg.delete()


            dictionary = {"Teams":{}}
            Fill_JSOn_File(file_path_Team_data ,dictionary)
            embed=discord.Embed(title="Watchlist", description="Watch liste wurde ge-cleart.", color=0xc0c0c0)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        


class Delt_player(commands.Cog):
    def __init__(self, bot:commands.Bot)-> None:
        self.bot = bot
    @app_commands.command(name = "delt_player", description="Löscht Spieler von der Watchlist.")


    async def choise_player_to_delt(self, interaction: discord.Interaction):

        dict = open_JSOn_File(file_path_Team_data)
        Full_player_list = Get_all_player_list(dict)
        Full_player_list_len = len(Full_player_list)
        x = -1
        options =[]
        while True:
            x = x + 1
            if x == Full_player_list_len:
                break
            name = Full_player_list[x]


            Team_name_from_player = Team_name_from_Player(dict, name)
            note = dict["Teams"][Team_name_from_player][name]["note"]
            options.append(discord.SelectOption(label=f"{name}", description=f"{Team_name_from_player}"))
        select  = Select(options = options)

        async def my_callback(interaction: discord.Interaction):

            name = select.values[0]

            dict = open_JSOn_File(file_path_Team_data)
            Team_name_from_player = Team_name_from_Player(dict, name)

            ID = dict["Teams"][Team_name_from_player][name]["ID"]
            note = dict["Teams"][Team_name_from_player][name]["note"]

            embed=discord.Embed(title=f"🚮 Soll der {name} gelöscht werden? 🚮")
            embed.add_field(name="Team", value=Team_name_from_player, inline=True)
            embed.add_field(name="Battlemetrics ID", value=ID, inline=True)
            embed.add_field(name="Note", value=note, inline=True)

            view = Confirm_say()
            await interaction.response.send_message(embed=embed, ephemeral=True, view=view)
            
            log (f"Send Confrim / Cancel abfrage.")


            log("Send Discordembed: Test Result")
            await view.wait()
            if view.value is None:
                self.confirm_Button = False
                log(f'Timed out... self.confirm_Button = {self.confirm_Button}')
                #return self.confirm_Button, self.say_channel_id, self.say_title, self.say_text

            elif view.value:
                self.confirm_Button = True

                log(f'Confirmed... self.confirm_Button = {self.confirm_Button}')
                JSOn_data = open_JSOn_File(file_path_Team_data)
                Team = Team_name_from_Player(JSOn_data, name)
                JSOn_data = delt_player (dict, Team, name)
                Fill_JSOn_File(file_path_Team_data, JSOn_data)

            else:
                self.confirm_Button = False
                log(f'Cancelled... self.confirm_Button = {self.confirm_Button}')
                #return self.confirm_Button, self.say_channel_id, self.say_title, self.say_text

        select.callback = my_callback
        view = View()
        view.add_item(select)
        embed=discord.Embed(title="Spieler löschen", description="Wähle einen Spieler aus!", color=0xff8040)
        await interaction.response.send_message(embed=embed, ephemeral=True, view=view)





class Delt_Team(commands.Cog):
    def __init__(self, bot:commands.Bot)-> None:
        self.bot = bot
    @app_commands.command(name = "delt_team", description="Löscht Team von der Watchlist.")


    async def choise_Team_to_delt(self, interaction: discord.Interaction):

        dict = open_JSOn_File(file_path_Team_data)
        Team_list = list(dict["Teams"].keys())
        Team_list_len = len(Team_list)
        x = -1
        options =[]
        while True:
            x = x + 1
            if x == Team_list_len:
                break
            Team_name = Team_list[x]

            note = dict["Teams"][Team_name]["note"]
            options.append(discord.SelectOption(label=f"{Team_name}", description=f"{note}"))
        select  = Select(options = options)

        async def my_callback(interaction: discord.Interaction):

            Team_name = select.values[0]

            dict = open_JSOn_File(file_path_Team_data)
            ## ad team names
            
            note = dict["Teams"][Team_name]["note"]

            embed=discord.Embed(title=f"🚮 Soll das Team {Team_name} gelöscht werden? 🚮")
            embed.add_field(name="Note", value=note, inline=True)

            view = Confirm_say()
            await interaction.response.send_message(embed=embed, ephemeral=True, view=view)
            
            log (f"Send Confrim / Cancel abfrage.")


            log("Send Discordembed: Test Result")
            await view.wait()
            if view.value is None:
                self.confirm_Button = False
                log(f'Timed out... self.confirm_Button = {self.confirm_Button}')
                #return self.confirm_Button, self.say_channel_id, self.say_title, self.say_text

            elif view.value:
                self.confirm_Button = True

                log(f'Confirmed... self.confirm_Button = {self.confirm_Button}')

                JSOn_data = open_JSOn_File(file_path_Team_data)
                embed_id = JSOn_data["Teams"][Team_name]["embed_id"]


                JSOn_data = delt_Team (JSOn_data, Team_name)
                Fill_JSOn_File(file_path_Team_data, JSOn_data)

                
                Rust_Bot_Channel = interaction.client.get_channel(Rust_Bot_Channel_ID)
                log (f"msg delt: {embed_id}: Team embed ({Team_name})")
                msg = await Rust_Bot_Channel.fetch_message(embed_id)
                await msg.delete()

            else:
                self.confirm_Button = False
                log(f'Cancelled... self.confirm_Button = {self.confirm_Button}')
                #return self.confirm_Button, self.say_channel_id, self.say_title, self.say_text

        select.callback = my_callback
        view = View()
        view.add_item(select)
        embed=discord.Embed(title="Spieler löschen", description="Wähle einen Spieler aus!", color=0xff8040)
        await interaction.response.send_message(embed=embed, ephemeral=True, view=view)

class Player_watch_loops(commands.Cog, commands.Bot):
    def __init__ (self, bot:commands.Bot):

        self.bot = bot
        self.myLoop.start(bot)

    Time_wait = 60
    @tasks.loop(seconds = Time_wait) # repeat after every 10 seconds
    
    
    async def myLoop(self,bot,):
        await self.bot.wait_until_ready()
        battlemetrics_Server_ID = (read_config(config_dir, "Rust", "battlemetrics_Server_ID"))
        JSOn_data = open_JSOn_File(file_path_Team_data)
        Team_list = list(JSOn_data["Teams"].keys())
        Team_list_len = len(Team_list)
        log(f"Loop Start")
        x = -1
        while True:
    
            x = x + 1
            if x == Team_list_len:
                break
            
            Team_Name = Team_list[x]
            Team_note = JSOn_data["Teams"][f"{Team_list[x]}"]["note"]
            Team_embed_id = JSOn_data["Teams"][f"{Team_list[x]}"]["embed_id"]
            Last_Status = JSOn_data["Teams"][f"{Team_list[x]}"]["Last_Status"]

            Never_played = False

            online = Team_online_status(JSOn_data, Team_Name, battlemetrics_Server_ID)



            if online == "Rate Limit Exceeded":
                print_x = -1
                while True:
                    print_x = print_x + 1
                    online = Team_online_status(JSOn_data, Team_Name, battlemetrics_Server_ID)
                    if online != "Rate Limit Exceeded":
                        print (f"print_x:{print_x} Team_online_status = Rate Limit Exceeded")
                        break

            time_stemp = time.time()
            Discord_time_stemp = discord_time_convert(int(time_stemp))
            description =f"Team note: `{Team_note}` \n aktualisiert {Discord_time_stemp}"
            Sub_alert = False

            if online == True:
                embed=discord.Embed(title=Team_Name, description=description , color=0x808040)
                if Last_Status == False:
                    Sub_alert = True

                JSOn_data["Teams"][f"{Team_list[x]}"]["Last_Status"] = True
                Fill_JSOn_File(file_path_Team_data, JSOn_data)


            else:

                embed=discord.Embed(title=Team_Name, description=description , color=0xff0000)
                if Last_Status == True:
                    Sub_alert = True


                JSOn_data["Teams"][f"{Team_list[x]}"]["Last_Status"]= False
                Fill_JSOn_File(file_path_Team_data, JSOn_data)
                    

            Player_list = get_all_Player_from_a_Team(JSOn_data, Team_Name)
            Player_list_len = len(Player_list)
            y = -1
            while True:
                y = y + 1
                if y == Player_list_len:
                    break

                Player = Player_list[y]
                Player_id = JSOn_data["Teams"][Team_Name][Player]["ID"]
                Player_note = JSOn_data["Teams"][Team_Name][Player]["note"]
                Plyer_first_name = Player 
                name_cange = Player_name_cange(JSOn_data, Team_Name, Player)
                Player_Bat_url = f"https://www.battlemetrics.com/players/{Player_id}"

                Player_server_data = Player_Server_info(Player_id, battlemetrics_Server_ID)
                if Player_server_data == "Rate Limit Exceeded":
                    x = x -1
                    break
                if Player_server_data == "400":
                    Never_played = True
                    value = f"❌ `Never played on that Server` ❌ \n note: `{Player_note}` \n Player ID: [{Player_id}]({Player_Bat_url})"
                    embed.add_field(name=Player, value= value , inline=True)

                else:

                    Online_ico = Player_server_data[0]
                    lastSeen = Player_server_data[1]
                    timePlayed = Player_server_data[2]
                    Player_Server_url= Player_server_data[3]
                    

                    value = f" {Online_ico}  {lastSeen} \n ServerZeit: `{timePlayed}h` \n note: `{Player_note}` \n Player ID: [{Player_id}]({Player_Bat_url})"
    
                    if str(name_cange[0]) == str(True):
                        embed.add_field(name=f"Oldname: {Player}\n🆕: {name_cange[1]}", value=  value  , inline=True)
                    else:
                        embed.add_field(name=f"{Player}", value= value , inline=True)
            
            if Sub_alert == True:

                Sub_Discord_ID_list = list(JSOn_data["Teams"][f"{Team_list[x]}"]["Sub_Discord_ID_list"])
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
                        if online == True:
                            embed_New_Status=discord.Embed(title="🟢 New Online Status 🟢", description=f"Team `{Team_Name}` ist jetzt Online! <#{Rust_Bot_Channel_ID}>", color=0xff8000)
                            await User.send(embed=embed_New_Status)
                            await User.send(embed=embed)
                        else:
                            embed_New_Status=discord.Embed(title="🔴 New Online Status 🔴", description=f"Team `{Team_Name}` ist jetzt Offline! <#{Rust_Bot_Channel_ID}>", color=0xff0000)
                            await User.send(embed=embed_New_Status)
                            await User.send(embed=embed)
            try:
                Rust_Bot_Channel= self.bot.get_channel(Rust_Bot_Channel_ID)
                msg = await Rust_Bot_Channel.fetch_message(Team_embed_id)
                await msg.edit(embed=embed)
                log(f"Discord: Edit Embed from Team [{Team_Name}] msg.id: [{msg.id}]")
            except:
                try:
                    JSOn_data = open_JSOn_File(file_path_Team_data)
                    Rust_Bot_Channel= self.bot.get_channel(Rust_Bot_Channel_ID)
                    Team_Card_embed = await Rust_Bot_Channel.send(embed=embed, view=Sub_button())
                    Team_Card_embed_id = (Team_Card_embed.id)
                    JSOn_data["Teams"][Team_Name]["embed_id"] = Team_Card_embed_id
                    Fill_JSOn_File(file_path_Team_data, JSOn_data)
                    log(f"Discord: send new Embed from Team [{Team_Name}] msg.id: [{Team_Card_embed_id}]")
                except:
                    pass


class Sub_button(discord.ui.View,):
    def __init__(self) -> None:
        super().__init__(timeout=None)
    
    @discord.ui.button(label = "🔔", style= discord.ButtonStyle.green, custom_id = "Sub")
    async def New_Sub(self, interaction: discord.Interaction, Button: discord.ui.Button):

        User = interaction.user
        User_ID = interaction.user.id

        embed_ID = interaction.message.id
        JSOn_data = open_JSOn_File(file_path_Team_data)
        Team_data = from_embed_ID_to_data(JSOn_data, embed_ID)
        Team_name = Team_data[0]
        Sub_Discord_ID_list = list(Team_data[1])
        Sub_Discord_ID_list.append

        Team_data = from_embed_ID_to_data(JSOn_data, embed_ID)
        Team_name = Team_data[0]
        Sub_Discord_ID_list = list(Team_data[1])

        #json_object = json.dumps(JSOn_data, indent = 4)

        if User_ID in Sub_Discord_ID_list:
            await interaction.response.send_message(f"Du Abonierst schon {Team_name}", ephemeral=True)
        else:
            Sub_Discord_ID_list.append(User_ID)
            JSOn_data["Teams"][f"{Team_name}"]["Sub_Discord_ID_list"] = Sub_Discord_ID_list
            Fill_JSOn_File(file_path_Team_data, JSOn_data)

            text = f"Ich werde dich hier über Direct Message informiren wenn der Online Status von {Team_name} sich geändert hat."
            embed=discord.Embed(title=f"🔔 Du Abonierst nun das Team: {Team_name} 🔔", description=text, color=0xff8040)
            await User.send(embed=embed)

            text = f"Ich werde dich über Direct Message informiren wenn der Online Status von {Team_name} sich geändert hat."
            embed=discord.Embed(title=f"🔔 Du Abonierst nun das Team: {Team_name} 🔔", description=text, color=0xff8040)
            await interaction.response.send_message(embed=embed, ephemeral=True)



    @discord.ui.button(label = "🔕", style= discord.ButtonStyle.grey, custom_id = "UnSub")
    async def deltSub(self, interaction: discord.Interaction, Button: discord.ui.Button):
            User = interaction.user
            User_ID = interaction.user.id

            embed_ID = interaction.message.id
            JSOn_data = open_JSOn_File(file_path_Team_data)
            Team_data = from_embed_ID_to_data(JSOn_data, embed_ID)
            Team_name = Team_data[0]
            Sub_Discord_ID_list = list(Team_data[1])
            if User_ID in Sub_Discord_ID_list:
                Sub_Discord_ID_list.remove(User_ID)
                JSOn_data["Teams"][f"{Team_name}"]["Sub_Discord_ID_list"] = Sub_Discord_ID_list
                Fill_JSOn_File(file_path_Team_data, JSOn_data)

                text = f"Ich werde dich hier über Direct Message nicht mehr informiren wenn der Online Status von {Team_name} sich geändert hat."
                embed=discord.Embed(title=f"🔕 Du Deabonnierst nun das Team: {Team_name} 🔕", description=text, color=0xff0000)
                await User.send(embed=embed)

                text = f"Ich werde dich über Direct Message nicht mehr informiren wenn der Online Status von {Team_name} sich geändert hat."
                embed=discord.Embed(title=f"🔕 Du Deabonnierst nun das Team: {Team_name} 🔕", description=text, color=0xff0000)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message(f"Du Abonierst zur Zeit das Team {Team_name} nicht.", ephemeral=True)

    @discord.ui.button(label = "alle Abos Löschen", style= discord.ButtonStyle.red, custom_id = "UnSubAll")
    async def deltAllSubs(self, interaction: discord.Interaction, Button: discord.ui.Button):
            User = interaction.user
            User_ID = interaction.user.id

            embed_ID = interaction.message.id
            JSOn_data = open_JSOn_File(file_path_Team_data)
            JSOn_data = delt_all_Player_subs(JSOn_data, User_ID)
            Fill_JSOn_File(file_path_Team_data, JSOn_data)

            text = f" Du Abonierst nun kein Team mehr."
            embed=discord.Embed(title=f"🔕", description=text, color=0xff0000)
            await interaction.response.send_message(embed=embed, ephemeral=True)







async def setup(bot: commands.Bot):
    await bot.add_cog(New_player(bot), guild=discord.Object(guild_id))
    await bot.add_cog(clear_watchlist(bot), guild=discord.Object(guild_id))
    await bot.add_cog(Player_watch_loops(bot), guild=discord.Object(guild_id))
    await bot.add_cog(Delt_player(bot), guild=discord.Object(guild_id))
    await bot.add_cog(Delt_Team(bot), guild=discord.Object(guild_id))
    bot.add_view(Sub_button())

    
    

    