import discord
from discord.ext import commands
from main import db
from datetime import datetime
from random import randrange

bot_channel = 741634902851846195
invalid_channels = [
    741634902851846195, 
    734883763678478417, 
    734883606555656334, 
    831600676680499261, 
    813403856263184414, 
    741641800183447602, 
    741041891222618152, 
    809046706401706024, 
    835226363748941824]

level = ["Level 5", "Level 10", "Level 20", "Level 30", "Level 50", "Level 75", "Level 100"]
levelnum = [5, 10, 20, 30, 50, 75, 100]
roleColor = ["Red", "Yellow", "Green", "Blue", "Pink", "Cyan", "Black"]
levelChannels = ["<#855017777931616306>", "<#855017863668695050>", "<#855017918378672158>", "<#855017968437035008>", "<#855018003786366976>", "<#855018157148209202>", "<#855018209270169620>"]

levelling = db["Levelling"]

class Levelling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        now = datetime.now()
        channel = self.bot.get_channel(bot_channel)
        if message.channel.id not in invalid_channels:
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
                        return await message.channel.send("There has been an error registering your message, please report this to a staff member!")

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
                        for i in range(len(level)):
                            if lvl == levelnum[i]:
                                for role in level:
                                    userRole = discord.utils.get(message.author.guild.roles, name=role)
                                    await message.author.remove_roles(userRole)

                                await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=level[i]))
                                return await channel.send(f"{message.author.mention} you have reached level {str(lvl)}! You have unlocked the color **{roleColor[i]}**. Please visit {levelChannels[i]} for your prize!")


                        return await channel.send(f"{message.author.mention} you have reached level {str(lvl)}!")

    @commands.command(name="rank", help="Check your xp.")
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


    @commands.command(name="lb", aliases=["leaderboard"], help="XP leaderboard")
    async def leaderboard(self, ctx):
        if ctx.channel.id == bot_channel:
            rankings = levelling.find({}).sort("xp", -1)
            i = 1
            embed = discord.Embed(title="Top 10 Rankings", color=discord.Color.blue())
            for x in rankings:
                try:
                    tempxp = x["xp"]
                    tempname = x["user"]
                    embed.add_field(name=f"{i}: {tempname}", value=f"Total XP: {tempxp}", inline=False)
                    i+= 1
                except Exception as e:
                    print(e)
                    return await ctx.send(embed=discord.Embed(title="Error!", description="Failed getting the leaderboard!", color=discord.Color.red()))
                if i == 11:
                    break
            await ctx.channel.send(embed=embed)
        else:
            return await ctx.channel.send(embed=discord.Embed(title="Error!", description="Please use the bots channel!", color=discord.Color.red()))


def setup(bot):
    bot.add_cog(Levelling(bot))