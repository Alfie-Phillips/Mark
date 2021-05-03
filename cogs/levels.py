import discord
from discord.ext import commands
from main import db
from datetime import datetime
from random import randrange

bot_channel = 806528778846994463
talk_channels = [806526223483535372]

level = ["Caveman", "Noob", "Amateur", "Professional", "Expert", "God", "Mark"]
levelnum = [2, 5, 10, 15, 20, 30, 50]

levelling = db["Levelling"]

class Levelling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        now = datetime.now()
        if message.channel.id in talk_channels:
            stats = levelling.find_one({"id": message.author.id})
            if not message.author.bot:
                if stats is None:
                    new_user = {
                        "id": int(message.author.id),
                        "user": str(message.author),
                        "xp": 0,
                        "time-created": str(f"{now.year}/{now.month}/{now.day}/{now.hour}:{now.minute}.{now.second}")
                    }

                    try:
                        levelling.insert_one(new_user)
                    except Exception as e:
                        print(e)

                else:
                    xp = stats["xp"] + 5
                    levelling.update_one({"id": message.author.id}, {"$set": {"xp": xp}})
                    lvl = 0
                    while True:
                        if xp < ((50 * (lvl**2)) + (50 * (lvl - 1))):
                            break
                        lvl += 1

                    xp -= ((50 * ((lvl - 1)**2)) + (50 * (lvl - 1)))
                    if xp == 0:
                        await message.channel.send(embed=discord.Embed(title="Levelled Up!", description=f"Well done {message.author.mention}! You leveled up to **level {str(lvl)}**!", color=discord.Color.green()))
                        for i in range(len(level)):
                            if lvl == levelnum[i]:
                                await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=level[i]))
                                embed = discord.Embed(title="New Role!", description=f"{message.author.mention} you have gotten role **{level[i]}**!", color=discord.Color.green())
                                embed.set_thumbnail(url=message.author.avatar_url)
                                await message.channel.send(embed=embed)


    @commands.command(name="rank")
    async def rank(self, ctx, user: discord.Member=None):
        if ctx.channel.id == bot_channel:
            if user == None:
                stats = levelling.find_one({"id": ctx.author.id})
                if stats is None:
                    embed = discord.Embed(title="Error!", description="You haven't sent any messages!", color=discord.Color.red())
                    return await ctx.send(embed=embed)
                else:
                    xp = stats["xp"]
                    lvl = 0
                    rank = 0
                    while True:
                        if xp < ((50*(lvl**2))+(50*lvl)):
                            break
                        lvl += 1
                    xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                    boxes = int((xp/(200*((1/2) * lvl)))*20)
                    rankings = levelling.find().sort("xp", -1)
                    for x in rankings:
                        rank += 1
                        if stats["id"] == x["id"]:
                            break
                    embed = discord.Embed(title=f"{ctx.author.name}'s level stats", color=discord.Color.blue())
                    embed.add_field(name="Level", value=f"{lvl}")
                    embed.add_field(name="XP", value=f"{xp}/{int(200*((1/2)*lvl))}", inline=True)
                    embed.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}", inline=True)
                    embed.add_field(name="Progress Bar [lvl]", value=boxes * ":blue_square:" + (20 - boxes) * ":white_large_square:", inline=False)
                    embed.set_thumbnail(url=ctx.author.avatar_url)
                    return await ctx.channel.send(embed=embed)

            else:
                stats = levelling.find_one({"id": user.id})
                if stats is None:
                    embed = discord.Embed(title="Error!", description="You haven't sent any messages!", color=discord.Color.red())
                    return await ctx.send(embed=embed)
                else:
                    xp = stats["xp"]
                    lvl = 0
                    rank = 0
                    while True:
                        if xp < ((50*(lvl**2))+(50*lvl)):
                            break
                        lvl += 1
                    xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                    boxes = int((xp/(200*((1/2) * lvl)))*20)
                    rankings = levelling.find().sort("xp", -1)
                    for x in rankings:
                        rank += 1
                        if stats["id"] == x["id"]:
                            break
                    embed = discord.Embed(title=f"{user.name}'s level stats", color=discord.Color.blue())
                    embed.add_field(name="Level", value=f"{lvl}")
                    embed.add_field(name="XP", value=f"{xp}/{int(200*((1/2)*lvl))}", inline=True)
                    embed.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}", inline=True)
                    embed.add_field(name="Progress Bar [lvl]", value=boxes * ":blue_square:" + (20 - boxes) * ":white_large_square:", inline=False)
                    embed.set_thumbnail(url=user.avatar_url)
                    return await ctx.channel.send(embed=embed)

        else:
            return await ctx.send(embed=discord.Embed(title="Error!", description="Please use the bots channel!", color=discord.Color.red()))


    @commands.command(name="lb", aliases=["leaderboard", "leader-board"])
    async def leaderboard(self, ctx):
        if ctx.channel.id == bot_channel:
            rankings = levelling.find({}).sort("xp", -1)
            i = 1
            embed = discord.Embed(title="Top 10 Rankings", color=discord.Color.blue())
            for x in rankings:
                try:
                    temp = ctx.guild.get_member(x["id"])
                    tempxp = x["xp"]
                    embed.add_field(name=f"{i}: {temp.name}", value=f"Total XP: {tempxp}", inline=False)
                    i+= 1
                except:
                    return await ctx.send(embed=discord.Embed(title="Error!", description="Failed getting the leaderboard!", color=discord.Color.red()))
                if i == 11:
                    break
            await ctx.channel.send(embed=embed)
        else:
            return await ctx.channel.send(embed=discord.Embed(title="Error!", description="Please use the bots channel!", color=discord.Color.red()))

    @commands.command(name="add")
    @commands.has_role("Admin")
    async def add(self, ctx, name, user: discord.Member, amount=100):
        if name == "xp":
            try:
                levelling.update_one({"id": user.id}, {"$inc": {"xp": amount}})
                return await ctx.send(embed=discord.Embed(description=f"Score added to {user.display_name}"))
            except Exception as e:
                print(e)
                return await ctx.send(embed=discord.Embed(title="Error!", description="Error adding score!"), color=discord.Color.red())

def setup(bot):
    bot.add_cog(Levelling(bot))