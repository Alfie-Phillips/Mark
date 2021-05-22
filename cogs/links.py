import asyncio
from curses.panel import bottom_panel
from datetime import datetime

import discord
from discord.ext import commands

class Links(commands.Cog()):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="website", aliases=["web", "webpage"])
    async def website(self, ctx):
        """Links for Mark's Website"""
        embed = discord.Embed(title="Mark's Website", description="[Link Here... :smile:](https://marktilbury.net/)", color=discord.Color.green())
        embed.set_footer(text="@Copyright Alfie Phillips")
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="tiktok")
    async def tiktok(self, ctx):
        """Links for Mark's socials"""
        embed = discord.Embed(title="Mark's TikTok",
                              description="[Link Here... :smile:](https://www.tiktok.com/@marktilbury?lang=en)", color=discord.Color.green())
        embed.set_footer(text="@Copyright Alfie Phillips")
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="instagram", aliases=["insta"])
    async def instagram(self, ctx):
        """Links for Mark's Instagram"""
        embed = discord.Embed(title="Mark's Instagram",
                              description="[Link Here... :smile:](https://www.instagram.com/marktilbury)", color=discord.Color.green())
        embed.set_footer(text="@Copyright Alfie Phillips")
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="facebook")
    async def facebook(self, ctx):
        """Links for Mark's Facebook"""
        embed = discord.Embed(title="Mark's Facebook",
                              description="[Link Here... :smile:](https://www.facebook.com/RealMarkTilbury)", color=discord.Color.green())
        embed.set_footer(text="@Copyright Alfie Phillips")
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="youtube")
    async def youtube(self, ctx):
        """Links for Mark's Youtube"""
        embed = discord.Embed(title="Mark's Youtube Channel",
                              description="[Link Here... :smile:](https://www.youtube.com/channel/UCxgAuX3XZROujMmGphN_scA)", color=discord.Color.green())
        embed.set_footer(text="@Copyright Alfie Phillips")
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="socials", aliases=["links", "social-media"])
    async def socials(self, ctx):
        embed = discord.Embed(title="Mark's Social Links! :smile:",
                              description="[Website](https://marktilbury.net/)\n[TikTok](https://www.tiktok.com/@marktilbury?lang=en)\n[Instagram](https://www.instagram.com/marktilbury)\n[Facebook](https://www.facebook.com/RealMarkTilbury)\n[Youtube](https://www.youtube.com/channel/UCxgAuX3XZROujMmGphN_scA)\n", color=discord.Color.green())
        embed.set_footer(text="@Copyright Alfie Phillips")
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="link-tree")
    async def link_tree(self, ctx):
        embed = discord.Embed(title="Mark's Link Tree!",
                              description="[Link to it here... :smile:](https://marktilbury.net/clickhere)", color=discord.Color.green())
        embed.set_footer(text="@Copyright Alfie Phillips")
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(Links(bot))
