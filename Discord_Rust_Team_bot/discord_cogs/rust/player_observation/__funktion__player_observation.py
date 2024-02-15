"""
Full Doku on: https://github.com/NapoII/Discord_Rust_Team_bot"
-----------------------------------------------
funktions for player_observation
------------------------------------------------
"""
import requests
from bs4 import BeautifulSoup
import datetime
from util.__Mydiscord_funktions__ import *
from util.__funktion__ import *


###



def player_exists(json_dir, player_name):
    with open(json_dir, 'r') as f:
        data = json.load(f)
        for team, players in data.items():
            if player_name in players:
                return True
    return False


def if_team_in_json(json_dir, team_name):
    with open(json_dir, 'r') as f:
        data = json.load(f)
        return team_name in data


def delt_all_Player_subs(JSOn_data, Player_ID):
    """Args:
    - JSOn_data: a dictionary containing information about Rust teams and players.
    - Player_ID: a string representing the ID of the player who will be unsubscribed from all teams.

Returns:
    - JSOn_data: the same dictionary as the input, but with the specified player removed from the "Sub_Discord_ID_list" of all teams.

Example Usage:
    >>> data = {
    ...      {
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
        {
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
    Team_list = list(JSOn_data.keys())
    Team_list_len = len(Team_list)

    x = -1
    while True:

        x = x + 1
        if x == Team_list_len:
            break

        Sub_Discord_ID_list = list(
            JSOn_data[f"{Team_list[x]}"]["Sub_Discord_ID_list"])
        try:
            Sub_Discord_ID_list.remove(Player_ID)
            JSOn_data[f"{Team_list[x]}"]["Sub_Discord_ID_list"] = Sub_Discord_ID_list
        except:
            pass
    return JSOn_data


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


def from_embed_ID_to_data(JSOn_data, embed_ID):
    """
Args:
    JSOn_data (dict): A dictionary that contains all of the JSON data for a game.
    embed_ID (str): A string that represents the embed ID.

Returns:
    Tuple: A tuple containing the team name and the sub discord ID.

Example Usage:
    >>> data = {"Team A": {"embed_id": "12345", "Sub_Discord_ID_list": ["123", "456"]}, "Team B": {"embed_id": "67890", "Sub_Discord_ID_list": ["789", "012"]}}}
    >>> from_embed_ID_to_data(data, "67890")
    ("Team B", ["789", "012"])
"""

    Team_list = list(JSOn_data.keys())
    Team_list_len = len(Team_list)

    x = -1
    while True:

        x = x + 1
        if x == Team_list_len:
            break

        Team_embed_id = JSOn_data[f"{Team_list[x]}"]["embed_id"]
        if Team_embed_id == embed_ID:
            Team = Team_list[x]
            Sub_Discord_ID = JSOn_data[f"{Team_list[x]}"]["Sub_Discord_ID_list"]
            return Team, Sub_Discord_ID


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
        >>> JSOn_data = {"TeamA": {"Player1": {"ID": 1}}}}
        >>> Team_Name = "TeamA"
        >>> Player = "Player1"
        >>> Player_name_change(JSOn_data, Team_Name, Player)
        (True, "NewName")
    """
    Player_id = JSOn_data[Team_Name][Player]["ID"]
    Player_Server_url = f"https://api.battlemetrics.com/players/{Player_id}"
    response = requests.get(Player_Server_url)
    json_data = response.json()
    New_name = json_data["data"]["attributes"]["name"]
    if Player == New_name:
        return False, New_name
    else:
        return True, New_name


def get_all_Player_from_a_Team(JSOn_data, Team):
    """Args:
    JSOn_data (dict): A dictionary containing information about teams and players.
    Team (str): The name of the team whose players will be returned.

Returns:
    list: A list containing the names of all the players in the given team.

Example Usage:
    >>> JSOn_data = {"Team1": {"note": "Some notes", "embed_id": "1234",
    ...     "Sub_Discord_ID_list": [], "Last_Status": False, "Player1": {"ID": "1", "note": ""},
    ...     "Player2": {"ID": "2", "note": ""}}, "Team2": {"note": "Some other notes",
    ...     "embed_id": "5678", "Sub_Discord_ID_list": [], "Last_Status": False,
    ...     "Player3": {"ID": "3", "note": ""}, "Player4": {"ID": "4", "note": ""}}}}
    >>> get_all_Player_from_a_Team(JSOn_data, "Team1")
    ['Player1', 'Player2']
"""

    Team_list = list(JSOn_data.keys())
    Team_list_len = len(Team_list)
    x = -1
    while True:
        x = x + 1
        if x == Team_list_len:
            break
        try:
            Team_Player_list = list(JSOn_data[f"{Team}"].keys())
            Team_Player_list.remove('note')
            Team_Player_list.remove('embed_id')
            Team_Player_list.remove('Sub_Discord_ID_list')
            Team_Player_list.remove("Last_Status")
        except:
            pass

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
    >>> JSOn_data = {"Team1": {"Player1": {"ID": "1234"}, "Player2": {"ID": "5678"}}}}
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
        Player_id = JSOn_data[Team_Name][Player]["ID"]

        Player_Server_url = f"https://api.battlemetrics.com/players/{Player_id}/servers/{servers_id}"
        response = requests.get(Player_Server_url)
    
        json_data = response.json()

        #json_object = json.dumps(json_data, indent = 2)
        try:
            Error_429 = json_data["errors"][0]["title"]
            if Error_429 == "Rate Limit Exceeded":
                print("Rate Limit Exceeded")
                return Error_429
        except:
            try:
                online = json_data["data"]["attributes"]["online"]
                if str(online) == "True":
                    return True
            except:
                online = json_data["errors"][0]["status"]


