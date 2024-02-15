"""Full Doku on: https://github.com/NapoII/Discord_Rust_Team_bot"
-----------------------------------------------
This cog creates automatic voice channels when the user needs them. And the user can manage them.
------------------------------------------------
"""

from discord.ext import commands, tasks
import random
import discord
from discord import app_commands
from discord import app_commands, ui

from util.__funktion__ import *
from util.__Mydiscord_funktions__ import *
from util.__my_imge_path__ import *

from discord_cogs.rust.channel_hopper.__funktion__channel_hopper import *

img_url = my_image_url()

current_dir = os.path.dirname(os.path.abspath(__file__))
bot_path = os.path.abspath(sys.argv[0])
bot_folder = os.path.dirname(bot_path)
config_dir = os.path.join(bot_folder, "config", "config.ini")
category_rust_id = read_config(config_dir, "categorys", "category_rust_id", "int")
json_path = os.path.join(bot_folder, "config", "json","channel_data.json")
content = {}
json_path = if_json_file_404(json_path, content)


json_rust_help_commands_data_dir = os.path.join(bot_folder, "config","json", "channel_hopper_commands.json")

guild_id = read_config(config_dir, "client", "guild_id", "int")
if guild_id == None:
    guild_id = 1
guild = discord.Object(id=guild_id)


icon_url = img_url.rust.team_logo
thumbnail_url = img_url.piktogramm.i
embed = discord.Embed(title="#rust-info", color=0x8080ff)

embed.set_thumbnail(url=thumbnail_url)

json_rust_help_commands_data = read_json_file(json_rust_help_commands_data_dir)

# Max number of fields per embed
max_fields_per_embed = 25
# Counter for fields
field_count = 0
# List to store embeds
help_embeds_list = []

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
        help_embeds_list.append(embed)
        # Create a new embed for the next set of fields
        embed = discord.Embed(title="#Voice-Channel-help", color=0x8080ff)
        embed.set_author(name=f"@{guild.name}",
                        icon_url=icon_url)
        embed.set_thumbnail(url=thumbnail_url)
        # Add the current field to the new embed
        embed.add_field(name=command, value=description, inline=True)
        # Increment field count for the new embed
        field_count += 1

# Append the last embed to the list
help_embeds_list.append(embed)


create_rust_voice_channel_id =  read_config(config_dir, "channels", "create_rust_voice_channel_id", "int")

if create_rust_voice_channel_id == None:
    create_rust_voice_channel_id = 1

category_rust_id = read_config(config_dir, "categorys", "category_rust_id", "int")
if category_rust_id == None:
    category_rust_id = 1


#channel_name_list = ["Airfield", "Bandit Camp", "Harbor", "Junkyard","Large Oil Rig","Launch Site","Lighthouse","Military Tunnels","Oil Rig","Outpost","Mining Outpost","Power Plant","Sewer Branch","Satellite Dish Array","The Dome","Train Yard","Train Tunnel Network","Water Treatment Plant"]

class channelHoper_setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_dir = config_dir

        # Hier wird die Methode beim Start des Bots aufgerufen
        self.bot.loop.create_task(self.setup_channel_hopper())

    async def setup_channel_hopper(self):
        print ("\n --> setup_channel_hopper\n")
        await self.bot.wait_until_ready()  
        guild = self.bot.get_guild(guild_id)  

        was_created_list = []


# Creates a new voice channel
        create_rust_voice_channel_boolean = read_config(config_dir,"channels", "create_rust_voice_channel_boolean", "boolean")
        if create_rust_voice_channel_boolean:
            
            print("Channel_hopper.py sleep 3sec")
            await asyncio.sleep(5)
            category_rust_id = read_config(config_dir, "categorys", "category_rust_id", "int")
            channel_name = "➕-create-channel-➕"
            create_rust_voice_channel_id = read_config(config_dir,"channels", "create_rust_voice_channel_id", "int")
            create_channel = discord.utils.get(guild.voice_channels, id=create_rust_voice_channel_id)

            if create_channel != None:
                print(f"The channel {create_channel.name} already exists.")
            else:
                print(f"The channel {channel_name} does not exist.")

                category_rust = discord.utils.get(guild.categories, id=category_rust_id)
                print (category_rust)
                print (type(category_rust))

                create_channel = await guild.create_voice_channel(channel_name, category=category_rust)
                print(f"The channel {create_channel.name} was created.")
                write_config(config_dir, "channels", "create_rust_voice_channel_id", create_channel.id)

                was_created_list.append(create_channel)


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
            try:
                dc_time = discord_time_convert(time.time())
                embed = discord.Embed(title=f"The following Channel Hopper System Channels have been created:",
                                    description=f"> The following channels had to be created:\n{text}\ncreated: {dc_time}",
                                    colour=0xffff80)
                embed_list = []
                embed_list.append(embed)
                bot_cmd_channel_id = read_config(config_dir, "channels", "bot_cmd_channel_id", "int")
                bot_cmd_channel = guild.get_channel(bot_cmd_channel_id)

                embed = discord.Embed(title="Restart the Bot",
                      description="> The Setup work is done \n **RESTART THE BOT**\nSo that he can run his normal routine!",
                      colour=0xf40006)

                embed.set_thumbnail(url=img_url.piktogramm.attention)
                embed_list.append(embed)
                await bot_cmd_channel.send(embeds=embed_list)

            except:
                pass



