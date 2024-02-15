"""Full Doku on: https://github.com/NapoII/Discord_Rust_Team_bot"
-----------------------------------------------
This COG is for embed a help information for Rust.
exampel : cctv codes
------------------------------------------------
"""

from discord import app_commands

from util.__funktion__ import *
from util.__my_imge_path__ import *
img_url = my_image_url()
# get the path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
bot_path = os.path.abspath(sys.argv[0])
bot_folder = os.path.dirname(bot_path)
# construct the path to the config.ini file relative to the current directory
config_dir = os.path.join(bot_folder, "config", "config.ini")

cctv_codes_json_dir = os.path.join(bot_folder, "config", "json", "cctv_codes.json")
price_list_json_dir = os.path.join(bot_folder, "config", "json", "price_list.json")
must_have_binds_json_dir = os.path.join(bot_folder, "config", "json", "must_have_binds.json")
json_rust_help_commands_data_dir = os.path.join(bot_folder, "config", "json", "rust_help_commands.json")


rust_help_commands_jason_data = read_json_file(json_rust_help_commands_data_dir)
rust_help_commands = [re.sub(r'\{[^}]*\}', '', entry["command"].replace("```", ""))
                      for entry in rust_help_commands_jason_data]

sec_to_delta = 6*60

guild_id = read_config(config_dir, "client", "guild_id")
if guild_id == None:
    guild_id = 1
guild_id = int(guild_id)

guild = discord.Object(id=guild_id)

