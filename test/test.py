import discord
from discord.ext import commands


# Client
Discord_token = "MTEwMzQwNzU1MDkxOTA4NjE1MQ.GyZ6pA.JMe_hXKrkfReEHF8o-ZRfHJOKf5zgBxS9WEmqQ"
Application_ID = 1103407550919086151

import discord
from discord.ext import commands

from discord import Intents

intents = Intents.default()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)


@client.event
async def on_ready():
    print('Bot ist bereit!')
    for guild in client.guilds:
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


        # Durchsucht alle vorhandenen Kategorien auf dem Server nach der Kategorie mit dem Namen "Rust"
        category_name = "-----🎮 - Rust - 🎮------"
        category_Rust = discord.utils.get(guild.categories, name=category_name)

        if category_Rust is not None:

            print(f"The category {category_Rust.name} already exists.")

        else:
            overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=False),Rust_role: discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True, speak=True),guild.me: discord.PermissionOverwrite(manage_channels=True)}

            print(f"The category {category_name} does not yet exist and will now be created")
            # Creates a new category
            category_Rust = await guild.create_category(category_name, overwrites=overwrites)
            print(f"The category {category_name} was created.")

            Server_Stats = await guild.create_text_channel("📈 Server Stats", category=category_Rust)
            print(f"The channel {Server_Stats.name} was created.")

            Player_Observation = await guild.create_text_channel("🔔 Player Observation", category=category_Rust)
            print(f"The channel {Player_Observation.name} was created.")

            Rust_info = await guild.create_text_channel("💻 Rust_info", category=category_Rust)
            print(f"The channel {Rust_info.name} was created.")

            Team_Chat = await guild.create_text_channel("📝 Team Chat", category=category_Rust)
            print(f"The channel {Team_Chat.name} was created.")

            Rust_main_voice = "Team-Voice" 
            # Creates a new Voice channel
            Rust_main_voice = await guild.create_voice_channel(Rust_main_voice, category=category_Rust)
            print(f"The voice channel {Rust_main_voice.name} has been created.")



        # Durchsucht alle vorhandenen Kategorien auf dem Server nach der Kategorie mit dem Namen "Rust"
        category_name = "-------💻 - Admin - 💻-------"
        category_Admin = discord.utils.get(guild.categories, name = category_name)
        if category_Admin is not None:

            print(f"The category {category_Admin.name} already exists.")

        else:
            overwrites = {guild.default_role: discord.PermissionOverwrite(view_channel=False),Admin_role: discord.PermissionOverwrite(view_channel=True),guild.me: discord.PermissionOverwrite(manage_channels=True)}
            print(f"The category {category_name} does not yet exist and will now be created")
            # Creates a new category
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(manage_channels=True),
                Admin_role: discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True, speak=True, view_channel=True)
            }

            category_Admin = await guild.create_category(category_name, overwrites=overwrites)
            await category_Admin.edit(position=1, reason="Set category position")
            await category_Admin.edit(sync_permissions=True, reason="Sync category permissions")



            print(f"The category {category_name} was created.")

            console = await guild.create_text_channel("▶️ console", category=category_Admin)
            print(f"The channel {console.name} was created.")

            delt_messages = await guild.create_text_channel("🚮 delt-messages", category= category_Admin)
            print(f"The channel {delt_messages.name} was created.")






client.run(Discord_token)
