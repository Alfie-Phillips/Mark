import discord
from discord.ext import commands
from random import randrange
import asyncio
from main import db
import pymongo

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
                    collection = db["Points"]
                    query = {"id": ctx.author.id, "points": 10}
                    collection.insert_one(query)

                elif second_random_number < random_number:
                    await ctx.send(f"Incorrect! The Number Was {str(second_random_number)}")
                elif second_random_number == random_number:
                    await ctx.send(f"Draw! The Number Was {str(second_random_number)}")
                    collection = db["Points"]
                    query = {"id": ctx.author.id, "points": 5}
                    collection.insert_one(query)
            elif answer.content == "l":
                if second_random_number < random_number:
                    await ctx.send(f"Correct! The Number Was {str(second_random_number)}")
                    collection = db["Points"]
                    query = {"id": ctx.author.id, "points": 10}
                    collection.insert_one(query)
                elif second_random_number > random_number:
                    await ctx.send(f"Incorrect! The Number Was {str(second_random_number)}")
                elif second_random_number == random_number:
                    await ctx.send(f"Draw! The Number Was {str(second_random_number)}")
                    collection = db["Points"]
                    query = {"id": ctx.author.id, "points": 5}
                    collection.insert_one(query)
            else:
                await ctx.send(f"{ctx.author.mention} | Invalid Input, type ***'h'*** for higher, and ***'l'*** for lower!")
        except asyncio.TimeoutError:
            return await ctx.send(f"You took too long to answer! {ctx.author.mention}")

    @commands.command(name="game-init")
    async def game_init(self, ctx):
        collection = db["Points"]
        user_id = {"id": ctx.author.id}
        score = collection.find(user_id)
        if not ctx.guild:
            return
        
        for result in score:
            if result["id"] == ctx.author.id:
                return await ctx.send("You have already initialized your account!")
        
        query = {
            "id": ctx.author.id,
            "username": ctx.author.name,
            "points": 0
        }

        message = await ctx.send("Loading...")
        collection.insert_one(query)
        await message.delete()
        embed = discord.Embed(title=f"Account created for {ctx.author.name}", description="Please use M.help for guidance on the commands!")
        await ctx.send(embed=embed)


    @commands.command(name="blackjack", aliases=["bj", "black-jack"])
    async def blackjack(self, ctx):
        print("Test")

def setup(bot: commands.Bot):
    bot.add_cog(Games(bot=bot))