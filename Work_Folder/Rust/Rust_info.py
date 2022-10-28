

from Imports import*
from discord import app_commands

guild_id = int(read_config(config_dir, "Client", "guild_id"))
guild = discord.Object(id=guild_id)
rust_info_channel_id = int(read_config(config_dir, "Channel", "rust_info_channel_id"))


class Rust_Info(commands.Cog, ):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="rust")

    async def send_info(self, ctx: commands.Context, first: str, second: str|None = None):
        rust_info_channel = self.bot.get_channel(rust_info_channel_id)
        
        if first.lower() == "help":
            embed=discord.Embed(title="#rust-info", color=0x8080ff)
            embed.set_author(name=f"@{ctx.author}")
            embed.set_thumbnail(url="https://i.imgur.com/sdr9twR.png")
            all_commands = """`!rust help` - Liste aller Commands
            `!rust cctv` - Liste aller CCTV Codes
            `!rust pager` - Liste aller Pager Codes
            `!rust cost` - Wichtige Preise
            `!rust fert {Anzahl an Fertilizer}` - Wie viel Scrap aus x Fertilizer
            `!rust giant {Anzahl an Diesel}` - Giant Excavator Rechner
            `!rust sulfur {Anzahl an sulfur}` - Wie viel Boom aus x Suflur
            `!rust raid` - Raid cost Liste"""
            embed.add_field(name="All Commands:", value=all_commands, inline=True)
            await rust_info_channel.send(embed=embed)


        if first.lower() == "raid":
            embed=discord.Embed(title="#Raid Cost Info",url=f"https://rustraidcalculator.com/HTML/raidCostChart.html", color=0x8080ff)
            embed.set_author(name=f"@{ctx.author}")
            embed.set_image(url="https://i.imgur.com/gckVnFB.png")
            await rust_info_channel.send(embed=embed)


        if first.lower() == "cctv":

            Airfield  = "`AIRFIELDHELIPAD`"
            Bandit_Camp = "`CASINO`\n`TOWNWEAPONS`"
            Dome = "`DOME1`\n`DOMETOPS`"
            Large_Oil_Rig = "`OILRIG2HELI`\n`OILRIG2DOCK`\n`OILRIG2EXHAUST`\n`OILRIG2L1`\n`OILRIG2L2`\n`OILRIG2L3A`\n`OILRIG2L3B`\n`OILRIG2L4`\n`OILRIG2L5`\n`OILRIG2L6A`\n`OILRIG2L6B`\n`OILRIG2L6C`\n`OILRIG2L6D`"
            Outpost = "`COMPOUNDSTREET`\n`COMPOUNDMUSIC`\n`COMPOUNDCRUDE`\n`COMPOUNDCHILL`"
            Small_Oil_Rig = "`OILRIG1HELI`\n`OILRIG1DOCK`\n`OILRIG1EXHAUST`\n`OILRIG1L1`\n`OILRIG1L2`\n`OILRIG1L3`\n`OILRIG1L4`"
            Underwater_Labs = "`AUXPOWER****`\n`BRIG****`\n`CANTINA****`\n`CAPTAINQUARTER****`\n`CLASSIFIED****`\n`CREWQUARTERS****`\n`HALLWAY****`\n`INFIRMARY****`\n`LAB****`\n`LOCKERROOM****`\n`OPERATIONS****`\n`SECURITYHALL****`\n`TECHCABINET****`\n"

            embed=discord.Embed(title="CCTV Codes", color=0x8080ff)
            embed.set_author(name=f"@{ctx.author}")
            embed.set_thumbnail(url="https://i.imgur.com/6GkZ17S.png")
            embed.add_field(name="Airfield", value=Airfield, inline=False)
            embed.add_field(name="Bandit Camp", value=Bandit_Camp, inline=False)
            embed.add_field(name="Dome", value=Dome, inline=False)
            embed.add_field(name="Large Oil Rig", value=Large_Oil_Rig, inline=False)
            embed.add_field(name="Outpost", value=Outpost, inline=False)
            embed.add_field(name="Small Oil Rig", value=Small_Oil_Rig, inline=False)
            embed.add_field(name="Underwater Labs", value=Underwater_Labs, inline=False)
            await rust_info_channel.send(embed=embed)


        if first.lower() == "pager":

            embed=discord.Embed(title="Pager / Frequency ", color=0x8080ff)
            embed.set_author(name=f"@{ctx.author}")
            embed.set_thumbnail(url="https://i.imgur.com/IoKrSDC.png")
            embed.add_field(name="Small Oil Rig", value="`4765`", inline=True)
            embed.add_field(name="Large Oil Rig", value="`4768`", inline=True)
            embed.add_field(name="Giant Excavator", value="`4777`", inline=True)
            await rust_info_channel.send(embed=embed)

        if first.lower() == "cost":
            embed=discord.Embed(title="Preisliste", color=0x8080ff)
            embed.set_author(name=f"@{ctx.author}")
            embed.set_thumbnail(url="https://i.imgur.com/EzCYdSa.png")
            Fishing_Village ="Boot `125 Scrap`\nRHIB `300 Scrap`\nOne-man Submarine `200 Scrap`\nTwo-man Submarine `300 Scrap`\n2*Torpedo `75 Scrap`"
            embed.add_field(name="Fishing Village", value=Fishing_Village, inline=False)
            await rust_info_channel.send(embed=embed)

        if first.lower() == "fert":

            if second == None:
                embed=discord.Embed(title="Fertilizer Calk", url="https://rustlabs.com/item/fertilizer", description="`2` Fertilizer ergeben `3` Scrap", color=0x0000ff)
                embed.set_author(name=f"@{ctx.author}")
                embed.set_thumbnail(url="https://rustlabs.com/img/items180/fertilizer.png")
                await rust_info_channel.send(embed=embed)

            else:
                fert_menge = int(second)
                fert_sel_min = 2
                fert_sell_Scrap = 3
                sell_Scrap_sum = int((fert_menge/fert_sel_min)*fert_sell_Scrap)
                embed=discord.Embed(title="Fertilizer Calk", url="https://rustlabs.com/item/fertilizer", description=f"`{fert_menge}` Fertilizer ergeben `{sell_Scrap_sum}` Scrap", color=0x0000ff)
                embed.set_author(name=f"@{ctx.author}")
                embed.set_thumbnail(url="https://rustlabs.com/img/items180/fertilizer.png")
                await rust_info_channel.send(embed=embed)


        if first.lower() == "giant":

            if second == None:
                embed=discord.Embed(title="Giant Excavator", url="https://rustlabs.com/entity/giant-excavator", description="Diesel 20 benötigen 40 min", color=0x8080ff)
                embed.set_author(name=f"@{ctx.author}")
                embed.add_field(name="HQM", value="`200.000`", inline=False)
                embed.add_field(name="Metal Fragments", value="`100.000`", inline=False)
                embed.add_field(name="Sulfur Ore", value="`40.000`", inline=False)
                embed.add_field(name="Stones", value="`2.000`", inline=False)
                embed.set_image(url="https://rustlabs.com/img/screenshots/excavator.png")
                await rust_info_channel.send(embed=embed)

            else:
                Diesel_Fuel = int(second)

                Fuel_max = 20
                min_max = 40
                Time_need = int((min_max/Fuel_max)*Diesel_Fuel)
                max_Metal = 100000
                max_Stone = 200000
                max_Sulfur = 40000
                max_HQM = 2000

                one_f_Metal = max_Metal/Fuel_max
                one_f_Stone = max_Stone/Fuel_max
                one_f_Sulfur = max_Sulfur/Fuel_max
                one_f_HQM = max_HQM/Fuel_max

                Metal = int(one_f_Metal * Diesel_Fuel)
                Stone = int(one_f_Stone * Diesel_Fuel)
                Sulfur = int(one_f_Sulfur * Diesel_Fuel)
                HQM = int(one_f_HQM * Diesel_Fuel)

                embed=discord.Embed(title="Giant Excavator", url="https://rustlabs.com/entity/giant-excavator", description=f"`{Diesel_Fuel}` Diesel benötigen `{Time_need}` min.", color=0x8080ff)
                embed.set_author(name=f"@{ctx.author}")
                embed.set_thumbnail(url="https://rustlabs.com/img/screenshots/excavator.png")
                embed.add_field(name="HQM", value=f"`{HQM}`", inline=False)
                embed.add_field(name="Metal Fragments", value=f"`{Metal}`", inline=False)
                embed.add_field(name="Sulfur Ore", value=f"`{Sulfur}`", inline=False)
                embed.add_field(name="Stones", value=f"`{Stone}`", inline=False)
                await rust_info_channel.send(embed=embed)

                Rocket_Sulf = 1400
                C4_Sulf = 2200
                Exploammo_Sulf  = 25
                Satchel_Sulf = 480

                Sulfur = int(Sulfur)
                Rocket = int(Sulfur/Rocket_Sulf)
                C4 = int(Sulfur/C4_Sulf)
                Exploammo = int(Sulfur/Exploammo_Sulf)
                Satchel = int(Sulfur/Satchel_Sulf)

                text = f"Aus {Sulfur} Sulfur:\n\nRockets: `{Rocket}`\nC4: `{C4}`\nExploammo: `{Exploammo}`\nSatchel: `{Satchel}`"

                embed=discord.Embed(title="Sulfur Calk", url="https://rustraidcalculator.com/HTML/raidCalc.html", description=text , color=0x0000ff)
                embed.set_author(name=f"@{ctx.author}")
                embed.set_thumbnail(url="https://rustlabs.com/img/items180/sulfur.png")
                await rust_info_channel.send(embed=embed)

        if first.lower() == "sulfur":


            Rocket_Sulf = 1400
            C4_Sulf = 2200
            Exploammo_Sulf  = 25
            Satchel_Sulf = 480

            Rocket_GP = 650
            C4_GP = 1000
            Exploammo_GP  = 10
            Satchel_GP = 240

            if second == None:


                text = f"Wie viel Sulfur wird benötigt:\n\nRocket: `{Rocket_Sulf} Sulfur` \nC4: `{C4_Sulf} Sulfur`\nExploammo: `{Exploammo_Sulf} Sulfur`\nSatchel: `{Satchel_Sulf} Sulfur`"

                embed=discord.Embed(title="Sulfur Calk", url="https://rustraidcalculator.com/HTML/raidCalc.html", description=text , color=0x0000ff)
                embed.set_author(name=f"@{ctx.author}")
                embed.set_thumbnail(url="https://rustlabs.com/img/items180/sulfur.png")
                await rust_info_channel.send(embed=embed)
            
            else:
                Sulfur = int(second)
                Rocket = int(Sulfur/Rocket_Sulf)
                C4 = int(Sulfur/C4_Sulf)
                Exploammo = int(Sulfur/Exploammo_Sulf)
                Satchel = int(Sulfur/Satchel_Sulf)

                text = f"Aus {Sulfur} Sulfur:\n\nRockets: `{Rocket}`\nC4: `{C4}`\nExploammo: `{Exploammo}`\nSatchel: `{Satchel}`"

                embed=discord.Embed(title="Sulfur Calk", url="https://rustraidcalculator.com/HTML/raidCalc.html", description=text , color=0x0000ff)
                embed.set_author(name=f"@{ctx.author}")
                embed.set_thumbnail(url="https://rustlabs.com/img/items180/sulfur.png")
                await rust_info_channel.send(embed=embed)






async def setup(bot: commands.Bot):
    await bot.add_cog(Rust_Info(bot))

