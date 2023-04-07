import os


# get the path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# construct the path to the config.ini file relative to the current directory
config_dir = os.path.join(current_dir, "config.ini")

print(config_dir)

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)