import asyncio
from discord.ext import commands
from discord.ext.commands import has_permissions
import discord
from datetime import datetime, timedelta
from discord.utils import get
import aiohttp
from time import sleep
from .utils.time import human_timedelta

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
        await asyncio.sleep(1.5)
        await ctx.message.delete()


    @commands.command(name="tiktok", aliases=["toktik"])
    async def links(self, ctx):
        """Links for Mark's socials"""
        embed = discord.Embed(title="Mark's TikTok", description="[Link Here... :smile:](https://www.tiktok.com/@marktilbury?lang=en)")
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="instagram", aliases=["insta"])
    async def instagram(self, ctx):
        """Links for Mark's Instagram"""
        embed = discord.Embed(title="Mark's Instagram", description="[Link Here... :smile:](https://www.instagram.com/marktilbury)")
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="facebook")
    async def facebook(self, ctx):
        """Links for Mark's Facebook"""
        embed = discord.Embed(title="Mark's Facebook", description="[Link Here... :smile:](https://www.facebook.com/RealMarkTilbury)")
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="youtube")
    async def youtube(self, ctx):
        """Links for Mark's Youtube"""
        embed = discord.Embed(title="Mark's Youtube Channel", description="[Link Here... :smile:](https://www.youtube.com/channel/UCxgAuX3XZROujMmGphN_scA)")
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
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
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="stock-market")
    async def stock_market(self, ctx):
        embed = discord.Embed(title="The Stock Market", description="✦ What is the stock market? - The stock market is what allows people to buy and sell investments. On the stock market you can trade stocks, index funds, bonds, ETFs, reits, options, mutual funds, these are all ways you can invest in the stock market. Nerdwallet does a great example at defining the stock market, they state the following, “The concept behind how the stock market works is pretty simple. Operating much like an auction house, the stock market enables buyers and sellers to negotiate prices and make trades.” This basically means you are buying a small part of a company for a price determined on supply and demand. [More Info Here... :smile:](https://www.investopedia.com/terms/s/stockmarket.asp)")
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()


    @commands.command(name="stock-shares")
    async def stock_shares(self, ctx):
        embed = discord.Embed(title="Stock Shares", description="✦ What are stocks and shares? - Stocks are a small percent of a company sold on the stock market in the form of shares. Investopedia defines stocks as the following, “A stock (also known as equity) is a security that represents the ownership of a fraction of a corporation. This entitles the owner of the stock to a proportion of the corporation's assets and profits equal to how much stock they own. Units of stock are called 'shares'. [More Info Here... :smile:](https://www.investopedia.com/terms/s/stockmarket.asp)")
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="stock-prices")
    async def stock_prices(self, ctx):
        embed = discord.Embed(title="Stock Prices", description='✦ What determines stock prices? - Stock prices are purely based on supply and demand, this is why sometimes a company may be doing amazing yet their stock may be dropping. So when investing in stocks or other types of investments it is important to look at EVERYTHING. This includes how the company is doing, public opinion, and the charts. Nerdwallet explains stock price as such, “That supply and demand help determine the price for each security, or the levels at which stock market participants — investors and traders — are willing to buy or sell.” And they also mention how buying and selling works, “Buyers offer a “bid,” or the highest amount they’re willing to pay, which is usually lower than the amount sellers “ask” for in exchange. This difference is called the bid-ask spread. For a trade to occur, a buyer needs to increase his price or a seller needs to decrease hers.” [More Info Here... :smile:](https://www.investopedia.com/terms/s/stockmarket.asp)')
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="stock-types")
    async def stock_type(self, ctx):
        embed = discord.Embed(title="Stock Types", description='✦ What types of stocks are there? - There are different groups of stock that serve different purposes in your portfolio. • Income/Dividend Stock - These stocks usually do not have crazy growth but rather high dividends yields which usually comes with higher payout ratios. These companies will usually payout every month, quarter, semi-annually, or yearly. • Cyclical Stock - These are stocks who will have ups and downs based on the economy and are more sensitive when there is an economic downturn. •Blue Chip Stocks -  Very safe stocks usually from big companies with large market caps. These companies will usually be a well known name like Walmart, Apple, or Coca Cola. These companies are more than likely to be financially sound and survive economic crashes. • Tech Stocks - Companies based around technology. These usually have the most growth but also come with an associated risk. Technology advances fast meaning if the company does not keep up it can fall out of favor. • Speculative Stocks - Usually extreme risk, these are companies that are new and usually don’t have much history or financial stability. These companies can bring immense profits as well as risk. • Defensive Stocks - Stocks that are extremely safe, these companies have been around for centuries sometimes and are impossible to stop. These stocks will do good and recover from crashes and sometimes even profit. Examples are prominent in the consumer staples sector, an example is Walmart. • Growth Stocks - Most do not pay out dividends as they would rather keep that money and reinvest it into their company for more growth. These stocks will bring good growth and profit is only made on capital gains. [More Info Here... :smile:](https://www.investopedia.com/terms/s/stockmarket.asp)')
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="brokers")
    async def brokerages(self, ctx):
        embed = discord.Embed(title="Brokerages", description='✦ What is a broker and brokerage? - A brokerage account is what will allow you to buy and sell stocks. Without a broker you cannot trade, when you decide to buy a stock it is sent to the broker (this used to be a real person on the floors of the NYSE, now it is all automatic), they will buy it for you and be the middleman. ✦ Can you invest in the stock market under the age of 18? - Yes, you can invest in the stock market under the age of 18, but only with the permission and having a parent signed on with you. In the UK you will need to open what is called a junior stocks and shares ISA, in the US you need what is called a custodial account. Both of these are accounts that belong to your parents until you are 18 and then owner ship is transferred to you, this will allow you to access the stock market and invest. You can find these by looking it up on google or going to your bank, as they will most likely help you set one up or recommend one. ✦ What are some good and trust worthy brokerage accounts? - Brokerages will depend on your location for the EU, typically Trading 212, Interactive Brokers, and EToro are used. For the US brokers like Webull, Robinhood (which is not a good choice as it is being investigated by the SEC, is very unreliable, and has a 10 million dollar lawsuit), Charles Schwab, E*TRADE, Think Or Swim, TD Ameritrade, are all great brokers. When choosing your broker it is a good idea to look at them all to see which one applies to what you are looking for. ✦ What is paper trading? - Paper trading is the act of trading with simulated money, this is most commonly used for practice. Investopedia says the following, "A paper trade is a simulated trade that allows an investor to practice buying and selling without risking real money." [More Info Here... :smile:](https://www.investopedia.com/terms/s/stockbroker.asp)')
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="index-funds", aliases=["etfs", "etf", "funds"])
    async def index_and_etf(self, ctx):
        embed = discord.Embed(title="Index Funds And ETF'S", description='- ETFs and Index Funds are both great ways to diversify investments, but how are they different? The main and biggest differences for the investor is cost, ETFs and Index Funds will have different costs associated with them for the investor. Index Funds are rebalanced daily which come in the form of commissions and other costs. ETFs on the other hand have another system as defined by Investopedia, " ETFs have a unique process called creation/redemption in-kind (meaning shares of ETFs can be created and redeemed with a like basket of securities) that avoids these transaction costs." Index Funds also have the cost of cash drag, which  ETFs do not have to deal with. However an advantage that Index Funds have over ETFs is when it comes to dividends. Index Funds will immediately reinvest their dividends compared to ETFs which pool them up and pay them out at the end of each quarter. ETFs also have lower management fees. However the biggest cost in ETFs is the shareholder transaction cost, which is usually 0 for Index Funds. \n[Index Funds](https://www.investopedia.com/terms/i/indexfund.asp) \n[ETF](https://www.investopedia.com/terms/e/etf.asp)')
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="freetrade")
    async def freetrade(self, ctx):
        embed = discord.Embed(title="Get A Free Stock On FreeTrade!", description="[Mark Tilbury's Promo Code Here... :smile:](https://freetrade.app.link/DiVJxPU22bb?_p=c11c32dc9e0b7af1e61890f4e0)")
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="public")
    async def public(self, ctx):
        embed = discord.Embed(title="Get A Free Stock On Public!", description="[Mark Tilbury's Promo Code Here... :smile:](https://public.com/mark)")
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="free-stocks")
    async def free_stocks(self, ctx):
        embed = discord.Embed(title="Free Stocks Offered By Mark", description="[FreeTrade Promo Code](https://freetrade.app.link/DiVJxPU22bb?_p=c11c32dc9e0b7af1e61890f4e0)\n[Public Promo Code](https://public.com/mark)")
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

        
    @commands.command(name="link-tree")
    async def link_tree(self, ctx):
        embed = discord.Embed(title="Mark's Link Tree!", description="[Link to it here... :smile:](https://marktilbury.net/clickhere)")
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(Commands(bot))
        