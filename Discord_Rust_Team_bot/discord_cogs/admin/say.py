""""
------------------------------------------------
Send a Embed
------------------------------------------------
A send ebmbed to channel for the discord admin.
------------------------------------------------
Full Doku on: https://github.com/NapoII/
"""

from discord.app_commands import Choice
import discord
from util.__funktion__ import *


import os
import sys
import discord


# Get the current directory of the script file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the absolute path of the script itself
bot_path = os.path.abspath(sys.argv[0])

# Get the directory containing the script
bot_folder = os.path.dirname(bot_path)

# Construct the path to the config.ini file relative to the current directory
config_dir = os.path.join(bot_folder, "config", "config.ini")

# Read the guild_id from the config.ini file
guild_id = int(read_config(config_dir, "client", "guild_id"))

# Create a discord Object representing the guild using the obtained guild_id
guild = discord.Object(id=guild_id)

class bot_say(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        """
        Constructor for the BotSay cog.

        Parameters:
        - bot (commands.Bot): The Discord bot instance.
        """
        self.bot = bot

    @app_commands.command(name="say", description="Sends an embed to a destination channel")
    async def Bot_send_modal(self, interaction: discord.Integration):
        """
        Sends a modal input to the user.

        Parameters:
        - ctx (commands.Context): The context of the command.

        Returns:
        - None
        """
        await interaction.response.send_modal(modal_input_say())


class modal_input_say(ui.Modal, title="/say"):
    """
    Custom modal input class for sending an embed to a specified channel.

    Attributes:
    - say_channel_id (ui.TextInput): Input for specifying the Channel ID where the embed will be sent.
    - say_title (ui.TextInput): Input for the title of the embed.
    - say_text (ui.TextInput): Input for the text content of the embed.
    """

    say_channel_id = ui.TextInput(
        label="Channel ID in which to send:",
        style=discord.TextStyle.short,
        placeholder="Channel ID",
        required=True,
        max_length=None)
    
    say_title = ui.TextInput(
        label="Embed Titel:",
        style=discord.TextStyle.short,
        placeholder="Embed title",
        required=True, max_length=None)
    
    say_text = ui.TextInput(
        label="Embed Text:",
        style=discord.TextStyle.long,
        placeholder="Text",
        required=True,
        max_length=None)

    #print("Send modal_input_say: say_channel_id | say_title | say_text")
    async def on_submit(self, interaction: discord.Interaction):
        """
        Callback method triggered when the user submits the modal form.

        Parameters:
        - interaction (discord.Interaction): The Discord interaction object.

        Returns:
        - None
        """

        guild = interaction.guild
        embed = discord.Embed(title=" ", color=0xffffff)
        embed.set_author(name=guild)
        embed.add_field(name=self.say_title, value=self.say_text, inline=True)

        view = Confirm_say()
        await interaction.response.send_message(embed=embed, ephemeral=False, view=view)

        print(f"Output modal_input_say: say_channel_id={self.say_channel_id} | say_title={self.say_title} | say_text={self.say_text}")
        print(f"Send Confrim / Cancel abfrage.")

        print("Send Discordembed: Test Result")
        await view.wait()
        if view.value is None:
            self.confirm_Button = False
            print(f'Timed out... self.confirm_Button = {self.confirm_Button}')
            # return self.confirm_Button, self.say_channel_id, self.say_title, self.say_text

        elif view.value:
            self.confirm_Button = True

            print(f'Confirmed... self.confirm_Button = {self.confirm_Button}')
            # return self.confirm_Button, self.say_channel_id, self.say_title, self.say_text

            embed = discord.Embed(title=" ", color=0xffffff)
            embed.set_author(name=guild)
            embed.add_field(name=self.say_title,
                            value=self.say_text, inline=True)
            say_channel_id = int(str((self.say_channel_id)))
            Channel = interaction.client.get_channel(say_channel_id)
            await Channel.send(embed=embed)

        else:
            self.confirm_Button = False
            print(f'Cancelled... self.confirm_Button = {self.confirm_Button}')
            # return self.confirm_Button, self.say_channel_id, self.say_title, self.say_text

# Confirm buttons


class Confirm_say(discord.ui.View):
    """
    Custom view class for confirming or cancelling an action.

    Attributes:
    - value (bool): Represents the confirmation status. True if confirmed, False if cancelled.
    """
    def __init__(self):
        """
        Constructor for ConfirmSay class.

        Parameters:
        - None
        """
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button, ):
        """
        Constructor for ConfirmSay class.

        Parameters:
        - None
        """
        await interaction.response.send_message('Confirming', ephemeral=True)
        print(f"Send Confrim / Cancel abfrage.")

        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        Constructor for ConfirmSay class.

        Parameters:
        - None
        """
        await interaction.response.send_message('Cancelling', ephemeral=True)
        self.value = False
        self.stop()


async def setup(bot: commands.Bot):
    """
    Setup function for adding the bot_say cog to the Discord bot.

    Parameters:
    - bot (commands.Bot): The Discord bot instance.

    Returns:
    - None
    """
    await bot.add_cog(bot_say(bot), guild=discord.Object(guild_id))
