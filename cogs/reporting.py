import discord
from discord.ext import commands
from datetime import datetime
from time import sleep
import asyncio
from discord.ext.commands import cooldown, BucketType
from main import db

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(name="report")
    async def report(self, ctx, user : discord.Member, *reason):
        collection = db["Reports"]
        mod_channel = self.bot.get_channel(734883606555656334)
        author = ctx.message.author
        now = datetime.now()
        rearray = ' '.join(reason[:]) 
        if user.bot:
            message = await ctx.send(f"You can't report a bot! {ctx.author.mention}")
            await asyncio.sleep(2)
            await ctx.message.delete()
            await asyncio.sleep(2)
            await message.delete()
        elif user == ctx.message.author:
            message = await ctx.send(f"You can't report yourself! {ctx.author.mention}")
            await asyncio.sleep(2)
            await ctx.message.delete()
            await asyncio.sleep(2)
            await message.delete()

        elif not rearray: 
            message = await ctx.send(f"{author.mention} has reported {user.mention}\nReason: Not provided")
            await ctx.message.delete()
            await mod_channel.send(f"{author.mention} has reported {user.mention}\nReason: Not provided\n\n<@&734889524303495279>")
            query = {
                "author-id": ctx.author.id,
                "author-name": ctx.author.name,
                "reported-user-id": user.id,
                "reported-user-name": user.name,
                "reason": None,
                "message-link": f"https://discordapp.com/channels/{ctx.guild.id}/{message.channel.id}/{message.id}",
                "time-created": f"{now.year}/{now.month}/{now.day}/{now.hour}:{now.minute}.{now.second}" 
            }
            collection.insert_one(query)
            return 
        else:
            message = await ctx.send(f"{author.mention} has reported {user.mention}\nReason: {rearray}")
            await ctx.message.delete()
            await mod_channel.send(f"{author.mention} has reported {user.mention}\nReason: {rearray}\n\n<@&734889524303495279>")
            query = {
                "author-id": ctx.author.id,
                "author-name": ctx.author.name,
                "reported-user-id": user.id,
                "reported-user-name": user.name,
                "reason": rearray,
                "message-link": f"https://discord.com/channels/{ctx.guild.id}/{message.channel.id}/{message.id}",
                "time-created": f"{now.year}/{now.month}/{now.day}/{now.hour}:{now.minute}.{now.second}" 
            }
            collection.insert_one(query)
            return 
    

    @report.error
    async def report_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title=f"Slow it down!",description=f"Try again in {error.retry_after:.2f}s.")
            await ctx.send(embed=em)

        else:
            print(error)


def setup(bot: commands.Bot):
    bot.add_cog(Moderation(bot=bot))
