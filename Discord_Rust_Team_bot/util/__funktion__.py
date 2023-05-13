"""
Full Doku on: https://github.com/NapoII/Discord_Rust_Team_bot"
-----------------------------------------------
ChatGPT promt for docstrgs:

write me a .py docstr ("""""") with the content:
Args, Returns, Example Usage for the code in eng.
Use for Args and Returns "- " for a listing and for Example Usage: ">>> ".
Here is the code:

"""

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
import logNow
import pyautogui
import requests
from discord import app_commands, ui
from discord.ext import commands
from logNow import *
from bs4 import BeautifulSoup

#    Prevents the code from being executed when the file is imported as a module.
if __name__ == "__funktion__":
    log("__function should not be executed when the file is imported as a module.\nThis was not the case!", "r")
else:
    pass


def read_config(config_dir, section, option):
    """Reads a specific option from a config file in a specific section.

    Args:
    - config_dir (str): The path of the config file.
    - section (str): The section where the searched option is located.
    - option (str): The name of the option being searched for.

    Returns:
    - str: The value of the searched option.

    Example Usage:
        Assuming you have a config file named 'example_config.ini' that looks like this:

        - [database]
        - host = localhost
        - port = 5432
        - username = dbuser
        - password = dbpass

        You can use the function to read the value of the 'host' option in the 'database' section like this:

        >>> read_config('example_config.ini', 'database', 'host')
        'localhost'
    """

    config = ConfigParser()
    config.read(config_dir)
    load_config = (config[section][option])
    if len(load_config) == 0 or load_config == "None":
        load_config = None

    log(f"Config loaded: [ {option} = {load_config} ]", "g")

    return load_config


def write_config(config_dir, section, Key, option):
    """
Args:
    - config_dir (str): The directory where the configuration file is located.
    - section (str): The section name in the configuration file.
    - Key (str): The key to update or add in the specified section.
    - option (str): The value to assign to the specified key.

Returns:
    - None

Example Usage:
    - Updating an existing key in a section of a configuration file
    >>>  write_config('config.ini', 'section1', 'key1', 'new_value')

    >>>  Adding a new key in a section of a configuration file
    >>>  write_config('config.ini', 'section2', 'key2', 'value2')
"""
    config = ConfigParser()
    # update existing value
    config.read(config_dir)
    try:
        config.add_section(section)
    except:
        pass
    option = str(option)
    config.set(section, Key, option)  # Updating existing entry
    with open(config_dir, 'w', encoding='utf-8') as configfile:
        config.write(configfile)
    print(
        f"\nChange settings -> {config_dir}\n[{section}]\n{Key}) = {option}\n")


def Folder_gen(Folder_Name, Folder_dir):
    """Creates a new folder if it does not already exist.

            Args:
            - folder_name (str): The name of the folder to be created.
            - folder_dir (str): The directory in which the folder is to be created.

            Returns:
            - str: The full path of the created folder.

            Example usage :
            >>> Folder_Name = "my_folder"
            >>> Folder_dir = "path/to/parent/directory"
            >>> created_folder_path = Folder_gen(Folder_Name, Folder_dir)
            >>> print("Created folder path:", created_folder_path)
    """

    print("Folder structure is checked and created if necessary...\n")
    folder = Folder_Name
    # Specifies desired file path
    #dir = "~/"+str(Folder_dir)+"/"+str(folder)
    full_path = Folder_dir + os.path.sep + Folder_Name
    # Adds file path with PC user name
    #full_path = os.path.expanduser(dir)
    # Checks file path for exsistance Ture/False
    if os.path.exists(full_path):
        print("Folder structure already exists")
        print("  ->   " + str(full_path))
    else:                                               # Creates folder if not available
        os.makedirs(full_path)
        log(f"The folder [{folder}] was created in the directory:\n  ->   {full_path}", "b")
        print("\n")
    return(os.path.normpath(full_path))


def Create_File(File_name, save_path, Inhalt):
    """Creates a new text file if it does not already exist and fills it with the specified content.

    Args:
    - File_name (str): The name of the text file.
    - save_path (str): The path where the text file should be saved.
    - Content (str): The content to be written to the text file.

    Returns:
    - str: The complete path of the created text file.

    Example usage:
    >>> file_name = "my_text_file.txt"
    >>> save_path = "/path/to/save/directory"
    >>> content = "This is the content of my text file."
    >>> created_file_path = Create_File(file_name, save_path, content)
    >>> print(created_file_path)
    '/path/to/save/directory/my_text_file.txt'
    """

    complete_Path_Text = save_path + os.path.sep + File_name
    if os.path.exists(complete_Path_Text):
        return complete_Path_Text
    else:
        # Create file
        file1 = open(complete_Path_Text, "w", encoding='utf-8')
        # toFile = input("Write what you want into the field")                   # File input def.
        # File is filled with input
        file1.write(f"{Inhalt}")
        file1.close()
        log(f"\nfile [{File_name}] is created...with conetnt:\{Inhalt}", "b")
        return complete_Path_Text


def Read_File_Out(dir):
    """
    Reads the contents of a file located at the given directory path and returns it as a string.

    Args:
    - dir (str): The directory path of the file to be read.

    Returns:
    - content (str): The contents of the file as a string.

    Example usage:
    >>> file_path = "/path/to/file.txt"
    >>> content = Read_File_Out(file_path)
    >>> print(content)
    'This is the content of the file.'
    """
    with open(dir, 'r', encoding='utf-8') as f:
        content = f.read()

    return content


