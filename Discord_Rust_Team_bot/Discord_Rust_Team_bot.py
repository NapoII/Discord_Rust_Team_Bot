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
file_path_Bilder = file_path + "/Bilder/"
#file_path_Work_Folder = file_path + "/Work_Folder/"


Bot_Path = os.path.dirname(sys.argv[0])
config_dir = os.path.join("cfg", "config.ini")

log("Bot_Path: ["+str(Bot_Path) + "]\n")

################################################################################################################################
# Load Config
# Client
Discord_token = read_config(config_dir, "Client", "Token")
Application_ID = read_config(config_dir, "Client", "Application_ID")

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
#rust_info_name =  read_config(config_dir, "Channel", "rust_info_name")
delt_messages_Channel_ID = int(read_config(
    config_dir, "Channel", "delt_messages_Channel_ID"))


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
# Main Programm

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=praefix,
            intents=discord.Intents.all(),
            application_id=Application_ID,
            activity=activity)
        #
        # "Work_Folder.Rust.test",
        self.initial_extensions = [
            "discord_cogs.Rust.player_watch",
            "discord_cogs.admin.say",
            "discord_cogs.Rust.server_abfrage",
            "discord_cogs.Rust.Rust_info",
            "discord_cogs.help_command",

        ]

    async def setup_hook(self):
        for ext in self.initial_extensions:
            await self.load_extension(ext)

        await bot.tree.sync(guild=discord.Object(guild_id))

    async def on_ready(self):
        log("Discord Bot logt sich ein | wait_until_ready")
        await self.wait_until_ready()
        log(f'Logged in as {self.user} (ID: {self.user.id})')

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
