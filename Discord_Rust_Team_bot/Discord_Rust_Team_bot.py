"""Full Doku on: https://github.com/NapoII/Discord_Rust_Team_bot"
-----------------------------------------------
This Python code provides a Discord bot that offers assistance for the game Rust.
The bot can check if certain players are online on a server
and display how many players are currently online.
It can be hosted on a server and used by players
to enhance their gaming experience.
This code can be shared on GitHub
to allow other Rust players to use and
contribute to the bot's development. 
------------------------------------------------
"""

# imports
import os
import sys
import time
from asyncio import tasks
from platform import python_version

import webbrowser
import discord
import pyautogui
from discord.ext import commands, tasks

from util.__funktion__ import *

# Discord_Rust_Team_bot.py
log(f'Programme has been started!', 'green')

################################################################################################################################
# PreSet Programm

v = "0.21.0"
py_name = os.path.basename(__file__)
file_path = os.path.dirname(sys.argv[0])
#file_path_Work_Folder = file_path + "/Work_Folder/"


Bot_Path = os.path.abspath(sys.argv[0])
config_dir = os.path.join(file_path, "cfg", "config.ini")
token_config_dir = os.path.join(file_path, "cfg", "token.ini")
log("Bot_Path: ["+str(Bot_Path) + "]\n")

################################################################################################################################
# Load Config
# Client
while True:
    try:
        Discord_token = read_config(token_config_dir, "Discord", "token")
        Application_ID = read_config(
            token_config_dir, "Discord", "Application_ID")
        guild_id = int(read_config(config_dir, "Client", "guild_id"))
        guild = discord.Object(id=guild_id)
        praefix = read_config(config_dir, "Client", "praefix")
        activity_text = (read_config(config_dir, "Client", "Activity"))
        activity = Discord_Activity(activity_text)
        break
    except:
        pyautogui.alert(text='Fill in the empty fields in both config files!',
                        title='Discord_Rust_Team_Bot', button='OK')
        webbrowser.open(token_config_dir)
        webbrowser.open(config_dir)
# Channel

Admin_Channel_ID = int(read_config(config_dir, "Channel", "Admin_Channel_ID"))
#Admin_Channel_name = read_config(config_dir, "Channel", "Admin_Channel_name")
rust_info_channel_id = int(read_config(
    config_dir, "Channel", "rust_info_channel_id"))

#server_stats_channel_id_name =  read_config(config_dir, "Channel", "server_stats_channel_id_name")
#rust_info_channel_name =  read_config(config_dir, "Channel", "rust_info_channel_name")
delt_messages_channel_id = int(read_config(
    config_dir, "Channel", "delt_messages_channel_id"))


# Rust Config
battlemetrics_Server_ID = read_config(
    config_dir, "Rust", "battlemetrics_Server_ID")
battlemetrics_api_server = "https://api.battlemetrics.com/servers/" + \
    str(battlemetrics_Server_ID)
Rust_Server_description_message_id = int(read_config(
    config_dir, "Rust", "Rust_Server_description_message_id"))
Rust_Server_embed_message_id = int(read_config(
    config_dir, "Rust", "Rust_Server_embed_message_id"))


