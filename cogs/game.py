import discord
from discord.ext import commands
import random
import asyncio
from main import db
import pymongo
import datetime
import itertools
import yfinance

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="account", aliases=["acc"])
    async def account(self, ctx, args=""):
        if not ctx.guild:
            return

        collection = db["Points"]

        if args == "":
            query = {"id": ctx.author.id, "username": ctx.author.name}
            score = collection.find_one(query)
            if score:
                _id = score["id"]
                username = score["username"]
                time_created = score["time-created"]
                points = score["points"]
                embed = discord.Embed(title="Your Game Account Stats", description=(f"Game ID: {_id}\nUsername: {username}\nDate Created: {time_created}\nPoints: {points}"))
                return await ctx.send(embed=embed)

            return await ctx.send("You have not created an account yet!")

        elif args == "init":
            user_id = {"id": ctx.author.id}
            score = collection.find(user_id)
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
            embed.set_footer(text="@Copyright Alfie Phillips")
            return await ctx.send(embed=embed)

        elif args == "delete":
            user = collection.find_one({"id": ctx.author.id})
            if user:
                embed = discord.Embed(title="Deleting Your Account", description="From this, you will lose all of your points, and your user data will be erased, and will not be able to be recovered. Please click the tick down below if you are sure you want to delete your account!")
                embed.set_footer(text="@Copyright Alfie Phillips")
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

        elif args == "points":
            user_id = {"id": ctx.author.id}
            score = collection.find_one(user_id)
            if score:
                points = str(score['points'])
                embed = discord.Embed(title="Your Game Points!", description=f"{points}")
                embed.set_footer(text="@Copyright Alfie Phillips")
                return await ctx.send(embed=embed)

            return await ctx.send("You have not created an account yet!")


    @commands.command(name="leaderboard", aliases=["lb"])
    async def leaderboard(self, ctx, amount=3):
        collection = db["Points"]
        leaderboard = []
        query = {}
        data = collection.find(query).limit(amount)
        for item in data:
            leaderboard.append({'name': item['username'], 'points': item['points']})

        print(leaderboard)

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name="hilo")
    async def hilo(self, ctx):
        collection = db["Points"]
        stocks = [
            'GME', 'TSLA', 'GOOGL', 'NCR', 'NIO',
            'AMC', "AMZN", "AAPL", "TWTR", "MSFT",
            "MVIS", "NOK", "NVDA", "ATVI", "PLTR",
            "SNDL", "VGAC", "VUSA", "BP"
        ]

        query = {"id": ctx.author.id, "username": ctx.author.name}
        user = collection.find_one(query)

        if not user:
            return await ctx.send("You have not initialized an account yet! M.game-init to create an account.")

        if not ctx.guild:
            return
        
        symbol1 = random.choice(stocks)
        stocks.remove(symbol1)
        symbol2 = random.choice(stocks)
        stocks.remove(symbol2)
        stock_count = len(stocks)

        try:
            ticker_one = yfinance.Ticker(symbol1)
            ticker_two = yfinance.Ticker(symbol2)
            ticker_one_data = ticker_one.history(period="1d")
            ticker_two_data = ticker_two.history(period="1d")

        except Exception as e:
            print(e)
            await ctx.send("Error grabbing current stock prices!")

        stock_one = round(ticker_one_data['Close'][0], 2)
        stock_two = round(ticker_two_data['Close'][0], 2)
        

        embed = discord.Embed(title="Choose which stock you believe is higher in price!", description=f"Your two stocks are: \n1. {str(symbol1)}\n2. {str(symbol2)}\nYou only have 10 seconds to answer! Reply (1) for stock one, and (2) for stock two!", color=14177041)
        embed.set_footer(text="Higher Or Lower. @Copyright Alfie Phillips")
        await ctx.message.delete()
        await ctx.send(embed=embed)

        def check(m):
            return m.channel == ctx.message.channel and m.author == ctx.message.author

        def winning_embed(winner, symbol1, symbol2, stock_one, stock_two):
            embed = discord.Embed(title=f"{winner} is a Winner!", description=f"10 Points have been awarded to you!\n{symbol1}: ${stock_one}\n{symbol2}: ${stock_two}", color=3066993)
            embed.set_footer(text="Higher Or Lower. @Copyright Alfie Phillips")
            return embed

        def losing_embed(loser, symbol1, symbol2, stock_one, stock_two):
            embed = discord.Embed(title=f"{loser} has lost!", description=f"5 Points have been deducted from you!\n{symbol1}: ${stock_one}\n{symbol2}: ${stock_two}", color=15158332)
            embed.set_footer(text="Higher Or Lower. @Copyright Alfie Phillips")
            return embed

        def drawing_embed(draw, symbol1, symbol2, stock_one, stock_two):
            embed = discord.Embed(title=f"{draw}, it is a draw!", description=f"5 Points have been given to you for your luck!\n{symbol1}: ${stock_one}\n{symbol2}: ${stock_two}", color=9807270)
            embed.set_footer(text="Higher Or Lower. @Copyright Alfie Phillips")
            return embed


        try:
            reply = await self.bot.wait_for('message', timeout=10.0, check=check)
            reply = reply.content.lower().strip()
            collection = db["Points"]
            if reply == "1":
                if stock_one > stock_two:
                    collection.update_one({"id": ctx.author.id, "username": ctx.author.name}, {"$inc":{"points": 10}})
                    return await ctx.send(embed=winning_embed(ctx.author.name, symbol1=symbol1, symbol2=symbol2, stock_one=stock_one, stock_two=stock_two))

                elif stock_one < stock_two:
                    collection.update_one({"id": ctx.author.id, "username": ctx.author.name}, {"$inc":{"points": -5}})
                    return await ctx.send(embed=losing_embed(ctx.author.name, symbol1=symbol1, symbol2=symbol2, stock_one=stock_one, stock_two=stock_two))

                elif stock_one == stock_two:
                    collection.update_one({"id": ctx.author.id, "username": ctx.author.name}, {"$inc":{"points": 5}})
                    return await ctx.send(embed=drawing_embed(ctx.author.name, symbol1=symbol1, symbol2=symbol2, stock_one=stock_one, stock_two=stock_two))

            elif reply == "2":
                if stock_two > stock_one:
                    collection.update_one({"id": ctx.author.id, "username": ctx.author.name}, {"$inc":{"points": 10}})
                    return await ctx.send(embed=winning_embed(ctx.author.name, symbol1=symbol1, symbol2=symbol2, stock_one=stock_one, stock_two=stock_two))

                elif stock_two < stock_one:
                    collection.update_one({"id": ctx.author.id, "username": ctx.author.name}, {"$inc":{"points": -5}})
                    return await ctx.send(embed=losing_embed(ctx.author.name, symbol1=symbol1, symbol2=symbol2, stock_one=stock_one, stock_two=stock_two))

                elif stock_two == stock_one:
                    collection.update_one({"id": ctx.author.id, "username": ctx.author.name}, {"$inc":{"points": 5}})
                    return await ctx.send(embed=drawing_embed(ctx.author.name, symbol1=symbol1, symbol2=symbol2, stock_one=stock_one, stock_two=stock_two))
            else:
                return await ctx.send("Invalid reply! Please try again.")

        except asyncio.TimeoutError:
            return await ctx.send("Time has ran out!")

        

    @hilo.error
    async def hilo_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"Slow it down!",description=f"Try again in {error.retry_after:.2f}s.")
            await ctx.send(embed=em)


def setup(bot: commands.Bot):
    bot.add_cog(Games(bot=bot))