def copy_image(source_file, dest_file) -> None:
    """Copies an image file from the source path to the destination path.

    Args:
    - source_file (str): The path of the image file to be copied.
    - dest_file (str): The path where the image file should be copied to.

    Returns:
    - file (str) full path of the img

    Raises:
    - IOError: If an error occurs while copying the file.

    Example usage:
    >>> source_path = "/path/to/source/image.jpg"
    >>> dest_path = "/path/to/destination/image.jpg"
    >>> copy_image(source_path, dest_path)
    '/path/to/destination/image.jpg'
    """
    try:
        shutil.copy(source_file, dest_file)
        file = dest_file
        log(f"Image [{file}] successfully copied!", "b")
        return file
    except IOError as e:
        log(f"Error when copying the file: {e}", "r")


def File_name_with_time(FileName):
    """Generate a filename with a timestamp.

    Args:
    - FileName (str): The name of the file.

    Returns:
    - FullName (str): The full name of the file with a timestamp in the format of "FileName-DD_MM_YYYY-HH.MM".

    Example usage:
    >>> Datei_name_mit_Zeit("report")
    'report-04_04_2023-15.30'
    """
    Date = Date_Time = (time.strftime("%d_%m-%Y-%H.%M")
                        )        # Generates date formater
    # Generates file name
    FullName = (FileName+"-"+(Date))
    return FullName


def TimeStemp():
    """
    Generates a timestamp string in the format of "dd_mm-yyyy_HH:MM:SS".

    Args:
        None

    Returns:
        A string representing the current date and time in the format "dd_mm-yyyy_HH:MM:SS".

    Example Usage:
        >>> TimeStemp()
        '04_04-2023_11:22:33'
    """
    TimeStemp = Date_Time = (time.strftime("%d_%m-%Y_%H:%M:%S"))
    return TimeStemp


################################################################################################################################
# def spez.


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


def discord_time_convert(time):
    """
    Converts a Unix timestamp to Discord time format.

    Args:
        time (int): A Unix timestamp to convert to Discord time format.

    Returns:
        - discord_time (str): A string representing the input timestamp in Discord time format.

    Example Usage:
        >>> timestamp = 1617123999
        >>> discord_time = discord_time_convert(timestamp)
        >>> print(discord_time)
        '<t:1617123999:R>'
            1678369942473.0
    """
    time = int(str(time)[:10])
    discord_time = (f"<t:{time}:R>")
    return discord_time


def ISO_Time_to_Milisec(time_str):
    """
    Converts an ISO-formatted datetime string to a Unix timestamp in milliseconds.

    Args:
        time_str (str): A datetime string in ISO format, e.g. "2022-01-01T00:00:00.000Z".

    Returns:
        - timestamp (str): A Unix timestamp in milliseconds as a string.

    Example Usage:
        >>> iso_time_str = "2022-01-01T00:00:00.000Z"
        >>> timestamp_ms = ISO_Time_to_Milisec(iso_time_str)
        >>> print(timestamp_ms)
        '1640995200'
    """
    dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
    return str(dt.timestamp() * 1000)


def Team_choice(Team_data_fiel_dir):
    """
    Retrieves a list of team names and their associated notes from a JSON file.

    Args:
        Team_data_fiel_dir (str): The file directory for the JSON file containing the team data.

    Returns:
        - Team_list (list): A list of team names as strings.
        - Team_Note_list (list): A list of notes associated with each team name as strings.

    Example Usage:
        >>> team_data_dir = "\Work_Folder\Rust\Team_data.json"
        >>> teams, notes = Team_choice(team_data_dir)
        >>> print(teams)
        ['Red Team', 'Blue Team', 'Green Team']
        >>> print(notes)
        ['This team is focused on offense.', 'This team is focused on defense.', 'This team is focused on resource gathering.']
    """
    #Team_data_fiel_dir = f"E:\Pr0grame\My_ Pyhton\work_in_progress\Discord_Bot_Napo_III_2.1\Work_Folder\Rust\Team_data.json"

    team_file = Read_File_Out(Team_data_fiel_dir)
    res = json.loads(team_file)
    Team_list = list(res["Teams"].keys())
    Team_list_len = len(Team_list)
    x = -1
    Team_Note_list = []
    while True:
        x = x + 1
        if x == Team_list_len:
            break

        note = res["Teams"][Team_list[x]]["note"]
        Team_Note_list.append(note)
    return Team_list, Team_Note_list


def add_player(dict, team, name, id, note):
    """
    Adds a new player to a team in a dictionary containing team data.

    Args:
        - dict (dict): A dictionary containing team data.
        - team (str): The name of the team the player will be added to.
        - name (str): The name of the new player.
        - id (str): The ID of the new player.
        - note (str): A note associated with the new player.
        - steam (str): Optinal steam info

    Returns:
        - dict (dict): The updated dictionary containing the new player's information.

    Example Usage:
        >>> team_data = {
                "Teams": {
                    "Red Team": {
                        "Player 1": {
                            "ID": "12345",
                            "note": "This player is a skilled sniper."
                        }
                    }
                }
            }
        >>> new_team_data = add_player(team_data, "Red Team", "Player 2", "67890", "This player is a great builder.")
        >>> print(new_team_data)
        {
            "Teams": {
                "Red Team": {
                    "Player 1": {
                        "ID": "12345",
                        "note": "This player is a skilled sniper."
                    },
                    "Player 2": {
                        "ID": "67890",
                        "note": "This player is a great builder."
                    }
                }
            }
        }
    """

    dict["Teams"][f"{team}"][f"{name}"] = {"ID": f"{id}", "note": f"{note}"}
    return dict


