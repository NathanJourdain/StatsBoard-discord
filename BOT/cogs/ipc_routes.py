import discord
from discord.ext import commands, ipc


class IpcRoutes(commands.Cog):
    def __init__(self, client: discord.Client):
        self.client: discord.Client = client

    @ipc.server.route()
    async def in_guild(self, guild_id: int):
        guild = await self.client.fetch_guild(guild_id)
        return '1'


def setup(client: discord.Client):
    client.add_cog(IpcRoutes(client))