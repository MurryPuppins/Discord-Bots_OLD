import discord
from discord.ext import commands, tasks
import schedule

bot = commands.Bot(command_prefix='<', case_insensitive=True)

client = discord.Client()
rankname = 'Clownfish'


@bot.event
async def on_ready():
    print('Successfully booted Guppy')
    await client.change_presence(activity=discord.Game(name='Hunting for Sharks!'))


@bot.command()
async def setrole(ctx):
    rankname = ctx
    await ctx.send('Auto-role has been set to ' + ctx)


#@tasks.loop(hours=24)
async def dq_ping():
    channel = get_channel(230131892316274691)
    await channel.send(format(client.mention(169554013837066241)))


@dq_ping.before_loop
async def bef():
    await bot.wait_until_ready()


@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name=rankname)
    await client.add_roles(role)
    channel = client.get_channel(666143692159188993)
    await channel.send(str(member) + ' has been autoroled!')

@bot.command()
async def ping(ctx):
    role = discord.utils.get(ctx.guild.roles, name='The Team!')
    if role in ctx.author.roles:
        await ctx.send('Pong!')
    else:
        await ctx.send('You need the ' + role.name + 'role!')

await dq_ping()
bot.run('NjcyNTk1NjcwNzYyNTIwNjA1.XjNx7Q.qCRYpCtsJyHXPX8U2nINE40xXY4')