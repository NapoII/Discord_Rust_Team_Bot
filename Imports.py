py_name = "Discord_Bot_Napo_III_2.1"
v = "0.0.1"
f0I = """
              .#:                                 
             .#MM:                                
            .#MMMM:                ,+%%+          
            %MMMMMM:            .+@MMMMM.         
           +MMMMMMMM:          ,@MMMMMM:          
          ,MMMMMMMMMM:        ,MMMMMMM:           
          %MMMMMMMMMMM:      .@MMMMMM:            
         :@MMMMMMMMMMM@      #MMMMMM:             
        %MMMMMMMMMMMM@.     ,MMMMMM:              
       %MMMMMMMMMMMM@.      #MMMMM#               
      :MMMMMMMMMMMM@.      .MMMMMMM.          ,+  
      #MMMMMMMMMMM#.       ,MMMMMMM:         :MM. 
     :MMMMMMMMMM#:         ,MMMMMMM%        :MMM. 
    .MMMMMMMMMM@.          ,MMMMMMM@       :MMMM. 
    #MMMMMMMMMMM@.         ,MMMMMMMM:.    :MMMM@  
   ,MMMMMMMMMMMMM@.        .MMMMMMMMMM@%::MMMMM%  
   %MMMMMMMMMMMMMM@.        #MMMMMMMMMMMMMMMMMM,  
  .MMMMMM@+,MMMMMMM@.      :MMMMMMMMMMMMMMMMMM#   
  ,MMMMM%.  ,MMMMMMM@.    +MMMMMMMMMMMMMMMMMM@.   
  +MMMM+     ,MMMMMMM@.  +MMMMMMMMMMMMMMMMMMM,    
  %MMM%       ,MMMMMMM@.+MMMMMMMMMMMMMMMMMM@,     
  %MMM.        ,MMMMMMMMMMMMMMMMMMMMMMMMMM%.      
  %MM+          ,MMMMMMMMMMMMMMMM+:%###%:.        
  +MM,           ,MMMMMMMMMMMMMM+                 
  ,MM             ,MMMMMMMMMMMM+                  
   @#             .#MMMMMMMMMM#                   
   ..            .#MMMMMMMMMMMM+                  
                .#MMMMMMMMMMMMMM+                 
               .#MMMMMMMMMMMMMMMM+                
              .#MMMMMMMMMMMMMMMMMM+               
             .@MMMMMMMMMMMMMMMMMMMM+              
            .@MMMMMMMMMMMMMMMMMMMMMM+             
           .@MMMMMMMMMM@%MMMMMMMMMMMM+            
          ,@MMMMMMMMMM@. %MMMMMMMMMMMM+           
         ,@MMMMMMMMMM@.   %MMMMMMMMMMMM+          
        ,@MMMMMMMMMM@,     %MMMMMMMMMMMM+         
       ,MMMMMMMMMMM@,       %MMMMMMMMMMMM+        
      ,MMMMMMMMMMMM,         %MMMMMMMMMMMM+       
     :MMMMMMMMMMMM,           %MMMMMMMMMMMM+      
    :MMMMMMMMMMMM:             %MMMMMMMMMMMM+     
   :MMMMMMMMMMMM:               %MMMMMMMMMMMM+    
  ,MMMMMMMMMMMM:                 %MMMMMMMMMMMM+   
  @MM#+@MMMMMM+                   %MMMMMMMMMMMM:  
 ,MM%  .MMMMM+                     %MMMMMMMMMMMM. 
 :MM+   @MMM+                       %MMMMMMMMMMM: 
 :MM#. ,MMM%                         %MMMMMMMMMM: 
 .MMM@#MMM%                           %MMMMMMMMM, 
  +MMMMMM%                             %MMMMMMM@. 
   :@MM@:                               %MMMMMM,  
     ,.                                  :#M@%,
   


- Imports
- created by Napo_II
- """ + v + """
- python 3.10.7
- https://github.com/NapoII/

"""
####################################################################################################
#import

import os
import os, sys
import time
import pyautogui
from configparser import ConfigParser
import urllib
import datetime

from discord.ext import commands
import discord
from discord import ui, app_commands
from datetime import datetime
import json
import requests
####################################################################################################
#def

def Folder_gen(Folder_Name, Folder_dir ):
   print("Ordner Struktur wird überprüft und ggf. angelegt...\n")
   folder = Folder_Name
   dir = "~/"+str(Folder_dir)+"/"+str(folder)           # gibt gewünschten Datei-Pfad an
   full_path = os.path.expanduser(dir)                 # ergänzt datei pfad mit PC User name
   if os.path.exists(full_path):                       # Prüft datei pfad nach exsistänz Ture/False
      print("Ordner Struktur existiert bereits")
      print("  ->   " + str(full_path))
   else:                                               # Erstellt Ordner falls nicht vorhadnen
      os.makedirs(full_path)
      print("Der Ordner ["+folder+"] wurde erstellt im Verzeichnis:" )
      print("  ->   " + str(full_path))
   print("\n")
   return(full_path)

