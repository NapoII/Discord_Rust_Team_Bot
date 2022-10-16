

from Imports import*
from discord import app_commands

guild_id = int(read_config(config_dir, "Client", "guild_id"))
guild = discord.Object(id=guild_id)
rust_info_channel_id = int(read_config(config_dir, "Channel", "rust_info_channel_id"))


class Rust_Info(commands.Cog, ):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.command(name="rust")
    async def send_info(self, ctx: commands.Context, help: str):
        rust_info_channel = self.bot.get_channel(rust_info_channel_id)



        if help.lower() == "help":
            embed=discord.Embed(title="#rust-info", color=0x8080ff)
            embed.set_thumbnail(url="https://i.imgur.com/sdr9twR.png")
            all_commands = "`!rust help`\n`!rust cctv`\n`!rust pager`\n`!rust cost`"
            embed.add_field(name="All Commands:", value=all_commands, inline=True)
            await rust_info_channel.send(embed=embed)


        if help.lower() == "cctv":

            Airfield  = "`AIRFIELDHELIPAD`"
            Bandit_Camp = "`CASINO`\n`TOWNWEAPONS`"
            Dome = "`DOME1`\n`DOMETOPS`"
            Large_Oil_Rig = "`OILRIG2HELI`\n`OILRIG2DOCK`\n`OILRIG2EXHAUST`\n`OILRIG2L1`\n`OILRIG2L2`\n`OILRIG2L3A`\n`OILRIG2L3B`\n`OILRIG2L4`\n`OILRIG2L5`\n`OILRIG2L6A`\n`OILRIG2L6B`\n`OILRIG2L6C`\n`OILRIG2L6D`"
            Outpost = "`COMPOUNDSTREET`\n`COMPOUNDMUSIC`\n`COMPOUNDCRUDE`\n`COMPOUNDCHILL`"
            Small_Oil_Rig = "`OILRIG1HELI`\n`OILRIG1DOCK`\n`OILRIG1EXHAUST`\n`OILRIG1L1`\n`OILRIG1L2`\n`OILRIG1L3`\n`OILRIG1L4`"
            Underwater_Labs = "`AUXPOWER****`\n`BRIG****`\n`CANTINA****`\n`CAPTAINQUARTER****`\n`CLASSIFIED****`\n`CREWQUARTERS****`\n`HALLWAY****`\n`INFIRMARY****`\n`LAB****`\n`LOCKERROOM****`\n`OPERATIONS****`\n`SECURITYHALL****`\n`TECHCABINET****`\n"

            embed=discord.Embed(title="CCTV Codes", color=0x8080ff)
            embed.set_author(name="!rust cctv")
            embed.set_thumbnail(url="https://i.imgur.com/6GkZ17S.png")
            embed.add_field(name="Airfield", value=Airfield, inline=False)
            embed.add_field(name="Bandit Camp", value=Bandit_Camp, inline=False)
            embed.add_field(name="Dome", value=Dome, inline=False)
            embed.add_field(name="Large Oil Rig", value=Large_Oil_Rig, inline=False)
            embed.add_field(name="Outpost", value=Outpost, inline=False)
            embed.add_field(name="Small Oil Rig", value=Small_Oil_Rig, inline=False)
            embed.add_field(name="Underwater Labs", value=Underwater_Labs, inline=False)
            await rust_info_channel.send(embed=embed)


        if help.lower() == "pager":

            embed=discord.Embed(title="Pager / Frequency ", color=0x8080ff)
            embed.set_author(name="!rust pager")
            embed.set_thumbnail(url="https://i.imgur.com/IoKrSDC.png")
            embed.add_field(name="Small Oil Rig", value="`4765`", inline=True)
            embed.add_field(name="Large Oil Rig", value="`4768`", inline=True)
            embed.add_field(name="Giant Excavator", value="`4777`", inline=True)
            await rust_info_channel.send(embed=embed)


        if help.lower() == "cost":
            embed=discord.Embed(title="Preisliste", color=0x8080ff)
            embed.set_author(name="!cost")
            embed.set_thumbnail(url="https://i.imgur.com/EzCYdSa.png")
            Fishing_Village ="Boot `125 Scrap`\nRHIB `300 Scrap`\nOne-man Submarine `200 Scrap`\nTwo-man Submarine `300 Scrap`\n2*Torpedo `75 Scrap`"
            embed.add_field(name="Fishing Village", value=Fishing_Village, inline=False)
            await rust_info_channel.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Rust_Info(bot))

