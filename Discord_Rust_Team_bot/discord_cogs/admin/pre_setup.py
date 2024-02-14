"""
------------------------------------------------
Discord Bot Setup Cog
------------------------------------------------

A versatile PyCog designed for quick Discord bot server setup.
Automatically creates essential channels and roles, streamlining the process.
Saves time for administrators, ensuring a seamless integration.
Documentation provides straightforward instructions for easy implementation.
----------------------------------------
Full Doku on: https://github.com/NapoII/
"""

# 
from discord.ext import commands
from util.__funktion__ import *
import discord

from util.__funktion__ import *
from util.__Mydiscord_funktions__ import *
from util.__my_imge_path__ import *

img_url = my_image_url()

print(img_url.piktogramm.attention)
# get the path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
bot_path = os.path.abspath(sys.argv[0])
bot_folder = os.path.dirname(bot_path)

token_config_dir = os.path.normpath(os.path.join(bot_folder, "config", "token.ini"))

# construct the path to the config.ini file relative to the current directory
config_dir = os.path.join(bot_folder, "config", "config.ini")

json_path_server_channel_data = os.path.join(current_dir, "server_channel_data.json")

bot_cmd_channel = read_config(config_dir, "channels", "bot_cmd_channel_id")


guild_id = read_config(config_dir, "client", "guild_id", "int")
if guild_id == None:
    guild_id = 1


class server_system_setup(commands.Cog):
    """
    Cog for setting up server-specific systems.

    Attributes:
        bot (commands.Bot): The Discord bot instance.
        config_dir (str): Example configuration directory.
    """

    def __init__(self, bot: commands.Bot):
        """
        Constructor method for server_system_setup Cog.

        Parameters:
            bot (commands.Bot): The Discord bot instance.
        """
        self.bot = bot
        self.config_dir = config_dir  # Beispiel-Konfigurationsverzeichnis


        # Call the method when the bot starts
        self.bot.loop.create_task(self.setup_ticket_system(bot))

    async def setup_ticket_system(self, bot):
        """
        Asynchronous method to set up the ticket system when the bot starts.

        This method is called by the bot when it starts and initializes the
        ticket system setup for the specified guild.
        """
        print("\n --> server_system_setup\n")
        await self.bot.wait_until_ready()
        guild = self.bot.get_guild(guild_id)

        # List to keep track of created items
        was_created_list = []


# Creates a new Role
        
        """
        Create a bot admin role if it doesn't exist and update the config with the role ID.

        Parameters:
        - guild (discord.Guild): The Discord guild where the role will be created.
        - config_dir (str): The directory for storing configuration information.

        Returns:
        - discord.Role: The created or existing bot admin role.

        """

        role_name = "🤖-Bot-Admin"
        role_colour = discord.Color.gold()
        bot_admin_role_id = read_config(config_dir,"roles", "bot_admin_role_id", "int")
        bot_admin_role = discord.utils.get(guild.roles, id=bot_admin_role_id)

        if bot_admin_role != None:
            print(f"The role {bot_admin_role.name} already exists.")
        else:
            print(f"The role {role_name} does not exist.")
            bot_admin_role = await guild.create_role(name=role_name, colour=role_colour)
            print(f"The role {bot_admin_role.name} was created.")
            write_config(config_dir, "roles", "bot_admin_role_id", bot_admin_role.id)


# Creates a new category
            
        """
    Create or get the admin category for the guild and update the config with the category ID.

    Parameters:
    - guild (discord.Guild): The Discord guild where the category will be created.
    - config_dir (str): The directory for storing configuration information.
    - was_created_list (list): A list to keep track of created categories.

    Returns:
    - discord.CategoryChannel: The created or existing admin category.
    """

        category_name = "--------💻 - Admin - 💻--------"
        category_admin_id = read_config(config_dir,"categorys", "category_admin_id", "int")
        category_admin = discord.utils.get(guild.categories, id=category_admin_id)

        if category_admin != None:
            print(f"The category {category_admin.name} already exists.")

        else:
            print(f"The category {category_name} does not yet exist and will now be created")
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, view_channel=False),  # Everyone can view and join the channel
                guild.me: discord.PermissionOverwrite(send_messages=True, read_messages=True)  # The bot can send messages, others can only view
            }

            category_admin = await guild.create_category(category_name, overwrites=overwrites)

            bot_admin_role_id = read_config(config_dir,"roles", "bot_admin_role_id", "int")
            bot_admin_role = discord.utils.get(guild.roles, id = bot_admin_role_id)
            await category_admin.set_permissions(bot_admin_role, read_messages=True, send_messages=True)

            print(f"The category {category_name} was created.")
            category_admin_name = category_admin.name
            category_admin_id = category_admin.id
            write_config(config_dir, "categorys","category_admin_id", category_admin_id)
            
            was_created_list.append(category_admin)


