# Imports Here...

import asyncio
import datetime
import random
import logging

import discord
from proto import MESSAGE
import yfinance
from discord.ext import commands
from time import sleep

from main import db



# Start Games Class
class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="account", aliases=["acc"])
    async def account(self, ctx, args=""):
        user_id = {"id": ctx.author.id}

        if not ctx.guild:
            return  # Check if it is written in the server.

        collection = db["Points"]

        if args == "":  # We check if the argument given is empty, to be able to show just the account

            user = collection.find_one(user_id)
            if user:
                _id = user["id"]
                username = user["username"]
                time_created = user["time-created"]
                points = user["points"]
                nickname = user['nickname']

                if nickname is None:
                    embed = discord.Embed(
                        title="Your Game Account Stats",
                        description=(
                            f"Game ID: {_id}\nUsername: {username}\nDate Created: {time_created}\nPoints: {points}")
                    )

                    embed.set_footer(text="@Copyright Alfie Phillips")
                    return await ctx.send(embed=embed)

                else:
                    embed = discord.Embed(
                        title="Your Game Account Stats",
                        description=(
                            f"Game ID: {_id}\nUsername: {username}\nNickname: {nickname}\nDate Created: {time_created}\nPoints: {points}")
                    )

                    embed.set_footer(text="@Copyright Alfie Phillips")
                    return await ctx.send(embed=embed)

            return await ctx.send("You have not created an account yet!")

        elif args == "init":  # Initiating an account
            users = collection.find(user_id)

            for result in users:
                # Iterating through all the users to check if the author id, matches the result id's
                if result["id"] == ctx.author.id:
                    if result["nickname"] != None:
                        nickname = result["nickname"]
                        return await ctx.send(f"You have already initialized your account {nickname}!")
                    return await ctx.send("You have already initialized your account!")


            now = datetime.datetime.now()  # Time of creation

            query = {
                "id": ctx.author.id,
                "username": ctx.author.name,
                "nickname": None,
                "time-created": f"{now.year}/{now.month}/{now.day}/{now.hour}:{now.minute}.{now.second}",
                "points": 0
            }  # Our query for User accounts

            message = await ctx.send("Loading...")  # Loading time for inserting query
            try:
                collection.insert_one(query)
            except Exception as e:
                print(e)
                return await ctx.send(f"Failed creating an account for {ctx.author.mention}!")

            await message.delete()

            embed = discord.Embed(title=f"Account created for {ctx.author.name}",
                                  description="Please use M.help for guidance on the commands!",
                                  color=discord.Color.red())
            embed.set_footer(text="@Copyright Alfie Phillips")

            return await ctx.send(embed=embed)

        elif args == "delete":  # Deleting accounts
            user = collection.find_one(user_id)

            if user:

                embed = discord.Embed(title="Deleting Your Account",
                                      description="From this, you will lose all of your points, and your user data will be erased, and will not be able to be recovered. Please click the tick down below if you are sure you want to delete your account!",
                                      color=discord.Color.red())

                embed.set_footer(text="@Copyright Alfie Phillips")

                await ctx.send(embed=embed)

                message = await ctx.send(f"{ctx.author.mention}. Are you sure you want to delete your account?")

                await message.add_reaction("✅")
                await message.add_reaction("❌")

                try:
                    reaction, user = await self.bot.wait_for(
                        "reaction_add",
                        check=lambda reaction, user:
                        str(reaction.emoji) == "✅" and user.id == ctx.author.id,
                        timeout=15.0
                    )

                    if reaction:
                        collection = db["Points"]
                        query = {"id": ctx.author.id}
                        delete = collection.delete_one(query)

                        try:
                            await message.delete()

                            loading = await ctx.send("Loading...")

                            collection.delete_one(query)

                            await loading.delete()
                            return await ctx.send("Your account has been deleted!")

                        except Exception as e:
                            await message.delete()

                            print(e)

                            return await ctx.send("There was an error deleting your account, please try again!")

                except asyncio.TimeoutError:

                    await message.delete()
                    return await ctx.send("Timed Out!")

            return await ctx.send("You do not have an account to delete!")

        elif args == "points":
            try:
                score = collection.find_one(user_id)
                points = str(score["points"])

                embed = discord.Embed(
                    title="Your Game Points!",
                    description=f"{points}",
                    color=discord.Color.blue()
                )
                embed.set_footer(text="@Copyright Alfie Phillips")

                return await ctx.send(embed=embed)

            except:
                return await ctx.send("You have not created an account yet!")

    @commands.command(name="games-leaderboard")
    async def leaderboard(self, ctx, amount=3):
        if amount > 20:
            return await ctx.send("You can't have a higher amount than 20 players!")
        collection = db["Points"]
        leaderboard = {}
        query = {}

        try:
            data = collection.find(query).limit(amount).sort('points', -1)
            index = 1
            em = discord.Embed(
                title=f"Top {str(amount)} Players on {ctx.guild}",
                description="This is decided upon the amount of points you have in your game account. If you don't have one, do M.account init!",
                color=discord.Color(0xfa43ee)
            )
            em.set_footer(text="@Copyright Alfie Phillips")
            for item in data:
                em.add_field(name=f"{str(index)}. {item['username']}", value=f"{str(item['points'])} points",
                             inline=False)

                if index == amount:
                    break

                else:
                    index += 1

            return await ctx.send(embed=em)

        except Exception as e:
            print(e)
            return await ctx.send("Showing the leaderboards has failed!")

    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.command(name="hilo")
    async def hilo(self, ctx, bet=5, leverage=1):
        collection = db["Points"]
        stocks = [
            'GME', 'TSLA', 'GOOGL', 'NCR', 'NIO',
            'AMC', "AMZN", "AAPL", "TWTR", "MSFT",
            "MVIS", "NOK", "NVDA", "ATVI", "PLTR",
            "SNDL", "VGAC", "BP"
        ]

        query = {"id": ctx.author.id, "username": ctx.author.name}
        user = collection.find_one(query)

        if not user:
            return await ctx.send("You have not initialized an account yet! M.account init to start!")

        if not ctx.guild:
            return

        if leverage > 5:
            return await ctx.send("You must not use above 5x Leverage!")

        points = user["points"]

        if bet > points + 5:
            return await ctx.send("You can't bet more than what you already have!")

        symbol1 = random.choice(stocks)
        stocks.remove(symbol1)

        symbol2 = random.choice(stocks)
        stocks.remove(symbol2)

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

        embed = discord.Embed(
            title="Choose which stock you believe is higher in price!",
            description=f"Your two stocks are: \n1. {str(symbol1)}\n2. {str(symbol2)}\nYou only have 10 seconds to answer! Reply (1) for stock one, and (2) for stock two!",
            color=14177041
        )

        embed.set_footer(text="Higher Or Lower. @Copyright Alfie Phillips")

        await ctx.message.delete()
        await ctx.send(embed=embed)

        def check(m):
            return m.channel == ctx.message.channel and m.author == ctx.message.author

        def winning_embed(winner, symbol1, symbol2, stock_one, stock_two, amount):
            embed = discord.Embed(title=f"{winner} is a Winner!",
                                  description=f"{str(amount)} Points have been awarded to you!\n{symbol1}: ${stock_one}\n{symbol2}: ${stock_two}",
                                  color=3066993)
            embed.set_footer(text="Higher Or Lower. @Copyright Alfie Phillips")
            return embed

        def losing_embed(loser, symbol1, symbol2, stock_one, stock_two, amount):
            embed = discord.Embed(title=f"{loser} has lost!",
                                  description=f"{str(amount)} Points have been deducted from you!\n{symbol1}: ${stock_one}\n{symbol2}: ${stock_two}",
                                  color=15158332)
            embed.set_footer(text="Higher Or Lower. @Copyright Alfie Phillips")
            return embed

        def drawing_embed(draw, symbol1, symbol2, stock_one, stock_two, amount):
            embed = discord.Embed(title=f"{draw}, it is a draw!",
                                  description=f"{str(amount)} Points have been given to you for your luck!\n{symbol1}: ${stock_one}\n{symbol2}: ${stock_two}",
                                  color=9807270)
            embed.set_footer(text="Higher Or Lower. @Copyright Alfie Phillips")
            return embed

        try:
            reply = await self.bot.wait_for('message', timeout=10.0, check=check)

            reply = reply.content.lower().strip()

            collection = db["Points"]

            winning_amount = round((float(bet) * float(leverage)), 1)
            losing_amount = round((float(bet) * float(leverage)), 1)
            drawing_amount = (bet / 2)

            if reply == "1":
                if stock_one > stock_two:
                    try:
                        collection.update_one({"id": ctx.author.id, "username": ctx.author.name},
                                              {"$inc": {"points": winning_amount}})
                        return await ctx.send(
                            embed=winning_embed(ctx.author.name, symbol1=symbol1, symbol2=symbol2, stock_one=stock_one,
                                                stock_two=stock_two, amount=winning_amount))
                    except Exception as e:
                        print(e)
                        return await ctx.send("Error sending confirmation message, please contact a member of staff!")

                elif stock_one < stock_two:
                    try:
                        if user["points"] - losing_amount <= 0:
                            collection.update_one({"id": ctx.author.id, "username": ctx.author.name},
                                                  {"$set": {"points": 0}})
                            return await ctx.send(embed=losing_embed(ctx.author.name, symbol1=symbol1, symbol2=symbol2,
                                                                     stock_one=stock_one, stock_two=stock_two,
                                                                     amount=losing_amount))
                        collection.update_one({"id": ctx.author.id, "username": ctx.author.name},
                                              {"$inc": {"points": -losing_amount}})
                        return await ctx.send(
                            embed=losing_embed(ctx.author.name, symbol1=symbol1, symbol2=symbol2, stock_one=stock_one,
                                               stock_two=stock_two, amount=losing_amount))

                    except Exception as e:
                        print(e)
                        return await ctx.send("Error sending confirmation message, please contact a member of staff!")

                elif stock_one == stock_two:
                    try:
                        collection.update_one({"id": ctx.author.id, "username": ctx.author.name},
                                              {"$inc": {"points": drawing_amount}})
                        return await ctx.send(
                            embed=drawing_embed(ctx.author.name, symbol1=symbol1, symbol2=symbol2, stock_one=stock_one,
                                                stock_two=stock_two, amount=drawing_amount))

                    except Exception as e:
                        print(e)
                        return await ctx.send("Error sending confirmation message, please contact a member of staff!")

            elif reply == "2":
                if stock_two > stock_one:
                    try:
                        collection.update_one({"id": ctx.author.id, "username": ctx.author.name},
                                              {"$inc": {"points": winning_amount}})
                        return await ctx.send(
                            embed=winning_embed(ctx.author.name, symbol1=symbol1, symbol2=symbol2, stock_one=stock_one,
                                                stock_two=stock_two, amount=winning_amount))
                    except Exception as e:
                        print(e)
                        return await ctx.send("Error sending confirmation message, please contact a member of staff!")

                elif stock_two < stock_one:
                    try:
                        if user["points"] - losing_amount <= 0:
                            collection.update_one({"id": ctx.author.id, "username": ctx.author.name},
                                                  {"$set": {"points": 0}})
                            return await ctx.send(embed=losing_embed(ctx.author.name, symbol1=symbol1, symbol2=symbol2,
                                                                     stock_one=stock_one, stock_two=stock_two,
                                                                     amount=losing_amount))
                        collection.update_one({"id": ctx.author.id, "username": ctx.author.name},
                                              {"$inc": {"points": -losing_amount}})
                        return await ctx.send(
                            embed=losing_embed(ctx.author.name, symbol1=symbol1, symbol2=symbol2, stock_one=stock_one,
                                               stock_two=stock_two, amount=losing_amount))

                    except Exception as e:
                        print(e)
                        return await ctx.send("Error sending confirmation message, please contact a member of staff!")

                elif stock_two == stock_one:
                    try:
                        collection.update_one({"id": ctx.author.id, "username": ctx.author.name},
                                              {"$inc": {"points": drawing_amount}})
                        return await ctx.send(
                            embed=drawing_embed(ctx.author.name, symbol1=symbol1, symbol2=symbol2, stock_one=stock_one,
                                                stock_two=stock_two, amount=drawing_amount))

                    except Exception as e:
                        print(e)
                        return await ctx.send("Error sending confirmation message, please contact a member of staff!")

            else:
                return await ctx.send("Invalid reply! Please try again.")

        except asyncio.TimeoutError:
            return await ctx.send("Time has ran out!")

    @hilo.error
    async def hilo_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title="Slow it down!", description=f"Try again in {error.retry_after:.2f}s.", color=discord.Color.red())
            em.set_footer(text="@Copyright Alfie Phillips")
            await ctx.send(embed=em)

def setup(bot: commands.Bot):
    bot.add_cog(Games(bot=bot))
