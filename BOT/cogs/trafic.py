from datetime import datetime

import discord
from discord.ext import commands
from utils import database as DBManager


class trafic(commands.Cog):

    def __init__(self, client) -> None:
        self.client: discord.Client = client


    @commands.Cog.listener(name="on_member_join")
    async def on_member_join(self, member: discord.Member) -> None:
        
        # Connection to the database
        connection = DBManager.connect_to_database(member.guild)

        date = datetime.now().strftime("%Y-%m-%d")

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Trafic WHERE date = ? AND guild = ?", (date,member.guild.id,))
        result = cursor.fetchone()
        if(result == None):
            cursor.execute("INSERT INTO Trafic (guild, new, leave) VALUES (?,?,?)", (member.guild.id, 1, 0,))
        else:
            cursor.execute("UPDATE Trafic SET new = new + 1 WHERE date = ? AND guild = ?", (date, member.guild.id,))
        connection.commit()
        connection.close()



    @commands.Cog.listener(name="on_member_remove")
    async def on_member_remove(self, member: discord.Member) -> None:
        
        # Connection to the database
        connection = DBManager.connect_to_database(member.guild)

        date = datetime.now().strftime("%Y-%m-%d")

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Trafic WHERE date = ? AND guild = ?", (date,member.guild.id,))
        result = cursor.fetchone()
        if(result == None):
            cursor.execute("INSERT INTO Trafic (guild, new, leave) VALUES (?,?,?)", (member.guild.id, 0, 1,))
        else:
            cursor.execute("UPDATE Trafic SET leave = leave + 1 WHERE date = ? AND guild = ?", (date, member.guild.id,))
        connection.commit()
        connection.close()




def setup(client: discord.Client) -> None:
    client.add_cog(trafic(client))
