from quart import redirect, Blueprint, render_template
from quart_discord import requires_authorization

from utils.utils import get_guild_stats, get_guilds, hasData

guilds = Blueprint('guilds', __name__)

@guilds.route('/guilds', methods=['GET'])
@requires_authorization
async def guilds_route():
    user_guilds = await get_guilds()
    return await render_template('guilds.html', title="My guilds", css="/static/styles/guilds.css",user_guilds=user_guilds)


@guilds.route('/guilds/<guild_id>', methods=['GET'])
@requires_authorization
async def guild_route(guild_id):
    user_guilds: list = await get_guilds()
    if guild_id not in [guild['guild_id'] for guild in user_guilds]:
        return redirect('/guilds')
    else:
        if not hasData(guild_id):
            return await render_template('botNotInGuild.html', title="Woops, bot not on this guild", css="/static/styles/guildInfo.css", user_guilds=user_guilds)
        else:
            guild_info = [guild for guild in user_guilds if guild['guild_id'] == guild_id][0]
            guild_stats = get_guild_stats(guild_info['guild_id'])
            return await render_template('guildInfo.html', title=guild_info['guild_name'], css="/static/styles/guildInfo.css",guild_info=guild_info, guild_stats=guild_stats, user_guilds=user_guilds)