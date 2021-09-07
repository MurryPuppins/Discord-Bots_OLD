import discord
from discord.ext import commands

"""
---------- Guppy Bot -----------
This is responsible for simple automated role-management on my
friend's Discord server. This is about as basic as a bot can get :)
"""

# Must establish/allow intents in order to allow user role modifications
intents = discord.Intents.default()
intents.members = True

# Variables
bot = commands.Bot(command_prefix='<', intents=intents)
bot.remove_command("help")
client = discord.Client()


# Bootup sequence for Guppy bot
@bot.event
async def on_ready():
    print('Successfully booted Guppy')
    await bot.change_presence(activity=discord.Game(name='Hunting for sharks!'))


# Assigns "Clownfish" role to all newly-joining users
@bot.event
async def on_member_join(member):
    await member.add_roles(discord.utils.get(member.guild.roles, name="Clownfish"))


# Error handling
@bot.event
async def on_command_error(ctx, error):
    if hasattr(ctx.command, 'on_error'):
        return
    if isinstance(error, commands.CommandNotFound):
        return


# Debug pinging functionality
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


# Secret for bot, *NEVER share this with ANYONE*
bot.run('')
