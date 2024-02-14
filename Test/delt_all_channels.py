

"""
This script is a Discord bot designed to clean a Discord server by deleting all channels, messages, and roles.
It connects to a specified Discord server, prompts the user to confirm the server,
and then proceeds to delete all channels, messages, and roles within the server.

- Token: "YOUR_TOKEN_HERE"
- Application ID: "YOUR_APPLICATION_ID_HERE"
- Server ID: "YOUR_SERVER_ID_HERE"

This script is intended for cleaning purposes and should be used with caution.
Ensure that you have the necessary permissions before running this script on a server.
"""


# Import necessary libraries
import discord
from discord.ext import commands
import pyautogui

# Define your Discord bot's token and application ID
token = 
application_id = 

# Define the server ID where you want to perform operations
SERVER_ID = 

# Set up Discord intents
intents = discord.Intents.default()
intents.all()

# Create a bot instance with specified command prefix and intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

    # Get the server object using the provided server ID
    server = bot.get_guild(int(SERVER_ID))
    print("\n")
    print(f'Successfully connected to server {server.name}')
    print(f"Server : {server.name}\n")
    print("\n")
    
    # Prompt user to confirm the correct server
    do_it = pyautogui.confirm(text=f'Server : {server.name}', title='Correct server?', buttons=['OK', 'Cancel'])

    # If user confirms, proceed with operations
    if do_it == 'OK':
        if server:
            # Delete all channels in the server
            channel_list = [channel.id for channel in server.channels]
            channel_list_len = len(channel_list)
            x = -1
            while True:
                x = x + 1
                if x == channel_list_len:
                    break
                channel = bot.get_channel(channel_list[x])
                await bot.get_channel(channel_list[x]).delete(reason="for test restart")
                print(f"-->> Deleted: {channel.name} - #{channel_list[x]}")

            # Delete all roles in the server
            roles_list = server.roles
            roles_list_len = len(roles_list)
            for role in roles_list:
                try:
                    await role.delete()
                    print(f"-->> Deleted: {role.name} - #{role.id}")
                except Exception as e:
                    print(f"Failed to delete role {role.name}: {e}")
        else:
            print(f'Server with ID {SERVER_ID} not found')
    else:
        pass
    
    # Print summary of operations performed
    print(f"""Done!\nNumber of deleted channels: {channel_list_len}\nNumber of deleted roles: {roles_list_len}""")

# Run the bot with the provided token
bot.run(token)
