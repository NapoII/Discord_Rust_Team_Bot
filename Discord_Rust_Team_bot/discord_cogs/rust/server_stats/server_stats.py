"""Full Doku on: https://github.com/NapoII/Discord_Rust_Team_bot"
-----------------------------------------------
This cog gen in a loop a embed for a Rust server.
------------------------------------------------
"""
# import interactions 
from discord import app_commands
from discord.ext import commands
from discord.ext import tasks
from util.__funktion__ import *


from discord_cogs.rust.server_stats.__funktion__server_stats import *
from util.__Mydiscord_funktions__ import *
from util.__my_imge_path__ import *
img_url = my_image_url()
# get the path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
bot_path = os.path.abspath(sys.argv[0])
bot_folder = os.path.dirname(bot_path)
server_player_num_dir = os.path.join(bot_folder, "discord_cogs", "rust", "server_stats", "server_player_num")
loop_num_dir = os.path.join(bot_folder, "discord_cogs","rust", "server_stats", "loop.num")

# construct the path to the config.ini file relative to the current directory
config_dir = os.path.join(bot_folder, "config", "config.ini")
guild_id = int(read_config(config_dir, "client", "guild_id"))
guild = discord.Object(id=guild_id)

server_stats_channel_id = read_config(config_dir,"channels", "server_stats_channel_id", "int")


print("\n --> server_stats\n")

