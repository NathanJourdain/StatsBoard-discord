import discord
from discord.ext import commands
from utils import database as DBManager


class invite(commands.Cog):

    def __init__(self, client) -> None:
        self.client: discord.Client = client

    @commands.Cog.listener(name="on_member_join")
    async def on_member_join(self, member: discord.Member) -> None:
        # Connection to the database
        connection = DBManager.connect_to_database(member.guild)
        cursor = connection.cursor()
        
        invites = await member.guild.invites()
        for invite in invites:
            cursor.execute("SELECT 1 FROM Invitations WHERE code = ? AND guild = ?", (invite.code, member.guild.id,))
            result = cursor.fetchone()
            if(result is None):
                cursor.execute("INSERT INTO Invitations (guild, code, creator_id, usage) VALUES(?, ?, ?, ?)", (member.guild.id, invite.code, invite.inviter.id, invite.uses))
            else:
                cursor.execute("UPDATE Invitations SET usage = ? WHERE code = ? AND guild = ?", (invite.uses, invite.code, member.guild.id,))


        connection.commit()
        connection.close() 

def setup(client: discord.Client) -> None:
    client.add_cog(invite(client))
