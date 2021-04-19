import discord
from discord.ext import commands
from random import randrange
import asyncio
from main import db
import pymongo
import datetime
import itertools

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="game-leaderboard")
    async def game_leaderboard(self, ctx, limit=None):
        pass

    @commands.command(name="game-points")
    async def game_points(self, ctx):
        if not ctx.guild:
            return

        collection = db["Points"]
        user_id = {"id": ctx.author.id}
        score = collection.find_one(user_id)
        if score:
            _sum = 0
            for i in score:
                _sum += int(i['points'])
            
            embed = discord.Embed(title="Your Game Points!", description=f"{str(_sum)}")
            return await ctx.send(embed=embed)

        return await ctx.send("You have not created an account yet!")

    @commands.cooldown(1, 120, commands.BucketType.user)
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
            if answer.content.lower() == "h" or answer.content.lower() == "higher":
                if second_random_number > random_number:
                    await ctx.send(f"Correct! The Number Was {str(second_random_number)}")
                    collection = db["Points"]
                    collection.update_one({"id": ctx.author.id, "username": ctx.author.name}, {"$inc":{"points": 10}})

                elif second_random_number < random_number:
                    await ctx.send(f"Incorrect! The Number Was {str(second_random_number)}")
                    collection = db["Points"]
                    collection.update_one({"id": ctx.author.id, "username": ctx.author.name}, {"$inc":{"points": -5}})
                elif second_random_number == random_number:
                    await ctx.send(f"Draw! The Number Was {str(second_random_number)}")
                    collection = db["Points"]
                    query = {"id": ctx.author.id, "points": 5}
                    collection.update_one({"id": ctx.author.id, "username": ctx.author.name}, {"$inc":{"points": 5}})
            elif answer.content.lower == "l" or answer.content.lower() == "lower":
                if second_random_number < random_number:
                    await ctx.send(f"Correct! The Number Was {str(second_random_number)}")
                    collection = db["Points"]
                    collection.update_one({"id": ctx.author.id, "username": ctx.author.name}, {"$inc":{"points": 10}})
                elif second_random_number > random_number:
                    await ctx.send(f"Incorrect! The Number Was {str(second_random_number)}")
                    collection = db["Points"]
                    collection.update_one({"id": ctx.author.id, "username": ctx.author.name}, {"$inc":{"points": -5}})
                elif second_random_number == random_number:
                    await ctx.send(f"Draw! The Number Was {str(second_random_number)}")
                    collection = db["Points"]
                    collection.update_one({"id": ctx.author.id, "username": ctx.author.name}, {"$inc":{"points": 5}})
            else:
                await ctx.send(f"{ctx.author.mention} | Invalid Input, type ***'h'*** for higher, and ***'l'*** for lower!")
        except asyncio.TimeoutError:
            return await ctx.send(f"You took too long to answer! {ctx.author.mention}")

    @hilo.error
    async def hilo_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"Slow it down bro!",description=f"Try again in {error.retry_after:.2f}s.")
            await ctx.send(embed=em)

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
        
        now = datetime.datetime.now()

        query = {
            "id": ctx.author.id,
            "username": ctx.author.name,
            "time-created": f"{now.year}/{now.month}/{now.day}/{now.hour}:{now.minute}.{now.second}",
            "points": 0
        }

        message = await ctx.send("Loading...")
        collection.insert_one(query)
        await message.delete()
        embed = discord.Embed(title=f"Account created for {ctx.author.name}", description="Please use M.help for guidance on the commands!")
        await ctx.send(embed=embed)


    @commands.command(name="del-game-account")
    async def del_game_account(self, ctx):
        collection = db["Points"]
        user = collection.find_one({"id": ctx.author.id})
        if user:
            embed = discord.Embed(title="Deleting Your Account", description="From this, you will lose all of your points, and your user data will be erased, and will not be able to be recovered. Please click the tick down below if you are sure you want to delete your account!")
            await ctx.send(embed=embed)
            message = await ctx.send(f"{ctx.author.mention}. Are you sure you want to delete your account?")
            await message.add_reaction("✅")
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: str(reaction.emoji) == "✅" and user.id == ctx.author.id, timeout=15.0)
                if reaction:
                    collection = db["Points"]
                    query = {"id": ctx.author.id}
                    delete = collection.delete_one(query)

                    if delete:
                        await message.delete()
                        return await ctx.send("Your account has been deleted!")

                    await message.delete()
                    return await ctx.send("There was an error deleting your account, please try again!")

            except asyncio.TimeoutError:
                message.delete()
                return await ctx.send("Timed Out!")

        return await ctx.send("You do not have an account to delete!")
    @commands.command(name="game-account")
    async def game_account(self, ctx):
        if not ctx.guild:
            return
        
        query = {"id": ctx.author.id, "username": ctx.author.name}
        collection = db["Points"]
        score = collection.find_one(query)
        if score:
            _id = score["id"]
            username = score["username"]
            time_created = score["time-created"]
            points = score["points"]
            embed = discord.Embed(title="Your Game Account Stats", description=(f"Game ID: {_id}\nUsername: {username}\nDate Created: {time_created}\nPoints: {points}"))
            return await ctx.send(embed=embed)

        return await ctx.send("You have not created an account yet!")


    @commands.command(name="blackjack", aliases=["bj", "black-jack"])
    async def blackjack(self, ctx):
        print("Test")

def setup(bot: commands.Bot):
    bot.add_cog(Games(bot=bot))