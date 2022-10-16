

from discord.app_commands import Choice
from Imports import*

guild_id = int(read_config(config_dir, "Client", "guild_id"))
guild = discord.Object(id=guild_id)

class bot_say(commands.Cog):
    def __init__(self, bot:commands.Bot)-> None:
        self.bot = bot

    @app_commands.command(name = "say", description="Sendet ein Embed in ein Ziel Channel")

    async def Bot_Test(
        self,
        interaction: discord.Integration):
        await interaction.response.send_modal(modal_input_say())

class modal_input_say(ui.Modal, title="/say"):

    say_channel_id = ui.TextInput(label ="Channel ID in der gesendet werden soll:", style = discord.TextStyle.short, placeholder="Channel ID", default="1012397680808443954", required=True, max_length=None)
    say_title = ui.TextInput(label ="Embed Titel:", style = discord.TextStyle.short, default="default text 1", placeholder="Embed Titel", required=True, max_length=None)
    say_text = ui.TextInput(label ="Embed Text:", style = discord.TextStyle.long, default="default text 2", placeholder="Text", required=True, max_length=None)
    
    #log("Send modal_input_say: say_channel_id | say_title | say_text")
    async def on_submit(self, interaction: discord.Interaction ):
        guild = interaction.guild
        embed=discord.Embed(title=" ", color=0xffffff)
        embed.set_author(name=guild)
        embed.add_field(name=self.say_title, value=self.say_text, inline=True)

        view = Confirm_say()
        await interaction.response.send_message(embed=embed, ephemeral=False, view=view)
        
        log(f"Output modal_input_say: say_channel_id={self.say_channel_id} | say_title={self.say_title} | say_text={self.say_text}")
        log (f"Send Confrim / Cancel abfrage.")


        log("Send Discordembed: Test Result")
        await view.wait()
        if view.value is None:
            self.confirm_Button = False
            log(f'Timed out... self.confirm_Button = {self.confirm_Button}')
            #return self.confirm_Button, self.say_channel_id, self.say_title, self.say_text

        elif view.value:
            self.confirm_Button = True

            log(f'Confirmed... self.confirm_Button = {self.confirm_Button}')
            #return self.confirm_Button, self.say_channel_id, self.say_title, self.say_text

            embed=discord.Embed(title=" ", color=0xffffff)
            embed.set_author(name=guild)
            embed.add_field(name= self.say_title, value=self.say_text, inline=True)
            say_channel_id = int(str((self.say_channel_id)))
            Channel = interaction.client.get_channel(say_channel_id)
            await Channel.send(embed=embed)
        
        else:
            self.confirm_Button = False
            log(f'Cancelled... self.confirm_Button = {self.confirm_Button}')
            #return self.confirm_Button, self.say_channel_id, self.say_title, self.say_text

### Confirm buttons
class Confirm_say(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button, ):
        await interaction.response.send_message('Confirming', ephemeral=True)
        log(f"Send Confrim / Cancel abfrage.")


        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Cancelling', ephemeral=True)
        self.value = False
        self.stop()





async def setup(bot: commands.Bot):
    await bot.add_cog(bot_say(bot), guild=discord.Object(guild_id))