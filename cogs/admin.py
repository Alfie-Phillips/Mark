import asyncio
from main import db

import discord
from discord.ext import commands

suggestion_channel = 747165320510308393
levelling = db["Levelling"]
points = db["Points"]
reports = db["Reports"]

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="accept", help="This is a Staff Command.")
    @commands.has_role("Moderator")
    async def accept(self, ctx, message_id: int, *, reason="None"):
        if not ctx.guild:
            return

        channel = self.bot.get_channel(suggestion_channel)
        try:
            message = await channel.fetch_message(message_id)
            await ctx.message.delete()

            author = message.embeds[0].author
            suggestion = message.embeds[0].fields[0].value
            name = author.name
            icon_url = author.icon_url
            em = discord.Embed(color=3340850)
            em.set_author(name=f"{name}", icon_url=f"{icon_url}")
            em.set_thumbnail(
                url="https://yt3.ggpht.com/ytc/AAUvwnhl2_dBWn3rL1fe5j7O0qDMKuAK-eorFyMk1NyiVQ=s900-c-k-c0x00ffffff-no-rj")
            em.add_field(name=f"Suggestion:", value=f"{suggestion}\n\n", inline=True)
            em.add_field(name=f"Status", value="Accepted ✅", inline=False)
            em.add_field(name=f"Staff answer by @{ctx.author.name}", value=f"{reason}")
            em.set_footer(text="@Copyright Alfie Phillips")
            return await message.edit(embed=em)

        except:
            await ctx.message.delete()
            return await ctx.send(f"{ctx.author.mention}. Message with id: {str(message_id)} was not found!")

    @commands.command(name="decline", help="This is a Staff Command.")
    @commands.has_role("Moderator")
    async def decline(self, ctx, message_id: int, *, reason="None"):
        if not ctx.guild:
            return

        channel = self.bot.get_channel(suggestion_channel)
        try:
            message = await channel.fetch_message(message_id)
            await ctx.message.delete()

            author = message.embeds[0].author
            suggestion = message.embeds[0].fields[0].value
            name = author.name
            icon_url = author.icon_url
            em = discord.Embed(color=16718080)
            em.set_author(name=f"{name}", icon_url=f"{icon_url}")
            em.set_thumbnail(
                url="https://yt3.ggpht.com/ytc/AAUvwnhl2_dBWn3rL1fe5j7O0qDMKuAK-eorFyMk1NyiVQ=s900-c-k-c0x00ffffff-no-rj")
            em.add_field(name=f"Suggestion:", value=f"{suggestion}\n\n", inline=True)
            em.add_field(name=f"Status", value="Declined ❌", inline=False)
            em.add_field(name=f"Staff answer by @{ctx.author.name}", value=f"{reason}")
            em.set_footer(text="@Copyright Alfie Phillips")
            await message.edit(embed=em)

        except:
            await ctx.message.delete()
            return await ctx.send(f"{ctx.author.mention}. Message with id: ({str(message_id)}) was not found!")

    @commands.command(name="add", help="This is a Staff Command.")
    @commands.has_role("Moderator")
    async def add(self, ctx, name, user: discord.Member, amount=100):
        if amount > 10000:
            return await ctx.send("You can't add over 10000 at a time!")

        if name == "xp":
            try:
                levelling.update_one({"id": user.id}, {"$inc": {"xp": amount}})
                return await ctx.send(embed=discord.Embed(description=f"XP added to {user.display_name}"))
            except Exception as e:
                print(e)
                return await ctx.send(embed=discord.Embed(title="Error!", description="Error adding XP!", color=discord.Color.red()))

        if name == "points":
            try:
                points.update_one({"id": user.id}, {"$inc": {"points": amount}})
                return await ctx.send(embed=discord.Embed(description=f"Points added to {user.display_name}"))
            except Exception as e:
                print(e)
                return await ctx.send(embed=discord.Embed(title="Error!", description="Error adding points!", color=discord.Color.red()))


    @commands.command(name="remove", help="This is a Staff Command.")
    @commands.has_role("Moderator")
    async def remove(self, ctx, name, user: discord.Member, amount=100):
        if amount > 10000:
            return await ctx.send("You can't add over 10000 at a time!")

        if name == "xp":
            try:
                levelling.update_one({"id": user.id}, {"$inc": {"xp": -amount}})
                return await ctx.send(embed=discord.Embed(description=f"XP removed from {user.display_name}"))
            except Exception as e:
                print(e)
                return await ctx.send(embed=discord.Embed(title="Error!", description="Error removing XP!", color=discord.Color.red()))

        if name == "points":
            try:
                points.update_one({"id": user.id}, {"$inc": {"points": -amount}})
                return await ctx.send(embed=discord.Embed(description=f"Points removed from {user.display_name}"))
            except Exception as e:
                print(e)
                return await ctx.send(embed=discord.Embed(title="Error!", description="Error removing points!", color=discord.Color.red()))

    
    # @commands.command(name="get-reports", help="This is a staff command.")
    # @commands.has_role("Moderator")
    # async def get_reports(self, ctx, limit=10):
    #     if limit > 50:
    #         return await ctx.send("")
    #     data = reports.find({}).limit(limit).sort("ordinal", 1)
    #     leaderboard = {}
    #     for entry in data:
    #         print(entry)



        

def setup(bot):
    bot.add_cog(Admin(bot))