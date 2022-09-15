import discord
import traceback
from discord import app_commands
import random
from creds import token
import sqlite3

"""
---------- Vibe Bot -----------
This is my Vibe Bot, which is found in over 500 servers and has issued thousands of vibe checks
Support Discord Server: https://discord.com/invite/7VemvMg

The majority of the implementation can be found on this Github; however, data may be omitted for security
and privacy reasons. If you have any questions, comments, or suggestions, please ping me in my support discord
above :)
"""

class vibeBot(discord.Client):
    def __init__(self) -> None:
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        # Broken, will fix later
        '''
        for cog in extensions:
            try:
                self.load_extension(cog)
            except Exception:
                print(f'Failed to load extension {cog}')
                traceback.print_exc
        '''
        await self.change_presence(activity=discord.Game(name='Now using slash commands! /vibe)'))
        print(f"We have logged in as {self.user}.")

# Variables

client = vibeBot()
filepath = 'memes/'
tree = app_commands.CommandTree(client)
conn = sqlite3.connect('vibebot.db')
cur = conn.cursor()


# Will fix later
'''
# Error handling, ctx = context, error = error
@client.event
async def on_command_error(ctx, error):
    if hasattr(ctx.command, 'on_error'):
        return
    if isinstance(error, commands.CommandNotFound):
        return
'''

# Vibe Suggestion helper function to insert into text
async def suggestadd(sug):
    with open('suggestions.txt', 'a') as f:
        f.write(str(sug) + '\n')
        f.close()
    return


# Vibe suggestion command for players to suggest new vibes
@tree.command(name="vibesug", description="Suggest a new vibe to be added! (Gifs work!)")
async def vibesug(interaction: discord.Interaction, suggestion: str):
    await suggestadd(suggestion)
    await interaction.response.send_message('Suggestion has been noted')


# Shows the number of servers the bot is in
@tree.command(name="friends", description="Friends? What's that?")
async def friends(interaction: discord.Interaction):
    await interaction.response.send_message('I am currently in ' + str(len(client.guilds)) + ' servers :sparkling_heart:')


# Helper function to load file containing vibes
def vibeload():
    with open('vibe.txt') as f:
        lines = [line.rstrip() for line in f]
    return lines


# Help command for commands relating to Vibe Bot, displayed in embedded message format
@tree.command(name="vibehelp", description="A Dummy's Guide to Vibe Bot")
async def help(interaction: discord.Interaction):
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
    embed.add_field(name='<vibesug x', value='Have a vibe suggestion? Run the command with the suggestion afterwards! E.g > <vibesug This bot is gucci gang', inline=False)
    await interaction.response.send_message(embed=embed)


# Invite command for the bot
@tree.command(name="vibeinvite", description="Need to spread the good word of the Vibe Bot?")
async def invite(interaction: discord.Interaction):
    await interaction.response.send_message('Eh, you likey my vibeys? You can invite me to your party at vibebot.murpups.dev :)')


# Primary entertainment command, returns vibe for user
# Increments vibecount upon each call for statistical purposes
@tree.command(name="vibe", description="Certified Vibe Check Issuer v2000!")
async def vibe(interaction: discord.Interaction):
    cur.execute("UPDATE vibecount SET count = count+1")
    conn.commit()
    vabe = random.choice(lines)
    if vabe[0] == ">":
        await interaction.response.send_message(file=discord.File(filepath + vabe[1:]))
    else:
        await interaction.response.send_message(vabe)


# Returns the number of vibe-checks the bot has issued (as of June 2021)
@tree.command(name="vibecount", description="I've issued too many damn vibes")
async def vibecount(interaction: discord.Interaction):
    cur.execute("SELECT count FROM vibecount")
    await interaction.response.send_message(cur.fetchone()[0])


# Command to test functionality/status of bot
@tree.command(name="ping", description="Knock knock; who's there?")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message('Pong!')


# Miscellaneous entertainment command: returns butter emoji
@tree.command(name="fetchbutter", description="Easter Egg #1, there's many more ;)")
async def fetchbutter(interaction: discord.Interaction):
    await interaction.response.send_message(':butter:')


# Loads the vibe check possibilities and runs the bot, token not available publicly (as it never should be)
lines = vibeload()
client.run(token)