# Creates a new text channel
            
        """
    Create or get the bot command channel, set up permissions, and send informational messages.

    Parameters:
    - guild (discord.Guild): The Discord guild where the channel will be created.
    - config_dir (str): The directory for storing configuration information.
    - was_created_list (list): A list to keep track of created channels.

    Returns:
    - discord.TextChannel: The created or existing bot command channel.
    """
        
        bot_cmd_channel_name = "💻-bot-cmd"
        bot_cmd_channel_id = read_config(config_dir,"channels", "bot_cmd_channel_id", "int")
        bot_cmd_channel = discord.utils.get(guild.text_channels, id=bot_cmd_channel_id)

        if bot_cmd_channel != None:
            print(f"The channel {bot_cmd_channel.name} already exists.")
        else:
            print(f"The channel {bot_cmd_channel_name} does not exist.")


            # Get the admin category for organizing channels
            category_admin_id = read_config(config_dir, "categorys", "category_admin_id", "int")
            category_admin = discord.utils.get(guild.categories, id=category_admin_id)

            # Define permissions for the channel
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, view_channel=False),  # Everyone can view and join the channel
                guild.me: discord.PermissionOverwrite(send_messages=True, read_messages=True)  # The bot can send messages, others can only view
            }

            # Create the bot command channel
            bot_cmd_channel = await guild.create_text_channel(bot_cmd_channel_name, category=category_admin, overwrites=overwrites)
            await bot_cmd_channel.set_permissions(guild.default_role, read_messages=False)

            # Set permissions for the bot admin role in the channel
            bot_admin_role_id = read_config(config_dir,"roles", "bot_admin_role_id", "int")
            bot_admin_role = discord.utils.get(guild.roles, id = bot_admin_role_id)
            await bot_cmd_channel.set_permissions(bot_admin_role, read_messages=True, send_messages=True)
            
            print(f"The channel {bot_cmd_channel.name} was created.")
            # Update the config with the channel information
            write_config(config_dir, "channels", "bot_cmd_channel_id", bot_cmd_channel.id)

            # Add the created channel to the list
            was_created_list.append(bot_cmd_channel)

            # Send informational messages to the channel
            embed_text = f"🔒 Please make sure to adjust the role settings for\n<#{category_admin_id}>\nto restrict channel visibility to authorized users,\ninstead of allowing it to be visible to everyone. 🔓"
            embed = discord.Embed(title="Attention!",description=embed_text, color=0x8080ff)
            embed.set_thumbnail(url=my_image_url.piktogramm.attention())
            await bot_cmd_channel.send(embed=embed)

            gif_url_expl = img_url.example.discord_role_rights

            text = ""
            list_of_hiden_commands = ["/say"]
            for hide_command in list_of_hiden_commands:
                text = text + f"- `{hide_command}`\n"

            description=f"""```Server settings > Intergation > Bot > Set commands```
            > That only the Users with the Role <@&{bot_admin_role.id}>
            > can see the **commands:**
            
            {text}"""


            embed = discord.Embed(title="/Commands Set rights manually",
                      description=description,
                      colour=0xff0000)

            embed.set_image(url=f"{gif_url_expl}")
            await bot_cmd_channel.send(embed=embed)


        """
    Announce the channels that have been created.

    - bot_cmd_channel (discord.TextChannel): The bot command channel where the announcement will be sent.
    - was_created_list (list): A list containing the created channels.

    """
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

            dc_time = discord_time_convert(time.time())
            embed = discord.Embed(title=f"The following Main System Channels have been created:",
                                description=f"> The following channels had to be created:\n{text}\ncreated: {dc_time}",
                                colour=0xffff80)
            await bot_cmd_channel.send(embed=embed)



async def setup(bot: commands.Bot):
    """
    Set up the server system.

    Parameters:
    - bot (commands.Bot): The Discord bot instance.
    - guild_id (int): The ID of the Discord guild to set up.

    Returns:
    None
    """
    await bot.add_cog(server_system_setup(bot), guild=discord.Object(guild_id))