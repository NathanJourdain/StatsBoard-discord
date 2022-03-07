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
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"      # !! Only in development environment.

app.config["DISCORD_CLIENT_ID"] = 931334094128840734    # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = "fVvNIFMDQc1m3HBJ0hkTpTShgnt1nIrc"                # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:1000/api/callback"                 # URL to your callback endpoint.
app.config["DISCORD_BOT_TOKEN"] = "OTMxMzM0MDk0MTI4ODQwNzM0.YeC6dw.zO9I_8QdNDNNZXHEkqNFbmJOjNc"                    # Required to access BOT resources.

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