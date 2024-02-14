import os
import requests
import time
from datetime import datetime

def str_to_unix(str):
    # Geben Sie die Zeit im ISO 8601-Format an

    # Konvertiere die Zeit in ein datetime-Objekt
    dt_object = datetime.fromisoformat(str.replace('Z', '+00:00'))

    # Konvertiere datetime-Objekt in Unix-Zeit
    unix_time = int(dt_object.timestamp())
    return(unix_time)

def discord_time_convert(time):
    """
    Converts a Unix timestamp to Discord time format.

    Args:
        time (int): A Unix timestamp to convert to Discord time format.



    Returns:
        - discord_time (str): A string representing the input timestamp in Discord time format.

    Example Usage:
        https://i.imgur.com/YjKkSiR.gif
        
        >>> timestamp = 1617123999
        >>> discord_time = discord_time_convert(timestamp)
        >>> print(discord_time)
        '<t:1617123999:R>'
            1678369942473.0
    """
    time = int(str(time)[:10])
    discord_time = (f"<t:{time}:R>")
    return discord_time




import discord
from discord.ext import commands

# Define your Discord bot's token and application ID
token = 
application_id = 

CHANNEL_ID = 

# Define intents
intents = discord.Intents.default()

# Create the bot client with intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Event triggered when the bot is ready
@bot.event
async def on_ready():
    """
    An event that triggers when the bot is ready.
    Sends an embed to the specified channel.
    """
    channel = bot.get_channel(int(CHANNEL_ID))


    ## add your embed to test -->



    time_stemp = time.time()
    Discord_time_stemp = discord_time_convert(int(time_stemp))

    server_embeds = []


    await channel.send(embeds=server_embeds, content=f"{server_url}")

# Run the bot
bot.run(token)

