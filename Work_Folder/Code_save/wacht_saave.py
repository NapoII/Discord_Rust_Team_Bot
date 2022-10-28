from ast import While
from interactions import Channel
import requests
import discord
#from discord import app_commands
from discord.ext import commands
from discord.ext import tasks
from Imports import*
from discord.app_commands import Choice
import json


guild_id = int(read_config(config_dir, "Client", "guild_id"))
guild = discord.Object(id=guild_id)
Rust_Bot_Channel_ID = int(read_config(config_dir, "Channel", "Rust_Bot_Channel_ID"))
Admin_Channel_ID = int(read_config(config_dir, "Channel", "Admin_Channel_ID"))
Rust_Bot_Channel_name =  read_config(config_dir, "Channel", "Rust_Bot_Channel_name")

def Team_choice():
    Team_data_fiel_dir = f"E:\Pr0grame\My_ Pyhton\work_in_progress\Discord_Bot_Napo_III_2.1\Work_Folder\Rust\Team_data.json"

    team_file = Read_Datei(Team_data_fiel_dir, "r")
    res = json.loads(team_file)
    Team_list = list(res["Teams"].keys())
    Team_list_len = len(Team_list)

    x = -1
    Choice_Team_list = []
    while True:
        x = x + 1
        if x == Team_list_len:
            break
        Team_list[x]
        Item = Choice(team =str(Team_list[x]), value = str(Team_list[x]))
        Choice_Team_list.append(Item)
    return Choice_Team_list



class add_Player(commands.Cog, ):


    def __init__(self, bot:commands.Bot, Team_list)-> None:
        self.bot = bot

    @app_commands.command(name = "add_Player", description="add_Player to the Watchlist.")

    @app_commands.describe(
        Player_id = "Rust Server ID from Battlemetrics",
        team = "Team name of the Player",
        note = "Note for the Player",)

    
    @app_commands.choices(numer= [
        Choice(name ="Eins", value = 1),
        Choice(name ="Zwei", value = 2),
        Choice(name ="Drei", value = 3),
        ])


    async def Server_change(
        self,
        interaction: discord.Integration,
        server_id: int):
        #Admin_Channel_ID = self.bot.get_channel(Admin_Channel_ID)

        url = f"https://api.battlemetrics.com/servers/{server_id}"
        response = requests.get(url)
        response_json = response.json()
        status_code = response.status_code

        Server_name = response_json["data"]["attributes"]["name"]
        server_ip = response_json["data"]["attributes"]["ip"]
        server_port = response_json["data"]["attributes"]["port"]
        server_ip_full = f"{server_ip}:{server_port}"
        server_status = response_json["data"]["attributes"]["status"]

        server_url = response_json["data"]["attributes"]["details"]["rust_url"]
        server_headerimage = response_json["data"]["attributes"]["details"]["rust_headerimage"]
        maxPlayers = response_json["data"]["attributes"]["maxPlayers"]
        players = response_json["data"]["attributes"]["players"]
        rust_description = response_json["data"]["attributes"]["details"]["rust_description"]


        embed=discord.Embed(title=f"{Server_name}", url=server_url)
        embed.set_thumbnail(url=server_headerimage)
        embed.add_field(name="status", value=f"{server_status}", inline=True)
        embed.add_field(name="Player", value=f"{players}/{maxPlayers}", inline=True)
        embed.add_field(name="Mit dem Server verbinden:", value=f"client.connect {server_ip_full}", inline=False)

        view = Confirm_say()
        await interaction.response.send_message(embed=embed, ephemeral=True, view=view)
        
        log(f"Discord Command: \"/change_server\" New Server ID [{server_id}]")
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
            #return self.confirm_Button, self.say_channel_id, self.say_title, self.say_text
            write_config(config_dir, "Rust", "battlemetrics_server_id",str(server_id))
        
        else:
            self.confirm_Button = False
            log(f'Cancelled... self.confirm_Button = {self.confirm_Button}')
            #return self.confirm_Button, self.say_channel_id, self.say_title, self.say_text


### Confirm buttons
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


async def setup(bot: commands.Bot):
    #await bot.add_cog(loops(bot), guild=discord.Object(guild_id))
    await bot.add_cog(add_Player(bot), guild=discord.Object(guild_id))