rust_info_channel_id = read_config(config_dir, "channels", "rust_info_channel_id")
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

        delt_msg_str = delt_str_time(sec_to_delta)

        if first.lower() in ["help", "info", "i"]:
            icon_url = img_url.rust.team_logo
            thumbnail_url = img_url.piktogramm.i
            embed = discord.Embed(title="#rust-info", color=0x8080ff)
            embed.set_author(name=f"@{ctx.author}",icon_url=f"{display_avatar}")
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
                    embed.set_author(name=f"@{ctx.author}",icon_url=f"{display_avatar}")
                    embed.set_thumbnail(url=thumbnail_url)
                    # Add the current field to the new embed
                    embed.add_field(name=command, value=description, inline=True)
                    # Increment field count for the new embed
                    field_count += 1

            # Append the last embed to the list
            embeds_list.append(embed)

            await rust_info_channel.send(embeds = embeds_list, delete_after=(sec_to_delta))

        if first.lower() == "raid":
            embed = discord.Embed(title="Raid Calculator",
                    url="https://napoii.github.io/Rust-Collection/Rust_Collection/Raid_Calc/raid_calc.html",
                    description=f"[Use the table and the calculator](https://napoii.github.io/Rust-Collection/Rust_Collection/Raid_Calc/raid_calc.html)\n\n{delt_msg_str}")
            embed.set_author(name=f"@{ctx.author}",icon_url=f"{display_avatar}")
            embed.set_image(url=img_url.rust.raid_card)
            await rust_info_channel.send(embed=embed, delete_after=(sec_to_delta))

        if first.lower() in ["cctv", "code"]:

            embed = discord.Embed(title="CCTV Codes",
                url="https://napoii.github.io/Rust-Collection/Rust_Collection/cctv_and_pager/cctv_and_pager.html",
                description=f"[Use CCTV Showcase to get a Cam Prevew](https://napoii.github.io/Rust-Collection/Rust_Collection/cctv_and_pager/cctv_and_pager.html)\n{delt_msg_str}")
            embed.set_author(name=f"@{ctx.author}",icon_url=f"{display_avatar}")
            embed.set_image(url=img_url.rust.cctv_card)
            embed.set_thumbnail(url=img_url.rust.cctv)
            cctv_codes_json = read_json_file(cctv_codes_json_dir)
            for monoment in cctv_codes_json:
                monoment_name  = monoment
                Code_list = cctv_codes_json[monoment]
                code_str = ""
                for num in Code_list:
                    code = Code_list[num]
                    code_str += f"`{code}`\n"

                embed.add_field(name=f"**{monoment_name}**",
                    value=f"{code_str}",
                    inline=False)

            await rust_info_channel.send(embed=embed, delete_after=(sec_to_delta))

        if first.lower() in ["pager", "transmiter", "code"]:
                
            embed = discord.Embed(title="Pager / Frequency ", url="https://napoii.github.io/Rust-Collection/Rust_Collection/cctv_and_pager/cctv_and_pager.html", description=f"[Use CCTV Showcase to get a Cam Prevew](https://napoii.github.io/Rust-Collection/Rust_Collection/cctv_and_pager/cctv_and_pager.html)\n{delt_msg_str}")
            embed.set_author(name=f"@{ctx.author}",icon_url=f"{display_avatar}")
            embed.set_thumbnail(url=img_url.rust.pager)
            embed.set_image(url=img_url.rust.cctv_card)
            embed.add_field(name="Small Oil Rig", value="`4765`", inline=True)
            embed.add_field(name="Large Oil Rig", value="`4768`", inline=True)
            embed.add_field(name="Giant Excavator",
                            value="`4777`", inline=True)
            await rust_info_channel.send(embed=embed, delete_after=(sec_to_delta))


        if first.lower() in ["cost", "price", "preis", "pricelist"]:

            embed = discord.Embed(title="Price list",
                url="https://napoii.github.io/Rust-Collection/",
            description=f"[For More Info go to Rust-Collection](https://napoii.github.io/Rust-Collection/)\n{delt_msg_str}")
            embed.set_thumbnail(url=img_url.rust.scrape)
            embed.set_image(url=img_url.rust.rust_collection)
            embed.set_author(name=f"@{ctx.author}",icon_url=f"{display_avatar}")

            price_list_json = read_json_file(price_list_json_dir)
            for monoment in price_list_json:
                monoment_name  = monoment
                list = price_list_json[monoment]
                price_str = ""
                for item in list:
                    price = list[item]
                    price_str += f"{item} - `{price}`\n"

                embed.add_field(name=f"{monoment_name}",
                                value=f"{price_str}", inline=False)

            await rust_info_channel.send(embed=embed, delete_after=(sec_to_delta))

        if first.lower() in ["fert", "fertiliser"]:
            url =r"https://napoii.github.io/Rust-Collection/Rust_Collection/Diesel_Calc/diesel_calc.html"
            text_link = f"[Use the calculator on Rust_Collection](https://napoii.github.io/Rust-Collection/Rust_Collection/Diesel_Calc/diesel_calc.html)\n"
            if second == None:
                embed = discord.Embed(title="Fertilizer Calk", url=url , description=f"{text_link}`2` Fertilizer yield `3` Scrap\n\n{delt_msg_str}", color=0x0000ff)
                embed.set_author(name=f"@{ctx.author}",icon_url=f"{display_avatar}")
                embed.set_thumbnail(url=img_url.rust.fertilizer)
                embed.set_image(url=img_url.rust.diesel_card)

                
                await rust_info_channel.send(embed=embed, delete_after=(sec_to_delta))

            else:
                fert_menge = int(second)
                fert_sel_min = 2
                fert_sell_Scrap = 3
                sell_Scrap_sum = int((fert_menge/fert_sel_min)*fert_sell_Scrap)
                embed = discord.Embed(title="Fertilizer Calk", url=url ,description=f"{text_link}`{decimal_separator(fert_menge)}` Fertilizer yield `{decimal_separator(sell_Scrap_sum)}` Scrap\n\n{delt_msg_str}", color=0x0000ff)
                embed.set_author(name=f"@{ctx.author}",icon_url=f"{display_avatar}")
                embed.set_thumbnail(url=img_url.rust.fertilizer)
                embed.set_image(url=img_url.rust.diesel_card)
                await rust_info_channel.send(embed=embed, delete_after=(sec_to_delta))


        if first.lower() in ["giant", "quarry", "diesel"]:
            text_link = f"[Use the calculator on Rust_Collection](https://napoii.github.io/Rust-Collection/Rust_Collection/Diesel_Calc/diesel_calc.html)\n\n{delt_msg_str}"
            url =r"https://napoii.github.io/Rust-Collection/Rust_Collection/Diesel_Calc/diesel_calc.html"
            url_img = img_url.rust.diesel_card
            embeds_list = []

            if second == None:
                diesel_fuel = 1
            else:
                diesel_fuel = int(second)

            # giant ex:
            
            time_for_one_giant = 2*60 #sec
            time_need_ginat = int((time_for_one_giant*diesel_fuel)/60)

            metal_giant_for_one = 5000
            max_stone_giant_for_one = 10000
            sulfur_giant_for_one = 2000
            hqm_giant_for_one = 100

            metal_giant = metal_giant_for_one * diesel_fuel
            stone_giant = max_stone_giant_for_one * diesel_fuel
            sulfur_giant = sulfur_giant_for_one * diesel_fuel
            hqm_giant = hqm_giant_for_one * diesel_fuel

            # querry:
            
            time_for_one_querry = 130 #sec
            time_need_querry = int((time_for_one_querry*diesel_fuel)/60)

            metal_querry_for_one = 1000
            max_stone_querry_for_one = 5000
            sulfur_querry_for_one = 1000
            hqm_querry_for_one = 50

            metal_querry = metal_querry_for_one * diesel_fuel
            stone_querry = max_stone_querry_for_one * diesel_fuel
            sulfur_querry = sulfur_querry_for_one * diesel_fuel
            hqm_querry = hqm_querry_for_one * diesel_fuel

            # boom
            rocket_sulf = 1400
            c4_sulf = 2200
            exploammo_sulf = 25
            satchel_sulf = 480

            # boom giant
            rocket_giant = sulfur_giant/rocket_sulf
            c4_giant = sulfur_giant/c4_sulf
            exploammo_giant = sulfur_giant/exploammo_sulf
            satchel_giant = sulfur_giant/satchel_sulf

            # boom querry
            rocket_querry = sulfur_querry/rocket_sulf
            c4_querry = sulfur_querry/c4_sulf
            exploammo_querry = sulfur_querry/exploammo_sulf
            satchel_querry = sulfur_querry/satchel_sulf

            embed_crad = discord.Embed(title="Diesel_Calc", url=url)
            embed_crad.set_image(url=url_img)
            await rust_info_channel.send(embed=embed_crad, delete_after=(sec_to_delta))

            description = f"""
            `{diesel_fuel}`Diesel need´s `{time_need_ginat}`min.

            **Sulfur Ore: **`{decimal_separator(sulfur_giant)}`
            **HQM: **`{decimal_separator(hqm_giant)}`
            **Metal Fragments: **`{decimal_separator(metal_giant)}`
            **Stones: **`{decimal_separator(stone_giant)}`

            {text_link}
            """
            embed_giant = discord.Embed(title="Giant Excavator", url=url , description=description, color=0x8080ff)
            embed_giant.set_author(name=f"@{ctx.author}", icon_url=f"{display_avatar}")
            embed_giant.set_thumbnail(url=img_url.rust.excavator)
            #embeds_list.append(embed_giant)
            await rust_info_channel.send(embed=embed_giant, delete_after=(sec_to_delta))

            description = f"""
            You can craft from `{decimal_separator(sulfur_giant)}`**Sulfur** from the Giant:

            **Rockets: **`{decimal_separator(rocket_giant)}`
            **C4: **`{decimal_separator(c4_giant)}`
            **Exploammo: **`{decimal_separator(exploammo_giant)}`
            **Satchel: **`{decimal_separator(satchel_giant)}`

            {text_link}
            """
            embed_boom_giant = discord.Embed(title="Boom Calcualtor from Giant Excavator", url=url, description=description, color=0x0000ff)
            embed_boom_giant.set_author(name=f"@{ctx.author}",icon_url=f"{display_avatar}")
            embed_boom_giant.set_thumbnail(url=img_url.rust.c4)

            #embeds_list.append(embed_boom_giant)
            await rust_info_channel.send(embed=embed_boom_giant, delete_after=(sec_to_delta))

            description = f"""
            `{diesel_fuel}`Diesel need´s `{time_need_querry}`min.

            **Sulfur Ore: **`{decimal_separator(sulfur_querry)}`
            **HQM: **`{decimal_separator(hqm_querry)}`
            **Metal Fragments: **`{decimal_separator(metal_querry)}`
            **Stones: **`{decimal_separator(stone_querry)}`

            {text_link}
            """

            embed_querry = discord.Embed(title="Mining Querry", url=url , description=description , color=0x8080ff)
            embed_querry.set_author(name=f"@{ctx.author}", icon_url=f"{display_avatar}")
            embed_querry.set_thumbnail(url=img_url.rust.mining_quarry)
            #embeds_list.append(embed_querry)
            await rust_info_channel.send(embed=embed_querry, delete_after=(sec_to_delta))

            description = f"""
            You can craft from `{decimal_separator(sulfur_querry)}`**Sulfur** from the querry:

            **Rockets: **`{decimal_separator(rocket_querry)}`
            **C4: **`{decimal_separator(c4_querry)}`
            **Exploammo: **`{decimal_separator(exploammo_querry)}`
            **Satchel: **`{decimal_separator(satchel_querry)}`

            {text_link}
            """

            text = f"{text_link}You can craft from `{decimal_separator(sulfur_querry)}`sulfur from the Querry:"
            embed_boom_querry = discord.Embed(title="Boom Calcualtor from Mining Querry", url=url, description=description, color=0x0000ff)
            embed_boom_querry.set_author(name=f"@{ctx.author}",icon_url=f"{display_avatar}")
            embed_boom_querry.set_thumbnail(url=img_url.rust.c4)
            #embeds_list.append(embed_boom_querry)
            await rust_info_channel.send(embed=embed_boom_querry, delete_after=(sec_to_delta))

            #len_embeds_list = len(embeds_list)
            #print(f"len_embeds_list={len_embeds_list}\nlist={embeds_list}")

            #await rust_info_channel.send(embeds=embeds_list)


        if first.lower() in ["sulfur", "sulf", "sulfor", "sul"] :
            text_link = "[More on Rust-Collection-Raid Calculator](https://napoii.github.io/Rust-Collection/Rust_Collection/Raid_Calc/raid_calc.html)\n\n"

            Rocket_Sulf = 1400
            C4_Sulf = 2200
            Exploammo_Sulf = 25
            Satchel_Sulf = 480

            Rocket_GP = 650
            C4_GP = 1000
            Exploammo_GP = 10
            Satchel_GP = 240

            if second == None:
                text = f"{text_link}How much sulfur is needed:\n\n" \
                    f"Rocket: `{decimal_separator(Rocket_Sulf)}` Sulfur\n" \
                    f"C4: `{decimal_separator(C4_Sulf)}` Sulfur\n" \
                    f"Exploammo: `{decimal_separator(Exploammo_Sulf)}` Sulfur\n" \
                    f"Satchel: `{decimal_separator(Satchel_Sulf)}` Sulfur\n\n" \
                    f"{delt_msg_str}"
                embed = discord.Embed(title="Sulfur Calk", url="https://rustraidcalculator.com/HTML/raidCalc.html", description=text, color=0x0000ff)
                embed.set_author(name=f"@{ctx.author}",icon_url=f"{display_avatar}")
                embed.set_thumbnail(url=img_url.rust.sulfur)
                embed.set_image(url=img_url.rust.raid_card)
                await rust_info_channel.send(embed=embed, delete_after=(sec_to_delta))

            else:
                Sulfur = int(second)
                Rocket = int(Sulfur/Rocket_Sulf)
                C4 = int(Sulfur/C4_Sulf)
                Exploammo = int(Sulfur/Exploammo_Sulf)
                Satchel = int(Sulfur/Satchel_Sulf)

                text = f"{text_link}From `{decimal_separator(Sulfur)}` Sulfur:\n\nRockets: `{Rocket}`\nC4: `{C4}`\nExploammo: `{decimal_separator(Exploammo)}`\nSatchel: `{Satchel}`\n\n{delt_msg_str}"

                embed = discord.Embed(title="Sulfur Calk", url="https://rustraidcalculator.com/HTML/raidCalc.html", description=text, color=0x0000ff)
                embed.set_author(name=f"@{ctx.author}",icon_url=f"{display_avatar}")
                embed.set_thumbnail(url=img_url.rust.sulfur)
                embed.set_image(url=img_url.rust.raid_card)
                await rust_info_channel.send(embed=embed, delete_after=(sec_to_delta))

        if first.lower() in ["bind", "bint"]:
            
            text_link = "[More on Rust-Collection](https://napoii.github.io/Rust-Collection/)\n\n"

            must_have_binds_json = read_json_file(must_have_binds_json_dir)
            description_str = f"{text_link}"
            x = 0
            for makro in must_have_binds_json:
                x += 1
                makro_name  = makro
                list = must_have_binds_json[makro]

                makro_name = makro
                description = must_have_binds_json[f"{makro}"]["description"]
                bind = must_have_binds_json[f"{makro}"]["bind"]
                action =  must_have_binds_json[f"{makro}"]["action"]

                description_str += f"**{x}. {makro_name}**{description}```bind {bind} {action}```\n"


            embed = discord.Embed(title="Must-have Extra Bind", url="https://steamcommunity.com/sharedfiles/filedetails/?id=2493654016", description=description_str+f"\n{delt_msg_str}")
            embed.set_author(name=f"@{ctx.author}", icon_url=f"{display_avatar}")
            embed.set_thumbnail( url=img_url.rust.bind)
            embed.set_image(url=img_url.rust.must_have_binds)

            await rust_info_channel.send(embed=embed, delete_after=(sec_to_delta))



        if first.lower() in ["elec", "elek"]:

            embed = discord.Embed(title="Must have Electronic Circuits",url="https://steamcommunity.com/sharedfiles/filedetails/?id=2375732344", description=f"Looking for essential circuits to enhance your gameplay? Check out my guide for a curated selection. Don't see what you need? Reach out to me on Steam or drop a comment below to suggest additions!\nKeep an eye out for updates allowing circuit board construction and saving for future use in-game\n\n{delt_msg_str}")
            embed.set_author(name=f"@{ctx.author}",icon_url=f"{display_avatar}")
            embed.set_thumbnail(url=img_url.rust.elec_mini)
            embed.set_image(url=img_url.rust.elec_card)
            embed.add_field(name="Steam Guide", value="[Must have Electronic Circuits](https://steamcommunity.com/sharedfiles/filedetails/?id=2375732344)", inline=False)
            await rust_info_channel.send(embed=embed, delete_after=(sec_to_delta))


class auto_smg_delt_server_info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config_dir = config_dir

    @commands.Cog.listener()
    async def on_message(self, message):


        player_observation = message.channel
        # Check if the message is from a bot to avoid potential loops
        if message.author.bot:
            return
        if message.channel.id != rust_info_channel_id:
            return
        
        message_content = message.content
        matched_command = next((command for command in rust_help_commands if message_content.startswith(command)), None)
        if matched_command:
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(f"\nplayer_observation - {current_time}:\n")
            print(f"Msg delt in 10s ec from: {message.author.name}:")
            print(f"msg:\n{message.content}\n")
            await message.delete()


async def setup(bot: commands.Bot):
    await bot.add_cog(Rust_Info(bot))
    await bot.add_cog(auto_smg_delt_server_info(bot))
