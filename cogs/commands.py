
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

    def members(self):
        members = set(self.bot.get_all_members())
        d = {'online': 0, 'idle': 0, 'dnd': 0, 'offline': 0}
        for member in members:
            d[str(member.status)] += 1
        return d

    @commands.command(name="users")
    async def users(self, ctx):
        """Information about users"""
        members = self.members()
        await ctx.send(f'***Users Description***'
                       f'```Online: {members["online"]}\n'
                       f'Idle: {members["idle"]}\n'
                       f'DND: {members["dnd"]}\n'
                       f'Offline: {members["offline"]}```')

    @commands.command(name="members")
    async def member_count(self, ctx):
        """Member Count"""
        await ctx.send(f"```Members Of The Mark Tilbury Discord: {ctx.guild.member_count}```")


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

    def get_github_link(self, base_url: str, branch: str, command: str):
        obj = self.bot.get_command(command.replace('.', ' '))

        source = obj.callback.__code__
        module = obj.callback.__module__

        lines, firstlineno = inspect.getsourcelines(source)
        location = module.replace('.', '/')
        url = f'{base_url}/blob/{branch}/{location}.py#L{firstlineno}-L{firstlineno + len(lines) - 1}'
        return url

    @commands.command()
    async def source(self, ctx, *, command: str = None):
        """Get source code for the bot or any command."""
        base_url = "https://github.com/Alfie-Phillips/mark-tilbury"

        if command is None:
            return await ctx.send(base_url)
        cmd = self.bot.get_command(command)
        if cmd is None:
            return await ctx.send(f'That command does not exist:\n{base_url}')

        try:
            source = inspect.getsource(cmd.callback)
        except AttributeError:
            return await ctx.send(f'That command does not exist:\n{base_url}')

        url = self.get_github_link(base_url=base_url, branch='master', command=command)

        pages = to_pages_by_lines(source, max_size=1900)

        await ctx.send(f'Command {cmd.qualified_name}: {url}')

        for page in pages:
            page = page.replace("`", "`\u200b")
            await ctx.send(f'```py\n{page}```')

    @commands.command(name="socials", aliases=["links", "social-media"])
    async def socials(self, ctx):
        embed = discord.Embed(title="Mark's Social Links! :smile:", description="[Website](https://marktilbury.net/)\n[TikTok](https://www.tiktok.com/@marktilbury?lang=en)\n[Instagram](https://www.instagram.com/marktilbury)\n[Facebook](https://www.facebook.com/RealMarkTilbury)\n[Youtube](https://www.youtube.com/channel/UCxgAuX3XZROujMmGphN_scA)\n")
        await ctx.send(embed=embed)
        sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="stock-market")
    async def stock_market(self, ctx):
        embed = discord.Embed(title="The Stock Market", description="✦ What is the stock market? - The stock market is what allows people to buy and sell investments. On the stock market you can trade stocks, index funds, bonds, ETFs, reits, options, mutual funds, these are all ways you can invest in the stock market. Nerdwallet does a great example at defining the stock market, they state the following, “The concept behind how the stock market works is pretty simple. Operating much like an auction house, the stock market enables buyers and sellers to negotiate prices and make trades.” This basically means you are buying a small part of a company for a price determined on supply and demand. [More Info Here... :smile:](https://www.investopedia.com/terms/s/stockmarket.asp)")
        await ctx.send(embed=embed)
        sleep(1.5)
        await ctx.message.delete()


    @commands.command(name="stock-shares")
    async def stock_shares(self, ctx):
        embed = discord.Embed(title="Stock Shares", description="✦ What are stocks and shares? - Stocks are a small percent of a company sold on the stock market in the form of shares. Investopedia defines stocks as the following, “A stock (also known as equity) is a security that represents the ownership of a fraction of a corporation. This entitles the owner of the stock to a proportion of the corporation's assets and profits equal to how much stock they own. Units of stock are called 'shares'. [More Info Here... :smile:](https://www.investopedia.com/terms/s/stockmarket.asp)")
        await ctx.send(embed=embed)
        sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="stock-prices")
    async def stock_prices(self, ctx):
        embed = discord.Embed(title="Stock Prices", description='✦ What determines stock prices? - Stock prices are purely based on supply and demand, this is why sometimes a company may be doing amazing yet their stock may be dropping. So when investing in stocks or other types of investments it is important to look at EVERYTHING. This includes how the company is doing, public opinion, and the charts. Nerdwallet explains stock price as such, “That supply and demand help determine the price for each security, or the levels at which stock market participants — investors and traders — are willing to buy or sell.” And they also mention how buying and selling works, “Buyers offer a “bid,” or the highest amount they’re willing to pay, which is usually lower than the amount sellers “ask” for in exchange. This difference is called the bid-ask spread. For a trade to occur, a buyer needs to increase his price or a seller needs to decrease hers.” [More Info Here... :smile:](https://www.investopedia.com/terms/s/stockmarket.asp)')
        await ctx.send(embed=embed)
        sleep(1.5)
        await ctx.message.delete()

    
        


def setup(bot):
    bot.add_cog(Commands(bot))
        