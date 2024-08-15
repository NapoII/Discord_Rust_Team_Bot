""""
------------------------------------------------
squad_manage
------------------------------------------------
Add description of the cog
------------------------------------------------
Full Doku on: https://github.com/NapoII/
"""

from util.__my_path_funktion__ import my_file_path
from util.__funktion__ import *
from discord_cogs.rust.squad_manage._funktion_squad_manage import *
from util.__my_imge_path__ import *
my_image_url = my_image_url()

config_ini_dir = my_file_path.config.config_ini_dir

from discord.ext import commands

import os
import sys

guild_id = guild_id = int(read_config(config_dir, "client", "guild_id"))
squad_team_list_json_dir= my_file_path.json.squad_team_list_json_dir


class squad_setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_dir = config_dir
        self.config_ini_dir = config_ini_dir  # Assuming this is defined somewhere
        # Use the predefined paths for JSON files
        self.squad_data_file = my_file_path.json.squad_team_list_json_dir
        self.bot.loop.create_task(self.setup_squad())

    async def setup_squad(self):
        squad_mode = my_file_path.config.squad_mode
        if not squad_mode:
            return
        
        print("\n --> setup_squad\n")
        await self.bot.wait_until_ready()
        guild = self.bot.get_guild(guild_id)

        # Ensure the category exists or create it
        category , rust_ultras_role, squad_lead_role = await self.ensure_category_exists(guild, "------🛡-Rust-Squads-🛡-------")

        # Load squad data from JSON
        with open(self.squad_data_file, 'r') as f:
            squad_data = json.load(f)

        # Ensure that each role has its own voice channel
        await self.ensure_voice_channels(guild, squad_data, category)

        # Setup Squad Panel Channel
        await self.setup_channel_with_message(
            guild,
            category,
            rust_ultras_role,
            "🛡️ Squad-Panel",
            "squad_panel_channel_id",
            "rust_squad_squad_panel_mgs_id",
            "Squad Roles",
            "Click on a role to join or leave the squad.",
            squad_data,
            include_add_delt=False,
        )

        # Setup Swarp Control Channel
        await self.setup_channel_with_message(
            guild,
            category,
            squad_lead_role,
            "👑-Squad-Lead",
            "swarp_control_channel_id",
            "rust_squad_control_mgs_id",
            "Swarp Control",
            "Manage your squad roles and swarp settings.",
            squad_data,
            include_add_delt=True,
            
        )


    async def setup_channel_with_message(self, guild, category, role_that_can_view, channel_name, channel_config_key, message_config_key, embed_title, embed_description, squad_data, include_add_delt):
        # Get the channel or create it within the category
        channel_id = read_config(self.config_ini_dir, "channels", channel_config_key, "int")
        channel = discord.utils.get(guild.text_channels, id=channel_id)

        if channel is None:
            print(f"Channel {channel_name} not found, creating new one.")
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False, view_channel=False),
                guild.me: discord.PermissionOverwrite(send_messages=True, read_messages=True)
            }


            overwrites[role_that_can_view] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

            channel = await guild.create_text_channel(channel_name, category=category, overwrites=overwrites)

            # Update config with new channel ID
            write_config(self.config_ini_dir, "channels", channel_config_key, channel.id)
            print(f"Channel {channel_name} created with ID {channel.id} and updated config.")

        # Attempt to load the message ID from file
        message_id_str = read_config(self.config_ini_dir, "msgs", message_config_key)
        message_id = int(message_id_str) if message_id_str else None

        # Validate the message_id and try to fetch the message
        if message_id:
            try:
                message = await channel.fetch_message(message_id)
                if message:
                    print(f"Reattached to existing message in {channel_name} with ID {message.id}.")
                    await self.attach_buttons_to_message(message, squad_data, include_add_delt=include_add_delt)
                    return
            except (discord.NotFound, discord.HTTPException):
                print(f"Stored message ID in {channel_name} not found or invalid. Creating a new message.")

        # Create a new message if no existing message was found
        if include_add_delt:
            embed = discord.Embed(title="Squad Leader Controle",
                        description=f"> **Squad-Role Button**: move all users with the respective squad role  into their squad voice channel.\n\n> **ADD Button** Create a new squad with its role and voice channel.\n\n> ** DELT** Delete a squad with its role and voice channel. ❗***Warning: This action is irreversible!***",
                        colour=0xffffff)
            embed.set_thumbnail(url=my_image_url.piktogramm.controle)

        if not include_add_delt:
            embed = discord.Embed(title="Join or Leave a Squad",
                    description=f"**Click on the squad name to join or leave the squad.**\n> The 👑-Squad-Lead  can automatically move\n> everyone with the squad role\n> into the respective squad channel.",
                    colour=0xffffff)

            embed.set_thumbnail(url=my_image_url.piktogramm.join)

        view = self.create_view_with_buttons(squad_data, include_add_delt=include_add_delt)
        message = await channel.send(embed=embed, view=view)

        # Save the message ID to the config
        write_config(self.config_ini_dir, "msgs", message_config_key, message.id)
        print(f"Created and saved new message in {channel_name} with ID {message.id} and updated config.")




    async def ensure_category_exists(self, guild, category_name):


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


