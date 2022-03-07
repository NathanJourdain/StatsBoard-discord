from datetime import datetime
import discord

import os
import sqlite3
import shutil

def connect_to_database(guild: discord.Guild) -> sqlite3.Connection:
    """
    Return the connection to database or create if not exist

    param ``guild``: The guild
    """

    connection = sqlite3.connect(f"../DATABASE/database.sqlite")
    cursor = connection.cursor()
    
    cursor.execute("SELECT 1 FROM Guild WHERE guild_id = ?", (guild.id,))
    if(cursor.fetchone() is None):
        # INSERT INTO Guild (guild_id, total_members, total_messages, total_boosts) VALUES (12345678, 50, 10, 0);
        cursor.execute("INSERT INTO Guild (guild_id, total_members, total_messages, total_boosts) VALUES (?, ?, ?, ?)",
        (guild.id, guild.member_count, 0, guild.premium_subscription_count,))
        connection.commit()    
    
    return connection
