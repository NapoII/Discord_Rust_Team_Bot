"""Full Doku on: https://github.com/NapoII/Discord_Rust_Team_bot"
-----------------------------------------------
This cog gen in a loop a embed for a Rust server.
------------------------------------------------
"""

from interactions import Channel
import requests
# import discord                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            rd
#from discord import app_commands
from discord.ext import commands
from discord.ext import tasks
from util.__funktion__ import *


# get the path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
bot_path = os.path.abspath(sys.argv[0])
bot_folder = os.path.dirname(bot_path)
# construct the path to the config.ini file relative to the current directory
config_dir = os.path.join(bot_folder, "cfg", "config.ini")
guild_id = int(read_config(config_dir, "Client", "guild_id"))
guild = discord.Object(id=guild_id)
server_stats_channel_id = int(read_config(config_dir, "Channel", "server_stats_channel_id"))
admin_channel_id = int(read_config(config_dir, "Channel", "admin_channel_id"))


class loops(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):

        self.bot = bot

        self.myLoop.start(bot)

    @tasks.loop(seconds=120)  # repeat after every 10 seconds
    async def myLoop(self, bot):
        await self.bot.wait_until_ready()
        server_id = int(read_config(
            config_dir, "Rust", "battlemetrics_server_id"))
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

        start_pos = (server_url.find("://"))+3
        http_str = server_url[start_pos:]
        if http_str in rust_description:
            rust_description = rust_description
        else:
            rust_description = f"Server URL: {server_url}\n{rust_description}"

        time_stemp = time.time()
        Discord_time_stemp = discord_time_convert(int(time_stemp))

        Server_ip_text = f"```client.connect {server_ip}:{server_port}```\nsteam://connect/{server_ip}:{server_port}\n battlemetricsID: `{server_id}` updated {Discord_time_stemp}"
        activity_text = f"Online: {players}/{maxPlayers}"

        await self.bot.change_presence(activity=discord.Game(activity_text))

        Rust_Bot_Channel = self.bot.get_channel(server_stats_channel_id)

        activity__channel_Name_text = f"🟢{players}von{maxPlayers}🟢Online"
        log(f"cange: Rust_Bot_Channel name to = {activity__channel_Name_text}")
        await Rust_Bot_Channel.edit(name=activity__channel_Name_text)
        #write_config(config_dir, "Channel", "rust_bot_channel_name",activity__channel_Name_text)

        log(f"Discord: change Bot Status[{activity_text}]")

        map_data = get_map_img(server_id)
        if map_data != False:
            thumbnailUrl = map_data[0]
            map_url = map_data[1]
            seed = map_data[2]
            size = map_data[3]

        embed = discord.Embed(
            title=f"{Server_name}", url=f"https://www.battlemetrics.com/servers/rust/{server_id}")
        embed.set_thumbnail(url=server_headerimage)
        embed.add_field(name="status", value=f"{server_status}", inline=True)
        embed.add_field(
            name="Player", value=f"{players}/{maxPlayers}", inline=True)
        if map_data == False:
            embed.add_field(
                name="Map", value="🚫 Server Map is not Vanilla 🚫", inline=False)
        if map_data != False:
            embed.add_field(
                name="Map", value=f"[Seed: {seed} Size: {size}]({map_url})", inline=False)
            embed.set_image(url=thumbnailUrl)
        embed.add_field(name="Connect to the server:",
                        value=Server_ip_text, inline=False)

        try:
            rust_server_embed_message_id = read_config(
                config_dir, "Rust", "rust_server_embed_message_id")
            msg = await Rust_Bot_Channel.fetch_message(rust_server_embed_message_id)
            await msg.edit(embed=embed)
            log(
                f"Discord: Edit [rust_server_embed_message] msg[{msg.id}] with new embed")
        except:
            msg = await Rust_Bot_Channel.send(embed=embed)
            log(
                f"Discord: Send [rust_server_embed_message] msg[{msg.id}] with new embed")
            write_config(config_dir, "Rust",
                         "rust_server_embed_message_id", str(msg.id))

        try:
            rust_server_description_message_id = read_config(
                config_dir, "Rust", "rust_server_description_message_id")
            msg = await Rust_Bot_Channel.fetch_message(rust_server_description_message_id)
            await msg.edit(content=rust_description)
            log(
                f"Discord: Edit [rust_server_description_message] msg[{msg.id}] with new content")
        except:
            msg = await Rust_Bot_Channel.send(content=rust_description)
            write_config(config_dir, "Rust",
                         "rust_server_description_message_id", str(msg.id))
            log(
                f"Discord: Send [rust_server_description_message] msg[{msg.id}]")


class change_server_id(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="change_server", description="Change the Rust Server ID")
    @app_commands.describe(
        server_id="Rust Server ID from Battlemetrics")
    async def Server_change(
            self,
            interaction: discord.Integration,
            server_id: int):
        #admin_channel_id = self.bot.get_channel(admin_channel_id)

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
        Server_ip_text = f"```client.connect {server_ip}:{server_port}```"

        embed = discord.Embed(title=f"{Server_name}", url=server_url)
        embed.set_thumbnail(url=server_headerimage)
        embed.add_field(name="status", value=f"{server_status}", inline=True)
        embed.add_field(
            name="Player", value=f"{players}/{maxPlayers}", inline=True)
        embed.add_field(name="Connect to the server:",
                        value=Server_ip_text, inline=False)

        view = Confirm_say()
        await interaction.response.send_message(embed=embed, ephemeral=True, view=view)

        log(f"Discord Command: \"/change_server\" New Server ID [{server_id}]")
        log(f"Send Confrim / Cancel query.")

        log("Send Discordembed: Test Result")
        await view.wait()
        if view.value is None:
            self.confirm_Button = False
            log(f'Timed out... self.confirm_Button = {self.confirm_Button}')
            # return self.confirm_Button, self.say_channel_id, self.say_title, self.say_text

        elif view.value:
            self.confirm_Button = True

            log(f'Confirmed... self.confirm_Button = {self.confirm_Button}')
            # return self.confirm_Button, self.say_channel_id, self.say_title, self.say_text
            write_config(config_dir, "Rust",
                         "battlemetrics_server_id", str(server_id))

        else:
            self.confirm_Button = False
            log(f'Cancelled... self.confirm_Button = {self.confirm_Button}')
            # return self.confirm_Button, self.say_channel_id, self.say_title, self.say_text


# Confirm buttons
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
    await bot.add_cog(loops(bot), guild=discord.Object(guild_id))
    await bot.add_cog(change_server_id(bot), guild=discord.Object(guild_id))