def Folder_gen_all(Folder_Name, Folder_dir ):
   print("Ordner Struktur wird überprüft und ggf. angelegt...\n")
   folder = Folder_Name
   if os.path.exists(Folder_dir):                       # Prüft datei pfad nach exsistänz Ture/False
      print("Ordner Struktur existiert bereits")
      print("  ->   " + str(Folder_dir))
   else:                                               # Erstellt Ordner falls nicht vorhadnen
      os.makedirs(Folder_dir)
      print("Der Ordner ["+folder+"] wurde erstellt im Verzeichnis:" )
      print("  ->   " + str(Folder_dir))
   print("\n")
   return(Folder_dir)

def Datei_name_mit_Zeit(FileName):
    Date = Date_Time=(time.strftime("%d_%m-%Y-%H.%M"))        # Generiert date formater
    FullName = (FileName+"-"+(Date))                           # Generiert Datei name
    return FullName

def Erstelle_TextDatei( Text_File_name, save_path, Inhalt ):
    complete_Path_Text = os.path.join(save_path+"\\"+Text_File_name+".txt")     # Path + text datei name
    if os.path.exists(complete_Path_Text):
        return complete_Path_Text
    else:
        print("\nTextdatei ["+str(Text_File_name)+".txt] wird erstellt...")
        file1 = open(complete_Path_Text, "w")                                         # Datei erstellen
        #toFile = input("Write what you want into the field")                   # Datei input def.
        file1.write(Inhalt)                                                    # Datei wird gefüllt mit input
        file1.close()
        return complete_Path_Text

def Fill_Datei(dir, toFill, Attribut):
    file1 = open(dir, Attribut,encoding="utf-8")                                 # Datei wird geöffnet
    #print("Datei ["+str(dir) + "] wird beschrieben und gespeichtert...\n")
    file1.write(toFill)                                             # Datei wird gefüllt mit input
    file1.close()

def Read_Datei(dir, Attribut):
    file1 = open(dir, Attribut,encoding="utf-8")
    context = (file1.read())                         # Datei wird geöffnet
    #print("Datei ["+str(dir) + "] wird geöffnet ...\n")                                            # Datei wird gefüllt mit input
    file1.close()
    return context


def TimeStemp():
    TimeStemp = Date_Time=(time.strftime("%d_%m-%Y_%H:%M:%S"))
    return TimeStemp

def log(Log_input):
    Fill_Datei(Log_File, TimeStemp()+" --> " + Log_input+"\n", "a")
    print (TimeStemp()+" --> " + Log_input+"\n")

def Zeit_pause(seconds):
    start_time = time.time()
    while True:                             # Zeit schelife startet
        current_time = time.time()
        elapsed_time = current_time - start_time        # berechung rest Zeit
        if elapsed_time > seconds:
            break

def read_config(config_dir, section, option):
    config = ConfigParser()
    config.read(config_dir)
    load_config = (config[section][option])

    print("Config geladen: [ "+(option) +" = "+ (load_config)+" ]")

    return load_config

def write_config(config_dir, section, Key, option):

    config = ConfigParser()
    # update existing value
    config.read(config_dir)
    try:
        config.add_section(section)
    except:
        pass
    config.set(section, Key,option) #Updating existing entry 
    with open(config_dir, 'w') as configfile:
        config.write(configfile)
    print ("\nEinstellungs änderung -> "+str(config_dir)+"\n"+"["+str(section)+"]\n"+str(Key)+" = " + str(option)+"\n")

def Download_from_link(link, dir):
    link = "https://i.imgur.com/Mk1KPNa.png"
    dir = "E://Pr0grame//My_ Pyhton//work_in_progress//Discord-Ticket-Bot//Bilder//Test.png"
    urllib.request.urlretrieve(link, dir)
    log ("Img download [" +link + "] und gespeichert in [ "+dir+ " ]")
    return dir

def parse_int_tuple(input):
    return tuple(int(k.strip()) for k in input[1:-1].split(','))

def parse_tuple(input):
    return tuple(k.strip() for k in input[1:-1].split(','))

def str_to_bool(input):
    if input == "True":
        input = True
    else:
        input = False
    return input

################################################################################################################################
#PreSet Programm

file_path = os.path.dirname(sys.argv[0])
file_path_Bilder = file_path + "/Bilder/"
file_path_Work_Folder = file_path + "/Work_Folder/"
config_dir = file_path +"/config.ini"

Doku_Folder = Folder_gen (py_name, "Documents/")
Log_Folder = Folder_gen ("Log", ("Documents/"+str(py_name)))
Log_File_name = Datei_name_mit_Zeit ("LogFile-"+str(py_name))
Log_File = Erstelle_TextDatei (Log_File_name, Log_Folder, f0I + "Log-File:\n---------------------------------------------------------------------------------------\n")

Bot_Path = os.path.dirname(sys.argv[0])
log ( "Bot_Path: ["+str(Bot_Path) + "]\n")


