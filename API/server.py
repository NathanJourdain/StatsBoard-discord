import os

from quart import Quart, redirect
from quart_discord import DiscordOAuth2Session, Unauthorized
from discord.ext import ipc

# Routes
from routes.api import api
from routes.guilds import guilds
from routes.home import home

app = Quart(__name__, template_folder='templates', static_folder='static')

app.secret_key = b"random bytes representing flask secret key"
# OAuth2 must make use of HTTPS in production environment.
# !! Only in development environment.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"

app.config["DISCORD_CLIENT_ID"] = 0   # Discord client ID.
# Discord client secret.
app.config["DISCORD_CLIENT_SECRET"] = ""
# URL to your callback endpoint.
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:1000/api/callback"
# Required to access BOT resources.
app.config["DISCORD_BOT_TOKEN"] = ""

# Ipc
ipc_client = ipc.Client(
    secret_key="123456789"
)

discord = DiscordOAuth2Session(app)

app.config['ipc_client'] = ipc_client
app.config['discord'] = discord


# Routes register
app.register_blueprint(home, url_prefix='/')
app.register_blueprint(api, url_prefix='/api/')
app.register_blueprint(guilds, url_prefix='/')


@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect("/api/login")


if __name__ == "__main__":
    app.run(port=1000, host="localhost")
