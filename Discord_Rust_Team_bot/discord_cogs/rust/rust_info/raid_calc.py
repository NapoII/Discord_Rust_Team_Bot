import discord
from discord.ui import Select, View, Modal, TextInput
from discord.ext import commands
from util.__funktion__ import decimal_separator

sec_to_delta = 6 * 60

# Base raid cost per structure
base_raid_cost = {
    "Wooden Door": {"Rocket": 1, "HV-Rocket":4, "INC-Rocket":1, "C4": 1, "Satchel": 2, "Explosive-Bullets":19, "beancan":6, "handmade-shell":45, "F1-Granade":23, "Molotov":2, "HP": 200, "best_with_t3": {"method": "Explosive-Bullets", "amount": 19}, "best_without_t3": {"method": "Molotov", "amount": 2} },

    "Sheet Metal Door": {"Rocket": 2, "HV-Rocket":11, "INC-Rocket":0, "C4": 1, "Satchel": 4, "Explosive-Bullets":63, "beancan":18, "handmade-shell":0, "F1-Granade":50, "Molotov":0, "HP": 250, "best_with_t3": {"method": "Explosive-Bullets", "amount": 63}, "best_without_t3": {"method": "Satchel", "amount": 4} },

    "Garage Door": {"Rocket": 3, "HV-Rocket":25, "INC-Rocket":0, "C4": 2, "Satchel": 9, "Explosive-Bullets":150, "beancan":42, "handmade-shell":0, "F1-Granade":120, "Molotov":0, "HP": 600, "best_with_t3": {"method": "C4+Rocket", "amount": {"C4": 1, "Rocket": 1}}, "best_without_t3": {"method": "Satchel", "amount": 9} },

    "Armored Door": {"Rocket": 5, "HV-Rocket":42, "INC-Rocket":0, "C4": 3, "Satchel": 15, "Explosive-Bullets":250, "beancan":69, "handmade-shell":0, "F1-Granade":200, "Molotov":0, "HP": 1000, "best_with_t3": {"method": "C4+Explosive-Bullets", "amount": {"C4": 2, "Explosive-Bullets": 31}}, "best_without_t3": {"method": "Satchel", "amount": 15} },

    "Wooden Wall": {"Rocket": 2, "HV-Rocket":9, "INC-Rocket":1, "C4": 1, "Satchel": 3, "Explosive-Bullets":49, "beancan":13, "handmade-shell":93, "F1-Granade":59, "Molotov":1, "HP": 250, "best_with_t3": {"method": "INC-Rocket", "amount": 1}, "best_without_t3": {"method": "Molotov", "amount": 1} },

    "Stone Wall": {"Rocket": 4, "HV-Rocket":32, "INC-Rocket":0, "C4": 2, "Satchel": 10, "Explosive-Bullets":185, "beancan":46, "handmade-shell":556, "F1-Granade":182, "Molotov":0, "HP": 500, "best_with_t3": {"method": "C4", "amount": 2}, "best_without_t3": {"method": "Satchel", "amount": 10} },

    "Sheet Metal Wall": {"Rocket": 8, "HV-Rocket":67, "INC-Rocket":0, "C4": 4, "Satchel": 23, "Explosive-Bullets":400, "beancan":112, "handmade-shell":0, "F1-Granade":993, "Molotov":0, "HP": 1000, "best_with_t3": {"method": "C4", "amount": 4}, "best_without_t3": {"method": "Satchel", "amount": 23} },

    "Armored Wall": {"Rocket": 15, "HV-Rocket":134, "INC-Rocket":0, "C4": 8, "Satchel": 46, "Explosive-Bullets":799, "beancan":223, "handmade-shell":0, "F1-Granade":1986, "Molotov":0, "HP": 2000, "best_with_t3": {"method": "C4+Explosive-Bullets", "amount": {"C4": 7, "Explosive-Bullets": 30}}, "best_without_t3": {"method": "Satchel", "amount": 46} },

    "Ladder Hatch": {"Rocket": 2, "HV-Rocket":11, "INC-Rocket":0, "C4": 1, "Satchel": 4, "Explosive-Bullets":63, "beancan":18, "handmade-shell":0, "F1-Granade":50, "Molotov":0, "HP": 250, "best_with_t3": {"method": "Explosive-Bullets", "amount": 63}, "best_without_t3": {"method": "Satchel", "amount": 4} },

    "Shop Front": {"Rocket": 6, "HV-Rocket":50, "INC-Rocket":0, "C4": 3, "Satchel": 18, "Explosive-Bullets":300, "beancan":99, "handmade-shell":0, "F1-Granade":0, "Molotov":0, "HP": 750, "best_with_t3": {"method": "C4+Rocket", "amount": {"C4": 2, "Rocket": 2}}, "best_without_t3": {"method": "Satchel", "amount": 18} },

    "High External Wooden Wall": {"Rocket": 1, "HV-Rocket":4, "INC-Rocket":0, "C4": 0.25, "Satchel": 2, "Explosive-Bullets":0, "beancan":0, "handmade-shell":0, "F1-Granade":0, "Molotov":0, "HP": 500, "best_with_t3": {"method": "INC-Rocket", "amount": 1}, "best_without_t3": {"method": "Molotov", "amount": 7} },

    "Auto Turret": {"Rocket": 4, "HV-Rocket":3, "INC-Rocket":1, "C4": 1, "Satchel": 2, "Explosive-Bullets":112, "beancan":16, "handmade-shell":56, "F1-Granade":10, "Molotov":0, "HP": 1000 , "best_with_t3": {"method": "HV-Rocket", "amount": 3}, "best_without_t3": {"method": "HV-Rocket", "amount": 3} },
}

