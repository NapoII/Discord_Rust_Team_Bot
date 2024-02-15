"""Full Doku on: https://github.com/NapoII/Discord_Rust_Team_bot"
-----------------------------------------------
This COG is for embed a help information for Rust.
exampel : cctv codes


------------------------------------------------
"""
# 
from discord.ext import commands, tasks
from util.__funktion__ import *
from util.__my_imge_path__ import *
img_url = my_image_url()
import random
import discord
from discord import app_commands
from discord import app_commands, ui
from discord import Color
import asyncio
from datetime import datetime

# get the path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
bot_path = os.path.abspath(sys.argv[0])
bot_folder = os.path.dirname(bot_path)



# construct the path to the config/ file relative to the current directory
config_dir = os.path.join(bot_folder, "config", "config.ini")

# json_path_server_channel_data_dir = os.path.join(current_dir, "server_channel_data.json")

json_rust_help_commands_data_dir = os.path.join(bot_folder, "config","json", "rust_help_commands.json")
json_rust_observation_commands_data_dir = os.path.join(bot_folder, "config","json", "observation_commands.json")

bot_cmd_channel = read_config(config_dir, "channels", "bot_cmd_channel_id")


guild_id = read_config(config_dir, "client", "guild_id", "int")
if guild_id == None:
    guild_id = 1



class rust_system_setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_dir = config_dir  


        # Here the method is called when the bot is started
        self.bot.loop.create_task(self.setup_rust_system())

    async def setup_rust_system(self):
        print ("\n --> rust_system_setup\n")
        await self.bot.wait_until_ready()  
        guild = self.bot.get_guild(guild_id)

        was_created_list = []


# Creates a new Role
        role_name = "🔥-Rust-Ultras"
        role_colour = discord.Color.red()
        rust_ultras_role_id = read_config(config_dir,"roles", "rust_ultras_role_id", "int")
        rust_ultras_role = discord.utils.get(guild.roles, id=rust_ultras_role_id)

        if rust_ultras_role != None:
            print(f"The role {rust_ultras_role.name} already exists.")
        else:
            print(f"The role {role_name} does not exist.")
            rust_ultras_role = await guild.create_role(name=role_name, colour=role_colour)
            print(f"The role {rust_ultras_role.name} was created.")
            write_config(config_dir, "roles", "rust_ultras_role_id", rust_ultras_role.id)


# Creates a new category
        category_name = "------🎮-Rust-Team-🎮-------"
        category_rust_id = read_config(config_dir,"categorys", "category_rust_id", "int")
        category_rust = discord.utils.get(guild.categories, id=category_rust_id)

        if category_rust != None:
            print(f"The category {category_rust.name} already exists.")

        else:
            print(f"The category {category_name} does not yet exist and will now be created")
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, view_channel=False),  # Everyone can view and join the channel
                guild.me: discord.PermissionOverwrite(send_messages=True, read_messages=True)  # The bot can send messages, others can only view
            }

            category_rust = await guild.create_category(category_name, overwrites=overwrites)

            rust_ultras_role_id = read_config(config_dir,"roles", "rust_ultras_role_id", "int")
            rust_ultras_role = discord.utils.get(guild.roles, id = rust_ultras_role_id)

            await category_rust.set_permissions(rust_ultras_role, read_messages=True, send_messages=True)

            print(f"The category {category_name} was created.")
            category_rust_name = category_rust.name
            category_rust_id = category_rust.id
            write_config(config_dir, "categorys","category_rust_id", category_rust_id)
            
            was_created_list.append(category_rust)


