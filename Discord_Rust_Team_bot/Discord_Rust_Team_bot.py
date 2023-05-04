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


Bot_Path = os.path.dirname(sys.argv[0])
config_dir = os.path.join(file_path,"cfg", "config.ini")
token_config_dir = os.path.join(file_path,"cfg", "token.ini")
print(token_config_dir)
log("Bot_Path: ["+str(Bot_Path) + "]\n")

################################################################################################################################
# Load Config
# Client
Discord_token = read_config(token_config_dir, "Discord", "token")
Application_ID = read_config(token_config_dir, "Discord", "Application_ID")

guild_name = read_config(config_dir, "Client", "guild_name")
guild_id = int(read_config(config_dir, "Client", "guild_id"))
guild = discord.Object(id=guild_id)
praefix = read_config(config_dir, "Client", "praefix")
activity_text = (read_config(config_dir, "Client", "Activity"))
activity = Discord_Activity(activity_text)

# Channel

Admin_Channel_ID = int(read_config(config_dir, "Channel", "Admin_Channel_ID"))
Admin_Channel_name = read_config(config_dir, "Channel", "Admin_Channel_name")
Rust_Bot_Channel_ID = int(read_config(
    config_dir, "Channel", "Rust_Bot_Channel_ID"))
Rust_info_channel_id = int(read_config(
    config_dir, "Channel", "rust_info_channel_id"))

#Rust_Bot_Channel_name =  read_config(config_dir, "Channel", "Rust_Bot_Channel_name")
#rust_info_channel_name =  read_config(config_dir, "Channel", "rust_info_channel_name")
delt_messages_Channel_ID = int(read_config(
    config_dir, "Channel", "delt_messages_Channel_ID"))



