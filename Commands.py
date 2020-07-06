import discord
from discord.ext import commands

"""
Future update in progress, implementing cogs and OOP functionality
"""


class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

        @commands.command()
        async def friends(self, ctx):
            await ctx.send('I am currently in ' + str(len(bot.guilds)) + ' servers :sparkling_heart:')