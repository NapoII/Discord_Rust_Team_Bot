"""
Full Doku on: https://github.com/NapoII/Discord_Rust_Team_bot"
-----------------------------------------------
funktions for player_observation
------------------------------------------------
"""

import requests
import re
import json
from util.__funktion__ import *

####
def add_player_to_data(json_path, key, new_player_data):
    with open(json_path, 'r') as file:
        data = json.load(file)

    if key in data:
        existing_players = data[key]
        for player, player_data in new_player_data.items():
            if player not in existing_players:
                existing_players[player] = player_data
                # Füge die Steam-URL unter der 'note' des Spielers hinzu
                if 'steam_url' in player_data:
                    existing_players[player]['note'] = f"[Steam URL]({player_data['steam_url']})"
    else:
        data[key] = new_player_data

    with open(json_path, 'w') as file:
        json.dump(data, file, indent=4)


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

    dict[f"{team}"][f"{name}"] = {"ID": f"{id}", "note": f"{note}"}
    return dict


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
    print(f"File [{dir}] is opened ...\n")
    file1.close()
    try:
        os.remove(dir)
    except OSError as e:
        print(e)
    else:
        print(f"Temp_Datei [{dir}] was deleted...\n")
    return context


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
>>> team_dict = {"Team1": {"note": "This is a note", "embed_id": "123456789"}}}
>>> team_dict = add_Team(team_dict, "Team2", "Another note", "987654321")
>>> print(team_dict)
{"Team1": {"note": "This is a note", "embed_id": "123456789"}, "Team2": {"note": "Another note", "embed_id": "987654321", "Sub_Discord_ID_list": [], "Last_Status": False}}}
"""
    dict.update({F"{team}": {}})
    dict[F"{team}"].update({"note": f"{note}"})
    dict[F"{team}"].update({"embed_id": f"{embed_id}"})
    dict[F"{team}"].update({"Sub_Discord_ID_list": []})
    dict[F"{team}"].update({"Last_Status": False})

    dict.update
    return dict


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
    print(f"Temp_Datei [{dir}] is described and saved...\n")
    file1.write(str(toFill))
    file1.close()
    return dir


def Team_choice(Team_data_fiel_dir):

    team_file = Read_File_Out(Team_data_fiel_dir)
    res = json.loads(team_file)
    Team_list = list(res.keys())
    Team_list_len = len(Team_list)
    x = -1
    Team_Note_list = []
    while True:
        x = x + 1
        if x == Team_list_len:
            break

        note = res[Team_list[x]]["note"]
        Team_Note_list.append(note)
    return Team_list, Team_Note_list



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
        if name_steam in data_steam_name:
            data_steam_name[name_steam]["ID"] = data_battlemetrics_server_id_name[name_steam]

    return(data_steam_name)


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


def team_cheack(server_id, steam_url):
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
    leftToCheck = compare_players(battlemetricsPlayers, initialFriendList['friends'])

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