def delt_player(dict, Team, Player):
    """
    Removes a player from a team in a dictionary containing team data.

    Args:
        - dict (dict): A dictionary containing team data.
        - Team (str): The name of the team the player will be removed from.
        - Player (str): The name of the player to be removed.

    Returns:
        - dict (dict): The updated dictionary with the player removed.

    Example Usage:
        >>> team_data = {
                "Teams": {
                    "Red Team": {
                        "Player 1": {
                            "ID": "12345",
                            "note": "This player is a skilled sniper."
                        },
                        "Player 2": {
                            "ID": "67890",
                            "note": "This player is a great builder."
                        }
                    }
                }
            }
        >>> new_team_data = delt_player(team_data, "Red Team", "Player 2")
        >>> print(new_team_data)
        {
            "Teams": {
                "Red Team": {
                    "Player 1": {
                        "ID": "12345",
                        "note": "This player is a skilled sniper."
                    }
                }
            }
        }
    """
    dict["Teams"][f"{Team}"].pop(f"{Player}")
    return dict


def add_Team(dict, team, note, embed_id):
    """
Add a new team to the dictionary with the given team name, note, and embed ID.

Args:
- dict: A dictionary containing the current team data.
- team (str): The name of the new team.
- note (str): A note to attach to the new team.
- embed_id (str): The ID of the embed to be used for the new team.

Returns:
- dict: The updated dictionary with the new team added.

Example Usage:
>>> team_dict = {"Teams": {"Team1": {"note": "This is a note", "embed_id": "123456789"}}}
>>> team_dict = add_Team(team_dict, "Team2", "Another note", "987654321")
>>> print(team_dict)
{"Teams": {"Team1": {"note": "This is a note", "embed_id": "123456789"}, "Team2": {"note": "Another note", "embed_id": "987654321", "Sub_Discord_ID_list": [], "Last_Status": False}}}
"""
    dict["Teams"].update({F"{team}": {}})
    dict["Teams"][F"{team}"].update({"note": f"{note}"})
    dict["Teams"][F"{team}"].update({"embed_id": f"{embed_id}"})
    dict["Teams"][F"{team}"].update({"Sub_Discord_ID_list": []})
    dict["Teams"][F"{team}"].update({"Last_Status": False})

    dict.update
    return dict


def delt_Team(dict, Team):
    """
Remove a team from the dictionary with the given team name.

Args:
- dict: A dictionary containing the current team data.
- Team (str): The name of the team to be removed.

Returns:
- dict: The updated dictionary with the team removed.

Example Usage:
>>> team_dict = {"Teams": {"Team1": {"note": "This is a note", "embed_id": "123456789"}, "Team2": {"note": "Another note", "embed_id": "987654321", "Sub_Discord_ID_list": [], "Last_Status": False}}}
>>> team_dict = delt_Team(team_dict, "Team2")
>>> print(team_dict)
{"Teams": {"Team1": {"note": "This is a note", "embed_id": "123456789"}}}
"""

    dict[f"Teams"].pop(f"{Team}")
    return dict


def open_JSOn_File(Json_fiel_dir):
    """
Args:
- Json_fiel_dir (str): the directory of the JSON file to be opened.

Returns:
- dict: the contents of the JSON file in dictionary format.

Example Usage:
>>> file_dir = "data/teams.json"
>>> team_data = open_JSOn_File(file_dir)
>>> print(team_data["Teams"]["Red"]["note"])
"Team Red is a PvP-oriented team"
"""
    f = open(Json_fiel_dir)
    dict = json.load(f)
    json_object = json.dumps(dict, indent=2)
    f.close()
    return dict


def Fill_JSOn_File(dir, dictionary):
    """
Args:
- dir (str): The directory of the file to be filled.
- dictionary (dict): The dictionary to be filled in the file.

Returns:
- None

Example Usage:
>>> Fill_JSOn_File("data.json", {"name": "John", "age": 30})
Datei [data.json] wird beschrieben und gespeichtert...
"""
    file1 = open(
        dir, "w", encoding="utf-8")                                 # Datei wird geöffnet
    print(f"File [{dir}] is described and saved...\n")
    json_object = json.dumps(dictionary, indent=4)
    # Datei wird gefüllt mit input
    file1.write(json_object)
    file1.close()


def create_and_fill_temp_bridge(toFill, dir):
    """Create and fill a temporary file with the provided content.

Args:
- toFill (str): The string content to be written to the temporary file.
- dir (str): The path and name of the file to be created.

Returns:
- str: The same string content that was written to the file.

Example Usage:
>>> create_and_fill_temp_bridge("This is some content.", "temp_file.txt")
'This is some content.'
"""
    file1 = open(
        dir, "a", encoding="utf-8")
    log(f"Temp_Datei [{dir}] is described and saved...\n")
    file1.write(str(toFill))
    file1.close()
    return dir


