import discord
import traceback
#import asyncio
from discord.ext import commands
import random
from creds import token
import json
import dbl
import sqlite3
#from creds import dbltoken


"""
async def getPrefix(client, msg):
    if msg.guild is None:
        return ">"
    else:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        return prefixes[str(msg.guild.id)]
"""


async def get_prefix(ctx, message):
    if not message.guild:
        return commands.when_mentioned_or("<")(bot, message)

    with open("prefixes.json", 'r') as f:
        prefixes = json.load(f)

    if str(message.guild.id) not in prefixes:
        return commands.when_mentioned_or("<")(bot, message)

    prefix = prefixes[str(message.guild.id)]
    return commands.when_mentioned_or(prefix)(bot, message)

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
    #await update_owner_msg()


async def update_owner_msg():
    msg = "Hello! First off, I apologize for the inconvenience this may have caused (if you got a duplicate of this, sorry, I forgot about an exception)! You are receiving this message because you are the owner of a discord that contains the Vibe bot, hence why I'm here <3. I just wanted to invite you to join our support discord, so that you can be part of the next poll that will determine the next series of updates for the bot! I would like the community to be involved in the decisions that set the course of the future of this bot, so I invite you to join the discord to participate in the poll and see all updates/information pertinent to the bot! If you do not wish to join, that is fine! This will most likely be the only message you'll receive in this fashion. Have a vibeful day! The link can be found here: https://discord.gg/XWsRnMt"
    for g in bot.guilds:
        try:
            await g.owner.send(msg)
        except Exception:
            pass


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


# Easter Egg command only found through vibe/guessing, not inside help command
@bot.command()
async def yousuck(ctx):
    await ctx.send("||What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Navy Seals, and I've been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I'm the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You're fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that's just with my bare hands. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little clever comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn't, you didn't, and now you're paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You're fucking dead, kiddo.||")


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


# Invite command for the bot
@bot.command()
async def invite(ctx):
    await ctx.send('Eh, you likey my vibeys? You can invite me to your party at vibebot.clutchgaming.xyz :)')


# Command to check vibe
@bot.command()
async def vibe(ctx):
    cur.execute("UPDATE vibecount SET count = count+1")
    conn.commit()
    vabe = random.choice(lines)
    if vabe[0] == ">":
        await ctx.send(file=discord.File(filepath + vabe[1:]))
    else:
        await ctx.send(vabe)
    #await ctx.send(random.choice(lines))


@bot.command()
async def vibecount(ctx):
    if ctx.message.author.id == 169554013837066241:
        cur.execute("SELECT count FROM vibecount")
        await ctx.send(cur.fetchone()[0])


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