class loops(commands.Cog, commands.Bot):
    def __init__(self, bot: commands.Bot):

        self.bot = bot
        self.myLoop.start(bot)

    @tasks.loop(seconds=60*3)  # repeat after every 10 seconds
        
    async def myLoop(self, bot):
        loop_num = new_loop_num(loop_num_dir)
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"\n\nServer_Stats - {loop_num}# - {current_time}\n")
        await self.bot.wait_until_ready()
        
        server_id = read_config(config_dir, "rust", "battlemetrics_server_id")

        server_id = read_config(config_dir, "rust", "battlemetrics_server_id")
        url = f"https://api.battlemetrics.com/servers/{server_id}"
        response = requests.get(url)
        response_json = response.json()

        status_code = response.status_code

        if status_code != 200:
            print(f"\nServer_Stats {current_time} --> API ERROR: {status_code} - {url}\n")

        if status_code == 200:

            players = response_json["data"]["attributes"]["players"]
            new_player_count, player_channge_indi = if_new_player_count(server_player_num_dir, players)
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print (f"SKIP ROUTINE {loop_num}# - {current_time} - Rust Server Player Count did not change!")
            if new_player_count:
                Server_name = response_json["data"]["attributes"]["name"]
                server_ip = response_json["data"]["attributes"]["ip"]
                server_port = response_json["data"]["attributes"]["port"]
                server_ip_full = f"{server_ip}:{server_port}"

                server_status = response_json["data"]["attributes"]["status"]
                if server_status == "online":
                    embed_side_colur = 0xff8080
                else:
                    embed_side_colur = 0xff0000
                players = response_json["data"]["attributes"]["players"]
                maxPlayers = response_json["data"]["attributes"]["maxPlayers"]

                rust_type = response_json["data"]["attributes"]["details"]["rust_type"]
                map = response_json["data"]["attributes"]["details"]["map"]
                server_headerimage = response_json["data"]["attributes"]["details"]["rust_headerimage"]
                server_url = response_json["data"]["attributes"]["details"]["rust_url"]
                rust_world_seed = response_json["data"]["attributes"]["details"]["rust_world_seed"]
                rust_world_size = response_json["data"]["attributes"]["details"]["rust_world_size"]
                map_url = response_json["data"]["attributes"]["details"]["rust_maps"]["url"]
                rust_description = response_json["data"]["attributes"]["details"]["rust_description"]
                rust_description.replace("\t", "")
                rust_modded = response_json["data"]["attributes"]["details"]["rust_modded"]
                last_wipe = response_json["data"]["attributes"]["details"]["rust_born"]
                last_wipe_unix = str_to_unix(last_wipe)
                last_wipe_discord_time = discord_time_convert(last_wipe_unix)
                teamUILimit = response_json["data"]["attributes"]["details"]["rust_settings"]["teamUILimit"]
                timeZone = response_json["data"]["attributes"]["details"]["rust_settings"]["timeZone"]

                time_stemp = time.time()
                Discord_time_stemp = discord_time_convert(int(time_stemp))

                server_embeds = []
                Server_card = discord.Embed(title=Server_name, url=f"https://www.battlemetrics.com/servers/rust/{server_id}",
                colour=embed_side_colur, description=f"""
                > **👥   Player: ({players}/{maxPlayers}) {player_channge_indi}** 
                > 🔄   Last Change: {Discord_time_stemp} 

                                    
                                    """)
                text = f"""
                > 🛠️   Server Type: `{rust_type}`
                > 👥   Team Size: `{teamUILimit}` 
                > 📅   Last Wipe: {last_wipe_discord_time} 
                > ⏰   Time: `{timeZone}`
                """
                Server_card.add_field(name=f" ",
                                value=f"{text}",
                                inline=True)

                text = f"""
                > 🗺️   Map: `{map}` 
                > 🌿   Seed: `{rust_world_seed}`
                > 🌱   Size: `{rust_world_size}` 
                > [Rust Map Link]({map_url})
                """
                Server_card.add_field(name=f" ",
                            value=f"{text}",
                            inline=True)
                
                Server_card.add_field(name=f"Connect to the server:",
                            value=f"```client.connect {server_ip_full}```",
                            inline=False)

                Server_card.set_image(url=server_headerimage)
                server_embeds.append(Server_card)
                Server_Description = discord.Embed(title="Server-Description", colour=embed_side_colur, description=f"{rust_description}")
                Server_Description.set_image(url=server_headerimage)
                server_embeds.append(Server_Description)

                activity_text = f"👥 ( {players} / {maxPlayers} ) {player_channge_indi}"

                activity = discord.CustomActivity(name=activity_text)
                await self.bot.change_presence(activity=activity)

                server_stats_channel_id = read_config(config_dir, "channels", "server_stats_channel_id", "int")
                server_stats_channel = self.bot.get_channel(server_stats_channel_id)


                activity_channel_Name_text = f"👥 {players} of {maxPlayers} {player_channge_indi}"
                # print(f"change: server_stats_channel name to = {activity_channel_Name_text}")
                # print("# asyncio.sleep(20) before  server_stats_channel name#")
                # await asyncio.sleep(30)
                # await server_stats_channel.edit(name=activity_channel_Name_text)
                # print("# asyncio.sleep(20) # asyncio.sleep(20) after server_stats_channel name#")
                # await asyncio.sleep(30)

                try:
                    rust_server_embed_message_id = read_config(config_dir, "msgs", "rust_server_embed_message_id", "int")
                    rust_server_embed_message = await server_stats_channel.fetch_message(rust_server_embed_message_id)
                    await rust_server_embed_message.edit(embeds=server_embeds)
                    print("# asyncio.sleep(20) after rust_server_embed_message #")
                    await asyncio.sleep(30)
                    print(f"Discord: Edit [rust_server_embed_message] msg[{rust_server_embed_message.id}] with new embed")
                except:
                    rust_server_embed_message = await server_stats_channel.send(embeds=server_embeds)
                    print(f"Discord: Send [rust_server_embed_message] msg[{rust_server_embed_message.id}] with new embed")
                    write_config(config_dir, "msgs", "rust_server_embed_message_id", rust_server_embed_message.id)


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
        # server_headerimage = response_json["data"]["attributes"]["details"]["rust_headerimage"]
        maxPlayers = response_json["data"]["attributes"]["maxPlayers"]
        players = response_json["data"]["attributes"]["players"]
        rust_description = response_json["data"]["attributes"]["details"]["rust_description"]
        Server_ip_text = f"```client.connect {server_ip}:{server_port}```"

        embed = discord.Embed(title=f"{Server_name}", url=server_url)
        # embed.set_thumbnail(url=server_headerimage)
        embed.add_field(name="status", value=f"{server_status}", inline=True)
        embed.add_field(name="Player", value=f"{players}/{maxPlayers}", inline=True)
        embed.add_field(name="Connect to the server:", value=Server_ip_text, inline=False)

        view = Confirm_say()
        await interaction.response.send_message(embed=embed, ephemeral=True, view=view)

        print(f"Discord Command: \"/change_server\" New Server ID [{server_id}]")
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
            # return self.confirm_Button, self.say_channel_id, self.say_title, self.say_text

            write_config(config_dir, "rust", "battlemetrics_server_id", str(server_id))

            server_stats_channel = self.bot.get_channel(server_stats_channel_id)

            Server_name
            discord_channel_name = re.sub(r'\W+', '-', Server_name)
            discord_channel_name = f"💻-Server-{discord_channel_name}"
            await server_stats_channel.edit(name=discord_channel_name)


        else:
            self.confirm_Button = False
            print(f'Cancelled... self.confirm_Button = {self.confirm_Button}')
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
        print(f"Send Confrim / Cancel query.")

        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Cancelling', ephemeral=True)
        self.value = False
        self.stop()