def read_and_delt_temp_bridge(dir):
    """Args:
- dir (str): The directory of the temporary file to read and delete.

Returns:
- content (str): The content of the temporary file.

This function reads the content of the temporary file located at `dir`, deletes the file, and returns the content as a string.

Example Usage:
>>> temp_file_content = read_and_delt_temp_bridge("path/to/temp_file.txt")
"""
    file1 = open(dir, "r", encoding="utf-8")
    context = (file1.read())
    log(f"File [{dir}] is opened ...\n")
    file1.close()
    try:
        os.remove(dir)
    except OSError as e:
        log(e)
    else:
        log(f"Temp_Datei [{dir}] was deleted...\n")
    return context


def get_all_embed_IDs(JSOn_data):
    """Get a list of all embed IDs for the teams in a given JSON data.

Args:
- JSOn_data (dict): A dictionary containing the JSON data.

Returns:
- Teams_embed_id_list (list): A list of all embed IDs for the teams in the JSON data.

Example Usage:
>>> JSOn_data = {
        "Teams": {
            "Team 1": {
                "note": "This is team 1.",
                "embed_id": "123456",
                "Sub_Discord_ID_list": [],
                "Last_Status": False
            },
            "Team 2": {
                "note": "This is team 2.",
                "embed_id": "789012",
                "Sub_Discord_ID_list": [],
                "Last_Status": False
            }
        }
    }
>>> get_all_embed_IDs(JSOn_data)
[123456, 789012]
"""

    Team_Player_list = list(JSOn_data["Teams"].keys())
    Team_Player_list_len = len(Team_Player_list)
    Teams_embed_id_list = []
    x = -1
    while True:
        x = x + 1
        if x == Team_Player_list_len:
            break

        embed_id = JSOn_data["Teams"][f"{Team_Player_list[x]}"]["embed_id"]
        Teams_embed_id_list.append(int(embed_id))
    return Teams_embed_id_list


def get_all_Player_from_a_Team(JSOn_data, Team):
    """Args:
    JSOn_data (dict): A dictionary containing information about teams and players.
    Team (str): The name of the team whose players will be returned.

Returns:
    list: A list containing the names of all the players in the given team.

Example Usage:
    >>> JSOn_data = {"Teams": {"Team1": {"note": "Some notes", "embed_id": "1234",
    ...     "Sub_Discord_ID_list": [], "Last_Status": False, "Player1": {"ID": "1", "note": ""},
    ...     "Player2": {"ID": "2", "note": ""}}, "Team2": {"note": "Some other notes",
    ...     "embed_id": "5678", "Sub_Discord_ID_list": [], "Last_Status": False,
    ...     "Player3": {"ID": "3", "note": ""}, "Player4": {"ID": "4", "note": ""}}}}
    >>> get_all_Player_from_a_Team(JSOn_data, "Team1")
    ['Player1', 'Player2']
"""
    Team_list = list(JSOn_data["Teams"].keys())
    Team_list_len = len(Team_list)
    x = -1
    while True:
        x = x + 1
        if x == Team_list_len:
            break

        Team_Player_list = list(JSOn_data["Teams"][f"{Team}"].keys())
        Team_Player_list.remove('note')
        Team_Player_list.remove('embed_id')
        Team_Player_list.remove('Sub_Discord_ID_list')
        Team_Player_list.remove("Last_Status")

    return Team_Player_list


def Team_online_status(JSOn_data, Team_Name, servers_id):
    """
Args:
    JSOn_data (dict): The JSON data containing information about teams and players.
    Team_Name (str): The name of the team to check for online status.
    servers_id (str): The ID of the game server to check player online status on.

Returns:
    bool or str: Returns True if at least one player from the given team is currently online on the specified server, False otherwise. If the function encounters an error, it returns a string describing the error.

Example Usage:
    >>> JSOn_data = {"Teams": {"Team1": {"Player1": {"ID": "1234"}, "Player2": {"ID": "5678"}}}}
    >>> Team_online_status(JSOn_data, "Team1", "9999")
    False
    >>> Team_online_status(JSOn_data, "Team1", "8888")
    'Rate Limit Exceeded'
"""

    online = False
    Player_list = get_all_Player_from_a_Team(JSOn_data, Team_Name)
    Player_list_len = len(Player_list)
    x = -1
    while True:
        x = x + 1

        if x == Player_list_len:
            break

        Player = Player_list[x]
        Player_id = JSOn_data["Teams"][Team_Name][Player]["ID"]

        Player_Server_url = f"https://api.battlemetrics.com/players/{Player_id}/servers/{servers_id}"
        response = requests.get(Player_Server_url)
        json_data = response.json()

        #json_object = json.dumps(json_data, indent = 2)
        try:
            Error_429 = json_data["errors"][0]["title"]
            if Error_429 == "Rate Limit Exceeded":
                log("Rate Limit Exceeded")
                return Error_429
        except:
            try:
                online = json_data["data"]["attributes"]["online"]
                if str(online) == "True":
                    return True
            except:
                online = json_data["errors"][0]["status"]


def Player_name_cange(JSOn_data, Team_Name, Player):
    """
    Change the player name for a given team in the JSON data using the
    BattleMetrics API.

    Args:
        - JSOn_data (dict): JSON data containing player information.
        - Team_Name (str): Name of the team to which the player belongs.
        - Player (str): Name of the player whose name is to be changed.

    Returns:
        - A tuple containing two values:
            - A boolean value indicating whether the name was changed (True)
              or not (False).
            - The new name of the player.

    Example Usage:
        >>> JSOn_data = {"Teams": {"TeamA": {"Player1": {"ID": 1}}}}
        >>> Team_Name = "TeamA"
        >>> Player = "Player1"
        >>> Player_name_change(JSOn_data, Team_Name, Player)
        (True, "NewName")
    """
    Player_id = JSOn_data["Teams"][Team_Name][Player]["ID"]
    Player_Server_url = f"https://api.battlemetrics.com/players/{Player_id}"
    response = requests.get(Player_Server_url)
    json_data = response.json()
    New_name = json_data["data"]["attributes"]["name"]
    if Player == New_name:
        return False, New_name
    else:
        return True, New_name