crafting_recipes = {
    "Rocket": {
        "craft_recipe": {
            "Sulfur": 1400,
            "Metal Pipe": 2
        },
        "output_amount": 1
    },
    "HV-Rocket": {
        "craft_recipe": {
            "Sulfur": 200,
            "Metal Pipe": 1
        },
        "output_amount": 1
    },
    "INC-Rocket": {
        "craft_recipe": {
            "Sulfur": 610,
            "Metal Pipe": 2
        },
        "output_amount": 1
    },
    "C4": {
        "craft_recipe": {
            "Tech Trash": 2,
            "Sulfur": 2200
        },
        "output_amount": 1
    },
    "Satchel": {
        "craft_recipe": {
            "Beancan": 4,
            "Sulfur": 480
        },
        "output_amount": 1
    },
    "Explosive-Bullets": {
        "craft_recipe": {
            "Metal Fragments": 5,
            "Gun Powder": 10,
            "Sulfur": 25
        },
        "output_amount": 2
    },
    "beancan": {
        "craft_recipe": {
            "Metal Fragments": 20,
            "Gun Powder": 60,
            "Sulfur": 120
        },
        "output_amount": 1
    },
    "handmade-shell": {
        "craft_recipe": {
            "Stone": 5,
            "Gun Powder": 5,
            "Sulfur": 10
        },
        "output_amount": 2
    },
    "F1-Granade": {
        "craft_recipe": {
            "Metal Fragments": 25,
            "Gun Powder": 30,
            "Sulfur": 60
        },
        "output_amount": 1
    },
    "Molotov": {
        "craft_recipe": {
            "Cloth": 10,
            "Low Grade": 50
        },
        "output_amount": 1
    }
}

