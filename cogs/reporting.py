import discord
from discord.ext import commands
import datetime
from time import sleep
import asyncio
from discord.ext.commands import cooldown, BucketType

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command("report")
    async def report(self, ctx, user : discord.Member, *reason):
        mod_channel = self.bot.get_channel(734883606555656334)
        author = ctx.message.author
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
            await ctx.send(f"{author.mention} has reported {user.mention}\nReason: Not provided")
            await ctx.message.delete()
            await mod_channel.send(f"{author.mention} has reported {user.mention}\nReason: Not provided\n\n<@&734889524303495279>")
        else:
            await ctx.send(f"{author.mention} has reported {user.mention}\nReason: {rearray}")
            await ctx.message.delete()
            await mod_channel.send(f"{author.mention} has reported {user.mention}\nReason: {rearray}\n\n<@&734889524303495279>")

def setup(bot: commands.Bot):
    bot.add_cog(Moderation(bot=bot))
