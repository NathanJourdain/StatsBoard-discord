from datetime import datetime

import discord
from discord.ext import commands
from utils import database as DBManager


class reaction(commands.Cog):

    def __init__(self, client) -> None:
        self.client: discord.Client = client


    @commands.Cog.listener(name="on_raw_reaction_add")
    async def on_raw_reaction_add(self, playload: discord.RawReactionActionEvent) -> None:
        
        # Connection to the database
        connection = DBManager.connect_to_database(self.client.get_guild(playload.guild_id))

        date = datetime.now().strftime("%Y-%m-%d")

        cursor = connection.cursor()
        cursor.execute("SELECT 1 FROM Reactions WHERE date = ? AND guild = ?", (date, playload.guild_id,))
        result = cursor.fetchone()
        if(result is None):
            cursor.execute("INSERT INTO Reactions (guild, reactions_add, reactions_remove) VALUES (?, ?, ?)", (playload.guild_id, 1, 0,))
        else:
            cursor.execute("UPDATE Reactions SET reactions_add = reactions_add + 1 WHERE date = ? AND guild = ?", (date, playload.guild_id,))
        connection.commit()
        connection.close()

    @commands.Cog.listener(name="on_raw_reaction_remove")
    async def on_raw_reaction_remove(self, playload: discord.RawReactionActionEvent) -> None:
        
        # Connection to the database
        connection = DBManager.connect_to_database(self.client.get_guild(playload.guild_id))

        date = datetime.now().strftime("%Y-%m-%d")

        cursor = connection.cursor()
        cursor.execute("SELECT 1 FROM Reactions WHERE date = ? AND guild = ?", (date, playload.guild_id,))
        result = cursor.fetchone()
        if(result is None):
            cursor.execute("INSERT INTO Reactions (guild, reactions_add, reactions_remove) VALUES (?, ?, ?)", (playload.guild_id, 0, 1,))
        else:
            cursor.execute("UPDATE Reactions SET reactions_remove = reactions_remove + 1 WHERE date = ? AND guild = ?", (date, playload.guild_id,))
        connection.commit()
        connection.close()




def setup(client: discord.Client) -> None:
    client.add_cog(reaction(client))
