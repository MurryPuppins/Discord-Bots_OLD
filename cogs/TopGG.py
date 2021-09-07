import dbl
import discord
from discord.ext import commands
from creds import dbltoken


# Cog class responsible for API interaction with the TopGG website (Where bot is posted and can be voted upon)
# Requires your own API/token, hence the "dbltoken
class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = dbltoken # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True) # Autopost will post your guild count every 30 minutes

    async def on_guild_post(self):
        print("Server count posted successfully")