base_raid_cost_images = {
    "Wooden Door": "https://usercontent.one/wp/rusttips.com/wp-content/uploads/raidcalc-icons/wooden-door.png?media=1734460827",
    "Sheet Metal Door": "https://usercontent.one/wp/rusttips.com/wp-content/uploads/raidcalc-icons/sheet-metal-door.png?media=1734460827",
    "Garage Door": "https://usercontent.one/wp/rusttips.com/wp-content/uploads/raidcalc-icons/garage-door.png?media=1734460827",
    "Armored Door": "https://usercontent.one/wp/rusttips.com/wp-content/uploads/raidcalc-icons/armored-door.png?media=1734460827",
    "Wooden Wall": "https://usercontent.one/wp/rusttips.com/wp-content/uploads/raidcalc-icons/wooden-wall.png?media=1734460827",
    "Stone Wall": "https://usercontent.one/wp/rusttips.com/wp-content/uploads/raidcalc-icons/stone-wall.png?media=1734460827",
    "Sheet Metal Wall": "https://usercontent.one/wp/rusttips.com/wp-content/uploads/raidcalc-icons/metal-wall.png?media=1734460827",
    "Armored Wall": "https://usercontent.one/wp/rusttips.com/wp-content/uploads/raidcalc-icons/armored-wall.png?media=1734460827",
    "Ladder Hatch": "https://usercontent.one/wp/rusttips.com/wp-content/uploads/raidcalc-icons/ladder-hatch.png?media=1734460827",
    "Shop Front": "https://usercontent.one/wp/rusttips.com/wp-content/uploads/raidcalc-icons/metal-shop-front.png?media=1734460827",
    "High External Wooden Wall": "https://usercontent.one/wp/rusttips.com/wp-content/uploads/raidcalc-icons/wooden-external-wall.png?media=1734460827",
    "Auto Turret": "https://usercontent.one/wp/rusttips.com/wp-content/uploads/raidcalc-icons/autoturret.png?media=1734460827",
}

# emoji_mapping = {
#     "Wooden Door": "<:woodendoor:1327517248721518633>",
#     "Sheet Metal Door": "<:sheetmetaldoor:1327517247060705311>",
#     "Garage Door": "<:garagedoor:1327517237573189642>",
#     "Armored Door": "<:armoreddoor:1327517235224514711>",
#     "Wooden Wall": "<:woodenwall:1327517255369494581>",
#     "Stone Wall": "<:stonewall:1327517359208140800>",
#     "Sheet Metal Wall": "<:metalwall:1327517251942879284>",
#     "Armored Wall": "<:armoredwall:1327517250407895141>",
#     "Ladder Hatch": "<:ladderhatch:1327517682290917426>",
#     "Shop Front": "<:shopfront:1327517230933741628>",
#     "High External Wooden Wall": "<:woodenexternalwall:1327517398169030676>",
#     "Auto Turret": "<:autoturret:1327517227150475347>"
# }

