"""Full Doku on: https://github.com/NapoII/Discord_Rust_Team_bot"
-----------------------------------------------
This COG is for embed a help information for Rust.
exampel : cctv codes
------------------------------------------------
"""

from discord import app_commands

from util.__funktion__ import *


# get the path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
bot_path = os.path.abspath(sys.argv[0])
bot_folder = os.path.dirname(bot_path)
# construct the path to the config.ini file relative to the current directory
config_dir = os.path.join(bot_folder, "cfg", "config.ini")

guild_id = read_config(config_dir, "Client", "guild_id")
if guild_id == None:
    guild_id = 1
guild_id = int(guild_id)

guild = discord.Object(id=guild_id)

rust_info_channel_id = read_config(
    config_dir, "Channel", "rust_info_channel_id")
if rust_info_channel_id == None:
    rust_info_channel_id = 1
rust_info_channel_id = int(rust_info_channel_id)


class Rust_Info(commands.Cog, ):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="rust")
    async def send_info(self, ctx: commands.Context, first: str, second: str | None = None):
        rust_info_channel = self.bot.get_channel(rust_info_channel_id)
        display_avatar = ctx.author.display_avatar

        print(f"{display_avatar}")

        if first.lower() == "help" or first.lower() == "info" or first.lower() == "i":
            embed = discord.Embed(title="#rust-info", color=0x8080ff)
            embed.set_author(name=f"@{ctx.author}",
                             icon_url=f"{display_avatar}")
            embed.set_thumbnail(url="https://i.imgur.com/sdr9twR.png")
            all_commands = """`!rust help` - List of all commands
            `!rust cctv` - List of all CCTV codes
            `!rust pager` - List of all pager codes
            `!rust cost` - Important prices
            `!rust fert {Number of Fertilizers}` - How much Scrap from x Fertilizer
            `!rust diesel {Number of Diesel}` - Giant Excavator / Mining Quarry - Calculator
            `!rust sulfur {Number of sulphur}` - How much boom from x suflur
            `!rust raid` - Raid costs list
            `!rust bind` - Must-have Extra Bind's
            `!rust elec` - Must have Electronic Circuits
            """
            embed.add_field(name="All Commands:",
                            value=all_commands, inline=True)
            await rust_info_channel.send(embed=embed)

        if first.lower() == "raid":
            embed = discord.Embed(
                title="#Raid Cost Info", url=f"https://rustraidcalculator.com/HTML/raidCostChart.html", color=0x8080ff)
            embed.set_author(name=f"@{ctx.author}",
                             icon_url=f"{display_avatar}")
            embed.set_image(url="https://i.imgur.com/gckVnFB.png")
            await rust_info_channel.send(embed=embed)

        if first.lower() == "cctv":

            Airfield = "`AIRFIELDHELIPAD`"
            Bandit_Camp = "`CASINO`\n`TOWNWEAPONS`"
            Dome = "`DOME1`\n`DOMETOPS`"
            Large_Oil_Rig = "`OILRIG2HELI`\n`OILRIG2DOCK`\n`OILRIG2EXHAUST`\n`OILRIG2L1`\n`OILRIG2L2`\n`OILRIG2L3A`\n`OILRIG2L3B`\n`OILRIG2L4`\n`OILRIG2L5`\n`OILRIG2L6A`\n`OILRIG2L6B`\n`OILRIG2L6C`\n`OILRIG2L6D`"
            Outpost = "`COMPOUNDSTREET`\n`COMPOUNDMUSIC`\n`COMPOUNDCRUDE`\n`COMPOUNDCHILL`"
            Small_Oil_Rig = "`OILRIG1HELI`\n`OILRIG1DOCK`\n`OILRIG1EXHAUST`\n`OILRIG1L1`\n`OILRIG1L2`\n`OILRIG1L3`\n`OILRIG1L4`"
            Underwater_Labs = "`AUXPOWER****`\n`BRIG****`\n`CANTINA****`\n`CAPTAINQUARTER****`\n`CLASSIFIED****`\n`CREWQUARTERS****`\n`HALLWAY****`\n`INFIRMARY****`\n`LAB****`\n`LOCKERROOM****`\n`OPERATIONS****`\n`SECURITYHALL****`\n`TECHCABINET****`\n"

            embed = discord.Embed(title="CCTV Codes", color=0x8080ff)
            embed.set_author(name=f"@{ctx.author}",
                             icon_url=f"{display_avatar}")
            embed.set_thumbnail(url="https://i.imgur.com/6GkZ17S.png")
            embed.add_field(name="Airfield", value=Airfield, inline=False)
            embed.add_field(name="Bandit Camp",
                            value=Bandit_Camp, inline=False)
            embed.add_field(name="Dome", value=Dome, inline=False)
            embed.add_field(name="Large Oil Rig",
                            value=Large_Oil_Rig, inline=False)
            embed.add_field(name="Outpost", value=Outpost, inline=False)
            embed.add_field(name="Small Oil Rig",
                            value=Small_Oil_Rig, inline=False)
            embed.add_field(name="Underwater Labs",
                            value=Underwater_Labs, inline=False)
            await rust_info_channel.send(embed=embed)

        if first.lower() == "pager":

            embed = discord.Embed(title="Pager / Frequency ", color=0x8080ff)
            embed.set_author(name=f"@{ctx.author}",
                             icon_url=f"{display_avatar}")
            embed.set_thumbnail(url="https://i.imgur.com/IoKrSDC.png")
            embed.add_field(name="Small Oil Rig", value="`4765`", inline=True)
            embed.add_field(name="Large Oil Rig", value="`4768`", inline=True)
            embed.add_field(name="Giant Excavator",
                            value="`4777`", inline=True)
            await rust_info_channel.send(embed=embed)

        if first.lower() == "cost":
            embed = discord.Embed(title="Price list", color=0x8080ff)
            embed.set_author(name=f"@{ctx.author}")
            embed.set_thumbnail(url="https://i.imgur.com/EzCYdSa.png")
            Fishing_Village = "Boot `125 Scrap`\nRHIB `300 Scrap`\nOne-man Submarine `200 Scrap`\nTwo-man Submarine `300 Scrap`\n2*Torpedo `75 Scrap`"
            embed.add_field(name="Fishing Village",
                            value=Fishing_Village, inline=False)
            await rust_info_channel.send(embed=embed)

        if first.lower() == "fert":

            if second == None:
                embed = discord.Embed(title="Fertilizer Calk", url="https://rustlabs.com/item/fertilizer",
                                      description="`2` Fertilizer yield `3` Scrap", color=0x0000ff)
                embed.set_author(name=f"@{ctx.author}",
                                 icon_url=f"{display_avatar}")
                embed.set_thumbnail(
                    url="https://rustlabs.com/img/items180/fertilizer.png")
                await rust_info_channel.send(embed=embed)

            else:
                fert_menge = int(second)
                fert_sel_min = 2
                fert_sell_Scrap = 3
                sell_Scrap_sum = int((fert_menge/fert_sel_min)*fert_sell_Scrap)
                embed = discord.Embed(title="Fertilizer Calk", url="https://rustlabs.com/item/fertilizer",
                                      description=f"`{fert_menge}` Fertilizer yield `{sell_Scrap_sum}` Scrap", color=0x0000ff)
                embed.set_author(name=f"@{ctx.author}")
                embed.set_thumbnail(
                    url="https://rustlabs.com/img/items180/fertilizer.png")
                await rust_info_channel.send(embed=embed)

        if first.lower() == "giant" or first.lower() == "quarry" or first.lower() == "diesel":

            if second == None:
                embed = discord.Embed(title="Giant Excavator", url="https://rustlabs.com/entity/giant-excavator",
                                      description="Diesel 20 need 40 min", color=0x8080ff)
                embed.set_author(name=f"@{ctx.author}",
                                 icon_url=f"{display_avatar}")
                embed.add_field(name="HQM", value="`200.000`", inline=False)
                embed.add_field(name="Metal Fragments",
                                value="`100.000`", inline=False)
                embed.add_field(name="Sulfur Ore",
                                value="`40.000`", inline=False)
                embed.add_field(name="Stones", value="`2.000`", inline=False)
                embed.set_image(
                    url="https://rustlabs.com/img/screenshots/excavator.png")
                await rust_info_channel.send(embed=embed)

                embed = discord.Embed(title="Mining Quarry", url="https://rustlabs.com/item/mining-quarry",
                                      description="Diesel 20 need 43 min", color=0x8080ff)
                embed.set_author(name=f"@{ctx.author}",
                                 icon_url=f"{display_avatar}")
                embed.add_field(
                    name="Stone Quarry", value=f"Metal Ore `20.000` and Stone `100.000`", inline=False)
                embed.add_field(name="HQM Quarry",
                                value=f"`1.000`", inline=False)
                embed.add_field(name="Sulfur Quarry",
                                value=f"`20.000`", inline=False)
                embed.add_field(
                    name="Pump Jack", value=f"Crude Oil `1.200` and Low Grade Fuel `3.400` = Low Grade Fuel`7.000` ", inline=False)
                embed.set_image(
                    url="https://rustlabs.com/img/items180/mining.quarry.png")
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

                embed = discord.Embed(title="Giant Excavator", url="https://rustlabs.com/entity/giant-excavator",
                                      description=f"`{Diesel_Fuel}` Diesel need `{Time_need}` min.", color=0x8080ff)
                embed.set_author(name=f"@{ctx.author}",
                                 icon_url=f"{display_avatar}")
                embed.set_thumbnail(
                    url="https://rustlabs.com/img/screenshots/excavator.png")
                embed.add_field(name="HQM", value=f"`{HQM}`", inline=False)
                embed.add_field(name="Metal Fragments",
                                value=f"`{Metal}`", inline=False)
                embed.add_field(name="Sulfur Ore",
                                value=f"`{Sulfur}`", inline=False)
                embed.add_field(
                    name="Stones", value=f"`{Stone}`", inline=False)
                await rust_info_channel.send(embed=embed)

                Rocket_Sulf = 1400
                C4_Sulf = 2200
                Exploammo_Sulf = 25
                Satchel_Sulf = 480

                Sulfur = int(Sulfur)
                Rocket = int(Sulfur/Rocket_Sulf)
                C4 = int(Sulfur/C4_Sulf)
                Exploammo = int(Sulfur/Exploammo_Sulf)
                Satchel = int(Sulfur/Satchel_Sulf)

                text = f"Aus {Sulfur} Sulfur:\n\nRockets: `{Rocket}`\nC4: `{C4}`\nExploammo: `{Exploammo}`\nSatchel: `{Satchel}`"

                embed = discord.Embed(
                    title="Sulfur Calk", url="https://rustraidcalculator.com/HTML/raidCalc.html", description=text, color=0x0000ff)
                embed.set_author(name=f"@{ctx.author}",
                                 icon_url=f"{display_avatar}")
                embed.set_thumbnail(
                    url="https://rustlabs.com/img/items180/sulfur.png")
                await rust_info_channel.send(embed=embed)

                Diesel_Fuel = int(second)

                Fuel_max = 20
                min_max = 43
                Time_need = int((min_max/Fuel_max)*Diesel_Fuel)
                max_Metal = 20000
                max_Stone = 100000
                max_Sulfur = 20000
                max_HQM = 1000
                max_Oil = 1200
                max_Fuel = 3400

                one_f_Metal = max_Metal/Fuel_max
                one_f_Stone = max_Stone/Fuel_max
                one_f_Sulfur = max_Sulfur/Fuel_max
                one_f_HQM = max_HQM/Fuel_max
                one_f_Oil = max_Oil/Fuel_max
                one_f_Fuel = max_Fuel/Fuel_max

                Metal = int(one_f_Metal * Diesel_Fuel)
                Stone = int(one_f_Stone * Diesel_Fuel)
                Sulfur = int(one_f_Sulfur * Diesel_Fuel)
                HQM = int(one_f_HQM * Diesel_Fuel)
                Oil = int(one_f_Oil * Diesel_Fuel)
                Fuel = int(one_f_Fuel * Diesel_Fuel)
                Oil_toFuel = int(((Oil/3)*9)+Fuel)

                embed = discord.Embed(title="Mining Quarry", url="https://rustlabs.com/item/mining-quarry",
                                      description=f"{Diesel_Fuel} Diesel need {Time_need} min", color=0x8080ff)
                embed.set_author(name=f"@{ctx.author}",
                                 icon_url=f"{display_avatar}")
                embed.add_field(
                    name="Stone Quarry", value=f"Metal Ore `{Metal}` and Stone `{Stone}`", inline=False)
                embed.add_field(name="HQM Quarry",
                                value=f"`{HQM}`", inline=False)
                embed.add_field(name="Sulfur Quarry",
                                value=f"`{Sulfur}`", inline=False)
                embed.add_field(
                    name="Pump Jack", value=f"Crude Oil `{Oil}` and Low Grade Fuel `{Fuel}` = Low Grade Fuel`{Oil_toFuel}` ", inline=False)
                embed.set_image(
                    url="https://rustlabs.com/img/items180/mining.quarry.png")
                await rust_info_channel.send(embed=embed)

                Rocket_Sulf = 1400
                C4_Sulf = 2200
                Exploammo_Sulf = 25
                Satchel_Sulf = 480

                Sulfur = int(Sulfur)
                Rocket = int(Sulfur/Rocket_Sulf)
                C4 = int(Sulfur/C4_Sulf)
                Exploammo = int(Sulfur/Exploammo_Sulf)
                Satchel = int(Sulfur/Satchel_Sulf)

                text = f"Aus {Sulfur} Sulfur:\n\nRockets: `{Rocket}`\nC4: `{C4}`\nExploammo: `{Exploammo}`\nSatchel: `{Satchel}`"

                embed = discord.Embed(
                    title="Sulfur Calk", url="https://rustraidcalculator.com/HTML/raidCalc.html", description=text, color=0x0000ff)
                embed.set_author(name=f"@{ctx.author}",
                                 icon_url=f"{display_avatar}")
                embed.set_thumbnail(
                    url="https://rustlabs.com/img/items180/sulfur.png")
                await rust_info_channel.send(embed=embed)

        if first.lower() == "sulfur":

            Rocket_Sulf = 1400
            C4_Sulf = 2200
            Exploammo_Sulf = 25
            Satchel_Sulf = 480

            Rocket_GP = 650
            C4_GP = 1000
            Exploammo_GP = 10
            Satchel_GP = 240

            if second == None:

                text = f"How much sulfur is needed:\n\nRocket: `{Rocket_Sulf} Sulfur` \nC4: `{C4_Sulf} Sulfur`\nExploammo: `{Exploammo_Sulf} Sulfur`\nSatchel: `{Satchel_Sulf} Sulfur`"

                embed = discord.Embed(
                    title="Sulfur Calk", url="https://rustraidcalculator.com/HTML/raidCalc.html", description=text, color=0x0000ff)
                embed.set_author(name=f"@{ctx.author}",
                                 icon_url=f"{display_avatar}")
                embed.set_thumbnail(
                    url="https://rustlabs.com/img/items180/sulfur.png")
                await rust_info_channel.send(embed=embed)

            else:
                Sulfur = int(second)
                Rocket = int(Sulfur/Rocket_Sulf)
                C4 = int(Sulfur/C4_Sulf)
                Exploammo = int(Sulfur/Exploammo_Sulf)
                Satchel = int(Sulfur/Satchel_Sulf)

                text = f"From {Sulfur} Sulfur:\n\nRockets: `{Rocket}`\nC4: `{C4}`\nExploammo: `{Exploammo}`\nSatchel: `{Satchel}`"

                embed = discord.Embed(
                    title="Sulfur Calk", url="https://rustraidcalculator.com/HTML/raidCalc.html", description=text, color=0x0000ff)
                embed.set_author(name=f"@{ctx.author}",
                                 icon_url=f"{display_avatar}")
                embed.set_thumbnail(
                    url="https://rustlabs.com/img/items180/sulfur.png")
                await rust_info_channel.send(embed=embed)

        if first.lower() == "bind":

            embed = discord.Embed(title="Must-have Extra Bind",
                                  url="https://steamcommunity.com/sharedfiles/filedetails/?id=2493654016", description="Top Bind´s")
            embed.set_author(name=f"@{ctx.author}",
                             icon_url=f"{display_avatar}")
            embed.set_thumbnail(
                url="https://steamuserimages-a.akamaihd.net/ugc/1782841546158853511/E74F024244C442AE5D85E781C5AABC298A6CB759/?imw=128&imh=128&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true")
            embed.add_field(
                name=" 1. Autorun", value="Press Y and you Run without pressing W\n `bind Y \"forward;sprint\"`", inline=False)
            embed.add_field(name=" 2. Auto Bandage Craft",
                            value="Press C and you craft on the Fly some Bandage in a Fight\n `bind C \"craft.add -2072273936 1\" `", inline=False)
            embed.add_field(name="3. Combatlog", value="Open the combatlog in the Console\n `bind f1 consoletoggle;combatlog`\nShow only the damge you deal\n`bind f2 \"consoletoggle;combatlog_outgoing\"`", inline=False)
            embed.add_field(
                name="4. Fast Suicide", value="Just HotKey the Kill Comand in the Console (Press END for Self kill)\n `bind end \"kill\"`", inline=False)
            embed.add_field(name="5. AutoMine bind", value="it automatically uses the attack action in conjunction with crouch - giving you more time to look around your surroundings more efficiently and ultimately allowing you to survive longer.\n `bind m \"attack;duck\"`", inline=True)
            embed.add_field(name=" 6. Toggle crouch",
                            value="Toggle crouch until you manually press crouch again\n `bind c duck`", inline=False)
            embed.add_field(name="7. Automatically heal",
                            value="automatically used bandage or syringe in slot 6:\n `bind T \"+slot6;+attack\"`", inline=False)
            embed.add_field(name="8. Automatically Player focus on Map",
                            value="The Map focus on Player if you open it.:\n`bind g \"+map;+focusmap\"`", inline=False)
            embed.add_field(name="9. Fast Switch to your Slot 4 and 5",
                            value="Better Control over your Hotbar.:\n`bind mousewheelup \"+slot4\"`\n`bind mousewheeldown \"+slot5\"`", inline=False)
            embed.add_field(
                name="More", value="Steam Guide: [Must-have Extra Bind](https://steamcommunity.com/sharedfiles/filedetails/?id=2493654016)", inline=False)
            await rust_info_channel.send(embed=embed)

        if first.lower() == "elec":

            embed = discord.Embed(title="Must have Electronic Circuits",
                                  url="https://steamcommunity.com/sharedfiles/filedetails/?id=2375732344", description="a collection of my must-have Electronic Circuits for Rust!")
            embed.set_author(name=f"@{ctx.author}",
                             icon_url=f"{display_avatar}")
            embed.set_thumbnail(
                url="https://steamuserimages-a.akamaihd.net/ugc/2039609591868400626/3DDEBD3AAF15EE8C54E98FE9805530E56FCC247B/?imw=128&imh=128&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=true")
            embed.add_field(name="Steam", value="Steam Guide: [Must-have Extra Bind](https://steamcommunity.com/sharedfiles/filedetails/?id=2375732344)", inline=False)
            await rust_info_channel.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(Rust_Info(bot))