################################################################################################################################
log ("Imports geladen : [" +str(file_path) + "/Imports.py]")
################################################################################################################################
#def spez.
import discord

def Discord_Activity(Text): # Bot aktivitäten Text
    #Activity = discord.Client(activity=discord.Game(name='my game'))
    Activity = discord.Activity(name=Text, type=discord.ActivityType.watching)
    return Activity

def discord_time_convert(time):
    discord_time = (f"<t:{time}:R>")
    return discord_time

import datetime
def ISO_Time_to_Milisec(time_str):
    date = datetime.datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    timestamp = str((date - datetime.datetime(1970, 1, 1)).total_seconds())
    return (timestamp[:10])

def Team_choice(Team_data_fiel_dir):
    #Team_data_fiel_dir = f"E:\Pr0grame\My_ Pyhton\work_in_progress\Discord_Bot_Napo_III_2.1\Work_Folder\Rust\Team_data.json"

    team_file = Read_Datei(Team_data_fiel_dir, "r")
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
    dict["Teams"][f"{team}"][f"{name}"] = {"ID":f"{id}","note":f"{note}"}
    return dict

def delt_player (dict, Team, Player):
    dict["Teams"][f"{Team}"].pop(f"{Player}")
    return dict

def add_Team(dict, team, note, embed_id):
    dict["Teams"].update ({F"{team}":{}})
    dict["Teams"][F"{team}"].update({"note":f"{note}"})
    dict["Teams"][F"{team}"].update({"embed_id":f"{embed_id}"})
    dict.update
    return dict

def delt_Team (dict, Team):

    dict[f"Teams"].pop(f"{Team}")
    return dict

def open_JSOn_File(Json_fiel_dir):
    f = open(Json_fiel_dir)
    dict = json.load(f)
    json_object = json.dumps(dict, indent = 2)
    f.close()
    return dict

def Fill_JSOn_File(dir, dictionary):
    file1 = open(dir, "w",encoding="utf-8")                                 # Datei wird geöffnet
    print("Datei ["+str(dir) + "] wird beschrieben und gespeichtert...\n")
    json_object = json.dumps(dictionary, indent = 4) 
    file1.write(json_object)                                             # Datei wird gefüllt mit input
    file1.close()

def create_and_fill_temp_bridge(toFill ,dir):
    file1 = open(dir, "a",encoding="utf-8")                                 # Datei wird geöffnet
    log("Temp_Datei ["+str(dir) + "] wird beschrieben und gespeichtert...\n")
    file1.write(str(toFill))                                             # Datei wird gefüllt mit input
    file1.close()
    return toFill

def read_and_delt_temp_bridge(dir):
    file1 = open(dir,"r" ,encoding="utf-8")
    context = (file1.read())                         # Datei wird geöffnet
    log("Datei ["+str(dir) + "] wird geöffnet ...\n")                                            # Datei wird gefüllt mit input
    file1.close()
    try:
        os.remove(dir)
    except OSError as e:
        log(e)
    else:
        log("Temp_Datei ["+str(dir) + "] wurde gelöscht...\n")
    return context

def get_all_embed_IDs(JSOn_data):
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

    return Team_Player_list

def Team_online_status(JSOn_data, Team_Name, servers_id):
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
            try:
                online = json_data["data"]["attributes"]["online"]
                if online == True:
                    return True
            except:
                online = json_data["errors"][0]["status"]
        return online

def Player_name_cange(JSOn_data, Team_Name, Player):

            Player_id = JSOn_data["Teams"][Team_Name][Player]["ID"]
            Player_Server_url = f"https://api.battlemetrics.com/players/{Player_id}"
            response = requests.get(Player_Server_url)
            json_data = response.json()
            New_name = json_data["data"]["attributes"]["name"]
            if Player == New_name:
                return False, New_name
            else:
                return True

def Player_Server_info(Player_id, servers_id):

            Player_Server_url = f"https://api.battlemetrics.com/players/{Player_id}/servers/{servers_id}"
            response = requests.get(Player_Server_url)
            json_data = response.json()
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

                return Online_ico, lastSeen, timePlayed , Player_Server_url
            except:
                online = json_data["errors"][0]["status"]
                return str(online)

def Get_all_player_list(dict):
    Full_Player_list =[]
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

    url = f"https://api.battlemetrics.com/servers/{Server_ID}"
    response = requests.get(url)
    response_json = response.json()
    try:
        map_url = response_json["data"]["attributes"]["details"]["rust_maps"]["url"]
        thumbnailUrl = response_json["data"]["attributes"]["details"]["rust_maps"]["thumbnailUrl"]
        seed = response_json["data"]["attributes"]["details"]["rust_maps"]["seed"]
        size = response_json["data"]["attributes"]["details"]["rust_maps"]["size"]

        thumbnailUrl = thumbnailUrl[:thumbnailUrl.rfind("Thumbnail.png")]+str("FullLabeledMap.png")
        
        return thumbnailUrl, map_url , seed, size

    except:
        return False