async def raid_calculator(ctx):
    # Dropdown options
    options = [
        discord.SelectOption(label=label, description=f"HP: {decimal_separator(base_raid_cost[label]['HP'])}")
        for label in base_raid_cost.keys()
    ]

    # Dropdown selection menu
    select = Select(
        placeholder="Choose what you want to raid...",
        options=options
    )

    # Define callback for when a user selects an option
    async def select_callback(interaction):
        selected = select.values[0]

        # Create a modal for input
        class RaidAmountModal(Modal):
            def __init__(self):
                super().__init__(title="Enter Raid Amount")

                # Input field for raid amount
                self.add_item(TextInput(label="How many parts do you want to raid?", placeholder="Enter a number"))

            # Callback when the modal is submitted
            async def on_submit(self, modal_interaction):
                amount = int(self.children[0].value)  # Get the input value and convert to int
                raid_costs = base_raid_cost[selected]

                total_cost = {}
                for material, raid_info in raid_costs.items():
                    print(f"Processing material: {material}, Raid Info: {raid_info}, Type: {type(raid_info)}")

                    if isinstance(raid_info, int):  # Handle direct integer values
                        sulfur_cost = 0
                        if material in crafting_recipes:
                            recipe = crafting_recipes[material]
                            sulfur_per_item = recipe['craft_recipe'].get('Sulfur', 0)
                            output_amount = recipe.get('output_amount', 1)
                            sulfur_cost = (sulfur_per_item / output_amount) * raid_info

                        total_cost[material] = {
                            'cost': raid_info * amount,
                            'sulfur': round(sulfur_cost * amount),
                        }

                    elif isinstance(raid_info, dict):  # Handle dictionary values
                        print(f"Skipping {material} as it contains additional data.")
                        continue

                    else:
                        print(f"Unknown type for {material}. Skipping...")
                        continue

                response_text = f"### **{decimal_separator(amount)} {selected}(s)** will require:\n"
                material_to_emoji = {
                    material: get_emoji_for_cost([material])[0] if get_emoji_for_cost([material]) else "❓"
                    for material in total_cost.keys()
                }
                response_text += "\n".join(
                    [
                        f"- {material_to_emoji.get(material, '❓')} **{decimal_separator(total['cost'])} {material}(s)** (+{decimal_separator(total['sulfur'])} {get_emoji_for_cost(['Sulfur'])[0]})"
                        for material, total in total_cost.items()
                    ]
                )

                # Add best methods
                best_methods = print_best_method(selected)
                best_with_t3 = best_methods['best_with_t3']
                best_without_t3 = best_methods['best_without_t3']

                emoji_with_t3 = (
                    get_emoji_for_cost([best_with_t3['method']])[0]
                    if best_with_t3['method'] in get_emoji_for_cost(best_methods.keys())
                    else ""
                )
                emoji_without_t3 = (
                    get_emoji_for_cost([best_without_t3['method']])[0]
                    if best_without_t3['method'] in get_emoji_for_cost(best_methods.keys())
                    else ""
                )
                # Function to calculate sulfur cost
                def calculate_sulfur_cost(amount_dict):
                    total_sulfur_cost = 0
                    for material, count in amount_dict.items():
                        if material in crafting_recipes:
                            recipe = crafting_recipes[material]
                            sulfur_per_item = recipe['craft_recipe'].get('Sulfur', 0)
                            output_amount = recipe.get('output_amount', 1)
                            total_sulfur_cost += (sulfur_per_item / output_amount) * count
                    return round(total_sulfur_cost)

                # Best method with T3
                if best_with_t3['method']:
                    if isinstance(best_with_t3['amount'], dict):  # Handle dictionary amount
                        # Scale amounts by the number of doors
                        scaled_amounts = {material: count * amount for material, count in best_with_t3['amount'].items()}
                        sulfur_cost = calculate_sulfur_cost(scaled_amounts)

                        # Add emojis to the method name
                        method_with_emojis = " + ".join(
                            f"{get_emoji_for_cost([part])[0]}{part}" for part in scaled_amounts.keys()
                        )

                        # Format the parts details
                        parts_details = " + ".join(
                            f"(**{count} {get_emoji_for_cost([part])[0]} {part}**)"
                            for part, count in scaled_amounts.items()
                        )

                        # Append to response
                        response_text += (
                            f"\n\n### **Best Method with T3:**\n > {method_with_emojis} {parts_details}"
                            f"\n> (Cost: **{decimal_separator(sulfur_cost)} Sulfur**)"
                        )
                    else:  # Handle single value
                        scaled_amount = best_with_t3['amount'] * amount
                        sulfur_cost = calculate_sulfur_cost({best_with_t3['method']: scaled_amount})
                        emoji_with_t3 = get_emoji_for_cost([best_with_t3['method']])[0]

                        response_text += (
                            f"\n\n### **Best Method with T3:** \n > {emoji_with_t3}{scaled_amount}X {best_with_t3['method']} "
                            f"\n> (**Cost**: **{decimal_separator(sulfur_cost)} Sulfur**)"
                        )
                else:
                    response_text += f"\n\n### **Best Method with T3:**\n> (+{decimal_separator(best_with_t3.get('cost', 0))} Sulfur)"

                # Best method without T3
                if best_without_t3['method']:
                    if isinstance(best_without_t3['amount'], dict):  # Handle dictionary amount
                        # Scale amounts by the number of doors
                        scaled_amounts = {material: count * amount for material, count in best_without_t3['amount'].items()}
                        sulfur_cost = calculate_sulfur_cost(scaled_amounts)

                        # Add emojis to the method name
                        method_with_emojis = " + ".join(
                            f"{get_emoji_for_cost([part])[0]}{part}" for part in scaled_amounts.keys()
                        )

                        # Format the parts details
                        parts_details = " + ".join(
                            f"(**{count} {get_emoji_for_cost([part])[0]} {part}**)"
                            for part, count in scaled_amounts.items()
                        )

                        # Append to response
                        response_text += (
                            f"\n### **Best Method without T3:**\n > {method_with_emojis} {parts_details}"
                            f"\n> (Cost: **{decimal_separator(sulfur_cost)} Sulfur**)"
                        )
                    else:  # Handle single value
                        scaled_amount = best_without_t3['amount'] * amount
                        sulfur_cost = calculate_sulfur_cost({best_without_t3['method']: scaled_amount})
                        emoji_without_t3 = get_emoji_for_cost([best_without_t3['method']])[0]

                        response_text += (
                            f"\n### **Best Method without T3:**\n > {emoji_without_t3}{scaled_amount}X {best_without_t3['method']} "
                            f"\n> (Cost: **{decimal_separator(sulfur_cost)} Sulfur**)"
                        )
                else:
                    response_text += f"\n### **Best Method without T3:**\n >(+{decimal_separator(best_without_t3.get('cost', 0))} Sulfur)"


                embed = discord.Embed(title=f"Raid Costs for {selected}", description=response_text)
                embed.set_image(url=base_raid_cost_images[selected])  # Add image corresponding to selected item

                # Send the embed as a response
                await modal_interaction.response.send_message(
                    embed=embed,
                    ephemeral=True  # Only visible to the user
                )

        # Send the modal to the user
        modal = RaidAmountModal()
        await interaction.response.send_modal(modal)

    select.callback = select_callback

    # Create a View to add dropdown and send embed
    view = View()
    view.add_item(select)

    # Send the view to the user
    await ctx.send(view=view, delete_after=(sec_to_delta))