def delt_Team(dict, Team):
    """
Remove a team from the dictionary with the given team name.

Args:
- dict: A dictionary containing the current team data.
- Team (str): The name of the team to be removed.

Returns:
- dict: The updated dictionary with the team removed.

Example Usage:
>>> team_dict = {"Team1": {"note": "This is a note", "embed_id": "123456789"}, "Team2": {"note": "Another note", "embed_id": "987654321", "Sub_Discord_ID_list": [], "Last_Status": False}}}
>>> team_dict = delt_Team(team_dict, "Team2")
>>> print(team_dict)
{"Team1": {"note": "This is a note", "embed_id": "123456789"}}}
"""

    dict.pop(f"{Team}")
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

                "Red Team": {
                    "Player 1": {
                        "ID": "12345",
                        "note": "This player is a skilled sniper."
                    }
                }
            }
        }
    """
    dict[f"{Team}"].pop(f"{Player}")
    return dict



def Team_name_from_Player(dict, Player_name):
    """
    Get the name of the team that a given player belongs to.

    Args:
        - data_dict (dict): A dictionary containing data for all teams and players.
        - player_name (str): The name of the player to look up.

    Returns:
        - The name of the team that the given player belongs to.

    Example Usage:
        >>> data_dict = {"TeamA": {"Player1": {"ID": 1}, "Player2": {"ID": 2}}, "TeamB": {"Player3": {"ID": 3}}}}
        >>> player_name = "Player2"
        >>> Team_name_from_Player(data_dict, player_name)
        "TeamA"
    """
    Team_list = list(dict.keys())
    Team_list_len = len(Team_list)
    x = -1
    while True:
        x = x + 1
        if x == Team_list_len:
            break

        Team_sepz_player_list = list(dict[Team_list[x]].keys())
        if Player_name in Team_sepz_player_list:
            return Team_list[x]


def get_all_embed_IDs(JSOn_data):
    """Get a list of all embed IDs for the teams in a given JSON data.

Args:
- JSOn_data (dict): A dictionary containing the JSON data.

Returns:
- Teams_embed_id_list (list): A list of all embed IDs for the teams in the JSON data.

Example Usage:
>>> JSOn_data = {

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

    Team_Player_list = list(JSOn_data.keys())
    Team_Player_list_len = len(Team_Player_list)
    Teams_embed_id_list = []
    x = -1
    while True:
        x = x + 1
        if x == Team_Player_list_len:
            break

        embed_id = JSOn_data[f"{Team_Player_list[x]}"]["embed_id"]
        Teams_embed_id_list.append(int(embed_id))
    return Teams_embed_id_list


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


def Team_choice(Team_data_fiel_dir):
    """
    Retrieves a list of team names and their associated notes from a JSON file.

    Args:
        Team_data_fiel_dir (str): The file directory for the JSON file containing the team data.

    Returns:
        - Team_list (list): A list of team names as strings.
        - Team_Note_list (list): A list of notes associated with each team name as strings.
"""

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
            print("Rate Limit Exceeded ")
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
        >>> data_dict ={"TeamA": {"Player1": {"ID": 1}, "Player2": {"ID": 2}}, "TeamB": {"Player3": {"ID": 3}}}}
        >>> Get_all_player_list(data_dict)
        ["Player1", "Player2", "Player3"]
    """
    Full_Player_list = []
    Team_list = list(dict.keys())
    Team_list_len = len(Team_list)
    x = -1
    while True:
        x = x + 1
        if x == Team_list_len:
            break

        Team_sepz_player_list = list(dict[Team_list[x]].keys())
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
    print(f"get_player_id_from_name({player_name}, {server_id}) use url_end = lastSeen")
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

            print(f"get_player_id_from_name({player_name}, {server_id}) use url_end = Score")
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
                    print(
                        f" get_player_id_from_name({player_name}, {server_id}) The item was not found.")
                    return None

    else:
        # If the element was not found, give an error message
        print(f" get_player_id_from_name({player_name}, {server_id}) The item was not found.")
        return None