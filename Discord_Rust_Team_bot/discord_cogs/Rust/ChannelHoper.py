"""Full Doku on: https://github.com/NapoII/Discord_Rust_Team_bot"
-----------------------------------------------
This COG is for embed a help information for Rust.
exampel : cctv codes
------------------------------------------------
"""

from discord import app_commands

from util.__funktion__ import *
import random

# get the path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
bot_path = os.path.abspath(sys.argv[0])
bot_folder = os.path.dirname(bot_path)
# construct the path to the config.ini file relative to the current directory
config_dir = os.path.join(bot_folder, "cfg", "config.ini")
guild_id = int(read_config(config_dir, "Client", "guild_id"))
guild = discord.Object(id=guild_id)


Channel_hoper_id =  int(read_config(config_dir, "Channel", "hopper_voice_channel_id"))
Channel_hoper_kat_id = int(read_config(config_dir, "Channel", "category_Rust_id"))
Channel_name_list = ["Airfield", "Bandit Camp", "Harbor", "Junkyard","Large Oil Rig","Launch Site","Lighthouse","Military Tunnels","Oil Rig","Outpost","Mining Outpost","Power Plant","Sewer Branch","Satellite Dish Array","The Dome","Train Yard","Train Tunnel Network","Water Treatment Plant"]

class ChannelHoper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_channels = {}  # Ein Wörterbuch zur Verfolgung der erstellten Kanäle

    async def create_voice_channel(self, user):
        category = discord.utils.get(user.guild.categories, id=Channel_hoper_kat_id)
        if not category:
            print(f"Kategorie mit ID {Channel_hoper_kat_id} wurde nicht gefunden.")
            return

        guild = user.guild
        random_pic = random.choice(Channel_name_list)
        new_channel = await category.create_voice_channel(f"{random_pic} | {user.name}")
        await user.move_to(new_channel)

        self.voice_channels[new_channel.id] = user.id

    async def delete_voice_channel(self, channel):
        if channel.id in self.voice_channels:
            del self.voice_channels[channel.id]
            await channel.delete()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel == after.channel:  # Der Benutzer hat seinen Sprachstatus nicht geändert
            return

        if after.channel and after.channel.id == Channel_hoper_id:  # Der Benutzer ist dem beobachteten Kanal beigetreten
            await self.create_voice_channel(member)
        elif before.channel and before.channel.id in self.voice_channels:  # Der Benutzer hat den erstellten Kanal verlassen
            channel = discord.utils.get(member.guild.voice_channels, id=before.channel.id)
            if channel and len(channel.members) == 0:
                await self.delete_voice_channel(channel)


async def setup(bot: commands.Bot):
    await bot.add_cog(ChannelHoper(bot), guild=discord.Object(guild_id))
