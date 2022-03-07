from quart import Blueprint, render_template, current_app
from quart_discord import DiscordOAuth2Session
from utils.utils import get_guilds

home = Blueprint('home', __name__)


@home.route('/')
async def home():
    discord: DiscordOAuth2Session = current_app.config["discord"]
    connected: bool = await discord.authorized
    if connected:
        user_guilds: list = await get_guilds()
    else:
        user_guilds = []

    return await render_template('home.html', connected=connected, user_guilds=user_guilds)
