import discord
#import asyncio
from discord.ext import commands
import random
from creds import token

bot = commands.Bot(command_prefix='<', case_insensitive=True)
client = discord.Client()
bot.remove_command('help')

# Bot start-up handler
@bot.event
async def on_ready():
    print('Successfully booted Vibe Bot Official')
    await bot.change_presence(activity=discord.Game(name='Straight vibin!'))

# Error handling, ctx = context, error = error
@bot.event
async def on_command_error(ctx, error):
    if hasattr(ctx.command, 'on_error'):
        return
    if isinstance(error, commands.CommandNotFound):
        return

# Helper function to append suggestion to suggestion file
async def suggestadd(sug):
    with open('suggestions.txt', 'a') as f:
        f.write(sug + '\n')
        f.close()
    return

# Suggestion command to handle suggestions for vibes from players
@bot.command()
async def vibesug(ctx, arg):
    await suggestadd(arg)
    await ctx.send('Suggestion has been noted!')


# Shows number of servers bot is in
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
    embed.add_field(name='<ping', value='Ping to test status of Vibe Bot!', inline=False)
    embed.add_field(name='<fetchbutter', value='Fetches you some butter!', inline=False)
    embed.add_field(name='<friends', value='See how many friends I have!', inline=False)
    embed.add_field(name='<vibesug ""', value='Have a vibe suggestion? Run the command *with* quotes! E.g > <vibesug "This bot is gucci gang"',
                    inline=False)
    await ctx.send(embed=embed)

# Command to check vibe
@bot.command()
async def vibe(ctx):
    await ctx.send(random.choice(lines))

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
