from platform import python_version


py_name = "Discord_Bot_Napo_III_2.1" 
v = "0.0.2"

####################################################################################################
# #   Intro

f0 =  """ 
                 .              .                 
             .,,:+.            .+:,,.             
          .,:+++++:            :+++++:,.          
        ,:+++++++++,,::::::::,,+++++++++:,        
       :++++++++++++++++++++++++++++++++++:       
      ,++++++++++++++++++++++++++++++++++++++,       
  .++++++++++++++++++++++++++++++++++++++++++++.  
  ,++++++++++++++++++++++++++++++++++++++++++++,  
  :++++++++++++++++++++++++++++++++++++++++++++:  
 .++++++++++++++++++++++++++++++++++++++++++++++. 
 ,+++++++++++++:,:++++++++++++++:,:+++++++++++++, 
 :+++++++++++:.   .:++++++++++:.   .:+++++++++++: 
 ++++++++++++.      :++++++++:      .++++++++++++ 
.+++++++++++:       .++++++++.       ,+++++++++++.
,+++++++++++,        :++++++:.       .+++++++++++,
,+++++++++++.        :++++++:        .+++++++++++,
:+++++++++++,        :++++++:.       ,+++++++++++:
:+++++++++++:       .++++++++.       ,+++++++++++:
+++++++++++++.      :++++++++:.     .+++++++++++++
+++++++++++++:.   .:++++++++++:.   .:+++++++++++++
+++++++++++++++:,:++++++++++++++:,:+++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++
++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++:,:++++++++++++++++++++++:,:+++++++++++
.:+++++++++:, .,:++++++++++++++++:,. ,:+++++++++:.
 .:++++++++++:,. ..,::++++++::,.. .,:++++++++++:. 
   .:++++++++++,                  ,++++++++++:.   
     ,:+++++++:                    :+++++++:,     
       ,:+++++.                    .+++++:,       
         .,:+,                      ,+:,.         
            .                        .            
""" 

f1 = """- """ + py_name + """
- created by Napo_II
- """ + v + f"""
- python {python_version()}
- https://github.com/NapoII/

"""
print(" \nProgramm wird gestartet ...")

####################################################################################################
#import

from asyncio import tasks
import os
import os, sys
import time
import pyautogui
from Imports import*


import discord
from discord.ext import commands
from discord.ext import tasks
################################################################################################################################
#PreSet Programm

file_path = os.path.dirname(sys.argv[0])
file_path_Bilder = file_path + "/Bilder/"
file_path_Work_Folder = file_path + "/Work_Folder/"


Doku_Folder = Folder_gen (py_name, "Documents/")
Log_Folder = Folder_gen ("Log", ("Documents/"+str(py_name)))
Log_File_name = Datei_name_mit_Zeit ("LogFile-"+str(py_name))
Log_File = Erstelle_TextDatei (Log_File_name, Log_Folder, f0 + "Log-File:\n---------------------------------------------------------------------------------------\n")


Bot_Path = os.path.dirname(sys.argv[0])
config_dir = file_path +"/config.ini"

log ( "Bot_Path: ["+str(Bot_Path) + "]\n")

################################################################################################################################
# Load Config
#Client
Discord_token = read_config(config_dir, "Client", "Token")
Application_ID = read_config(config_dir, "Client", "Application_ID")

guild_name = read_config(config_dir, "Client", "guild_name")
guild_id = int(read_config(config_dir, "Client", "guild_id"))
guild = discord.Object(id=guild_id)
praefix = read_config(config_dir, "Client", "praefix")
activity_text = (read_config(config_dir, "Client", "Activity"))
activity = Discord_Activity(activity_text)
#Channel
Admin_Channel_ID = int(read_config(config_dir, "Channel", "Admin_Channel_ID"))
Admin_Channel_name = read_config(config_dir, "Channel", "Admin_Channel_name")
Rust_Bot_Channel_ID = int(read_config(config_dir, "Channel", "Rust_Bot_Channel_ID"))
Rust_Bot_Channel_name =  read_config(config_dir, "Channel", "Rust_Bot_Channel_name")
delt_messages_Channel_ID = int(read_config(config_dir, "Channel", "delt_messages_Channel_ID"))


# Rust Config
battlemetrics_Server_ID = read_config(config_dir, "Rust", "battlemetrics_Server_ID")
battlemetrics_api_server = "https://api.battlemetrics.com/servers/"+str(battlemetrics_Server_ID)
Rust_Server_description_message_id = int(read_config(config_dir, "Rust", "Rust_Server_description_message_id"))
Rust_Server_embed_message_id = int(read_config(config_dir, "Rust", "Rust_Server_embed_message_id"))
battlemetrics_player_list = read_config(config_dir, "Rust", "battlemetrics_player_list")


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
        #"Work_Folder.Rust.test",
        self.initial_extensions = [
            "Work_Folder.Rust.player_watch",
            "Work_Folder.admin.say",
            "Work_Folder.Rust.server_abfrage",
            "Work_Folder.Rust.Rust_info",
            "help_command",
            
        ]
        #"Work_Folder.Rust.cargo_timer"
    
    async def setup_hook(self):
        for ext in self.initial_extensions:
            await self.load_extension(ext)

        await bot.tree.sync (guild =discord.Object(guild_id))


    async def on_ready(self):
        log("Discord Bot logt sich ein | wait_until_ready")
        await self.wait_until_ready()
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

        text = f"\n\nThe Bot: [ {self.user} | ID:{self.user.id} ] is connected to [{guild_name}] id: [{guild_id}]\nActivity_text:["+str(activity_text)+"]\n\n📶 Bot is Online and Rdy to Run... 📶 \n"
        print(f0+f1)
        channel = self.get_channel(Admin_Channel_ID)
        log(str(text))

        #change_status.start()

        embed=discord.Embed(title= py_name , color=0xff80ff)
        embed.set_author(name="created by Napo_II", url="https://github.com/NapoII/")
        embed.set_thumbnail(url="https://i.imgur.com/qqEH4R4.png")
        embed.add_field(name="Version", value=v, inline=True)
        embed.add_field(name="python", value=f"{python_version()}", inline=True)
        embed.add_field(name="github", value="/NapoII", inline=False)
        await channel.send(embed=embed)

        embed=discord.Embed(title="📶 Bot is Online and Rdy to Run... 📶", color=0xff8080)
        embed.add_field(name="client.name", value=self.user.name, inline=True)
        embed.add_field(name="guild_name", value=guild_name, inline=True)
        embed.add_field(name="guild_id", value=str(guild_id), inline=True)
        await channel.send(embed=embed)

  

        @bot.event
        async def on_message(message):  # this event is called when a message is sent by anyone
            # if the user is the client user itself, ignore the message
            await bot.process_commands(message)
            if message.content == praefix:
                return
            
            if message.author == bot.user:
                return
            # this is the string text message of the Message
            content_m = message.content

            # this is the sender of the Message
            user = message.author
            # this is the channel of there the message is sent
            channel_m = message.channel
            # this is a list of the roles from the message sender
            try:
                roles = message.author.roles
            except:
                pass
            guild = message.guild
            if message.author == bot.user:
                return

            log(str(user) + ": (#"+ str(channel_m)+") say: " + content_m)















bot = MyBot()
bot.run(Discord_token)