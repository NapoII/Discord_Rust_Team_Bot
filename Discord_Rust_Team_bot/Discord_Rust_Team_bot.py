"""Full Doku on: https://github.com/NapoII/"
-----------------------------------------------
add doku
------------------------------------------------
"""
#### import

import os
import sys

import time
import discord
from discord.ext import commands, tasks

from util.__funktion__ import *
from util.__Mydiscord_funktions__ import *

from util.__my_imge_path__ import *
img_url = my_image_url()

from util.__my_path_funktion__ import *
my_file_path = my_file_path()

#### pre Var
py_name = os.path.basename(__file__)



################################################################################################################################
"""
Loading Configuration:
Loads configuration settings from token.ini and config.ini files.
- Discord_token: Token for the Discord bot.
- Application_ID: Discord application ID.
- guild_id: ID of the Discord server.
- praefix: Command prefix for the bot.
- activity_text: Text for the bot's activity status.

"""



# Client
Discord_token = my_file_path.config.Discord_token
Application_ID = my_file_path.config.Application_ID


guild_id = my_file_path.config.guild_id
guild = discord.Object(id=guild_id)
praefix = my_file_path.config.praefix
activity_text = my_file_path.config.activity_text
activity = Discord_Activity(activity_text)


################################################################################################################################
# main

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=praefix,
            intents=discord.Intents.all(),
            application_id=Application_ID,
            activity=discord.Game(activity_text)
        )

        # List of initial extensions to load
        # add more cogs here

        self.initial_extensions = [
            "discord_cogs.rust.setup.rust_pre_setup",
            "discord_cogs.rust.channel_hopper.channel_hopper",
            "discord_cogs.rust.server_stats.server_stats",
            "discord_cogs.rust.team_cheack.team_cheack",
            "discord_cogs.rust.player_observation.player_observation",
            "discord_cogs.rust.rust_info.rust_info",
            "discord_cogs.rust.squad_manage.squad_manage"
        
        ]


    async def setup_hook(self):
        """Load initial extensions during bot setup."""
        for ext in self.initial_extensions:
            await self.load_extension(ext)

        await bot.tree.sync(guild=discord.Object(guild_id))

    async def on_ready(self):
        """Event triggered when the bot is ready."""
        guild = self.get_guild(guild_id)  # Access guild from the class attribute
        if not guild:
            print("Bot is not in the specified guild. Please check your configuration.")
            return

        print(f'\nLogged in as {self.user} (ID: {self.user.id})')

        time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{time_str} --> 📶 Bot is Online and Ready to Run... 📶")
        print("\n")


# Instantiate and run the bot
bot = MyBot()
bot.run(Discord_token)


################################################################################################################################
#   Link collection for useful are for discord py
#
#   Discord PY Doku : https://discordpy.readthedocs.io/en/stable/
#   Embed generator : https://embed.dan.onl/


"""
Discord Embed Limits

If you plan on using embed responses for your bot you should know the limits of the embeds on Discord or you will get Invalid Form Body errors:

    Embed title is limited to 256 characters
    Embed description is limited to 4096 characters
    An embed can contain a maximum of 25 fields
    A field name/title is limited to 256 character and the value of the field is limited to 1024 characters
    Embed footer is limited to 2048 characters
    Embed author name is limited to 256 characters
    The total of characters allowed in an embed is 6000
"""