def Player_Server_info(Player_id, servers_id):
    """
    Get the server information for a given player ID and server ID using the
    BattleMetrics API.

    Args:
        - Player_id (str): ID of the player.
        - servers_id (str): ID of the server.

    Returns:
        - A tuple containing the following values:
            - A string indicating whether the player is online or offline.
            - A string indicating the last time the player was seen on the server.
            - A float indicating the total time the player has played on the server (in hours).
            - The URL of the BattleMetrics API call made to retrieve the data.

    If an error occurs during the API call, a string containing the error status code is returned.

    Example Usage:
        >>> Player_id = "12345"
        >>> servers_id = "67890"
        >>> Player_Server_info(Player_id, servers_id)
        ("🟢", "2 days, 3 hours ago", 12.34, "https://api.battlemetrics.com/players/12345/servers/67890")
    """
    Player_Server_url = f"https://api.battlemetrics.com/players/{Player_id}/servers/{servers_id}"
    response = requests.get(Player_Server_url)
    json_data = response.json()
    #json_object = json.dumps(json_data, indent = 2)
    try:
        Error_429 = json_data["errors"][0]["title"]
        if Error_429 == "Rate Limit Exceeded":
            log("Rate Limit Exceeded ")
            return Error_429
    except:
        pass

    try:
        online = json_data["data"]["attributes"]["online"]

        if online == True:
            Online_ico = "🟢"
        else:
            Online_ico = "🔴"

        lastSeen = json_data["data"]["attributes"]["lastSeen"]
        lastSeen = ISO_Time_to_Milisec(lastSeen)
        lastSeen = discord_time_convert(lastSeen)
        timePlayed = json_data["data"]["attributes"]["timePlayed"]
        timePlayed = round(int(timePlayed)/60/60, 2)

        return Online_ico, lastSeen, timePlayed, Player_Server_url
    except:
        online = json_data["errors"][0]["status"]
        return str(online)


def Get_all_player_list(dict):
    """
    Get a list of all players in the data dictionary.

    Args:
        - data_dict (dict): A dictionary containing data for all teams and players.

    Returns:
        - A list of all players in the data dictionary.

    Example Usage:
        >>> data_dict = {"Teams": {"TeamA": {"Player1": {"ID": 1}, "Player2": {"ID": 2}}, "TeamB": {"Player3": {"ID": 3}}}}
        >>> Get_all_player_list(data_dict)
        ["Player1", "Player2", "Player3"]
    """
    Full_Player_list = []
    Team_list = list(dict["Teams"].keys())
    Team_list_len = len(Team_list)
    x = -1
    while True:
        x = x + 1
        if x == Team_list_len:
            break

        Team_sepz_player_list = list(dict["Teams"][Team_list[x]].keys())
        Team_sepz_player_list.remove("note")
        Team_sepz_player_list.remove("embed_id")
        Team_sepz_player_list.remove("Sub_Discord_ID_list")
        Team_sepz_player_list.remove("Last_Status")

        Team_sepz_player_list_len = len(Team_sepz_player_list)
        y = -1
        while True:
            y = y + 1
            if y == Team_sepz_player_list_len:
                break
            item = Team_sepz_player_list[y]
            Full_Player_list.append(item)

    return(Full_Player_list)


def Team_name_from_Player(dict, Player_name):
    """
    Get the name of the team that a given player belongs to.

    Args:
        - data_dict (dict): A dictionary containing data for all teams and players.
        - player_name (str): The name of the player to look up.

    Returns:
        - The name of the team that the given player belongs to.

    Example Usage:
        >>> data_dict = {"Teams": {"TeamA": {"Player1": {"ID": 1}, "Player2": {"ID": 2}}, "TeamB": {"Player3": {"ID": 3}}}}
        >>> player_name = "Player2"
        >>> Team_name_from_Player(data_dict, player_name)
        "TeamA"
    """
    Team_list = list(dict["Teams"].keys())
    Team_list_len = len(Team_list)
    x = -1
    while True:
        x = x + 1
        if x == Team_list_len:
            break

        Team_sepz_player_list = list(dict["Teams"][Team_list[x]].keys())
        if Player_name in Team_sepz_player_list:
            return Team_list[x]


def get_map_img(Server_ID):
    """
    Retrieve information about a Rust server's map image.

    Args:
        - server_id (str): The ID of the server to look up.

    Returns:
        - If successful, a tuple containing:
            - The URL of the full labeled map image.
            - The URL of the raw map image.
            - The seed used to generate the map.
            - The size of the map in kilometers.
        - If unsuccessful, False.

    Example Usage:
        >>> server_id = "12345"
        >>> get_map_img(server_id)
        ("https://example.com/map.jpg", "https://example.com/map_full.jpg", "12345", "4000")
    """
    url = f"https://api.battlemetrics.com/servers/{Server_ID}"
    response = requests.get(url)
    response_json = response.json()
    try:
        map_url = response_json["data"]["attributes"]["details"]["rust_maps"]["url"]
        thumbnailUrl = response_json["data"]["attributes"]["details"]["rust_maps"]["thumbnailUrl"]
        seed = response_json["data"]["attributes"]["details"]["rust_maps"]["seed"]
        size = response_json["data"]["attributes"]["details"]["rust_maps"]["size"]

        thumbnailUrl = thumbnailUrl[:thumbnailUrl.rfind(
            "Thumbnail.png")]+str("FullLabeledMap.png")

        return thumbnailUrl, map_url, seed, size

    except:
        return False