class auto_smg_delt_serverstats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_dir = config_dir

    @commands.Cog.listener()
    async def on_message(self, message):

        delt_delay_sec = 60
        delt_msg_str = delt_str_time(delt_delay_sec)

        player_observation = message.channel
        # Check if the message is from a bot to avoid potential loops
        if message.author.bot:
            return
        if message.channel.id != server_stats_channel_id:
            return
        else:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(f"\nplayer_observation - {current_time}:\n")
            print(f"Msg delt in 10s ec from: {message.author.name}:")
            print(f"msg:\n{message.content}\n")
            await message.delete(delay = delt_delay_sec)

            if message.content not in ["/change_server"]:
                guild = message.guild
                server_stats_channel = discord.utils.get(guild.text_channels, id=server_stats_channel_id)
                rust_team_text_channel_id = read_config(config_dir,"channels", "rust_team_text_channel_id", "int")
                embeds_list = []

                description = f"<@{message.author.id}>\nThe Server Stats **channel is not a chat channel.**\nPlease utilize the channel designated for chatting, which is <#{rust_team_text_channel_id}>\n\n{delt_msg_str}\n\n**In this channel, you can use the following commands:**"
                embed_attention = discord.Embed(title="Please Note: Server Stats Channel Usage", description=description, colour=0x004000)
                embed_attention.set_thumbnail(url=img_url.piktogramm.attention)
                embeds_list.append(embed_attention)

                icon_url = message.author.display_avatar

                embed = discord.Embed(title="#rust-server-stats")

                embed.set_author(name=f"@{message.author.name}", icon_url=icon_url)
                embed.add_field(name="```/change_server```",
                                value="Change the server to which the bot should be connected by entering the battlemetrics id of the server",
                                inline=False)
                url_gif_expl = my_image_url.battlemetrics_url
                embed.set_image(url=url_gif_expl)
                embed.set_thumbnail(url=img_url.piktogramm.i)
                embeds_list.append(embed)
                await server_stats_channel.send(embeds=embeds_list, delete_after=delt_delay_sec)

                guild = message.guild
                rust_team_text_channel = discord.utils.get(guild.text_channels, id=rust_team_text_channel_id)
                content =f"Message from <@{message.author.id}>\n> {message.content}"
                await rust_team_text_channel.send(content=content)
        

async def setup(bot: commands.Bot):
    await bot.add_cog(loops(bot), guild=discord.Object(guild_id))
    await bot.add_cog(change_server_id(bot), guild=discord.Object(guild_id))
    await bot.add_cog(auto_smg_delt_serverstats(bot), guild=discord.Object(guild_id))

# counts = discord.CustomActivity(name=f"Vote end timer changed")
# await self.bot.change_presence(activity=counts)