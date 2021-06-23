import discord
import json
import sys
import traceback
from discord.ext import commands

async def get_prefix(ctx, message):
    if not message.guild:
        return commands.when_mentioned_or("<")(bot, message)

    with open("../vibeBotOfficial/prefixes.json", 'r') as f:
        prefixes = json.load(f)

    if str(message.guild.id) not in prefixes:
        return commands.when_mentioned_or("<")(bot, message)

    prefix = prefixes[str(message.guild.id)]
    return commands.when_mentioned_or(prefix)(bot, message)

extensions = ('cogs.commands',
              'cogs.prefix',
              )
bot = commands.Bot(command_prefix=get_prefix)
client = discord.Client()
bot.remove_command('help')
filepath = 'memes/'

@bot.event
async def on_ready():
    for cog in extensions:
        try:
            bot.load_extension(cog)
        except Exception:
            print(f'Failed to load extension {cog}.', file=sys.stderr)
            traceback.print_exc()
    print('Done bootin botty boi')

# Error handling, ctx = context, error = error
@bot.event
async def on_command_error(ctx, error):
    if hasattr(ctx.command, 'on_error'):
        return
    if isinstance(error, commands.CommandNotFound):
        return

bot.run('NjI2ODQ0MDc0MjI5MzY2Nzg0.XY0ACQ.uI1rJcn8AEyLX6X3MCdPXyjx4l0')