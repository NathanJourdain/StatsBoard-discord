import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from utils import database as DBManager
from datetime import datetime



class infoGuild(commands.Cog):

    def __init__(self, client) -> None:
        self.client: discord.Client = client

    @cog_ext.cog_slash(name="info", description="Get information about the guild.", guild_ids=[865708078820622358])
    async def info_guild(self, ctx: SlashContext) -> None:
        embed = discord.Embed(title="Guild Information", color=self.client.color)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)


        embed.add_field(name="​", value=f"```yaml\nName\n```**➥ {ctx.guild.name}**", inline=True)
        embed.add_field(name="​", value=f"```yaml\nID\n```**➥ {ctx.guild.id}**", inline=True)
        embed.add_field(name="​", value=f"```yaml\nOwner\n```**➥ {ctx.guild.owner.mention}**", inline=False)
        embed.add_field(name="​", value=f"```yaml\nMembers\n```**➥ {ctx.guild.member_count} members**", inline=True)
        embed.add_field(name="​", value=f"```yaml\nChannels\n```**➥ {len(ctx.guild.text_channels) + len(ctx.guild.voice_channels)} channels**", inline=True)
        embed.add_field(name="​", value=f"```yaml\nRoles\n```**➥ {len(ctx.guild.roles)} roles**", inline=False)
        embed.add_field(name="​", value=f"```yaml\nEmojis\n```**➥ {len(ctx.guild.emojis)} emojis**", inline=True)
        embed.add_field(name="​", value=f"```yaml\nCreated at\n```**➥ {ctx.guild.created_at.strftime('%d/%m/%Y')}**", inline=True)

        connection = DBManager.connect_to_database(ctx.guild)
        cursor = connection.cursor()
        cursor.execute("SELECT sum(nb_messages) FROM Messages WHERE guild = ?", (ctx.guild.id,))
        result = cursor.fetchone()
        embed.add_field(name="​", value=f"```yaml\nTotal messages\n```**➥ {result[0]} messages**", inline=False)

        embed.timestamp = datetime.utcnow()
        embed.set_footer(text=f"StatsBoard", icon_url=self.client.user.avatar_url)

        await ctx.send(embed=embed)
    

def setup(client: discord.Client) -> None:
    client.add_cog(infoGuild(client))
