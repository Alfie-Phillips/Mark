# Imports here...

import asyncio
from datetime import datetime
import time

import discord
from discord.ext import commands

from main import db


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 120, commands.BucketType.user)
    @commands.command(name="report", help="Report a user to the staff team.")
    async def report(self, ctx, user: discord.Member, *reason):
        
        now = datetime.now()
        ordinal = time.time()
        collection = db["Reports"]
        mod_channel = self.bot.get_channel(734883606555656334)
        author = ctx.message.author
        rearray = ' '.join(reason[:])
        
        if user.bot:
            message = await ctx.send(f"You can't report a bot! {ctx.author.mention}")
            await ctx.message.delete()
            await message.delete()
            
        elif user == ctx.message.author:
            message = await ctx.send(f"You can't report yourself! {ctx.author.mention}")
            await ctx.message.delete()
            await message.delete()

        elif not rearray:
            await ctx.message.delete()
            await mod_channel.send(
                f"{author.display_name} has reported {user.display_name}\nReason: Not provided\n\n<@&734889524303495279>")
            
            query = {
                "author-id": ctx.author.id,
                "author-name": ctx.author.name,
                "reported-user-id": user.id,
                "reported-user-name": user.name,
                "reason": None,
                "message-link": f"https://discordapp.com/channels/{ctx.guild.id}/{ctx.message.channel.id}/{ctx.message.id}",
                "time-created": f"{now.year}/{now.month}/{now.day}/{now.hour}:{now.minute}.{now.second}",
                "ordinal": ordinal
            }
            
            try:
                
                collection.insert_one(query)
                
            except Exception as e:
                
                print(e)
                return await ctx.send(embed=discord.Embed(title="Error!", description="Error making the report! Please try again."))
            
        else:
            await ctx.message.delete()
            
            em = discord.Embed(title=f"{author.display_name} has reported {user.display_name}", color=discord.Color.light_grey())
            em.add_field(name="Reason", value=f"{rearray}", inline=False)
            
            await mod_channel.send(embed=em)
            
            query = {
                "author-id": ctx.author.id,
                "author-name": ctx.author.name,
                "reported-user-id": user.id,
                "reported-user-name": user.name,
                "reason": rearray,
                "message-link": f"https://discord.com/channels/{ctx.guild.id}/{ctx.message.channel.id}/{ctx.message.id}",
                "time-created": f"{now.year}/{now.month}/{now.day}/{now.hour}:{now.minute}.{now.second}",
                "ordinal": ordinal
            }
            try:
                
                collection.insert_one(query)
                
            except Exception as error:
                
                print(error)
                return await ctx.send(embed=discord.Embed(title="Error!", description="Error making the report! Please try again."))
            
    @commands.Cog.listener(name='on_message')
    async def mark_twitter(self, message):
        if "mark" in message.content.lower() and "twitter" in message.content.lower():
            await message.channel.send("Mark **DOES NOT** have a Twitter account. Please report and block the user.")

    @report.error
    async def report_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            
            em = discord.Embed(title="Slow it down!", description=f"Try again in {error.retry_after:.2f}s.", color=discord.Color.red())
            await ctx.send(embed=em)
            
        else:
            print(error)


def setup(bot: commands.Bot):
    bot.add_cog(Moderation(bot=bot))