# Creates a new text channel
        server_stats_channel_name = "📈 Server Stats"
        server_stats_channel_id = read_config(config_dir,"channels", "server_stats_channel_id", "int")
        server_stats_channel = discord.utils.get(guild.text_channels, id=server_stats_channel_id)

        if server_stats_channel != None:
            print(f"The channel {server_stats_channel.name} already exists.")
        else:
            print(f"The channel {server_stats_channel_name} does not exist.")

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, view_channel=False),  # Everyone can view and join the channel
                guild.me: discord.PermissionOverwrite(send_messages=True, read_messages=True)  # The bot can send messages, others can only view
            }

            server_stats_channel = await guild.create_text_channel(server_stats_channel_name, category=category_rust, overwrites=overwrites)
            
            await server_stats_channel.set_permissions(guild.default_role, read_messages=False)
            await server_stats_channel.set_permissions(rust_ultras_role, read_messages=True, send_messages=True)
            
            print(f"The channel {server_stats_channel.name} was created.")
            write_config(config_dir, "channels", "server_stats_channel_id", server_stats_channel.id)

            embed = discord.Embed(title="#rust-server-stats")

            embed.set_author(name=f"@{guild.name}", icon_url=img_url.rust.team_logo)
            embed.add_field(name="```/change_server```",
                            value="Change the server to which the bot should be connected by entering the battlemetrics id of the server",
                            inline=False)
            url_gif_expl = img_url.example.battlemetrics_url
            embed.set_image(url=url_gif_expl)
            embed.set_thumbnail(url=img_url.piktogramm.i)
            await server_stats_channel.send(embed=embed)

            was_created_list.append(server_stats_channel)


# Creates a new text channel
        player_observation_name = "🔔-Player-Observation"
        player_observation_channel_id = read_config(config_dir,"channels", "player_observation_channel_id", "int")
        player_observation = discord.utils.get(guild.text_channels, id=player_observation_channel_id)

        if player_observation != None:
            print(f"The channel {player_observation.name} already exists.")
        else:
            print(f"The channel {player_observation_name} does not exist.")

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, view_channel=False),  # Everyone can view and join the channel
                guild.me: discord.PermissionOverwrite(send_messages=True, read_messages=True)  # The bot can send messages, others can only view
            }

            player_observation = await guild.create_text_channel(player_observation_name, category=category_rust, overwrites=overwrites)
            
            await player_observation.set_permissions(guild.default_role, read_messages=False)
            await player_observation.set_permissions(rust_ultras_role, read_messages=True, send_messages=True)
            
            print(f"The channel {player_observation.name} was created.")
            write_config(config_dir, "channels", "player_observation_channel_id", player_observation.id)

            icon_url = img_url.rust.team_logo
            thumbnail_url = img_url.piktogramm.i
            embed = discord.Embed(title="#rust-player-observation", color=0x8080ff)
            embed.set_author(name=f"@{guild.name}",icon_url=icon_url)
            embed.set_thumbnail(url=thumbnail_url)

            json_rust_observation_commands_data = read_json_file(json_rust_observation_commands_data_dir)

            # Max number of fields per embed
            max_fields_per_embed = 25

            # Counter for fields
            field_count = 0

            # List to store embeds
            embeds_list = []

            for item in json_rust_observation_commands_data:
                if field_count < max_fields_per_embed:
                    command = item["command"]
                    description = item["description"]
                    embed.add_field(name=command, value=description, inline=False)
                    field_count += 1
                else:
                    # Reset field count
                    field_count = 0
                    # Append current embed to the list
                    embeds_list.append(embed)
                    # Create a new embed for the next set of fields
                    embed = discord.Embed(title="#rust-player-observation", color=0x8080ff)
                    embed.set_author(name=f"@{guild.name}",
                                    icon_url=icon_url)
                    embed.set_thumbnail(url=thumbnail_url)
                    # Add the current field to the new embed
                    embed.add_field(name=command, value=description, inline=True)
                    # Increment field count for the new embed
                    field_count += 1

            # Append the last embed to the list
            embeds_list.append(embed)
            await player_observation.send(embeds=embeds_list)

            was_created_list.append(player_observation)


