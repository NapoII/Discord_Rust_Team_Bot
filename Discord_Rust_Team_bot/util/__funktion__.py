"""
----------------------------------------
__funktion__
----------------------------------------
Use: - from util.__funktion__ import *

ChatGPT promt for docstrgs:

In copy code mode,

write me a .py docstr ("""""") with the content:
Args, Returns and Example Usage.
For Args and Returns create a list with "- ".
and for Example Usage create a list with ">>>  ".
Here is the code:
----------------------------------------
Full Doku on: https://github.com/NapoII/
"""
# import
import json
import subprocess
import os
from configparser import ConfigParser
import shutil
import time
import sys
import requests
from datetime import datetime

from util.__Mydiscord_funktions__ import *

# Get the current directory of the script file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the absolute path of the script itself
bot_path = os.path.abspath(sys.argv[0])

# Get the directory containing the script
bot_folder = os.path.dirname(bot_path)

# Construct the path to the config.ini file relative to the current directory
config_dir = os.path.join(bot_folder, "config", "config.ini")


def new_path(base_path, *additional_paths):
    """
    Combines paths based on a base and optional additional paths.
    
    Args:
        base_path (str): The base path.
        *additional_paths (str): Any number of additional paths.
        
    Returns:
        str: The combined and normalised path.
    """
    # Normalise the base path
    base_path = os.path.normpath(base_path)
    
    # Add all additional paths and create the combined path
    combined_path = os.path.join(base_path, *additional_paths)
    
    # Normalise and return the combined path
    return os.path.normpath(combined_path)


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

    option = str(option)
    config = ConfigParser()
    # update existing value
    config.read(config_dir)
    try:
        config.add_section(section)
    except:
        pass
    config.set(section, Key, option) #Updating existing entry 
    with open(config_dir, 'w') as configfile:
        config.write(configfile)
    print (f"\nChange settings -> {config_dir}\n[{section}]\n{Key}) = {option}\n")



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
        print(f"The folder [{folder}] was created in the directory:\n  ->   {full_path}", "b")
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
        print(f"\nfile [{File_name}] is created...with conetnt: {Inhalt}")
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
        print(f"Image [{file}] successfully copied!", "b")
        return file
    except IOError as e:
        print(f"Error when copying the file: {e}", "r")


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
    Date = Date_Time=(time.strftime("%d_%m-%Y-%H.%M"))        # Generates date formater
    FullName = (FileName+"-"+(Date))                           # Generates file name
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
    TimeStemp = Date_Time=(time.strftime("%d_%m-%Y_%H:%M:%S"))
    return TimeStemp


def cheack_config(default_long_Str):
    """
    Generate a config file path in the 'config' directory of the current main file's directory.
    
    Args:
    - default_long_Str (str): A long string representing the default configuration
    
    Returns:
    - config_path (str): The absolute path to the generated config file
    
    Example Usage:
    >>> default_config = "This is the default configuration"
    >>> check_config(default_config)
    '/path/to/main_dir/config/config.ini'
    """
    main_file = sys.modules['__main__'].__file__
    main_dir = os.path.dirname(main_file)
    config_path =  Folder_gen("config", main_dir)
    config_path = Create_File("config.ini", config_path, default_long_Str)
    return config_path

if __name__ == "__funktion__":
    print("__function should not be executed when the file is imported as a module.\nThis was not the case!", "r")
else:
    cheack_config("""[Test]
    abc = 123""")




import os
import subprocess

def get_last_commit_info(folder_path="."):
    """
    Retrieve information about the last Git commit for a specified folder.

    Example:
    `git_last_commit, git_last_date, git_branch = get_last_commit_info()`

    Parameters:
    - folder_path (str): The relative path to the target folder. Default is the current directory.

    Returns:
    - tuple: A tuple containing the last Git commit comment, the commit date, and the current branch name.

    Raises:
    - subprocess.CalledProcessError: If the Git command execution fails.

    Notes:
    - This function uses the 'git log' command to retrieve the last commit information, including the comment,
      date, and branch.
    - If an error occurs during the Git command execution, the function falls back to the saved information
      in the configuration file or database.

    """

    try:
        # Get the absolute path of the parent directory
        current_directory = os.path.dirname(os.path.abspath(__file__))
        target_directory = os.path.join(current_directory, folder_path)

        # Git command to retrieve the last commit information (comment, date, and branch)
        git_command = "git log -1 --pretty=%B,%cd,%D"

        # Execute the Git command in the target directory and decode the output
        commit_info = subprocess.check_output(git_command, cwd=target_directory, shell=True, text=True)

        # Split the output into comment, date, and branch
        commit_comment, commit_date, commit_branch = commit_info.strip().split(",", 2)

        # Save the information to a configuration file or database if needed
        write_config(config_dir, "git", "last_git_comment", commit_comment)
        write_config(config_dir, "git", "last_git_commit_date", commit_date)
        write_config(config_dir, "git", "last_git_branch", commit_branch)

        return commit_comment.strip(), commit_date.strip(), commit_branch.strip()

    except subprocess.CalledProcessError:
        # If an error occurs, fallback to the saved information in the configuration file or database
        last_git_comment = read_config(config_dir, "git", "last_git_comment")
        last_git_commit_date = read_config(config_dir, "git", "last_git_commit_date")
        last_git_branch = read_config(config_dir, "git", "last_git_branch")

        return last_git_comment, last_git_commit_date, last_git_branch


def read_json_file(file_path):
    """
    Reads the contents of a JSON file and returns the resulting JSON object.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: The JSON object from the file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def fill_json_file(dir, dictionary):
    """
    Fill a JSON file with provided dictionary data.
    
    Args:
        dir (str): Directory path of the JSON file.
        dictionary (dict): Dictionary data to be written into the JSON file.
        
    Returns:
        None
    """
    # Open the JSON file in write mode
    with open(dir, 'w') as file:
        # Write dictionary data to the file with indentation for readability
        json.dump(dictionary, file, indent=4)


################################################################################################################################
#def spez.
def if_json_file_404(json_path, content):
    """
    Checks if the JSON file is not found (HTTP status code 404).

    :param json_path: The path to the JSON file.
    :param content: The content of the JSON file if it needs to be created.
    :return: The path to the JSON file.
    """
    if not os.path.exists(json_path):
        with open(json_path, 'w') as json_file:
            json.dump(content, json_file, indent=4)
    return json_path


def new_loop_num(file_path):
    try:
        # Open the file and read the current value
        with open(file_path, 'r') as file:
            content = file.readline().strip()
            if content:
                num = int(content)
                num += 1  # Increment the value by 1
            else:
                num = 1
    except FileNotFoundError:
        # If the file is not found, start with 1
        num = 1

    # Write the new value to the file
    with open(file_path, 'w') as file:
        file.write(str(num))

    return num


def decimal_separator(number):
    formatted_number = '{:,.0f}'.format(number)
    return formatted_number.replace(',', '.')

def delt_str_time(sec_to_delta):
    """
    ~~This mgs gets delt in 60 sec~~"

    """
    current_unix_time = int(time.time())
    delt_unix_time = discord_time_convert(current_unix_time + sec_to_delta)
    delt_msg_str = f"~~This mgs gets delt {delt_unix_time}~~"
    return delt_msg_str