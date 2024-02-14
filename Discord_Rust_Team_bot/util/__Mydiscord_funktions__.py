"""
Full Doku on: https://github.com/NapoII/Discord_Rust_Team_bot"
-----------------------------------------------
from util.__funktion__ import *
from util.__Mydiscord_funktions__ import *
------------------------------------------------
"""

import discord
from util.__funktion__ import *

import asyncio
import datetime
import json
import os
import re
import shutil
import sys
import time
import urllib
from configparser import ConfigParser
from datetime import datetime

import discord
from discord import app_commands, ui
from discord.ext import commands

def discord_time_convert(time):
    """
    Converts a Unix timestamp to Discord time format.

    Args:
        time (int): A Unix timestamp to convert to Discord time format.



    Returns:
        - discord_time (str): A string representing the input timestamp in Discord time format.

    Example Usage:
        https://i.imgur.com/YjKkSiR.gif
        
        >>> timestamp = 1617123999
        >>> discord_time = discord_time_convert(timestamp)
        >>> print(discord_time)
        '<t:1617123999:R>'
            1678369942473.0
    """
    time = int(str(time)[:10])
    discord_time = (f"<t:{time}:R>")
    return discord_time


def Discord_Activity(Text):
    """
    Creates a Discord Activity object with the specified text and type.

    Args:
        Text (str): The text to display as the activity.

    Returns:
        - Activity (discord.Activity): A Discord Activity object with the specified text and type.

    Example Usage:
        >>> import discord
        >>> activity = Discord_Activity("Watching a movie")
        >>> client = discord.Client(activity=activity)
    """
    #Activity = discord.Client(activity=discord.Game(name='my game'))
    Activity = discord.Activity(name=Text, type=discord.ActivityType.watching)
    return Activity

# add your discord def´s in here -->

def contains_only_numbers(string):
    """
    Check if a string consists only of numbers.

    Args:
        string (str): The input string to be checked.

    Returns:
        bool: True if the string consists only of numbers, False otherwise.

    Example Usage:
        >>> contains_only_numbers("12345")
        True

        >>> contains_only_numbers("abc123")
        False
    """
    if string.isdigit():
        return True
    else:
        return False
    

def add_new_channel_data(user_name, user_id, channel_id, json_path):
    # Read in the existing JSON file
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Add the new data
    new_channel_data = {
        "user_id": {
            "owner_name":user_name,
            "channel_id": channel_id,
            "channel_msg_id": "",
            "admin": [user_id],
            "limit": "0",
            "banned": "",
            "hide": False,
            "stay": False
        }
    }

    # Add the new data to the existing data object
    data[user_id] = new_channel_data["user_id"]

    # Write the updated data back to the JSON file
    with open(json_path, 'w') as file:
        json.dump(data, file, indent=2)


def is_user_in(user_id, json_path):
    if user_id == int:
        user_id = str(user_id)
    # Read in the JSON file
    with open(json_path, 'r') as file:
        data = json.load(file)
    return str(user_id) in data.keys()


def is_channel_id_in(channel_id, json_path):
    if channel_id == str:
        channel_id = int(channel_id)
    # Read in the JSON file
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Check whether the channel_id is present
    for user_id, user_data in data.items():
        if "channel_id" in user_data and user_data["channel_id"] == channel_id:
            return True

    # If the channel_id was not found
    return False


def delete_data_with_channel_id(channel_id, json_path):
    # Read in the existing JSON file
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Check if the channel_id is present
    for user_id, user_data in list(data.items()):
        if "channel_id" in user_data and user_data["channel_id"] == channel_id:
            # Delete the parent data object
            del data[user_id]

    # Write the updated data back to the JSON file
    with open(json_path, 'w') as file:
        json.dump(data, file, indent=2)


def get_channel_id_from(owner_id, json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)

    for channel_id, channel_data in data.items():
        if channel_id == str(owner_id):
            return channel_data.get("channel_id")
    return None  # If the owner_id is not found