# Creates a new text channel
        rust_info_name = "🌐-Rust-info"
        rust_info_channel_id = read_config(config_dir,"channels", "rust_info_channel_id", "int")
        rust_info = discord.utils.get(guild.text_channels, id=rust_info_channel_id)

        if rust_info != None:
            print(f"The channel {rust_info.name} already exists.")
        else:
            print(f"The channel {rust_info_name} does not exist.")

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, view_channel=False),  # Everyone can view and join the channel
                guild.me: discord.PermissionOverwrite(send_messages=True, read_messages=True)  # The bot can send messages, others can only view
            }

            rust_info = await guild.create_text_channel(rust_info_name, category=category_rust, overwrites=overwrites)
            
            await rust_info.set_permissions(guild.default_role, read_messages=False)
            await rust_info.set_permissions(rust_ultras_role, read_messages=True, send_messages=True)
            
            print(f"The channel {rust_info.name} was created.")
            write_config(config_dir, "channels", "rust_info_channel_id", rust_info.id)

            icon_url = img_url.rust.team_logo
            thumbnail_url = img_url.piktogramm.i
            embed = discord.Embed(title="#rust-info", color=0x8080ff)
            embed.set_author(name=f"@{guild.name}",
                            icon_url=icon_url)
            embed.set_thumbnail(url=thumbnail_url)

            json_rust_help_commands_data = read_json_file(json_rust_help_commands_data_dir)

            # Max number of fields per embed
            max_fields_per_embed = 25

            # Counter for fields
            field_count = 0

            # List to store embeds
            embeds_list = []

            for item in json_rust_help_commands_data:
                if field_count < max_fields_per_embed:
                    command = item["command"]
                    description = item["description"]
                    embed.add_field(name=command, value=description, inline=False)
                    field_count += 1
                else:
                    # Reset field count
                    field_count = 0
                    # Append current embed to the list
                    embeds_list.append(embed)
                    # Create a new embed for the next set of fields
                    embed = discord.Embed(title="#rust-info", color=0x8080ff)
                    embed.set_author(name=f"@{guild.name}",
                                    icon_url=icon_url)
                    embed.set_thumbnail(url=thumbnail_url)
                    # Add the current field to the new embed
                    embed.add_field(name=command, value=description, inline=True)
                    # Increment field count for the new embed
                    field_count += 1

            # Append the last embed to the list
            embeds_list.append(embed)

            await rust_info.send(embeds = embeds_list)

            was_created_list.append(rust_info)


# Creates a new text channel
        rust_team_name = "💬-team-chat"
        rust_team_text_channel_id = read_config(config_dir,"channels", "rust_team_text_channel_id", "int")
        rust_team_text_channel = discord.utils.get(guild.text_channels, id=rust_team_text_channel_id)

        if rust_team_text_channel != None:
            print(f"The channel {rust_team_text_channel.name} already exists.")
        else:
            print(f"The channel rust_team_text_channel does not exist.")

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, view_channel=False),  # Everyone can view and join the channel
                guild.me: discord.PermissionOverwrite(send_messages=True, read_messages=True)  # The bot can send messages, others can only view
            }

            rust_team_text_channel = await guild.create_text_channel(rust_team_name, category=category_rust, overwrites=overwrites)
            
            await rust_team_text_channel.set_permissions(guild.default_role, read_messages=False)
            await rust_team_text_channel.set_permissions(rust_ultras_role, read_messages=True, send_messages=True)
            
            print(f"The channel {rust_team_text_channel.name} was created.")
            write_config(config_dir, "channels", "rust_team_text_channel_id", rust_team_text_channel.id)

            embed = discord.Embed(colour=0xffffff, description=f"**This channel is exclusively for <@&{rust_ultras_role_id}>. 🔒**\n> Here, we strategize raids and plan our next moves. 💥\n> **Let's conquer together!🚀**\n#TeamWorkMakesTheDreamWork")
            embed.set_thumbnail(url=img_url.piktogramm.text_talk)
            embed.set_author(name="🛡️ Welcome to the Rust Ultra Team communication channel! 🛠️")
            await rust_team_text_channel.send(embed=embed)

            was_created_list.append(rust_team_text_channel)


        was_created_list_len = len(was_created_list)
        if was_created_list_len != 0:
            x = -1
            text = ""
            while True:
                x = x + 1
                if x == was_created_list_len:
                    break
                id = was_created_list[x].id
                text = text + f"<#{id}>\n"


            bot_cmd_channel_id = read_config(config_dir,"channels", "bot_cmd_channel_id", "int")
            bot_cmd_channel = discord.utils.get(guild.text_channels, id=bot_cmd_channel_id)
            dc_time = discord_time_convert(time.time())
            embed = discord.Embed(title=f"The following Rust Team Channels have been created:",
                                description=f"> The following channels had to be created:\n{text}\ncreated: {dc_time}",
                                colour=0xffff80)
            await bot_cmd_channel.send(embed=embed)



async def setup(bot: commands.Bot):
    await bot.add_cog(rust_system_setup(bot), guild=discord.Object(guild_id))