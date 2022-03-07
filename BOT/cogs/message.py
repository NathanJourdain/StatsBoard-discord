from datetime import datetime

import discord
from discord.ext import commands
from utils import database as DBManager


class message(commands.Cog):

    def __init__(self, client) -> None:
        self.client: discord.Client = client


    @commands.Cog.listener(name="on_message")
    async def on_message(self, message: discord.Message) -> None:
        
        # Connection to the database
        connection = DBManager.connect_to_database(message.guild)

        date = datetime.now().strftime("%Y-%m-%d")

        cursor = connection.cursor()
        cursor.execute("SELECT 1 FROM Messages WHERE date = ? AND guild = ?", (date, message.guild.id,))
        result = cursor.fetchone()
        if(result is None):
            cursor.execute("INSERT INTO Messages (guild, nb_messages) VALUES (?, ?)", (message.guild.id, 1))
        else:
            cursor.execute("UPDATE Messages SET  nb_messages = nb_messages + 1 WHERE date = ? AND guild = ?", (date, message.guild.id,))
        connection.commit()
        connection.close()





def setup(client: discord.Client) -> None:
    client.add_cog(message(client))