def print_best_method(structure):
    best_with_t3 = base_raid_cost[structure]['best_with_t3']
    best_without_t3 = base_raid_cost[structure]['best_without_t3']

    # Combine multiple items into a single string with a "+" sign
    if isinstance(best_with_t3['method'], list):
        best_with_t3_method = " + ".join(best_with_t3['method'])
    else:
        best_with_t3_method = best_with_t3['method']

    if isinstance(best_without_t3['method'], list):
        best_without_t3_method = " + ".join(best_without_t3['method'])
    else:
        best_without_t3_method = best_without_t3['method']

    return {
        'best_with_t3': {'method': best_with_t3_method, 'amount': best_with_t3['amount']},
        'best_without_t3': {'method': best_without_t3_method, 'amount': best_without_t3['amount']}
    }

def get_emoji_for_cost(materials):
    emojis = {
        "Rocket": "<:rocket:1327517680521056297>",
        "HV-Rocket": "<:rockethv:1327517223639580703>",
        "INC-Rocket": "<:rocketinc:1327517678877020293>",
        "C4": "<:c4:1327517219588145182>",
        "Satchel": "<:satchel:1327517217595592725>",
        "Explosive-Bullets": "<:exploammo:1327517216450547712>",
        "beancan": "<:beancan:1327517209693523978>",
        "handmade-shell": "<:handmadeshell:1327517208125112392>",
        "F1-Granade": "<:f1grenade:1327517205998338088>",
        "Molotov": "<:molotovcoctail:1328364758843527278>",
        "HP": ":shield:",
        "Sulfur": "<:sulfurcooked:1327517183953207348>",
        "Metal Pipe": "<:pipes:1327517175426056244>",
        "Gun Powder": "<:gunpowder:1327517185601437738>",
        "Low Grade": "<:lowgrade:1327517180262088768>",
        "Cloth": "<:cloth:1327517179100397690>",
        "Metal Fragments": "<:metalfrags:1327517108485230623>",
        "Tech Trash": "<:techtrash:1327517090969550972>"

    }
    return [emojis[material] for material in materials if material in emojis]
