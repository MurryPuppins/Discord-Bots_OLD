import discord
#import asyncio
from discord.ext import commands
import random
from creds import token
from creds import dbltoken
import json
import dbl

async def getPrefix(client, message):
    if message.guild is None:
        return ">"
    else:
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
async def yousuck(ctx):
    await ctx.send("||What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Navy Seals, and I've been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills. I am trained in gorilla warfare and I'm the top sniper in the entire US armed forces. You are nothing to me but just another target. I will wipe you the fuck out with precision the likes of which has never been seen before on this Earth, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of spies across the USA and your IP is being traced right now so you better prepare for the storm, maggot. The storm that wipes out the pathetic little thing you call your life. You're fucking dead, kid. I can be anywhere, anytime, and I can kill you in over seven hundred ways, and that's just with my bare hands. Not only am I extensively trained in unarmed combat, but I have access to the entire arsenal of the United States Marine Corps and I will use it to its full extent to wipe your miserable ass off the face of the continent, you little shit. If only you could have known what unholy retribution your little clever comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn't, you didn't, and now you're paying the price, you goddamn idiot. I will shit fury all over you and you will drown in it. You're fucking dead, kiddo.||")

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
    await update_owner_msg()

async def update_owner_msg():
    msg = "Hello! First off, I apologize for the inconvenience this may cause! You are receiving this message because you are the owner of a discord that contains the Vibe bot, hence why I'm here <3. I just wanted to invite you to join our support discord, so that you can be part of the next poll that will determine the next series of updates for the bot! I would like the community to be involved in the decisions that set the course of the future of this bot, so I invite you to join the discord to participate in the poll and see all updates/information pertinent to the bot! If you do not wish to join, that is fine! This will most likely be the only message you'll receive in this fashion. Have a vibeful day! The link can be found here: https://discord.gg/XWsRnMt"
    for g in bot.guilds:
        await g.owner.send(msg)



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
