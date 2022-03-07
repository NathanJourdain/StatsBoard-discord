import sqlite3
from quart import jsonify, redirect, Blueprint, current_app, session
from quart_discord import DiscordOAuth2Session, requires_authorization, models

from utils.utils import *

api = Blueprint('api', __name__)


@api.route('/', methods=['GET'])
@requires_authorization
async def index_api():
    return jsonify()

@api.route("/login/")
async def login_api():
    discord: DiscordOAuth2Session = current_app.config["discord"]
    return await discord.create_session()

@api.route("/logout/")
async def logout_api():
    session.clear()
    return redirect("/")

@api.route('/callback', methods=['GET'])
async def callback_api():
    discord: DiscordOAuth2Session = current_app.config["discord"]
    await discord.callback()
    return redirect("/guilds")



@api.route('/messages/<int:guild_id>', methods=['GET'])
@requires_authorization
async def messages_api(guild_id: int):
    messages = get_messages(guild_id)
    if messages:
        for data in messages:
            messages[messages.index(data)] = {"date": data[0], "nb_messages": data[1]}
        return jsonify(messages)
    else:
        return jsonify({"error": "No data found"})


@api.route('/trafic/<int:guild_id>', methods=['GET'])
@requires_authorization
async def trafic_api(guild_id: int):
    trafic = get_trafic(guild_id)
    if trafic:
        for data in trafic:
            trafic[trafic.index(data)] = {"date": data[0], "new": data[1], "leave": data[2]}
        return jsonify(trafic)
    else:
        return jsonify({"error": "No data found"})


@api.route('/reactions/<int:guild_id>', methods=['GET'])
@requires_authorization
async def reactions_api(guild_id: int):
    reactions = get_reactions(guild_id)
    if reactions: 
        for data in reactions:
            reactions[reactions.index(data)] = {"date": data[0], "add": data[1], "remove": data[2]}
        return jsonify(reactions)
    else:
        return jsonify({"error": "No data found"})

@api.route('/invitations/<int:guild_id>', methods=['GET'])
@requires_authorization
async def invitations_api(guild_id: int):
    invitations = get_invitations(guild_id)
    if invitations: 
        for data in invitations:
            invitations[invitations.index(data)] = {"code": data[0], "creator_id": data[1], "usage": data[2]}
        return jsonify(invitations)
    else:
        return jsonify({"error": "No data found"})


@api.route('/guilds/', methods=['GET'])
@requires_authorization
async def guild_api():
    user_guilds = await get_guilds()
    return jsonify(user_guilds)


@api.route('/guilds/info/<int:guild_id>', methods=['GET'])
@requires_authorization
async def guild_info_api(guild_id: int):
    # get the guild name
    discord: DiscordOAuth2Session = current_app.config["discord"]
    guilds: list = await discord.fetch_guilds()
    guild = None
    for i in guilds:
        if i.id == guild_id:
            guild = i
            break 
    if guild:
        if(hasData(guild_id) is False):
            return jsonify({"error": "No data found"})

        return jsonify({
            "guild_id": str(guild_id),
            "guild_name": guild.name,
            "guild_icon": guild.icon_url,
            "messages": get_messages(guild_id),
            "trafic": get_trafic(guild_id),
            "reactions": get_reactions(guild_id),
            "invitations": get_invitations(guild_id),
            "total_members": get_total_members(guild_id),
            "total_messages": get_total_messages(guild_id),
        })
    else:
        return jsonify({"error": "No guild found"})