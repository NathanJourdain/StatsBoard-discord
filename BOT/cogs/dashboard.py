import discord
from discord.ext import commands
from discord.ext.commands import has_permissions 
from discord_slash import SlashContext, cog_ext


class dashboard(commands.Cog):

    def __init__(self, client) -> None:
        self.client: discord.Client = client

    @cog_ext.cog_slash(name="dashboard", description="Get the link to the dashboard", guild_ids=[865708078820622358])
    @has_permissions(manage_guild=True)
    async def dashboard(self, ctx: SlashContext) -> None:
        embed = discord.Embed(title="Dashboard", color=self.client.color)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.description = f"**➥ [Click here to access the dashboard](http://127.0.0.1:1000/guilds/865708078820622358)**"


        await  ctx.send(embed=embed)

def setup(client: discord.Client) -> None:
    client.add_cog(dashboard(client))