################################################################################################################################
################################################################################################################################
# Main Programm

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=praefix,
            intents=discord.Intents.all(),
            application_id=Application_ID,
            activity=activity)

        # "Work_Folder.Rust.test",
        self.initial_extensions = [
            "discord_cogs.Rust.player_watch",
            "discord_cogs.admin.say",
            "discord_cogs.Rust.Rust_info",
            "discord_cogs.help_command",
            "discord_cogs.Rust.server_stats",
            "discord_cogs.Rust.ChannelHoper",
            "discord_cogs.Rust.team_check",
        ]

    async def setup_hook(self):
        for ext in self.initial_extensions:
            await self.load_extension(ext)

        await bot.tree.sync(guild=discord.Object(guild_id))

    async def on_ready(self):
        log("Discord Bot logs in | wait_until_ready")
        await self.wait_until_ready()
        log(f'Logged in as {self.user} (ID: {self.user.id})')

        for guild in bot.guilds:

            Admin_role_name = "Admin"
            Admin_role_colour = discord.Colour.blue()
            # Check whether the role already exists
            existing_role = discord.utils.get(
                guild.roles, name=Admin_role_name)

            if existing_role is None:
                # If the role does not exist, create a new role
                Admin_role = await guild.create_role(name=Admin_role_name, colour=Admin_role_colour)

                # Confirmation message
                log(f"The role {Admin_role_name} was created.", "b")
            else:
                # If the role already exists, here is an error message or action
                log(f"The role {Admin_role_name} already exists.", "b")
                Admin_role = discord.utils.get(
                    guild.roles, name=Admin_role_name)

            Rust_role_name = "Rust Ultras"
            Rust_role_colour = discord.Colour.red()
            # Check whether the role already exists
            existing_role = discord.utils.get(guild.roles, name=Rust_role_name)

            if existing_role is None:
                # If the role does not exist, create a new role
                Rust_role = await guild.create_role(name=Rust_role_name, colour=Rust_role_colour)

                # Confirmation message
                log(f"The role {Rust_role_name} was created.", "b")
            else:
                # If the role already exists, here is an error message or action
                log(f"The role {Rust_role_name} already exists.", "b")
                Rust_role = discord.utils.get(guild.roles, name=Rust_role_name)

            # Searches all existing categories on the server for the category with the name "Rust".
            category_name = "-----🎮 - Rust - 🎮------"
            category_Rust = discord.utils.get(
                guild.categories, name=category_name)

            if category_Rust is not None:

                log(f"The category {category_Rust.name} already exists.")

            else:
                overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=False), Rust_role: discord.PermissionOverwrite(
                    read_messages=True, send_messages=True, connect=True, speak=True), guild.me: discord.PermissionOverwrite(manage_channels=True)}

                log(
                    f"The category {category_name} does not yet exist and will now be created")
                # Creates a new category
                category_Rust = await guild.create_category(category_name, overwrites=overwrites)
                log(f"The category {category_name} was created.")
                category_Rust_name = category_Rust.name
                category_Rust_id = category_Rust.id
                write_config(config_dir, "Channel",
                             "category_Rust_id", category_Rust_id)

                Server_Stats = await guild.create_text_channel("📈 Server Stats", category=category_Rust)
                log(f"The channel {Server_Stats.name} was created.")

                server_stats_channel_id_name = Server_Stats.name
                server_stats_channel_id = Server_Stats.id
                write_config(config_dir, "Channel",
                             "server_stats_channel_id", server_stats_channel_id)
                #write_config(config_dir, "Channel", "server_stats_channel_id_name", server_stats_channel_id_name)

                player_observation = await guild.create_text_channel("🔔 Player Observation", category=category_Rust)
                player_observation_channel_id = player_observation.id
                player_observation_name = player_observation.name
                write_config(
                    config_dir, "Channel", "player_observation_channel_id", player_observation_channel_id)
                log(f"The channel {player_observation.name} was created.")

                Rust_info = await guild.create_text_channel("💻 Rust_info", category=category_Rust)

                embed = discord.Embed(title="#rust-info", color=0x8080ff)
                embed.set_author(name=f"@{guild.name}",
                                icon_url=f"https://i.imgur.com/sGX6nZz.png")
                embed.set_thumbnail(url="https://i.imgur.com/sdr9twR.png")
                all_commands = """`!rust help` - List of all commands
                `!rust cctv` - List of all CCTV codes
                `!rust pager` - List of all pager codes
                `!rust cost` - Important prices
                `!rust fert {Number of Fertilizers}` - How much Scrap from x Fertilizer
                `!rust diesel {Number of Diesel}` - Giant Excavator / Mining Quarry - Calculator
                `!rust sulfur {Number of sulphur}` - How much boom from x suflur
                `!rust raid` - Raid costs list
                `!rust bind` - Must-have Extra Bind's
                `!rust elec` - Must have Electronic Circuits
                """
                embed.add_field(name="All Commands:",
                                value=all_commands, inline=True)
                await Rust_info.send(embed=embed)

                rust_info_channel_id = Rust_info.id
                rust_info_channel_name = Rust_info.name
                write_config(config_dir, "Channel",
                             "rust_info_channel_id", rust_info_channel_id)
                #write_config(config_dir, "Channel", "rust_info_channel_name", rust_info_channel_name)
                log(f"The channel {rust_info_channel_name} was created.")

                Team_Chat = await guild.create_text_channel("📝 Team Chat", category=category_Rust)
                log(f"The channel {Team_Chat.name} was created.")

                Rust_main_voice = "Create new channel"
                # Creates a new Voice channel
                hopper_voice = await guild.create_voice_channel(Rust_main_voice, category=category_Rust)
                log(f"The voice channel {hopper_voice.name} has been created.")
                hopper_voice_channel_id = hopper_voice.id
                hopper_voice_channel_name = hopper_voice.name
                write_config(config_dir, "Channel",
                             "hopper_voice_channel_id", hopper_voice_channel_id)

            # Searches all existing categories on the server for the category with the name "Rust".
            category_name = "-------💻 - Admin - 💻-------"
            category_Admin = discord.utils.get(
                guild.categories, name=category_name)
            if category_Admin is not None:
                log(f"The category {category_Admin.name} already exists.")

            else:
                overwrites = {guild.default_role: discord.PermissionOverwrite(view_channel=False), Admin_role: discord.PermissionOverwrite(
                    view_channel=True), guild.me: discord.PermissionOverwrite(manage_channels=True)}
                log(
                    f"The category {category_name} does not yet exist and will now be created")
                # Creates a new category
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    guild.me: discord.PermissionOverwrite(manage_channels=True),
                    Admin_role: discord.PermissionOverwrite(
                        read_messages=True, send_messages=True, connect=True, speak=True, view_channel=True)
                }

                category_Admin = await guild.create_category(category_name, overwrites=overwrites)
                await category_Admin.edit(position=1, reason="Set category position")
                await category_Admin.edit(sync_permissions=True, reason="Sync category permissions")

                log(f"The category {category_name} was created.")

                console = await guild.create_text_channel(">_ console", category=category_Admin)

                Admin_Channel_ID = console.id
                Admin_Channel_name = console.name
                write_config(config_dir, "Channel",
                             "admin_channel_id", Admin_Channel_ID)
                #write_config(config_dir, "Channel", "admin_channel_name", Admin_Channel_name)
                log(f"The channel {console.name} was created.")

                embed = discord.Embed(
                    title="🍾Nice, the Bot has created the required channels for the Rust Team🍾", color=0xff8080)
                embed.add_field(name="💻Restart the Bot Now💻",
                                value="So that the bot can run its routine", inline=True)
                await console.send(embed=embed)

                delt_messages = await guild.create_text_channel("🚮 delt-messages", category=category_Admin)
                log(f"The channel {delt_messages.name} was created.")

                delt_messages_channel_id = delt_messages.id
                delt_messages_name = delt_messages.name
                write_config(config_dir, "Channel",
                             "delt_messages_channel_id", delt_messages_channel_id)
                #write_config(config_dir, "Channel", "delt_messages_channel_name", delt_messages_name)
                log(f"The channel {delt_messages_name} was created.")

        text = f"\n\nThe Bot: [ {self.user} | ID:{self.user.id} ] is connected to [{guild.name}] id: [{guild.id}]\nActivity_text:[{activity_text}]\n\n📶 Bot is Online and Rdy to Run... 📶 \n"

        Admin_Channel_ID = int(read_config(
            config_dir, "Channel", "Admin_Channel_ID"))
        channel = self.get_channel(Admin_Channel_ID)
        log(str(text))

        embed = discord.Embed(title=py_name, color=0xff80ff)
        embed.set_author(name="created by Napo_II",
                         url="https://github.com/NapoII/Discord_Rust_Team_bot")
        embed.set_thumbnail(url="https://i.imgur.com/qqEH4R4.png")
        embed.add_field(name="Version", value=v, inline=True)
        embed.add_field(
            name="python", value=f"{python_version()}", inline=True)
        embed.add_field(name="github", value="/NapoII", inline=False)
        await channel.send(embed=embed)

        embed = discord.Embed(
            title="📶 Bot is Online and Rdy to Run... 📶", color=0xff8080)
        embed.add_field(name="client.name", value=self.user.name, inline=True)
        embed.add_field(name="guild.name", value=guild.name, inline=True)
        embed.add_field(name="guild.id", value=str(guild.id), inline=True)
        await channel.send(embed=embed)

        @bot.event
        # this event is called when a message is sent by anyone
        async def on_message(message):
            # if the user is the client user itself, ignore the message
            await bot.process_commands(message)
            # if message.content == praefix:
            #    return

            if message.author == bot.user:
                return
            # this is the string text message of the Message
            content_m = message.content

            # this is the sender of the Message
            user = message.author
            # this is the channel of there the message is sent
            channel_m = message.channel
            channel_m_id = message.channel.id
            # this is a list of the roles from the message sender
            try:
                roles = message.author.roles
            except:
                pass
            guild = message.guild
            if message.author == bot.user:
                return

            log(str(user) + ": (#" + str(channel_m)+") say: " + content_m)
            rust_info_channel_id = int(read_config(
                config_dir, "Channel", "rust_info_channel_id"))
            player_observation_channel_id = int(read_config(
                config_dir, "Channel", "player_observation_channel_id"))
            log(
                f"channel_m_id= {channel_m_id} == server_stats_channel_id_name= {rust_info_channel_id}")
            if channel_m_id == rust_info_channel_id or channel_m_id == player_observation_channel_id:

                await message.delete()
                log(f"Message was deleted by the bot:{channel_m} {message}")

        @bot.event
        async def on_message_delete(message):

            message_author = str(message.author)
            message_channel = "#" + str(message.channel)
            message_content = str(message.content)

            log("Message deleted from "+str(message_author)+" in the channel: " +
                str(message_channel)+"\n Message: "+str(message_content))

            if message.author == bot.user:
                return

            Date_Time = (time.strftime("%d_%m-%Y %H:%M"))

            embed = discord.Embed(title="Deleted message", description=(
                "am "+str(Date_Time)), color=0xff0000)
            embed.set_thumbnail(url="https://i.imgur.com/PdLm65I.png")

            embed.add_field(name=message_author,
                            value="Channel: "+message_channel, inline=True)
            embed.set_footer(text=message_content)
            delt_messages_channel_id = int(read_config(
                config_dir, "Channel", "delt_messages_channel_id"))
            Adelt_messages_name_discord = bot.get_channel(
                delt_messages_channel_id)
            await Adelt_messages_name_discord.send(embed=embed)


bot = MyBot()
bot.run(Discord_token)
