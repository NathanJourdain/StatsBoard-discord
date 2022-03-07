import discord
from discord.ext import commands

from utils import database as DBManager

class join_guild(commands.Cog):

    def __init__(self, client) -> None:
        self.client: discord.Client = client


    @commands.Cog.listener(name="on_guild_join")
    async def on_guild_join(self, guild: discord.Guild):
        
        # Connection à la base de données
        self.connection = DBManager.connect_to_database(guild)




def setup(client: discord.Client) -> None:
    client.add_cog(join_guild(client))