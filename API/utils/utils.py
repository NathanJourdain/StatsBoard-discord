import sqlite3
from quart_discord import DiscordOAuth2Session
from quart import current_app

# UTILS FUNCTIONS
async def get_guilds() -> list:
    discord: DiscordOAuth2Session = current_app.config["discord"]

    # Retourne les serveurs du user
    guilds = await discord.fetch_guilds()

    user_guilds = []
    for guild in guilds:
        if guild.permissions.administrator:
            user_guilds.append({"guild_id": str(guild.id), "guild_name": guild.name, "guild_icon": guild.icon_url})
    return user_guilds

def get_messages(guild_id) -> list:
    database: sqlite3.Connection = sqlite3.connect("../DATABASE/database.sqlite")
    cursor: sqlite3.Cursor = database.cursor()
    cursor.execute("SELECT date, nb_messages FROM messages WHERE guild = ? ORDER BY date ASC", (guild_id,))
    messages = cursor.fetchall()
    database.close()
    return messages

def get_trafic(guild_id) -> list:
    database: sqlite3.Connection = sqlite3.connect("../DATABASE/database.sqlite")
    cursor: sqlite3.Cursor = database.cursor()
    cursor.execute("SELECT date, new, leave FROM trafic WHERE guild = ? ORDER BY date ASC", (guild_id,))
    trafic = cursor.fetchall()
    database.close()
    return trafic

def get_reactions(guild_id) -> list:
    database: sqlite3.Connection = sqlite3.connect("../DATABASE/database.sqlite")
    cursor: sqlite3.Cursor = database.cursor()
    cursor.execute("SELECT date, reactions_add, reactions_remove FROM reactions WHERE guild = ? ORDER BY date ASC", (guild_id,))
    reactions = cursor.fetchall()
    database.close()
    return reactions

def get_invitations(guild_id) -> list:
    database: sqlite3.Connection = sqlite3.connect("../DATABASE/database.sqlite")
    cursor: sqlite3.Cursor = database.cursor()
    cursor.execute("SELECT code, usage, creator_id FROM invitations WHERE guild = ? ORDER BY usage AsC", (guild_id,))
    invitations = cursor.fetchall()
    database.close()
    return invitations

def get_total_members(guild_id) -> int:
    database: sqlite3.Connection = sqlite3.connect("../DATABASE/database.sqlite")
    cursor: sqlite3.Cursor = database.cursor()
    cursor.execute("SELECT total_members FROM guild WHERE guild_id = ?", (guild_id,))
    invitations = cursor.fetchone()
    database.close()
    return int(invitations[0])

def get_total_messages(guild_id) -> int:
    database: sqlite3.Connection = sqlite3.connect("../DATABASE/database.sqlite")
    cursor: sqlite3.Cursor = database.cursor()
    cursor.execute("SELECT total_messages FROM guild WHERE guild_id = ?", (guild_id,))
    invitations = cursor.fetchone()
    database.close()
    return int(invitations[0])

def hasData(guild_id) -> bool:
    database: sqlite3.Connection = sqlite3.connect("../DATABASE/database.sqlite")
    cursor: sqlite3.Cursor = database.cursor()
    cursor.execute("SELECT 1 FROM guild WHERE guild_id = ?", (guild_id,))
    data = cursor.fetchone()
    database.close()
    return bool(data)

def get_guild_stats(guild_id) -> dict:    
    return {
            "messages": get_messages(guild_id),
            "trafic": get_trafic(guild_id),
            "reactions": get_reactions(guild_id),
            "invitations": get_invitations(guild_id),
            "total_members": get_total_members(guild_id),
            "total_messages": get_total_messages(guild_id),
        }