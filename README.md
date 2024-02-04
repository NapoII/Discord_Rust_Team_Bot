attention some API have an update and the bot have a big bug now I will fix it in the next few days, if you do not use it, write me, I give you the dev version SORRY give me time and this bot is on the status of sterioids !!!
for now just use the brench https://github.com/NapoII/Discord_Rust_Team_Bot/tree/ryyott
- 04.02.2024

[![github/NapoII](https://raw.githubusercontent.com/NapoII/Discord_Rust_Team_bot/main/README_img/Readme_top.png)](https://github.com/NapoII)

# Discord_Rust_Team_bot

[![downloads/total](https://img.shields.io/github/downloads/NapoII/Discord_Rust_Team_bot/total)](https://github.com/NapoII/Discord_Rust_Team_bot/archive/refs/heads/main.zip) [![github/repo-size](https://img.shields.io/github/repo-size/NapoII/Discord_Rust_Team_bot)](https://github.com/NapoII/Discord_Rust_Team_bot/archive/refs/heads/main.zip) [![github/license](https://img.shields.io/github/license/NapoII/Discord_Rust_Team_bot)](https://github.com/NapoII/Discord_Rust_Team_bot/blob/main/LICENSE) [![github/last-commit](https://img.shields.io/github/downloads/NapoII/Discord_Rust_Team_bot/total)](https://img.shields.io/github/issues/NapoII/Discord_Rust_Team_bot?style=plastic) [![github/issues_open](https://img.shields.io/github/issues/NapoII/Discord_Rust_Team_bot?style=plastic)](https://img.shields.io/github/issues-raw/NapoII/Discord_Rust_Team_bot) [![github/stars](https://img.shields.io/github/stars/NapoII/Discord_Rust_Team_bot?style=social)](https://github.com/NapoII/Discord_Rust_Team_bot/stargazers) [![discord](https://img.shields.io/discord/190307701169979393)](https://discord.gg/knTKtKVfnr)

 A Discord bot that offers assistance for the game Rust. The bot can check if certain players are online on a server and display how many players are currently online. It can be hosted on a server and used by players to enhance their gaming experience. This code can be shared on GitHub to allow other Rust players to use and contribute to the bot's development. 

## 📝 Table of Contents
- [Discord\_Rust\_Team\_bot](#discord_rust_team_bot)
  - [📝 Table of Contents](#-table-of-contents)
  - [🎥 Demo / Working ](#-demo--working-)
    - [Create Channel Structure ](#create-channel-structure-)
    - [Rust help Commands ](#rust-help-commands-)
    - [Server-Status ](#server-status-)
    - [Player Watch List ](#player-watch-list-)
    - [Cheak if more Teammates ](#cheak-if-more-teammates-)
  - [💻 Install ](#-install-)
  - [💭 How it works ](#-how-it-works-)
  - [📚 Lizenz ](#-lizenz-)

Cheak if more Teammates <a name = "Team_cheak"
## 🎥 Demo / Working <a name = "demo"></a>

### Create Channel Structure <a name = "Structure"></a>
The bot automatically creates the required channels when it is first started so that you can get started straight away.

![First Start](https://raw.githubusercontent.com/NapoII/Discord_Rust_Team_Bot/main/README_img/auto_channel_gen.gif)

To keep the Discord Rust area as clear as possible, only as many voice channels as necessary are automatically created and deleted again.

![First Start](https://raw.githubusercontent.com/NapoII/Discord_Rust_Team_Bot/main/README_img/voice_channel_create_auto.gif)

### Rust help Commands <a name = "!rust"></a>

Various small helper tools are included

![!rust help](https://raw.githubusercontent.com/NapoII/Discord_Rust_Team_Bot/main/README_img/rust_help_list.png)

e.g. you can calculate how much you get from x diesel and how much of it you can craft for raiding.

![!rust diesel](https://raw.githubusercontent.com/NapoII/Discord_Rust_Team_Bot/main/README_img/rust_diesel.gif)

and additional standard information

![ghelp_embed](https://raw.githubusercontent.com/NapoII/Discord_Rust_Team_bot/main/README_img/rust-help_embed.png)


### Server-Status <a name = "server"></a>

The number of players of the specific server are displayed

![server_status_channel_name](https://raw.githubusercontent.com/NapoII/Discord_Rust_Team_Bot/main/README_img/server_status_channel_name.png)
![Online_Status](https://raw.githubusercontent.com/NapoII/Discord_Rust_Team_bot/main/README_img/Online_Status.png)

Additional information about the server such as ip, map website, etc. is displayed.

![Server_status](https://raw.githubusercontent.com/NapoII/Discord_Rust_Team_bot/main/README_img/Server_status.png)


### Player Watch List <a name = "Player_Watch_List"></a>
You can monitor certain players to see how long they are on the server, etc.

![player_status](https://raw.githubusercontent.com/NapoII/Discord_Rust_Team_Bot/main/README_img/player_status.png)

Or get notified if a certain group of players goes online or offline from the server.

![player_status_sub](https://raw.githubusercontent.com/NapoII/Discord_Rust_Team_Bot/main/README_img/sub.gif)

### Cheak if more Teammates <a name = "Team_cheak"></a>
You can use a steam ID or steam profile page url to see if any of his team mates are playing on the server.

![player_status_sub](https://raw.githubusercontent.com/NapoII/Discord_Rust_Team_Bot/main/README_img/teack_check.gif)



## 💻 Install <a name = "usage"></a>

1. Clone or download the Bot Package and install the required requirements.
    ```cmd
    git clone https://github.com/NapoII/Discord_Rust_Team_bot
    pip install -r requirements.txt
    ```

2. Enter your Discord Bot token and application_id in the token.ini             `Discord_Rust_Team_bot\cfg\token.ini`
    https://discord.com/developers/applications/

3. Add the server_id to the config.ini file 
   `Discord_Rust_Team_bot\cfg\config.ini`
   
    ![server_id](https://raw.githubusercontent.com/NapoII/Discord_Rust_Team_Bot/main/README_img/Server_id.gif)
    
    You can ingonir the other settings for now. The bot will change them on its own

4. Don't forget to let join your own Discord-bot to your Discord
5. 
    ![bot](https://raw.githubusercontent.com/NapoII/Discord_Rust_Team_Bot/main/README_img/bot.gif)

5. Start the py bot for the first time and wait until it has created all channels and roles. (to avoid errors you can start the .py in admin mode) 
    `Discord_Rust_Team_bot\Discord_Rust_Team_bot.py`

6. Restart the py Bot now to start its normal routine

7. change the server ID. Type `/change_server` in your Discord.
    You take the ID from battlemetrics: https://www.battlemetrics.com/servers/search
    
    ![bot](https://raw.githubusercontent.com/NapoII/Discord_Rust_Team_Bot/main/README_img/server_id_first.gif)
    
8. ☕Now that the bot is ready for use, treat yourself to a cup of tea.☕


## 💭 How it works <a name = "Use"></a>
- `!help` - list all commmands
- `!rust help` - list all Rust info help tools
- `/change_server`- Use Battlemetrics.com to determine the server ID and /change_server register.

- `/add_player` - Use Battlemetrics.com to find out the player ID. Add a note to the player. Now, if necessary, create a new team or assign it to the new player in an existing team via the menu..
- `/delt_player` - Selecting a player from the list to remove him/her.
- `/delt_team` - Select team from the list to remove it."
- `/clear_watchlist`\nAttention removes all players and all teams irrevocably."
- `/team_check` - Checks a player for possible team members on the server using their steam ID or URL.


## 📚 Lizenz <a name = "Lizenz"></a>
MIT License

Copyright (c) 2023 NapoII
<small><small><small>
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE
    
<p align="center">
<img src="https://raw.githubusercontent.com/NapoII/NapoII/233630a814f7979f575c7f764dbf1f4804b05332/Bottom.svg" alt="Github Stats" />
</p>
