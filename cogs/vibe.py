from discord.ext import commands
import discord
import random
from testingJunk.testbot import filepath

# Vibe Suggestion helper function to insert into text
async def suggestadd(sug):
    with open('suggestions.txt', 'a') as f:
        f.write(str(sug) + '\n')
        f.close()
    return

# Helper function to load file containing vibes
def vibeload():
    with open('vibe.txt') as f:
        lines = [line.rstrip() for line in f]
    return lines


class Vibe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    # Vibe suggestion command for players to suggest new vibes
    async def vibesug(self, ctx, *, arg):
        await suggestadd(arg)
        await ctx.send('Suggestion has been noted!')

    @commands.command()
    # Command to check vibe
    async def vibe(self, ctx):
        vabe = random.choice(lines)
        if vabe[0] == ">":
            await ctx.send(file=discord.File(filepath + vabe[1:]))
        else:
            await ctx.send(vabe)


def setup(bot):
    bot.add_cog(Vibe(bot))


vibeload()
lines = vibeload()
