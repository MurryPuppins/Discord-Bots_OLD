import discord
#import asyncio
from discord.ext import commands
import random
from creds import token
from creds import dbltoken
import json
import dbl

async def getPrefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

bot = commands.Bot(command_prefix='<', case_insensitive=True)
client = discord.Client()
bot.remove_command('help')
filepath = 'memes/'

class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = dbltoken # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True) # Autopost will post your guild count every 30 minutes

    async def on_guild_post(self):
        print("Server count posted successfully")

def setup(bot):
    bot.add_cog(TopGG(bot))

@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '>'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@bot.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@bot.command()
async def prefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f'Prefix changed to: {prefix}')

# Bot start-up handler
@bot.event
async def on_ready():
    guilds = bot.guilds
    with open('prefixes.json', 'r') as f:
        curr = json.load(f)
    for g in guilds:
        if g.id in curr:
            return
        else:
            curr[str(g.id)] = '<'
    with open('prefixes.json', 'w') as f:
        json.dump(curr, f, indent=4)
    print('Successfully booted Vibe Bot Official')
    await bot.change_presence(activity=discord.Game(name='Straight vibin!'))
    await setup(bot)


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

# Help command for commands relating to Vibe Bot
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

# Command to check vibe
@bot.command()
async def vibe(ctx):
    vabe = random.choice(lines)
    if vabe[0] == ">":
        await ctx.send(file=discord.File(filepath + vabe[1:]))
    else:
        await ctx.send(vabe)
    #await ctx.send(random.choice(lines))

# Command to test functionality/status of bot
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

# Fun command to fetch butter/return butter emoji
@bot.command()
async def fetchbutter(ctx):
    await ctx.send(':butter:')

# Loads the vibe check possibilities and runs the bot
lines = vibeload()
bot.run(token)
