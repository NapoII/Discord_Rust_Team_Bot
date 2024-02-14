"""
Full Doku on: https://github.com/NapoII/Discord_Rust_Team_bot"
-----------------------------------------------
funktions for server_stats
------------------------------------------------
"""
import requests
from datetime import datetime

def if_new_player_count(file_path, new_player_num):
    try:
        # Open the file and read the current player count
        with open(file_path, 'r') as file:
            current_player_num = int(file.read())
    except FileNotFoundError:
        # If the file is not found, create it with the specified player count
        with open(file_path, 'w') as file:
            file.write(str(new_player_num))
        return True, None  # Return True and no change type as this is the first player count

    # Check if the player count has changed
    if current_player_num < new_player_num:
        change_type = "🔼"
    elif current_player_num > new_player_num:
        change_type = "🔽"
    else:
        change_type = ""

    if current_player_num != new_player_num:
        # Write the new player count to the file
        with open(file_path, 'w') as file:
            file.write(str(new_player_num))
        return True, change_type
    else:
        return False, None  # Return False as there is no change and no change type available




def str_to_unix(str):
    # Specify the time in ISO 8601 format

    # Convert the time into a datetime object
    dt_object = datetime.fromisoformat(str.replace('Z', '+00:00'))

    # Convert datetime object to Unix time
    unix_time = int(dt_object.timestamp())
    return unix_time


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

        thumbnailUrl = thumbnailUrl[:thumbnailUrl.rfind("Thumbnail.png")]+str("FullLabeledMap.png")

        return thumbnailUrl, map_url, seed, size

    except:
        return False