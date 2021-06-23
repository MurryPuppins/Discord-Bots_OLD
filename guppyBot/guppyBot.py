import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='<', intents=intents)
bot.remove_command("help")
client = discord.Client()


@bot.event
async def on_ready():
    print('Successfully booted Guppy')
    await bot.change_presence(activity=discord.Game(name='Hunting for sharks!'))


@bot.event
async def on_member_join(member):
    await member.add_roles(discord.utils.get(member.guild.roles, name="Clownfish"))


@bot.event
async def on_command_error(ctx, error):
    if hasattr(ctx.command, 'on_error'):
        return
    if isinstance(error, commands.CommandNotFound):
        return


@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


bot.run('')