#player_have_channel_list = []
class channelHoper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_channels = {}  # A dictionary for tracking the channels created <-- bug if restart forgott old channels
        #self.player_have_channel_list = {}
    async def create_voice_channel(self, user):
        category = discord.utils.get(user.guild.categories, id=category_rust_id)
        if not category:
            print(f"Category with ID {category_rust_id} was not found.")
            return

        guild = user.guild
        user_id = user.id
        user_name = user.name
        if is_user_in(user_id, json_path) == True:

            channel_id = get_channel_id_from(user_id, json_path)
            channel = self.bot.get_channel(channel_id)

            embed = discord.Embed(title="You already have a voice channel",
                      description=f"""> Only one voice channel per user.\n> I moved you into the channel.
                      
                      <#{channel_id}>""",
                      colour=0xff0000)

            await user.move_to(channel)


            embed_to_send = []
            embed_to_send.extend(help_embeds_list)
            embed_to_send.append(embed)

            await user.send(embeds=embed_to_send)

        if is_user_in(user_id, json_path) == False:
        #if user_id not in self.voice_channels.values():
            #if user.id not in self.voice_channels.values:
            
            channel_name_list = [
    "Airfield",
    "Bandit Camp",
    "Harbor",
    "Junkyard",
    "Large Oil Rig",
    "Launch Site",
    "Lighthouse",
    "Military Tunnels",
    "Oil Rig",
    "Outpost",
    "Mining Outpost",
    "Power Plant",
    "Sewer Branch",
    "Satellite Dish Array",
    "The Dome",
    "Train Yard",
    "Train Tunnel Network",
    "Water Treatment Plant"
]
            random_pic = random.choice(channel_name_list)

            new_channel = await category.create_voice_channel(f"🔊 {random_pic}")
            new_channel_id = new_channel.id

            add_new_channel_data(user_name, user_id, new_channel_id, json_path)

            owner_id = find_main_key(new_channel.id, json_path)
            print(f"interaction_channel.id {new_channel.id}")
            data = read_json_file(json_path)
            limit = new_channel.user_limit
            admin_list = get_item_from_channel("admin", new_channel.id, data)
            admin_list_len = len(admin_list)
            owner = await self.bot.fetch_user(owner_id)

            
            x = -1
            admin_text = ""
            while True:
                x = x + 1
                if x == admin_list_len:
                    break
                admin = admin_list[x]
                admin_text = admin_text +f"<@{admin}> "

            stay = get_item_from_channel("stay", new_channel.id, data)
            hide = get_item_from_channel("hide", new_channel.id, data)

            embed = discord.Embed(title=f"<#{new_channel.id}>",
                                description=f"<@{owner.id}>, is the owner of  <#{new_channel.id}>\n\n > The following User have admin rights on this channel:\n{admin_text}\n",
                                colour=0x00b0f4)

            embed.set_author(name="Channel Info")

            embed.add_field(name="Stay mode",
                            value=stay,
                            inline=True)
            embed.add_field(name="Hide mode",
                            value=hide,
                            inline=True)
            embed.add_field(name="User limit",
                            value=limit,
                            inline=True)

            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1152320067636318318/1180709211227815946/T71E5dZZSZeNXeDZ2EqjRQ.jpg?ex=657e6824&is=656bf324&hm=724143488b281a3cff0fb73171c011fc0f71d24989dc1d7614a56a8cea9b65c9&")

            embed.set_footer(text="for help type /vc_help",
                 icon_url="https://cdn.discordapp.com/attachments/1152320067636318318/1180709211227815946/T71E5dZZSZeNXeDZ2EqjRQ.jpg?ex=657e6824&is=656bf324&hm=724143488b281a3cff0fb73171c011fc0f71d24989dc1d7614a56a8cea9b65c9&")
            
            embed_to_send = []
            embed_to_send.extend(help_embeds_list)
            embed_to_send.append(embed)

            channel_msg = await new_channel.send(embeds=embed_to_send)

            fill_item_in_channel(new_channel.id, "channel_msg_id", channel_msg.id, json_path)

            #new_channel = await category.create_voice_channel(f"{random_pic} | {user.name}")
            await user.move_to(new_channel)
            user_img = user.display_avatar

            self.voice_channels[new_channel.id] = user.id



    async def delete_voice_channel(self, channel):
        if is_channel_id_in(channel.id, json_path) == True:
        # if channel.id in self.voice_channels:
            #del self.voice_channels[channel.id]
            stay_status = get_item_from_channel("stay",channel.id, json_path)
            if stay_status == False:
                delete_data_with_channel_id(channel.id, json_path)
                await channel.delete()
            if stay_status == True:
                
                admin_list = get_admin_list(channel.id, json_path)
                admin_list_len = len(admin_list)
                x = -1
                admin_text = ""
                while True:
                    x = x + 1
                    if x == admin_list_len:
                        break
                    admin = admin_list[x]
                    user = await self.bot.fetch_user(admin)
                    admin_text = admin_text + f"@{user.name} "
                embed_text = f"""The following users have the rights to do so:
                {admin_text}"""
                embed = discord.Embed(title="The channel is only deleted again when the /vc_stay command is executed", description= embed_text, color=0x00ff00)
                # Here it is assumed that 'create_channel' is the reference to the created voice channel.
                embed.set_thumbnail(url=img_url.piktogramm.read)
                await channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel == after.channel:  # The user has not changed his language status
            return
        #create_rust_voice_channel_id =  read_config(config_dir, "channels", "create_rust_voice_channel_id", "int")
        if after.channel and after.channel.id == create_rust_voice_channel_id:  # The user has joined the channel being watched
            await self.create_voice_channel(member)
        #elif before.channel and before.channel.id in self.voice_channels:  # The user has left the created channel
        elif before.channel and is_channel_id_in(before.channel.id, json_path):
            channel = discord.utils.get(member.guild.voice_channels, id=before.channel.id)
            if channel and len(channel.members) == 0:
                await self.delete_voice_channel(channel)



