"""
from util.__my_path_funktion__ import *
my_file_path = my_file_path()
"""

import os, sys
from configparser import ConfigParser
def read_config(config_dir, section, option, arg=None):
    """Reads a configuration file and returns the specified value as the desired data type.

    Args:
    - config_dir (str): The directory where the configuration file is located.
    - section (str): The section of the configuration file where the option is located.
    - option (str): The option to retrieve from the configuration file.
    - arg (str, optional): The desired data type of the retrieved value. Can be "float", "int", "tuple", or "boolean". Defaults to None.

    Returns:
    - If arg is not provided: the value of the specified option as a string.
    - If arg is "float": the value of the specified option as a float.
    - If arg is "int": the value of the specified option as an integer.
    - If arg is "tuple": the value of the specified option as a tuple of integers.
    - If arg is "boolean": the value of the specified option as a boolean.

    Example Usage:
    >>> read_config("config.ini", "database", "port")
    '5432'

    >>> read_config("config.ini", "database", "port", "int")
    5432

    >>> read_config("config.ini", "database", "credentials", "tuple")
    (123456, 'password')

    >>> read_config("config.ini", "database", "enabled", "bool")
    True
    """
    config = ConfigParser()
    config.read(config_dir)
    load_config = config[section][option]
    if arg:
        arg = arg.lower()
    
    if arg == "float":
        config_float = float(load_config)
        print(f"Config loaded: [ ({option})  = ({config_float}) ] conv to float")
        return config_float

    elif arg == "int":
        config_int = int(load_config)
        print(f"Config loaded: [ ({option})  = ({config_int}) ] conv to int")
        return config_int
    
    elif arg == "tuple":
        config_tuple = tuple(map(int, load_config.split(",")))
        print(f"Config loaded: [ ({option})  = ({config_tuple}) ] conv to tuple")
        return config_tuple
    
    elif arg == "boolean" or arg == "bool":
        config_bool = load_config.lower() in ['true', '1', 'yes', 'y']
        print(f"Config loaded: [ ({option})  = ({config_bool}) ] conv to boolean")
        return config_bool
    
    else:
        print(f"Config loaded: [ ({option})  = ({load_config}) ]")
        return load_config

class my_file_path:
    def __init__(self):

        self.bot_path = os.path.abspath(sys.argv[0])
        

    class main:
        bot_path = os.path.abspath(sys.argv[0])
        bot_folder = os.path.dirname(bot_path)
        
        bot_folder = os.path.dirname(bot_path)
        img_dir = os.path.normpath(os.path.join(bot_folder, "img"))
        util = os.path.normpath(os.path.join(bot_folder, "util"))
        config_dir = os.path.normpath(os.path.join(bot_folder, "config"))


    class config:
        bot_path = os.path.abspath(sys.argv[0])
        bot_folder = os.path.dirname(bot_path)

        config_dir = os.path.normpath(os.path.join(bot_folder, "config"))
        json_dir = os.path.join(config_dir, "json")
        log_dir = os.path.normpath(os.path.join(config_dir, "log"))

        config_ini_dir = os.path.normpath(os.path.join(config_dir, "config.ini"))
        token_ini_dir = os.path.normpath(os.path.join(config_dir, "token.ini"))

        Discord_token = read_config(token_ini_dir, "discord", "token")
        Application_ID = read_config(token_ini_dir, "discord", "application_id")

        guild_id = read_config(config_ini_dir, "client", "guild_id", "int")

        praefix = read_config(config_ini_dir, "client", "praefix")
        activity_text = read_config(config_ini_dir, "client", "activity")

        category_rust_id = read_config(config_ini_dir, "categorys", "category_rust_id")
        create_rust_voice_channel_id = read_config(config_ini_dir, "channels", "create_rust_voice_channel_id")
        create_rust_voice_channel_boolean = read_config(config_ini_dir, "channels", "create_rust_voice_channel_boolean","boolean")
        category_rust_squad_id = read_config(config_ini_dir, "categorys", "category_rust_squad_id")

        squad_mode = read_config(config_ini_dir, "rust", "squad_mode")

        rust_squad_squad_panel_mgs_id = read_config(config_ini_dir, "msgs", "rust_squad_squad_panel_mgs_id")
        rust_squad_control_mgs_id = read_config(config_ini_dir, "msgs", "rust_squad_control_mgs_id")

        squad_panel_channel_id = read_config(config_ini_dir, "channels", "squad_panel_channel_id")

        

    class json:
        
        bot_path = os.path.abspath(sys.argv[0])
        bot_folder = os.path.dirname(bot_path)
        config_dir = os.path.normpath(os.path.join(bot_folder, "config"))

        json_dir = os.path.join(config_dir, "json")

        channel_data_json_dir = os.path.normpath(os.path.join(json_dir, "channel_data.json"))
        channel_hopper_commands_json_dir = os.path.normpath(os.path.join(json_dir, "channel_hopper_commands.json"))
        squad_team_list_json_dir = os.path.normpath(os.path.join(json_dir, "squad_team_list.json"))
        squad_message_id_json_dir = os.path.normpath(os.path.join(json_dir, "squad_message_id.json"))




    class log:
        bot_path = os.path.abspath(sys.argv[0])
        bot_folder = os.path.dirname(bot_path)
        config_dir = os.path.normpath(os.path.join(bot_folder, "config"))
        log_dir = os.path.normpath(os.path.join(config_dir, "log"))


    # class img:
    #     bot_path = os.path.abspath(sys.argv[0])
    #     bot_folder = os.path.dirname(bot_path)
    #     config_dir = os.path.normpath(os.path.join(bot_folder, "config"))
    #     img_dir = os.path.normpath(os.path.join(config_dir, "img")) 