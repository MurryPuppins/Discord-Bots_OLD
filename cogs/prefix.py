from discord.ext import commands
import discord
import json

"""
Cog file responsible for allowing server-owner modification of their server prefix for the VibeBot
Only the server owners may change the bots prefix, for security reasons
"""


# Helper function to check if user is server owner
async def is_guild_owner(ctx):
    if ctx.guild is not None:
        return ctx.author.id == ctx.guild.owner.id


# Cog class for handling server prefix changes
# Prefixes are stored in local JSON file
class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(is_guild_owner)
    async def prefix(self, ctx, *, pre):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = pre
        await ctx.send(f'Prefix is set to: {pre}')

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)


# Adds cog to bot
def setup(bot):
    bot.add_cog(Prefix(bot))