def from_embed_ID_to_data(JSOn_data, embed_ID):
    """
Args:
    JSOn_data (dict): A dictionary that contains all of the JSON data for a game.
    embed_ID (str): A string that represents the embed ID.

Returns:
    Tuple: A tuple containing the team name and the sub discord ID.

Example Usage:
    >>> data = {"Teams": {"Team A": {"embed_id": "12345", "Sub_Discord_ID_list": ["123", "456"]}, "Team B": {"embed_id": "67890", "Sub_Discord_ID_list": ["789", "012"]}}}
    >>> from_embed_ID_to_data(data, "67890")
    ("Team B", ["789", "012"])
"""

    Team_list = list(JSOn_data["Teams"].keys())
    Team_list_len = len(Team_list)

    x = -1
    while True:

        x = x + 1
        if x == Team_list_len:
            break

        Team_embed_id = JSOn_data["Teams"][f"{Team_list[x]}"]["embed_id"]
        if Team_embed_id == embed_ID:
            Team = Team_list[x]
            Sub_Discord_ID = JSOn_data["Teams"][f"{Team_list[x]}"]["Sub_Discord_ID_list"]
            return Team, Sub_Discord_ID


def delt_all_Player_subs(JSOn_data, Player_ID):
    """Args:
    - JSOn_data: a dictionary containing information about Rust teams and players.
    - Player_ID: a string representing the ID of the player who will be unsubscribed from all teams.

Returns:
    - JSOn_data: the same dictionary as the input, but with the specified player removed from the "Sub_Discord_ID_list" of all teams.

Example Usage:
    >>> data = {
    ...     "Teams": {
    ...         "TeamA": {
    ...             "note": "",
    ...             "embed_id": "123456789",
    ...             "Sub_Discord_ID_list": ["player1", "player2", "player3"],
    ...             "Last_Status": []
    ...         },
    ...         "TeamB": {
    ...             "note": "",
    ...             "embed_id": "987654321",
    ...             "Sub_Discord_ID_list": ["player1", "player4"],
    ...             "Last_Status": []
    ...         }
    ...     }
    ... }
    >>> Player_ID = "player1"
    >>> updated_data = delt_all_Player_subs(data, Player_ID)
    >>> print(updated_data)
    {
        "Teams": {
            "TeamA": {
                "note": "",
                "embed_id": "123456789",
                "Sub_Discord_ID_list": ["player2", "player3"],
                "Last_Status": []
            },
            "TeamB": {
                "note": "",
                "embed_id": "987654321",
                "Sub_Discord_ID_list": ["player4"],
                "Last_Status": []
            }
        }
    }
"""
    Team_list = list(JSOn_data["Teams"].keys())
    Team_list_len = len(Team_list)

    x = -1
    while True:

        x = x + 1
        if x == Team_list_len:
            break

        Sub_Discord_ID_list = list(
            JSOn_data["Teams"][f"{Team_list[x]}"]["Sub_Discord_ID_list"])
        try:
            Sub_Discord_ID_list.remove(Player_ID)
            JSOn_data["Teams"][f"{Team_list[x]}"]["Sub_Discord_ID_list"] = Sub_Discord_ID_list
        except:
            pass
    return JSOn_data


def scrape(url):
    """
This function takes a URL as input and tries to scrape the page using the requests module in Python. If successful, it returns the HTML content of the page, otherwise, it returns False.

Args:
url (str): The URL of the page to scrape.

Returns:
str or bool: The HTML content of the page as a string if the scraping is successful, otherwise, False.

Example Usage:
>>> html = scrape('https://www.example.com')
>>> if html:
... print(html)
... else:
... print('Scraping failed.')
"""
    try:
        page = requests.get(url)
        return page.text
    except:
        print(f'Could not scrape: {url}')
        return False


