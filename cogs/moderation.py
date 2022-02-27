import asyncio
import time
import discord

from envconfig import *
from datetime import datetime
from discord.ext import commands
from main import db


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 120, commands.BucketType.user)
    @commands.command(name="report", help="Report a user to the staff team.")
    async def report(self, ctx, user: discord.Member, *reason):
        """
        Report a user using the Mark Tilbury Bot
        """

        # Vars
        now = datetime.now()
        ordinal = time.time()
        collection = db["Reports"]
        mod_channel = self.bot.get_channel(int(MODERATOR_CHANNEL))
        author = ctx.message.author
        rearray = ' '.join(reason[:])
        
        # Check if the reported user is a bot
        if user.bot:
            message = await ctx.send(f"You can't report a bot! {ctx.author.mention}")
            await ctx.message.delete()
            await message.delete()
        
        # Check if the user has reported themselves
        elif user == ctx.message.author:
            message = await ctx.send(f"You can't report yourself! {ctx.author.mention}")
            await ctx.message.delete()
            await message.delete()

        # Check if there is no reason provided
        elif not rearray:
            # Delete the original message
            await ctx.message.delete()

            # Send to the 'moderation' channel
            await mod_channel.send(
                f"{author.display_name} has reported {user.display_name}\nReason: Not provided\n\n<@&734889524303495279>")
            
            # Create a new 'report' query
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
            
            # Insert the report into the database
            try:
                
                collection.insert_one(query)
                
            except Exception as error:
                # Handle database rejection

                raise error
                return await ctx.send(embed=discord.Embed(title="Error!", description="Error making the report! Please try again."))
            
        else:
            # Delete the original message
            await ctx.message.delete()
            
            # Create a new embed message
            em = discord.Embed(title=f"{author.display_name} has reported {user.display_name}", color=discord.Color.light_grey())
            em.add_field(name="Reason", value=f"{rearray}", inline=False)
            
            # Send to the 'moderation' channel
            await mod_channel.send(embed=em)
            
            # Create a new 'report' query
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

            # Insert the report into the database
            try:
                
                collection.insert_one(query)
                
            except Exception as error:
                # Handle database rejection

                raise error
                return await ctx.send(embed=discord.Embed(title="Error!", description="Error making the report! Please try again."))

    @report.error
    async def report_error(self, ctx, error):
        """
        Handle discord errors
        """
        if isinstance(error, commands.CommandOnCooldown):
            
            em = discord.Embed(title="Slow it down!", description=f"Try again in {error.retry_after:.2f}s.", color=discord.Color.red())
            await ctx.send(embed=em)
            
        else:
            raise error


def setup(bot: commands.Bot):
    bot.add_cog(Moderation(bot=bot))
