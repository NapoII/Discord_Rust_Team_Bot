from multiprocessing.sharedctypes import Value
import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice
from discord.ext import tasks
from Imports import*


guild_id = int(read_config(config_dir, "Client", "guild_id"))
guild = discord.Object(id=guild_id)
Rust_Bot_Channel_ID = int(read_config(config_dir, "Channel", "Rust_Bot_Channel_ID"))


class Event_timer_command(commands.Cog, commands.bot):
    def __init__(self, bot:commands.bot)-> None:
        self.bot = bot

    @app_commands.command(name = "cargo", description="Sendet ein Cargo/Attack Heli Timer in den Rust-Bot Channel")


    async def Bot_Test(
        self,
        interaction: discord.Integration):
        await interaction.response.send_modal(Timer_embed())

class Timer_embed(commands.Cog):

    #log("Send modal_input_say: say_channel_id | say_title | say_text")
    async def on_submit(self, interaction: discord.Interaction, bot:commands.Bot):

        embed_img_url = f"https://i.imgur.com/fEBeG5L.png"
        embed=discord.Embed(title="Cargo / Attack Heli Timer", description="<t:1665065100:R>", color=0x80ff00)
        embed.add_field(name="Cargo", value="max time in :<t:1665065100:R>", inline=True)
        embed.add_field(name="Attack Heli", value="max time in <t:1665065100:R>", inline=True)
        embed.set_image(url=embed_img_url)

        try:
            cargo_timer_message_id = int(read_config(config_dir, "Rust", "cargo_timer_message_id"))
            Rust_Bot_Channel = self.get_channel(Rust_Bot_Channel_ID)
            msg = await Rust_Bot_Channel.fetch_message(cargo_timer_message_id)
            await msg.edit(embed=embed)
        except:
            cargo_timer_message_id = int(read_config(config_dir, "Rust", "cargo_timer_message_id"))
            Rust_Bot_Channel = self.get_channel(Rust_Bot_Channel_ID)
            msg = await Rust_Bot_Channel.send(embed=embed)

        await interaction.response.send_message(embed=embed)





async def setup(bot: commands.Bot):
    await bot.add_cog(Event_timer_command(bot), guild=guild)