def get_player_id_from_name(player_name, server_id):
    """
Args:
player_name (str): The name of the player to search for.
server_id (str): The ID of the server to search on.

Returns:
str: The ID of the player, if found, or None if the player is not found.

Example Usage:
>>> get_player_id_from_name('JohnDoe', '123456')
https://www.battlemetrics.com/rcon/players/987654321
"""
    log(f"get_player_id_from_name({player_name}, {server_id}) use url_end = lastSeen")
    url = f"https://www.battlemetrics.com/players?filter%5Bsearch%5D={player_name}&filter%5BplayerFlags%5D=&filter%5Bservers%5D={server_id}&sort=-lastSeen"

    html = scrape(url)
    soup = BeautifulSoup(html, 'html.parser')

    # FFinding the HTML element with the class 'player-name'
    player_name_herf = soup.find('a', {'class': 'player-name'})

    if player_name_herf is not None:
        # If the element was found, output the URL from the 'href' attribute
        href = player_name_herf.get('href')
        print(href)
        # Split the string into a list using '/' as the delimiter, and get the last item
        result = href.split('/')[-1]

        bat_name = get_player_name(result)
        print(f"bat_name= {bat_name} player_name= {player_name}")
        if bat_name == player_name:
            return result
        else:

            log(f"get_player_id_from_name({player_name}, {server_id}) use url_end = Score")
            url = f"https://www.battlemetrics.com/players?filter%5Bsearch%5D={player_name}&filter%5BplayerFlags%5D=&filter%5Bservers%5D={server_id}&sort=score"
            html = scrape(url)
            soup = BeautifulSoup(html, 'html.parser')

            # FFinding the HTML element with the class 'player-name'
            player_name_herf = soup.find('a', {'class': 'player-name'})

            if player_name_herf is not None:
                # If the element was found, output the URL from the 'href' attribute
                href = player_name_herf.get('href')
                print(href)
                # Split the string into a list using '/' as the delimiter, and get the last item
                result = href.split('/')[-1]

                bat_name = get_player_name(result)
                print(f"bat_name= {bat_name} player_name= {player_name}")
                if bat_name == player_name:
                    return result
                else:
                    log(
                        f" get_player_id_from_name({player_name}, {server_id}) The item was not found.")
                    return None

    else:
        # If the element was not found, give an error message
        log(f" get_player_id_from_name({player_name}, {server_id}) The item was not found.")
        return None


def get_player_name(player_id):
    """
Args:
    server_id (int): The ID of the Battlemetrics server to check.
    steam_url (str): The Steam URL of the player to start checking from.

Returns:
    dict: A dictionary with the names of the players found, their Steam URL, and the server ID checked. Returns None if the initial Steam URL is invalid or if no players were found on the server.

Example Usage:
>>> team_cheacker(1234567, "https://steamcommunity.com/profiles/12345678901234567/")
Team Detector Result:

Name:                               SteamID:            Link:
ExamplePlayer1                      12345678901234567  https://steamcommunity.com/profiles/12345678901234567/
ExamplePlayer2                      23456789012345678  https://steamcommunity.com/profiles/23456789012345678/
"""

    url = f'https://api.battlemetrics.com/players/{player_id}'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()['data']
        name = data['attributes']['name']
        return name
    else:
        print(f"Error {response.status_code}: Could not get data from {url}")
        return None


def team_checker(server_id, steam_url):
    """
This function checks a Rust server to determine if any players on the server are friends with the provided Steam account.

Args:

    server_id (int): The ID of the Rust server to check
    steam_url (str): The Steam profile URL to check for friends on the Rust server

Returns:

    data (dict): A dictionary containing the names and Steam profile URLs of the friends found on the Rust server. If no friends are found, returns None.

Example Usage:

            team_cheacker(123456, 'https://steamcommunity.com/profiles/1234567890/')
            Team Detector Result:
            Name: SteamID: Link:
            Player 1 1234567890 https://steamcommunity.com/profiles/1234567890/
            Player 2 0987654321 https://steamcommunity.com/profiles/0987654321/
            {'Player 1': {'steam_url': 'https://steamcommunity.com/profiles/1234567890/'}, 'Player 2': {'steam_url': 'https://steamcommunity.com/profiles/0987654321/'}}
            """
    data = {}
    battlemetrics_url = f"https://www.battlemetrics.com/servers/rust/{server_id}"

    battlemetricsPlayers = get_battlemetrics_players(battlemetrics_url)
    initialFriendList = get_friend_list(steam_url)
    if initialFriendList == None:
        return None

    friends = {initialFriendList['steamId']: initialFriendList['name']}
    leftToCheck = compare_players(
        battlemetricsPlayers, initialFriendList['friends'])

    while True:
        if len(leftToCheck) == 0:
            break

        newLeft = []
        for steamId, name in leftToCheck:
            friendList = get_friend_list(
                f'https://steamcommunity.com/profiles/{steamId}/friends')
            friends[friendList['steamId']] = friendList['name']
            for steamIdC, nameC in compare_players(battlemetricsPlayers, friendList['friends']):
                if steamIdC not in friends and not any(steamIdC in x for x in newLeft):
                    newLeft.append([steamIdC, nameC])

        leftToCheck = newLeft

    print('Team Detector Result:\n')
    print('Name:'.ljust(34) + 'SteamID:'.ljust(19) + 'Link:')

    for steamId, name in friends.items():
        data[name] = {"steam_url": steam_url}
    return data


def get_battlemetrics_players(url):
    """
This function takes a 'url' string as input and returns a list of player names for a specified Battlemetrics game server.

Args:
- url (str): The URL of the Battlemetrics game server page for which to retrieve player information.

Returns:
- (list): A list of player names currently on the specified Battlemetrics game server. Returns an error message and exits the program if player information cannot be retrieved.

Example Usage:
>>> url = 'https://www.battlemetrics.com/servers/1234567'
>>> get_battlemetrics_players(url)
['Player1Name', 'Player2Name', 'Player3Name']
"""

    content = scrape(url)
    if content == False:
        print('Could not scrape Battlemetrics Server Page')
        exit()

    regex = r'<a class="css-zwebxb" href="/players/\d+?">(.+?)</a>'
    players = re.findall(regex, content)
    if len(players) == 0:
        print('Could not match players on the Battlemetrics Server Page.')
        exit()

    return players


