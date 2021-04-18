import discord
from discord.ext import commands
from random import randrange
import asyncio


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="hilo", aliases=["highlow", "high-low", "hl", "higherorlower", "higher-or-lower"])
    async def hilo(self, ctx):
        if not ctx.guild:
            return
        
        random_number = randrange(1, 100)
        embed = discord.Embed(title="Pick a random number between 1 and 100! :smile:", description=f"Your Number Is {str(random_number)}", color=14177041)
        embed.set_footer(text="10 Seconds | Higher Or Lower")
        await ctx.message.delete()
        await ctx.send(embed=embed)

        def check(m):
            return m.channel == ctx.message.channel and m.author == ctx.message.author
        
        try:
            answer = await self.bot.wait_for('message', timeout=10.0, check=check)
            second_random_number = randrange(1, 100)
            if answer.content == "h":
                if second_random_number > random_number:
                    await ctx.send(f"Correct! The Number Was {str(second_random_number)}")
                elif second_random_number < random_number:
                    await ctx.send(f"Incorrect! The Number Was {str(second_random_number)}")
                elif second_random_number == random_number:
                    await ctx.send(f"Draw! The Number Was {str(second_random_number)}")
            elif answer.content == "l":
                if second_random_number < random_number:
                    await ctx.send(f"Correct! The Number Was {str(second_random_number)}")
                elif second_random_number > random_number:
                    await ctx.send(f"Incorrect! The Number Was {str(second_random_number)}")
                elif second_random_number == random_number:
                    await ctx.send(f"Draw! The Number Was {str(second_random_number)}")
            else:
                await ctx.send(f"{ctx.author.mention} | Invalid Input, type ***'h'*** for higher, and ***'l'*** for lower!")
        except asyncio.TimeoutError:
            return await ctx.send(f"You took too long to answer! {ctx.author.mention}")

    @commands.command(name="blackjack", aliases=["bj", "black-jack"])
    async def blackjack(self, ctx):
        pass

def setup(bot: commands.Bot):
    bot.add_cog(Games(bot=bot))