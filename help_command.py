

from Imports import*
from discord.ui import Select
from discord.ui import View

guild_id = int(read_config(config_dir, "Client", "guild_id"))
guild = discord.Object(id=guild_id)


class help(commands.Cog, ):


    def __init__(self, bot:commands.Bot,)-> None:
        self.bot = bot

    @app_commands.command(name = "help", description="Fragen zum Discord Bot")

    



    async def help_list(self,
    interaction: discord.Interaction,):
        options =[]
        options.append(discord.SelectOption(label=f"Rust", description="Alles Infos zu den Rust-Botcommands"))
        select  = Select(options = options)


        async def my_callback(interaction: discord.Interaction):

            auswahl = select.values[0]

            if auswahl == "Rust":
                embed=discord.Embed(title="Help / Rust Bot", description="Auflistung von allen Comands", color=0x8080ff)
                embed.set_thumbnail(url="https://i.imgur.com/Twekn9L.png")

                text_serveraendern = f"`/change_server`\nMit Battlemetrics.com Server ID ermitteln und mit /change_server eintragen."
                text_addplayer = f"`/add_player`\nMit Battlemetrics.com Spieler ID ermitteln und mit /change_server eintragen. Zusätzlich eine Notiz dem Spieler hinzufügen. Nun bei Bedarf ein neues Team erstellen, oder in einem bestehenden Team über das Menü dem neuen Spieler zuteilen."
                text_deltplayer = f"`/delt_player`\nSpieler aus der Liste auswählen, um ihn zu entfernen."
                text_deltteam = f"`/delt_team`\nTeam aus der Liste auswählen, um es zu entfernen."
                text_clear = f"`/clear_watchlist`\n Achtung entfernt alle Spieler und alle Teams unwiderruflich."

                embed.add_field(name="Rust Server ändern", value=text_serveraendern, inline=False)
                embed.add_field(name="Neuen Spieler anlegen", value=text_addplayer, inline=False)
                embed.add_field(name="Spieler entfernen", value=text_deltplayer, inline=False)
                embed.add_field(name="Team entfernen", value=text_deltteam, inline=False)
                embed.add_field(name="Watchlist leeren", value=text_clear, inline=False)
                await interaction.response.edit_message(embed=embed)



            
  


        select.callback = my_callback
        view = View()
        view.add_item(select)
        embed=discord.Embed(title="Spieler löschen", description="Wähle einen Spieler aus!", color=0xff8040)
        await interaction.response.send_message(embed=embed, ephemeral=True, view=view)












async def setup(bot: commands.Bot):
    await bot.add_cog(help(bot), guild=discord.Object(guild_id))

