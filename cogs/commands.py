from discord.ext import commands
import discord

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Ping command for connectivity testing
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

    # Help command for commands relating to Vibe Bot
    @commands.command()
    async def help(self, ctx):
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
        embed.add_field(name='<vibesug x',
                        value='Have a vibe suggestion? Run the command with the suggestion afterwards! E.g > <vibesug This bot is gucci gang',
                        inline=False)
        await ctx.send(embed=embed)

        # Fun command to fetch butter/return butter emoji
        @commands.command()
        async def fetchbutter(self, ctx):
            await ctx.send(':butter:')


def setup(bot):
    bot.add_cog(Commands(bot))