# Creates a new Role
        role_name = "👑-Squad-Lead"
        role_colour = discord.Color.red()
        squad_lead_role_id = read_config(config_dir,"roles", "squad_lead_role_id", "int")
        squad_lead_role = discord.utils.get(guild.roles, id=squad_lead_role_id)

        if squad_lead_role != None:
            print(f"The role {squad_lead_role.name} already exists.")
        else:
            print(f"The role {role_name} does not exist.")
            squad_lead_role = await guild.create_role(name=role_name, colour=role_colour)
            print(f"The role {squad_lead_role.name} was created.")
            write_config(config_dir, "roles", "squad_lead_role_id", squad_lead_role.id)


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
        category_rust_squad_id = read_config(config_dir,"categorys", "category_rust_squad_id", "int")
        category_rust = discord.utils.get(guild.categories, id=category_rust_squad_id)

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
            category_rust_squad_id = category_rust.id
            write_config(config_dir, "categorys","category_rust_squad_id", category_rust_squad_id)
            
        return category_rust , rust_ultras_role, squad_lead_role

    async def ensure_voice_channels(self, guild, squad_data, category):
        print("Ensuring all roles have corresponding voice channels...")
        channels_created = False

        for squad_id, squad_info in squad_data.items():
            role_id = squad_info.get("role_id")
            role_name = squad_info["squad_name"]
            role_colour = discord.Color.green()
            rust_role = discord.utils.get(guild.roles, id=role_id)

            if rust_role != None:
                print(f"The role {role_name} already exists.")
            else:
                print(f"The role {squad_info["squad_name"]} does not exist.")
                rust_role = await guild.create_role(name=role_name, colour=role_colour)
                squad_info["role_id"] = rust_role.id
                channels_created = True
                print(f"The role {role_name} was created.")


            voice_channel_id = squad_info.get("voice_channel_id")
            voice_channel = discord.utils.get(guild.voice_channels, id=voice_channel_id)

            if voice_channel is None:
                print(f"Voice channel for role {squad_info['squad_name']} not found, creating new one.")
                role = discord.utils.get(guild.roles, id=squad_info["role_id"])

                new_channel = await guild.create_voice_channel(squad_info["squad_name"], category=category)
                squad_info["voice_channel_id"] = new_channel.id
                channels_created = True
                print(f"Created new voice channel {new_channel.name} with ID {new_channel.id} for role {role.name}.")

        if channels_created:
            # Save the updated squad data with the new voice_channel_id
            with open(self.squad_data_file, 'w') as f:
                json.dump(squad_data, f, indent=4)
            print("Updated squad data JSON file with new IDs.")
        else:
            pass

    def create_view_with_buttons(self, squad_data, include_add_delt=False):
        view = discord.ui.View()

        # Add the dynamic role buttons
        for squad_id, squad_info in squad_data.items():
            role_button = discord.ui.Button(label=squad_info["squad_name"], custom_id=f"squad_role_{squad_id}")
            role_button.callback = self.handle_role_button
            view.add_item(role_button)

        # Optionally add ADD and DELT buttons
        if include_add_delt:
            add_button = discord.ui.Button(label="ADD", style=discord.ButtonStyle.green, custom_id="squad_add")
            delt_button = discord.ui.Button(label="DELT", style=discord.ButtonStyle.red, custom_id="squad_delt")

            add_button.callback = self.handle_add_button
            delt_button.callback = self.handle_delt_button

            view.add_item(add_button)
            view.add_item(delt_button)

        return view

    async def attach_buttons_to_message(self, message, squad_data, include_add_delt=False):
        view = self.create_view_with_buttons(squad_data, include_add_delt)
        await message.edit(view=view)


    async def handle_role_button(self, interaction: discord.Interaction):
        squad_id = interaction.data['custom_id'].split('_')[-1]
        user = interaction.user
        guild = interaction.guild

        with open(self.squad_data_file, 'r') as f:
            squad_data = json.load(f)

        if squad_id in squad_data:
            role_id = squad_data[squad_id]["role_id"]
            voice_channel_id = squad_data[squad_id]["voice_channel_id"]

            role = discord.utils.get(guild.roles, id=role_id)
            voice_channel = discord.utils.get(guild.voice_channels, id=voice_channel_id)

            if interaction.message.id == int(read_config(self.config_ini_dir, "msgs", "rust_squad_squad_panel_mgs_id")):
                # Handle adding or removing the role
                if role in user.roles:
                    await user.remove_roles(role)
                    embed = discord.Embed(description=f"**You’ve left the squad <@&{role.id}>**\n> Click the button again to rejoin if you change your mind.",
                      colour=0xff0000)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    await user.add_roles(role)
                    embed = discord.Embed(description=f"**You’ve joined the squad <@&{role.id}>! **\n    > Click the button again to leave the squad.",
                      colour=0xff8040)
                    await interaction.response.send_message(embed=embed, ephemeral=True)

            elif interaction.message.id == int(read_config(self.config_ini_dir, "msgs", "rust_squad_control_mgs_id")):
                # Move all members with the role to the corresponding voice channel
                if role and voice_channel:
                    members_with_role = [member for member in guild.members if role in member.roles]
                    for member in members_with_role:
                        try:
                            if member.voice is not None:  # Ensure the member is in a voice channel
                                await member.move_to(voice_channel)
                        except Exception as e:
                            print(f"Could not move {member.display_name}: {e}")

                    embed = discord.Embed(description=f"All **<@&{role.id}>** Squad members \nhave been moved to the voice channel\n**<#{voice_channel.id}>**",
                      colour=0x0080ff)
                    await interaction.response.send_message(embed=embed, ephemeral=True)


    async def handle_add_button(self, interaction: discord.Interaction):
        modal = AddSquadModal()

        # Send the modal to the user
        await interaction.response.send_modal(modal)

        # Handle the submission of the modal
        def check(modal_interaction):
            return modal_interaction.custom_id == modal.custom_id and modal_interaction.user.id == interaction.user.id

        try:
            modal_interaction = await self.bot.wait_for('modal_submit', check=check, timeout=300)
            squad_name = modal_interaction.data['components'][0]['value']
            description = modal_interaction.data['components'][1]['value']

            await self.create_squad(interaction, squad_name, description)
            embed = discord.Embed(description=f"Squad **{squad_name}** created successfully!",
                                colour=0x0080ff)
            await modal_interaction.response.send_message(embed=embed, ephemeral=True)
        except asyncio.TimeoutError:
            await interaction.followup.send("You took too long to respond.", ephemeral=True)

    async def create_squad(self, interaction: discord.Interaction, squad_name: str, description: str):
        guild = interaction.guild
        
        # Step 2: Create Role
        role = await guild.create_role(name=squad_name)
        
        # Step 3: Create Voice Channel
        category_rust_squad_id = read_config(self.config_ini_dir, "categorys", "category_rust_squad_id", "int")
        category = discord.utils.get(guild.categories, id=category_rust_squad_id)
        voice_channel = await guild.create_voice_channel(squad_name, category=category)

        # Step 4: Update JSON
        with open(self.squad_data_file, 'r') as f:
            squad_data = json.load(f)

        new_squad_id = str(role.id)
        squad_data[new_squad_id] = {
            "squad_name": squad_name,
            "role_id": role.id,
            "voice_channel_id": voice_channel.id,
            "description": description,
        }

        with open(self.squad_data_file, 'w') as f:
            json.dump(squad_data, f, indent=4)

        # Step 5: Update squad-lead and 🛡-squad-panel Messages
        swarp_control_channel_id = read_config(self.config_ini_dir, "channels", "swarp_control_channel_id", "int")
        squad_panel_channel_id = read_config(self.config_ini_dir, "channels", "squad_panel_channel_id", "int")

        swarp_control_channel = discord.utils.get(guild.text_channels, id=swarp_control_channel_id)
        squad_panel_channel = discord.utils.get(guild.text_channels, id=squad_panel_channel_id)

        if swarp_control_channel:
            await self.update_channel_message(swarp_control_channel, squad_data, include_add_delt=True)

        if squad_panel_channel:
            await self.update_channel_message(squad_panel_channel, squad_data, include_add_delt=False)

    async def update_channel_message(self, channel, squad_data, include_add_delt):
        if "squad-lead" in channel.name:
            config_name = "rust_squad_control_mgs_id"
        if "squad-panel" in channel.name:
            config_name = "rust_squad_squad_panel_mgs_id"
            
        message_id_str = read_config(self.config_ini_dir, "msgs", config_name)
        message_id = int(message_id_str) if message_id_str else None

        if message_id:
            try:
                message = await channel.fetch_message(message_id)
                await self.attach_buttons_to_message(message, squad_data, include_add_delt=include_add_delt)
            except (discord.NotFound, discord.HTTPException):
                await self.create_new_channel_message(channel, squad_data, include_add_delt)
        else:
            await self.create_new_channel_message(channel, squad_data, include_add_delt)

    async def create_new_channel_message(self, channel, squad_data, include_add_delt):
        embed = discord.Embed(title="Squad Roles", description=f"Click on a button to join or leave the squad.")
        view = self.create_view_with_buttons(squad_data, include_add_delt=include_add_delt)
        message = await channel.send(embed=embed, view=view)

        config_name = f"rust_squad_{channel.name.replace(" ", "_").lower()}_mgs_id"
        write_config(self.config_ini_dir, "msgs", config_name, message.id)


    async def handle_delt_button(self, interaction: discord.Interaction):
        # Load squad data from JSON
        with open(self.squad_data_file, 'r') as f:
            squad_data = json.load(f)

        # Create a dropdown with all roles
        options = []
        for squad_id, squad_info in squad_data.items():
            options.append(discord.SelectOption(label=squad_info["squad_name"], value=squad_id))

        if not options:
            embed = discord.Embed(description="No Squad available for deletion.",
                      colour=0xff0000)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        # Create a view with the select menu
        select_menu = discord.ui.Select(placeholder="Select a role to delete", options=options)
        select_menu.callback = self.handle_select_delete

        view = discord.ui.View()
        view.add_item(select_menu)
        embed = discord.Embed(description="**Select the role you want to delete:**",
                            colour=0xff0000)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    async def handle_select_delete(self, interaction: discord.Interaction):
        selected_squad_id = interaction.data['values'][0]  # Get the selected squad ID

        # Load squad data from JSON
        with open(self.squad_data_file, 'r') as f:
            squad_data = json.load(f)

        if selected_squad_id in squad_data:
            role_id = squad_data[selected_squad_id]["role_id"]
            voice_channel_id = squad_data[selected_squad_id]["voice_channel_id"]

            role = discord.utils.get(interaction.guild.roles, id=role_id)
            voice_channel = discord.utils.get(interaction.guild.voice_channels, id=voice_channel_id)

            if role:
                await role.delete()
            if voice_channel:
                await voice_channel.delete()

            # Remove the role from the JSON
            del squad_data[selected_squad_id]

            with open(self.squad_data_file, 'w') as f:
                json.dump(squad_data, f, indent=4)

            embed = discord.Embed(description=f"Role **{role.name}** and associated voice channel have been deleted.",
                      colour=0xff0000)
            await interaction.response.send_message(embed=embed, ephemeral=True)

            # Update the squad-lead and squad-panel messages
            await self.update_swarp_control_and_squad_panel(interaction.guild, squad_data)
        else:
            embed = discord.Embed(description="The selected squad no longer exists.",
                      colour=0xff0000)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    async def update_swarp_control_and_squad_panel(self, guild, squad_data):
        # Update Swarp Control Channel
        swarp_control_channel_id = read_config(self.config_ini_dir, "channels", "swarp_control_channel_id", "int")
        squad_panel_channel_id = read_config(self.config_ini_dir, "channels", "squad_panel_channel_id", "int")

        swarp_control_channel = discord.utils.get(guild.text_channels, id=swarp_control_channel_id)
        squad_panel_channel = discord.utils.get(guild.text_channels, id=squad_panel_channel_id)

        if swarp_control_channel:
            await self.update_channel_message(swarp_control_channel, squad_data, include_add_delt=True)

        if squad_panel_channel:
            await self.update_channel_message(squad_panel_channel, squad_data, include_add_delt=False)

    async def update_channel_message(self, channel, squad_data, include_add_delt):
        # Fetch the existing message or create a new one if it doesn't exist
        if "squad-lead" in channel.name:
            config_name = "rust_squad_control_mgs_id"
        if "squad-panel" in channel.name:
            config_name = "rust_squad_squad_panel_mgs_id"
            
        message_id_str = read_config(self.config_ini_dir, "msgs", config_name)
        message_id = int(message_id_str) if message_id_str else None

        if message_id:
            try:
                message = await channel.fetch_message(message_id)
                await self.attach_buttons_to_message(message, squad_data, include_add_delt=include_add_delt)
            except (discord.NotFound, discord.HTTPException):
                await self.create_new_channel_message(channel, squad_data, include_add_delt)
        else:
            await self.create_new_channel_message(channel, squad_data, include_add_delt)

    async def create_new_channel_message(self, channel, squad_data, include_add_delt):
        embed = discord.Embed(title="Join or Leave a Squad",
                            description=f"**Click on the squad name to join or leave the squad.**\n> The 👑-Squad-Lead  can automatically move\n> everyone with the squad role\n> into the respective squad channel.",
                            colour=0xffffff)

        embed.set_thumbnail(url=my_image_url.piktogramm.join)
        
        view = self.create_view_with_buttons(squad_data, include_add_delt=include_add_delt)
        message = await channel.send(embed=embed, view=view)

        config_name = f"rust_squad_{channel.name.replace(' ', '_').lower()}_mgs_id"
        write_config(self.config_ini_dir, "msgs", config_name, message.id)



class AddSquadModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Add New Squad")

        # Add text inputs to the modal
        self.squad_name = discord.ui.TextInput(
            label="Squad Name",
            placeholder="Enter squad name",
            max_length=100,
        )
        self.add_item(self.squad_name)

        self.description = discord.ui.TextInput(
            label="Description",
            style=discord.TextStyle.paragraph,
            placeholder="Enter squad description",
            max_length=300,
        )
        self.add_item(self.description)

    async def on_submit(self, interaction: discord.Interaction):
        # Access the bot through the interaction object
        bot = interaction.client

        squad_name = self.squad_name.value
        description = self.description.value

        # Call the create_squad method from the squad_setup class
        cog = bot.get_cog("squad_setup")
        if cog:
            await cog.create_squad(interaction, squad_name, description)

        embed = discord.Embed(description=f"Squad **{squad_name}** created successfully!",
                      colour=0xff80ff)
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(squad_setup(bot), guild=discord.Object(guild_id)) # <-- change class name