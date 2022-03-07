import discord
from discord.ext import commands, ipc
from discord.ext.commands.errors import ExtensionNotLoaded
from discord_slash import SlashCommand
import os

DEFAULT_PREFIX = "."
TOKEN = ""


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ipc = ipc.Server(self, secret_key="123456789")

       # Load cogs
        for filename in os.listdir("./cogs"):
            if filename.endswith('.py'):
                try:
                    self.load_extension(f"cogs.{filename[:-3]}")
                except Exception as e:
                    print(e)

    async def on_ready(self):
        print("Bot is ready.")

    async def on_ipc_ready(self):
        print("Ipc is ready.")

    async def on_ipc_error(self, endpoint, error):
        print(endpoint, "raised", error)


client = Bot(command_prefix=DEFAULT_PREFIX, intents=discord.Intents.all())
slash = SlashCommand(client, override_type=True,
                     sync_commands=True, sync_on_cog_reload=True)
client.remove_command("help")

client.color = discord.Color.from_rgb(10, 105, 69)

# reload command


@client.command()
@commands.is_owner()
async def reload(ctx):
    for filename in os.listdir("./cogs"):
        if filename.endswith('.py'):
            try:
                client.reload_extension(f"cogs.{filename[:-3]}")
            except ExtensionNotLoaded as e:
                client.load_extension(f"cogs.{filename[:-3]}")
    await ctx.send("Reload effectué !", delete_after=5)


client.ipc.start()
client.run(TOKEN)
