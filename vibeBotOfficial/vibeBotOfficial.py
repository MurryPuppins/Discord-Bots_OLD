import discord
import traceback
from discord.ext import commands
import random
from creds import token
import json
import sqlite3

"""
---------- Vibe Bot -----------
This is my Vibe Bot, which is found in over 450 servers and has given thousands of vibe checks
Support Discord Server: https://discord.com/invite/7VemvMg

The majority of the implementation can be found on this Github; however, data may be omitted for security
and privacy reasons. If you have any questions, comments, or suggestions, please ping me in my support discord
above :)
"""


# Responsible for loading current prefixes
async def get_prefix(ctx, message):
    if not message.guild:
        return commands.when_mentioned_or("<")(bot, message)

    with open("prefixes.json", 'r') as f:
        prefixes = json.load(f)

    if str(message.guild.id) not in prefixes:
        return commands.when_mentioned_or("<")(bot, message)

    prefix = prefixes[str(message.guild.id)]
    return commands.when_mentioned_or(prefix)(bot, message)

# Variables
bot = commands.Bot(command_prefix=get_prefix)
client = discord.Client()
bot.remove_command('help')
filepath = 'memes/'
extensions = ('cogs.prefix', 'cogs.TopGG')

conn = sqlite3.connect('vibebot.db')
cur = conn.cursor()


# Bot start-up handler
@bot.event
async def on_ready():
    for cog in extensions:
        try:
            bot.load_extension(cog)
        except Exception:
            print(f'Failed to load extension {cog}')
            traceback.print_exc
    print('Successfully booted Vibe Bot Official')
    await bot.change_presence(activity=discord.Game(name='Straight vibin!'))


# Error handling, ctx = context, error = error
@bot.event
async def on_command_error(ctx, error):
    if hasattr(ctx.command, 'on_error'):
        return
    if isinstance(error, commands.CommandNotFound):
        return


# Vibe Suggestion helper function to insert into text
async def suggestadd(sug):
    with open('suggestions.txt', 'a') as f:
        f.write(str(sug) + '\n')
        f.close()
    return


# Vibe suggestion command for players to suggest new vibes
@bot.command()
async def vibesug(ctx, *, arg):
    await suggestadd(arg)
    await ctx.send('Suggestion has been noted!')


# Shows the number of servers the bot is in
@bot.command()
async def friends(ctx):
    await ctx.send('I am currently in ' + str(len(bot.guilds)) + ' servers :sparkling_heart:')


# Helper function to load file containing vibes
def vibeload():
    with open('vibe.txt') as f:
        lines = [line.rstrip() for line in f]
    return lines


# Help command for commands relating to Vibe Bot, displayed in embedded message format
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title='Help List',
        description='All commands relevant to Vibe Bot!',
        colour=discord.Colour.dark_magenta()
    )
    embed.set_author(name='Vibe Bot')
    embed.add_field(name='<vibe', value='Checks your vibe!', inline=False)
    embed.add_field(name='<prefix', value='Change the prefix!', inline=False)
    embed.add_field(name='<ping', value='Ping to test status of Vibe Bot!', inline=False)
    embed.add_field(name='<fetchbutter', value='Fetches you some butter!', inline=False)
    embed.add_field(name='<friends', value='See how many friends I have!', inline=False)
    embed.add_field(name='<vibesug x', value='Have a vibe suggestion? Run the command with the suggestion afterwards! E.g > <vibesug This bot is gucci gang', inline=False)
    await ctx.send(embed=embed)


# Invite command for the bot
@bot.command()
async def invite(ctx):
    await ctx.send('Eh, you likey my vibeys? You can invite me to your party at vibebot.clutchgaming.xyz :)')


# Primary entertainment command, returns vibe for user
# Increments vibecount upon each call for statistical purposes
@bot.command()
async def vibe(ctx):
    cur.execute("UPDATE vibecount SET count = count+1")
    conn.commit()
    vabe = random.choice(lines)
    if vabe[0] == ">":
        await ctx.send(file=discord.File(filepath + vabe[1:]))
    else:
        await ctx.send(vabe)


# Returns the number of vibe-checks the bot has issued (as of June 2021)
@bot.command()
async def vibecount(ctx):
    cur.execute("SELECT count FROM vibecount")
    await ctx.send(cur.fetchone()[0])


# Command to test functionality/status of bot
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')


# Miscellaneous entertainment command: returns butter emoji
@bot.command()
async def fetchbutter(ctx):
    await ctx.send(':butter:')


# Loads the vibe check possibilities and runs the bot, token not available publicly (as it never should be)
lines = vibeload()
bot.run(token)
