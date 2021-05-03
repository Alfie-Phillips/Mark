import discord
from discord.ext import commands
from main import db
from datetime import datetime
from random import randrange

bot_channel = [806528778846994463]
talk_channels = [806526223483535372]

level = ["Caveman", "Noob", "Amateur", "Professional", "Expert", "God"]
levelnum = [5, 10, 15, 20, 30, 50]

collection = db["Levelling"]

class Levelling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        now = datetime.now()
        if message.channel.id in talk_channels:
            stats = collection.find_one({"id": message.author.id})
            if not message.author.bot:
                if stats is None:
                    new_user = {
                        "id": int(message.author.id),
                        "user": str(message.author),
                        "xp": 0,
                        "time-created": str(f"{now.year}/{now.month}/{now.day}/{now.hour}:{now.minute}.{now.second}")
                    }
                    try:
                        collection.insert_one(new_user)
                    except Exception as e:
                        print(e)

                else:
                    print("Here")
                    xp = stats["xp"] + 5
                    collection.update_one({"id": message.author.id}, {"$set": {"xp": xp}})
                    lvl = 0
                    while True:
                        if xp < ((50*(lvl**2))+(50*(lvl-1))):
                            break
                        lvl += 1
                        print(str(xp))
                        print("still checking")

                    print("past while loop " + str(xp))
                    xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                    if xp == 0:
                        await message.channel.send(f"Well done {message.author.mention}! You leveled up to **level {str(lvl)}**!")
                        for i in range(len(level)):
                            print("hello")
                            if lvl == levelnum[i]:
                                await message.channel.send("Thingy")
                                # await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=level[i]))
                                # embed = discord.Embed(description=f"{message.author.mention} you have gotten role **{level[i]}**!")
                                # embed.set_thumbnail(url=message.author.avatar_url)
                                # await message.channel.send(embed=embed)


    # @commands.command(name="rank")
    # async def rank(self, ctx, user=None):
    #     if ctx.message.channel_id == bot_channel:
    #         if user is None:
    #             stats = levelling.find_one({"id": ctx.author.id})
    #             if stats is None:
    #                 embed = discord.Embed(description="You haven't sent any messages yet!")
    #                 return await ctx.channel.send(embed=embed)
    #             else:
    #                 xp = stats["xp"]
    #                 lvl = 0
    #                 rank = 0
    #                 checking = True
    #                 while checking:
    #                     if xp < ((50*(lvl**2))+(50*(lvl-1))):
    #                         break
    #                     lvl += 1
    #                 xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
    #                 boxes = int((xp/(200*((1/2) * lvl)))*20)
    #                 rankings = levelling.find().sort("xp", -1)
    #                 for x in rankings:
    #                     rank += 1
    #                     if stats["id"] == x["id"]:
    #                         break
    #                 embed = discord.Embed(title=f"{ctx.author.name}'s level stats")
    #                 embed.add_field(name="Name", value=ctx.author.mention, inline=True)
    #                 embed.add_field(name="XP", value=f"{xp}/{int(200*((1/2)*lvl))}", inline=True)
    #                 embed.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}", inline=True)
    #                 embed.add_field(name="Progress Bar [lvl]", value=boxes * ":blue_square:" + (20 - boxes) * ":white_large_square:", inline=False)
    #                 embed.set_thumbnail(url=ctx.author.avatar_url)
    #                 return await ctx.channel.send(embed=embed)
    #         else:
    #             if isinstance(user, int):
    #                 try:
    #                     stats = levelling.find_one({"id": user})
    #                 except Exception as e:
    #                     print(e)
    #                     embed = discord.Embed(description="User with that id does not exist!")
    #                     return await ctx.send(embed=embed)

    #                 if stats is None:
    #                     embed = discord.Embed(description="This user hasn't sent any messages yet!")
    #                     return await ctx.channel.send(embed=embed)
    #                 else:
    #                     xp = stats["xp"]
    #                     lvl = 0
    #                     rank = 0
    #                     checking - True
    #                     while checking:
    #                          if xp < ((50*(lvl**2))+(50*(lvl-1))):
    #                             break
    #                          lvl += 1

    #                     xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
    #                     boxes = int((xp/(200*((1/2) * lvl)))*20)
    #                     rankings = levelling.find().sort("xp", -1)
    #                     for x in rankings:
    #                         rank += 1
    #                         if stats["id"] == x["id"]:
    #                             break

    #                     member = self.bot.get_user(user)
    #                     embed = discord.Embed(title=f"{member.name}'s level stats")
    #                     embed.add_field(name="Name", value=member.mention, inline=True)
    #                     embed.add_field(name="XP", value=f"{xp}/{int(200*((1/2)*lvl))}", inline=True)
    #                     embed.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}", inline=True)
    #                     embed.add_field(name="Progress Bar [lvl]", value=boxes * ":blue_square:" + (20 - boxes) * ":white_large_square:", inline=False)
    #                     embed.set_thumbnail(url=member.avatar_url)
    #                     return await ctx.channel.send(embed=embed)
    #             else:
    #                 try:
    #                     stats = levelling.find_one({"id": user.id})
    #                 except Exception as e:
    #                     print(e)
    #                     embed = discord.Embed(description="That user does not exist!")
    #                     return await ctx.send(embed=embed)

    #                 if stats is None:
    #                     embed = discord.Embed(description="This user hasn't sent any messages yet!")
    #                     return await ctx.channel.send(embed=embed)
    #                 else:
    #                     xp = stats["xp"]
    #                     lvl = 0
    #                     rank = 0
    #                     checking - True
    #                     while checking:
    #                          if xp < ((50*(lvl**2))+(50*(lvl-1))):
    #                             break
    #                          lvl += 1

    #                     xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
    #                     boxes = int((xp/(200*((1/2) * lvl)))*20)
    #                     rankings = levelling.find().sort("xp", -1)
    #                     for x in rankings:
    #                         rank += 1
    #                         if stats["id"] == x["id"]:
    #                             break

    #                     member = self.bot.get_user(user.id)
    #                     embed = discord.Embed(title=f"{member.name}'s level stats")
    #                     embed.add_field(name="Name", value=member.mention, inline=True)
    #                     embed.add_field(name="XP", value=f"{xp}/{int(200*((1/2)*lvl))}", inline=True)
    #                     embed.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}", inline=True)
    #                     embed.add_field(name="Progress Bar [lvl]", value=boxes * ":blue_square:" + (20 - boxes) * ":white_large_square:", inline=False)
    #                     embed.set_thumbnail(url=member.avatar_url)
    #                     return await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Levelling(bot))