# Rust Config
battlemetrics_Server_ID = read_config(config_dir, "Rust", "battlemetrics_Server_ID")
battlemetrics_api_server = "https://api.battlemetrics.com/servers/" + str(battlemetrics_Server_ID)
Rust_Server_description_message_id = int(read_config(config_dir, "Rust", "Rust_Server_description_message_id"))
Rust_Server_embed_message_id = int(read_config(config_dir, "Rust", "Rust_Server_embed_message_id"))


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
        """            "discord_cogs.Rust.player_watch",
            "discord_cogs.admin.say",
            "discord_cogs.Rust.server_abfrage",
            "discord_cogs.Rust.Rust_info",
            "discord_cogs.help_command","""
        # "Work_Folder.Rust.test",
        self.initial_extensions = [


        ]

    async def setup_hook(self):
        for ext in self.initial_extensions:
            await self.load_extension(ext)

        await bot.tree.sync(guild=discord.Object(guild_id))

    async def on_ready(self):
        log("Discord Bot logt sich ein | wait_until_ready")
        await self.wait_until_ready()
        log(f'Logged in as {self.user} (ID: {self.user.id})')








        for guild in bot.guilds:
                print(guild.id)

                Admin_role_name = "Admin"
                Admin_role_colour = discord.Colour.blue()
                # Check whether the role already exists
                existing_role = discord.utils.get(guild.roles, name=Admin_role_name)

                if existing_role is None:
                    # If the role does not exist, create a new role
                    Admin_role = await guild.create_role(name=Admin_role_name, colour=Admin_role_colour)

                    # Confirmation message
                    print(f"The role {Admin_role_name} was created.")
                else:
                    # If the role already exists, here is an error message or action
                    print(f"The role {Admin_role_name} already exists.")
                    role = discord.utils.get(guild.roles, name=Admin_role_name)

                Rust_role_name = "Rust Ultras"
                Rust_role_colour = discord.Colour.red()
                # Check whether the role already exists
                existing_role = discord.utils.get(guild.roles, name=Rust_role_name)

                if existing_role is None:
                    # If the role does not exist, create a new role
                    Rust_role = await guild.create_role(name=Rust_role_name, colour=Rust_role_colour)

                    # Confirmation message
                    print(f"The role {Rust_role_name} was created.")
                else:
                    # If the role already exists, here is an error message or action
                    print(f"The role {Rust_role_name} already exists.")
                    role = discord.utils.get(guild.roles, name=Rust_role_name)

                # Searches all existing categories on the server for the category with the name "Rust".
                category_name = "-----🎮 - Rust - 🎮------"
                category_Rust = discord.utils.get(guild.categories, name=category_name)

                if category_Rust is not None:

                    print(f"The category {category_Rust.name} already exists.")

                else:
                    overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=False), Rust_role: discord.PermissionOverwrite(
                        read_messages=True, send_messages=True, connect=True, speak=True), guild.me: discord.PermissionOverwrite(manage_channels=True)}

                    print(
                        f"The category {category_name} does not yet exist and will now be created")
                    # Creates a new category
                    category_Rust = await guild.create_category(category_name, overwrites=overwrites)
                    print(f"The category {category_name} was created.")

                    Server_Stats = await guild.create_text_channel("📈 Server Stats", category=category_Rust)
                    print(f"The channel {Server_Stats.name} was created.")

                    rust_bot_channel_name = Server_Stats.name
                    Rust_Bot_Channel_ID = Server_Stats.id
                    write_config(config_dir, "Channel", "rust_bot_channel_id", Rust_Bot_Channel_ID)
                    write_config(config_dir, "Channel", "rust_bot_channel_name", rust_bot_channel_name)

                    Player_Observation = await guild.create_text_channel("🔔 Player Observation", category=category_Rust)
                    print(f"The channel {Player_Observation.name} was created.")

                    Rust_info = await guild.create_text_channel("💻 Rust_info", category=category_Rust)
                    print(f"The channel {Rust_info.name} was created.")

                    Rust_info_channel_id = Rust_info.id
                    rust_info_channel_name = Rust_info.name
                    write_config(config_dir, "Channel", "rust_info_channel_id", Rust_info_channel_id)
                    write_config(config_dir, "Channel", "rust_info_channel_name", rust_info_channel_name)
                    print(f"The channel {rust_info_channel_name} was created.")

                    Team_Chat = await guild.create_text_channel("📝 Team Chat", category=category_Rust)
                    print(f"The channel {Team_Chat.name} was created.")

                    Rust_main_voice = "Team-Voice"
                    # Creates a new Voice channel
                    Rust_main_voice = await guild.create_voice_channel(Rust_main_voice, category=category_Rust)
                    print(
                        f"The voice channel {Rust_main_voice.name} has been created.")

                # Searches all existing categories on the server for the category with the name "Rust".
                category_name = "-------💻 - Admin - 💻-------"
                category_Admin = discord.utils.get(
                    guild.categories, name=category_name)
                if category_Admin is not None:

                    print(f"The category {category_Admin.name} already exists.")

                else:
                    overwrites = {guild.default_role: discord.PermissionOverwrite(view_channel=False), Admin_role: discord.PermissionOverwrite(
                        view_channel=True), guild.me: discord.PermissionOverwrite(manage_channels=True)}
                    print(
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

                    print(f"The category {category_name} was created.")

                    console = await guild.create_text_channel(">_ console", category=category_Admin)

                    Admin_Channel_ID = console.id
                    Admin_Channel_name = console.name
                    write_config(config_dir, "Channel", "admin_channel_id", Admin_Channel_ID)
                    write_config(config_dir, "Channel", "admin_channel_name", Admin_Channel_name)
                    print(f"The channel {console.name} was created.")

                    delt_messages = await guild.create_text_channel("🚮 delt-messages", category=category_Admin)
                    print(f"The channel {delt_messages.name} was created.")

                    delt_messages_Channel_ID = delt_messages.id
                    delt_messages_name = delt_messages.name
                    write_config(config_dir, "Channel", "delt_messages_channel_id", delt_messages_Channel_ID)
                    write_config(config_dir, "Channel", "delt_messages_channel_name", delt_messages_name)
                    print(f"The channel {delt_messages_name} was created.")






















        text = f"\n\nThe Bot: [ {self.user} | ID:{self.user.id} ] is connected to [{guild_name}] id: [{guild_id}]\nActivity_text:["+str(
            activity_text)+"]\n\n📶 Bot is Online and Rdy to Run... 📶 \n"
        channel = self.get_channel(Admin_Channel_ID)
        log(str(text))

        # change_status.start()

        embed = discord.Embed(title=py_name, color=0xff80ff)
        embed.set_author(name="created by Napo_II",
                         url="https://github.com/NapoII/")
        embed.set_thumbnail(url="https://i.imgur.com/qqEH4R4.png")
        embed.add_field(name="Version", value=v, inline=True)
        embed.add_field(
            name="python", value=f"{python_version()}", inline=True)
        embed.add_field(name="github", value="/NapoII", inline=False)
        await channel.send(embed=embed)

        embed = discord.Embed(
            title="📶 Bot is Online and Rdy to Run... 📶", color=0xff8080)
        embed.add_field(name="client.name", value=self.user.name, inline=True)
        embed.add_field(name="guild_name", value=guild_name, inline=True)
        embed.add_field(name="guild_id", value=str(guild_id), inline=True)
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

            print(
                f"channel_m_id= {channel_m_id} == Rust_Bot_Channel_name= {Rust_Bot_Channel_ID}")

            if channel_m_id == Rust_Bot_Channel_ID:

                await message.delete()
                log(f"Nachricht wurde vom Bot gelöscht:{channel_m} {message}")

            if channel_m_id == Rust_info_channel_id:

                await message.delete()
                log(f"Nachricht wurde vom Bot gelöscht:{channel_m} {message}")

        @bot.event
        async def on_message_delete(message):

            message_author = str(message.author)
            message_channel = "#" + str(message.channel)
            message_content = str(message.content)

            log("Nachricht wurde gelöscht von "+str(message_author)+" im Channel: " +
                str(message_channel)+"\n Nachricht: "+str(message_content))

            if message.author == bot.user:
                return

            Date_Time = (time.strftime("%d_%m-%Y %H:%M"))

            embed = discord.Embed(title="Gelöschte Nachricht", description=(
                "am "+str(Date_Time)), color=0xff0000)
            embed.set_thumbnail(url="https://i.imgur.com/PdLm65I.png")

            embed.add_field(name=message_author,
                            value="Channel: "+message_channel, inline=True)
            embed.set_footer(text=message_content)
            Adelt_messages_name_discord = bot.get_channel(
                delt_messages_Channel_ID)
            await Adelt_messages_name_discord.send(embed=embed)


bot = MyBot()
bot.run(Discord_token)