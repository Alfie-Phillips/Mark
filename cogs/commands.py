
from discord.ext import commands
import discord
from datetime import datetime, timedelta
from discord.utils import get
import aiohttp
import zlib
import re
import os
import io
from time import sleep

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="website", aliases=["web", "webpage"])
    async def website(self, ctx):
        """Links for Mark's Website"""
        embed = discord.Embed(title="Mark's Website", description="[Link Here... :smile:](https://marktilbury.net/)")
        await ctx.send(embed=embed)
        sleep(1.5)
        await ctx.message.delete()


    @commands.command(name="tiktok", aliases=["toktik"])
    async def links(self, ctx):
        """Links for Mark's socials"""
        embed = discord.Embed(title="Mark's TikTok", description="[Link Here... :smile:](https://www.tiktok.com/@marktilbury?lang=en)")
        await ctx.send(embed=embed)
        sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="instagram", aliases=["insta"])
    async def instagram(self, ctx):
        """Links for Mark's Instagram"""
        embed = discord.Embed(title="Mark's Instagram", description="[Link Here... :smile:](https://www.instagram.com/marktilbury)")
        await ctx.send(embed=embed)
        sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="facebook")
    async def facebook(self, ctx):
        """Links for Mark's Facebook"""
        embed = discord.Embed(title="Mark's Facebook", description="[Link Here... :smile:](https://www.facebook.com/RealMarkTilbury)")
        await ctx.send(embed=embed)
        sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="youtube")
    async def youtube(self, ctx):
        """Links for Mark's Youtube"""
        embed = discord.Embed(title="Mark's Youtube Channel", description="[Link Here... :smile:](https://www.youtube.com/channel/UCxgAuX3XZROujMmGphN_scA)")
        await ctx.send(embed=embed)
        sleep(1.5)
        await ctx.message.delete()



def setup(bot):
    bot.add_cog(Commands(bot))
        