def get_friend_list(url):
    """
This function takes a 'url' string as input and returns a dictionary containing the name, Steam ID, and list of friends for a user's Steam profile.

Args:
- url (str): The URL of the Steam profile page for which to retrieve friend information.

Returns:
- (dict): A dictionary containing the name, Steam ID, and list of friends for the specified Steam profile. Returns 'None' if the friend list cannot be retrieved.

Example Usage:
>>> url = 'https://steamcommunity.com/profiles/123456'
>>> get_friend_list(url)
{'name': 'PlayerName', 'steamId': '123456', 'friends': [('friend1_steamId', 'Friend1Name'), ('friend2_steamId', 'Friend2Name'), ('friend3_steamId', 'Friend3Name')]}
"""

    if not 'friends' in url:
        url += '/friends'

    content = scrape(url)
    if content == False:
        print('Could not scrape friend list page')
        exit()

    regex = r'<meta property="og:title" content="(.+?)">'
    name = re.findall(regex, content)[0]
    regex = r',"steamid":"(.+?)",'
    try:
        steamId = re.findall(regex, content)[0]
        regex = r'data-steamid="(.+?)".*?<div class="friend_block_content">(.+?)<br>'
        friends = re.findall(regex, content, re.MULTILINE | re.S)

        return {"name": name, "steamId": steamId, "friends": friends}
    except:
        return None


def compare_players(battlemetricsPlayers, friendList):
    """
This function takes two lists, 'battlemetricsPlayers' and 'friendList', and returns a new list containing only the Steam IDs and names of players who are on both lists.

Args:
- battlemetricsPlayers (list): A list of player names currently on a game server.
- friendList (list): A list of tuples containing Steam IDs and names for a user's friends.

Returns:
- (list): A list of tuples containing only the Steam IDs and names that are present in both 'battlemetricsPlayers' and 'friendList'.

Example Usage:
>>> battlemetricsPlayers = ['PlayerName1', 'PlayerName2', 'PlayerName3']
>>> friendList = [(123456, 'PlayerName2'), (7891011, 'PlayerName3'), (12131415, 'PlayerName4')]
>>> compare_players(battlemetricsPlayers, friendList)
[(123456, 'PlayerName2'), (7891011, 'PlayerName3')]
"""

    players = []
    for steamId, name in friendList:
        if name in battlemetricsPlayers:
            players.append([steamId, name])

    return players


def generate_list_of_online_players(server_id):
    """
This function takes a 'server_id' integer as input and generates a dictionary containing the name and ID of each online player on that server.

Args:
- server_id (int): The server ID number for which to retrieve player information.

Returns:
- (dict): A dictionary containing the name and ID of each online player on the specified server.

Example Usage:
>>> generate_list_of_online_players(12345)
{'PlayerName1': 'id1', 'PlayerName2': 'id2', 'PlayerName3': 'id3'}
"""

    url = f'https://api.battlemetrics.com/servers/{server_id}?include=player'

    # Send the GET request with the specified parameters
    response = requests.get(url)

    response_json = response.json()
    # Print the response content
    # print(response.content)

    data = {}
    included = response_json["included"]
    included_len = (len(included))-1
    x = -1
    while True:
        if x == included_len:
            break
        x = x + 1

        name = included[x]["attributes"]["name"]
        id = included[x]["attributes"]["id"]
        data[name] = id
    return data


def zip_data_steamname_and_bat_id(data_steam_name, data_battlemetrics_server_id_name):
    """
This function takes two dictionaries, 'data_steam_name' and 'data_battlemetrics_server_id_name', 
as arguments and adds the server ID value to each corresponding dictionary item in 'data_steam_name'. 

Args:
- data_steam_name (dict): A dictionary containing Steam names as keys.
- data_battlemetrics_server_id_name (dict): A dictionary containing server names and their corresponding IDs.

Returns:
- (dict): A dictionary containing Steam names and their corresponding server IDs, with the IDs added from 'data_battlemetrics_server_id_name'.

Example Usage:
>>> data_steam_name = {'SteamName1': {'value1': 1}, 'SteamName2': {'value2': 2}}
>>> data_battlemetrics_server_id_name = {'SteamName1': 'ID1', 'SteamName2': 'ID2'}
>>> zip_data_steamname_and_bat_id(data_steam_name, data_battlemetrics_server_id_name)
{'SteamName1': {'value1': 1, 'ID': 'ID1'}, 'SteamName2': {'value2': 2, 'ID': 'ID2'}}
    """
    data_steam_name_len = len(data_steam_name)

    data_steam_only_name = list(data_steam_name.keys())
    print(data_steam_name)
    x = -1
    while True:
        if x == (data_steam_name_len)-1:
            break
        x = x + 1

        name_steam = data_steam_only_name[x]
        if name_steam in data_battlemetrics_server_id_name:
            data_steam_name[name_steam]["ID"] = data_battlemetrics_server_id_name[name_steam]

    return(data_steam_name)


def get_all_online_player(server_id):
    url = f'https://api.battlemetrics.com/servers/{server_id}?include=player'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
    else:
        return None

    full_online_player_list = {}
    data = data["included"]

    data_len = len(data)

    x = -1
    while True:
        x = x + 1
        if x == data_len:
            break

        name = data[x]["attributes"]["name"]
        id = data[x]["attributes"]["id"]
        full_online_player_list[name] = {id}

    full_online_player_list = dict(sorted(full_online_player_list.items()))
    return(full_online_player_list)