def is_he_channel_admin(user_id, channel_id, json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)

    for key, value in data.items():
        if "channel_id" in value and value["channel_id"] == channel_id:
            if "admin" in value and user_id in value["admin"]:
                return True

    return False


def get_channel_id_for_user_in_admin(user_id, json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)

    for key, value in data.items():
        if "admin" in value:
            if user_id == value["admin"] or (isinstance(value["admin"], list) and user_id in value["admin"]):
                return value["channel_id"]

    return False


def get_list_for_all_admin_server_from_user(user_id, json_path):
    channel_ids = []

    with open(json_path, 'r') as file:
        data = json.load(file)

    for key, value in data.items():
        if "admin" in value:
            if user_id == value["admin"] or (isinstance(value["admin"], list) and user_id in value["admin"]):
                channel_ids.append(value["channel_id"])

    return channel_ids


def get_item_from_channel(item, target_channel_id, json_input):
    # If json_input is a file path, read the JSON file
    if isinstance(json_input, str):
        with open(json_input, 'r') as file:
            data = json.load(file)
    # If json_input is already a JSON object, use it directly
    elif isinstance(json_input, dict):
        data = json_input
    else:
        raise ValueError("Invalid json_input type. Please provide either a file path (str) or a JSON object (dict).")

    # Search the data structure for the subcategory with the target channel ID
    for main_key, subcategory_data in data.items():
        if "channel_id" in subcategory_data and subcategory_data["channel_id"] == target_channel_id:
            value = data.get(main_key, {}).get(f"{item}")
            return value
    
    return None


def switch_stay_status(target_channel_id, json_path):
    # Read in the JSON file
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Search the data structure for the subcategory with the target channel ID
    for main_key, subcategory_data in data.items():
        if "channel_id" in subcategory_data and subcategory_data["channel_id"] == target_channel_id:
            # Toggle the "stay" value
            subcategory_data["stay"] = not subcategory_data.get("stay", True)

            # Write the updated data back to the JSON file
            with open(json_path, 'w') as write_file:
                json.dump(data, write_file, indent=2)

            # Return the updated "stay" value
            return subcategory_data["stay"]

    # Return None if the target channel ID is not found
    return None


def get_admin_list(channel_id, json_path):
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)

        for key, value in data.items():
            if "channel_id" in value and value["channel_id"] == channel_id:
                return value.get("admin", [])
        
        print(f"Channel mit ID {channel_id} nicht gefunden.")
        return []

    except FileNotFoundError:
        print(f"Datei {json_path} nicht gefunden.")
        return []
    

def read_json_file(json_path):
    try:
        with open(json_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Fehler beim Laden der JSON-Datei {json_path}.")
        return None


def find_main_key(target_channel_id, data_or_path):
    if isinstance(data_or_path, str):  # If it's a file path, load the data.
        with open(data_or_path, 'r') as file:
            data = json.load(file)
    elif isinstance(data_or_path, dict):  # If it's already loaded data, use it directly.
        data = data_or_path
    else:
        raise ValueError("Invalid type for data_or_path. Expected either a file path (str) or already loaded data (dict).")

    for main_key, channel_data in data.items():
        if "channel_id" in channel_data and channel_data["channel_id"] == target_channel_id:
            return main_key

    return None



def fill_item_in_channel(channel_id, item, fill, json_path):
    # Load the JSON from the file
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Iterate through the keys of the outer object
    for key, value in data.items():
        # Check if the channel_id is present in the inner object
        if "channel_id" in value and value["channel_id"] == channel_id:
            # Update the element in the found object
            value[item] = fill

            # Save the updated data back to the file
            with open(json_path, 'w') as file:
                json.dump(data, file, indent=2)
            print(f"Successfully updated {item} for channel {channel_id}.")
            return  # Exit the function after the update is done

    # If the function reaches here, the channel was not found
    print(f"Channel {channel_id} not found.")