class bot_vc_rename(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    description = "Rename the Voice Channel."

    @app_commands.command(name="vc_rename", description=description)
    @app_commands.describe(
        new_channel_name="New name for your Voice Channel.",
    )
    async def vc_rename(self , interaction: discord.Interaction, new_channel_name: str,):
        self.new_channel_name = new_channel_name

        interaction_user_id = interaction.user.id
        target_channel_id = interaction.channel.id
        if is_he_channel_admin(interaction_user_id, target_channel_id, json_path) == True:

            old_name = interaction.channel.name
            await interaction.channel.edit(name = new_channel_name)

            embed = discord.Embed(title="Channel name has been changed", description=f"""from `{old_name}` to `{new_channel_name}`.
                                    
                                <#{interaction.channel.id}>""")
            embed.set_thumbnail(url=img_url.piktogramm.change)
            msg = await interaction.response.send_message(embed=embed, ephemeral=True,)


            channel_msg_id = get_item_from_channel("channel_msg_id", target_channel_id, json_path)
            channel_msg = await interaction.channel.fetch_message(channel_msg_id)

            data = read_json_file(json_path)
            owner_id = find_main_key(interaction.channel.id, data)
            limit = interaction.channel.user_limit
            admin_list = get_item_from_channel("admin", interaction.channel.id, data)
            admin_list_len = len(admin_list)
            owner = await self.bot.fetch_user(owner_id)
        
            x = -1
            admin_text = ""
            while True:
                x = x + 1
                if x == admin_list_len:
                    break
                admin = admin_list[x]
                admin_text = admin_text +f"<@{admin}> "

            stay = get_item_from_channel("stay", interaction.channel.id, data)
            hide = get_item_from_channel("hide", interaction.channel.id, data)


            embed = discord.Embed(title=f"<#{interaction.channel.id}>",
                                description=f"<@{owner.id}>, is the owner of this Voice Channel\nThe following User have admin rights on this channel:\n{admin_text}\n",
                                colour=0x00b0f4)

            embed.set_author(name="Channel Info")

            embed.add_field(name="Stay mode",
                            value=stay,
                            inline=True)
            embed.add_field(name="Hide mode",
                            value=hide,
                            inline=True)
            embed.add_field(name="User limit",
                            value=limit,
                            inline=True)

            embed.set_thumbnail(url=img_url.gta.blond)
            embed.set_footer(text="for help type /vc_help",
                 icon_url=img_url.gta.blond)
            await channel_msg.edit(embed=embed)

        else:
            if len(get_list_for_all_admin_server_from_user(interaction_user_id, json_path)) <= 0:
                embed=discord.Embed(title="You do not have a channel with admin rights", description=f"""You can create a channel by jumping into the create channel:      
                                        <#{create_rust_voice_channel_id}>""", color=0xff0000)
                embed.set_thumbnail(url=img_url.piktogramm.attention)
                msg = await interaction.response.send_message(embed=embed, ephemeral=True,)


            else:
                channel_id_list = get_list_for_all_admin_server_from_user(interaction_user_id,json_path)
                channel_id_list_len = len(channel_id_list)
                x = -1
                channel_id_ist_in_str = ""
                while True:
                    x = x + 1
                    if x == channel_id_list_len:
                        break
                    channel_id_ist_in_str = channel_id_ist_in_str + f"<#{channel_id_list[x]}>\n"
                
                embed=discord.Embed(title="You write the commands in the wrong channel", description=f"""These are all channels in which you have admin rights:      
                                        {channel_id_ist_in_str}
write the command in the desired channel.""", color=0xff0000)
                embed.set_thumbnail(url=img_url.piktogramm.attention)
                msg = await interaction.response.send_message(embed=embed, ephemeral=True,)



class bot_vc_limit(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    description = "Set the maximum number of users."

    @app_commands.command(name="vc_limit", description=description)
    @app_commands.describe(
        new_limit="Set the limit of users in a channel.",
    )
    async def vc_limit(self, interaction: discord.Interaction, new_limit: int,):
        self.new_limit = new_limit
        interaction_user_id = interaction.user.id
        interaction_channel = interaction.channel

        if is_he_channel_admin(interaction_user_id, interaction_channel.id, json_path) == True:
            channel_id = get_channel_id_from(interaction_user_id, json_path)
            channel = self.bot.get_channel(channel_id)

            old_limit = channel.user_limit 
            await channel.edit(user_limit=new_limit)

            embed=discord.Embed(title="Channel limit has been changed", description=f"""from `{old_limit}` to `{new_limit}`.
                                    
                                <#{channel_id}>""", color=0xfffff)
            embed.set_thumbnail(url=img_url.piktogramm.change)
            msg = await interaction.response.send_message(embed=embed, ephemeral=True)

            target_channel_id = interaction.channel.id
            channel_msg_id = get_item_from_channel("channel_msg_id", target_channel_id, json_path)
            channel_msg = await interaction.channel.fetch_message(channel_msg_id)

            data = read_json_file(json_path)
            owner_id = find_main_key(interaction.channel.id, data)
            limit = interaction.channel.user_limit
            admin_list = get_item_from_channel("admin", interaction.channel.id, data)
            admin_list_len = len(admin_list)
            owner = await self.bot.fetch_user(owner_id)
        
            x = -1
            admin_text = ""
            while True:
                x = x + 1
                if x == admin_list_len:
                    break
                admin = admin_list[x]
                admin_text = admin_text +f"<@{admin}> "

            stay = get_item_from_channel("stay", interaction.channel.id, data)
            hide = get_item_from_channel("hide", interaction.channel.id, data)


            embed = discord.Embed(title=f"<#{interaction.channel.id}>",
                                description=f"<@{owner.id}>, is the owner of this Voice Channel\nThe following User have admin rights on this channel:\n{admin_text}\n",
                                colour=0x00b0f4)

            embed.set_author(name="Channel Info")

            embed.add_field(name="Stay mode",
                            value=stay,
                            inline=True)
            embed.add_field(name="Hide mode",
                            value=hide,
                            inline=True)
            embed.add_field(name="User limit",
                            value=limit,
                            inline=True)

            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1152320067636318318/1180709211227815946/T71E5dZZSZeNXeDZ2EqjRQ.jpg?ex=657e6824&is=656bf324&hm=724143488b281a3cff0fb73171c011fc0f71d24989dc1d7614a56a8cea9b65c9&")

            embed.set_footer(text="for help type /vc_help",
                 icon_url="https://cdn.discordapp.com/attachments/1152320067636318318/1180709211227815946/T71E5dZZSZeNXeDZ2EqjRQ.jpg?ex=657e6824&is=656bf324&hm=724143488b281a3cff0fb73171c011fc0f71d24989dc1d7614a56a8cea9b65c9&")
            await channel_msg.edit(embed=embed)

        else:
            if len(get_list_for_all_admin_server_from_user(interaction_user_id, json_path)) <= 0:
                embed=discord.Embed(title="You do not have a channel with admin rights", description=f"""You can create a channel by jumping into the create channel:      
                                        <#{create_rust_voice_channel_id}>""", color=0xff0000)
                embed.set_thumbnail(url=img_url.piktogramm.attention)
                msg = await interaction.response.send_message(embed=embed, ephemeral=True,)


            else:
                channel_id_list = get_list_for_all_admin_server_from_user(interaction_user_id,json_path)
                channel_id_list_len = len(channel_id_list)
                x = -1
                channel_id_ist_in_str = ""
                while True:
                    x = x + 1
                    if x == channel_id_list_len:
                        break
                    channel_id_ist_in_str = channel_id_ist_in_str + f"<#{channel_id_list[x]}>\n"
                
                embed=discord.Embed(title="You write the commands in the wrong channel", description=f"""These are all channels in which you have admin rights:      
                                        {channel_id_ist_in_str}
write the command in the desired channel.""", color=0xff0000)
                embed.set_thumbnail(url=img_url.piktogramm.attention)
                msg = await interaction.response.send_message(embed=embed, ephemeral=True,)


class bot_vc_stay(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    description = "Switch the status whether the server may be deleted after leaving"

    @app_commands.command(name="vc_stay", description=description)

    async def vc_stay(self, interaction: discord.Interaction):
        interaction_user_id = interaction.user.id
        interaction_channel = interaction.channel

        if is_he_channel_admin(interaction_user_id, interaction_channel.id, json_path) == True:
            channel_id = get_channel_id_from(interaction_user_id, json_path)
            channel = self.bot.get_channel(channel_id)


            new_stay_status = switch_stay_status(channel_id, json_path)
            if new_stay_status == True:
                text = "The channel is now not deleted when empty."
            else:
                text = "The channel is now deleted again when it is empty"

            embed=discord.Embed(title="Stay status was changed..", description=f"""{text}
                                    
                                <#{channel_id}>""", color=0xfffff)

            embed.set_thumbnail(url=img_url.piktogramm.change)
            msg = await interaction.response.send_message(embed=embed, ephemeral=True)

            target_channel_id = interaction.channel.id
            channel_msg_id = get_item_from_channel("channel_msg_id", target_channel_id, json_path)
            channel_msg = await interaction.channel.fetch_message(channel_msg_id)

            data = read_json_file(json_path)
            owner_id = find_main_key(interaction.channel.id, data)
            limit = interaction.channel.user_limit
            admin_list = get_item_from_channel("admin", interaction.channel.id, data)
            admin_list_len = len(admin_list)
            owner = await self.bot.fetch_user(owner_id)
        
            x = -1
            admin_text = ""
            while True:
                x = x + 1
                if x == admin_list_len:
                    break
                admin = admin_list[x]
                admin_text = admin_text +f"<@{admin}> "

            stay = get_item_from_channel("stay", interaction.channel.id, data)
            hide = get_item_from_channel("hide", interaction.channel.id, data)


            embed = discord.Embed(title=f"<#{interaction.channel.id}>",
                                description=f"<@{owner.id}>, is the owner of this Voice Channel\nThe following User have admin rights on this channel:\n{admin_text}\n",
                                colour=0x00b0f4)

            embed.set_author(name="Channel Info")

            embed.add_field(name="Stay mode",
                            value=stay,
                            inline=True)
            embed.add_field(name="Hide mode",
                            value=hide,
                            inline=True)
            embed.add_field(name="User limit",
                            value=limit,
                            inline=True)

            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1152320067636318318/1180709211227815946/T71E5dZZSZeNXeDZ2EqjRQ.jpg?ex=657e6824&is=656bf324&hm=724143488b281a3cff0fb73171c011fc0f71d24989dc1d7614a56a8cea9b65c9&")

            embed.set_footer(text="for help type /vc_help",
                 icon_url="https://cdn.discordapp.com/attachments/1152320067636318318/1180709211227815946/T71E5dZZSZeNXeDZ2EqjRQ.jpg?ex=657e6824&is=656bf324&hm=724143488b281a3cff0fb73171c011fc0f71d24989dc1d7614a56a8cea9b65c9&")
            await channel_msg.edit(embed=embed)

            
        else:
            if len(get_list_for_all_admin_server_from_user(interaction_user_id, json_path)) <= 0:
                embed=discord.Embed(title="You do not have a channel with admin rights", description=f"""You can create a channel by jumping into the create channel:      
                                        <#{create_rust_voice_channel_id}>""", color=0xff0000)
                embed.set_thumbnail(url=img_url.piktogramm.attention)
                msg = await interaction.response.send_message(embed=embed, ephemeral=True,)


            else:
                channel_id_list = get_list_for_all_admin_server_from_user(interaction_user_id,json_path)
                channel_id_list_len = len(channel_id_list)
                x = -1
                channel_id_ist_in_str = ""
                while True:
                    x = x + 1
                    if x == channel_id_list_len:
                        break
                    channel_id_ist_in_str = channel_id_ist_in_str + f"<#{channel_id_list[x]}>\n"
                
                embed=discord.Embed(title="You write the commands in the wrong channel", description=f"""These are all channels in which you have admin rights:      
                                        {channel_id_ist_in_str}
write the command in the desired channel.""", color=0xff0000)
                embed.set_thumbnail(url=img_url.piktogramm.attention)
                msg = await interaction.response.send_message(embed=embed, ephemeral=True,)


class bot_vc_kick(commands.Cog):
    def __init__(self, bot: commands.Bot, interaction: discord.Interaction) -> None:
        self.bot = bot

    members = discord.VoiceChannel.members

    description = "Kick a user from your Channel"
    
    @app_commands.command(name="vc_kick", description=description)
    @app_commands.describe(player_to_kick='Player choose')
    @app_commands.choices(player_to_kick=[
        discord.app_commands.Choice(name='Blue', value=1),
        discord.app_commands.Choice(name='Green', value=3)])
    
    async def choisecolor(self, interaction: discord.Interaction, player_to_kick: discord.app_commands.Choice[int]):
        # code for kick the user.id ....
        await interaction.response.send_message(f"test {player_to_kick.name}")                                                                                                                                                  


class bot_vc_help(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    description = "Shows you a list of all commands and your channels on which you are an administrator"

    @app_commands.command(name="vc_help", description=description)

    async def vc_help(self, interaction: discord.Interaction):

        interaction_user_id = interaction.user.id
        interaction_channel = interaction.channel


        msg = await interaction.channel.send(embeds=help_embeds_list)

        list_of_admin_channel_from_user = get_list_for_all_admin_server_from_user(interaction_user_id, json_path)
        list_of_admin_channel_from_user_len = len(list_of_admin_channel_from_user)
        try:
            if list_of_admin_channel_from_user_len != 0:
                x = -1
                list_text = ""
                while True:
                    x = x + 1
                    if x == list_of_admin_channel_from_user_len:
                        break
                    list_text = list_text +f"<#{list_of_admin_channel_from_user[x]}>\n"


                embed = discord.Embed(title="List of all your channels with administrator rights",
                        description=f"{list_text}")
                msg = await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(title="You don't have a voice channel or right for one at the moment", description=f"But you can create one under <#{create_rust_voice_channel_id}>")
            
            msg = await interaction.response.send_message(embed=embed, ephemeral=True)
        except:
            pass


async def setup(bot: commands.Bot):
    await bot.add_cog(channelHoper_setup(bot), guild=discord.Object(guild_id))
    await bot.add_cog(channelHoper(bot), guild=discord.Object(guild_id))
    await bot.add_cog(bot_vc_rename(bot), guild=discord.Object(guild_id))
    await bot.add_cog(bot_vc_limit(bot), guild=discord.Object(guild_id))
    await bot.add_cog(bot_vc_stay(bot), guild=discord.Object(guild_id))
    await bot.add_cog(bot_vc_help(bot), guild=discord.Object(guild_id))
    #await bot.add_cog(bot_vc_kick(bot), guild=discord.Object(guild_id))


