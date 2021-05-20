import asyncio
from datetime import datetime

import discord
from discord.ext import commands

import inspect

from flask import helpers
from .utils.helpers import to_pages_by_lines

from main import db

collection = db["Points"]


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def members(self):
        members = set(self.bot.get_all_members())
        stats = {'online': 0, 'idle': 0, 'dnd': 0, 'offline': 0}
        for member in members:
            stats[str(member.status)] += 1
        return stats

    @staticmethod
    def em(title: str, description: str):
        return discord.Embed(title=title, description=description)

    @commands.command(name="ping")
    async def ping(self, ctx):
        embed = discord.Embed(title="My Current Ping!", description=f"{round(self.bot.latency, 1)}ms!", color=discord.Color.green())
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="nick")
    async def nick(self, ctx, name):
        user_id = {
            "id": ctx.author.id
        }

        try:
            user = collection.find_one(user_id)
        except:
            return await ctx.send("You have not created an account yet!")

        collection.update_one({"id": ctx.author.id}, {"$set": {"nickname": name}})

        return await ctx.send(f"I will now refer to you as '{name}'")

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
        embed = discord.Embed(title=f"Members Of The Mark Tilbury Discord", description=f"{ctx.guild.member_count} members!", color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command(name="website", aliases=["web", "webpage"])
    async def website(self, ctx):
        """Links for Mark's Website"""
        embed = discord.Embed(title="Mark's Website", description="[Link Here... :smile:](https://marktilbury.net/)", color=discord.Color.green())
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="tiktok")
    async def tiktok(self, ctx):
        """Links for Mark's socials"""
        embed = discord.Embed(title="Mark's TikTok",
                              description="[Link Here... :smile:](https://www.tiktok.com/@marktilbury?lang=en)", color=discord.Color.green())
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="instagram", aliases=["insta"])
    async def instagram(self, ctx):
        """Links for Mark's Instagram"""
        embed = discord.Embed(title="Mark's Instagram",
                              description="[Link Here... :smile:](https://www.instagram.com/marktilbury)", color=discord.Color.green())
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="facebook")
    async def facebook(self, ctx):
        """Links for Mark's Facebook"""
        embed = discord.Embed(title="Mark's Facebook",
                              description="[Link Here... :smile:](https://www.facebook.com/RealMarkTilbury)", color=discord.Color.green())
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="youtube")
    async def youtube(self, ctx):
        """Links for Mark's Youtube"""
        embed = discord.Embed(title="Mark's Youtube Channel",
                              description="[Link Here... :smile:](https://www.youtube.com/channel/UCxgAuX3XZROujMmGphN_scA)", color=discord.Color.green())
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
        embed = discord.Embed(title="Mark's Social Links! :smile:",
                              description="[Website](https://marktilbury.net/)\n[TikTok](https://www.tiktok.com/@marktilbury?lang=en)\n[Instagram](https://www.instagram.com/marktilbury)\n[Facebook](https://www.facebook.com/RealMarkTilbury)\n[Youtube](https://www.youtube.com/channel/UCxgAuX3XZROujMmGphN_scA)\n", color=discord.Color.green())
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="stock")
    async def stock(self, ctx, args=""):
        def em(title, description):
            embed = discord.Embed(title=title, description=description, color=discord.Color.green())
            return embed

        if args == "market":
            await ctx.send(embed=em("The Stock Market",
                                    "✦ What is the stock market? - The stock market is what allows people to buy and sell investments. On the stock market you can trade stocks, index funds, bonds, ETFs, reits, options, mutual funds, these are all ways you can invest in the stock market. Nerdwallet does a great example at defining the stock market, they state the following, “The concept behind how the stock market works is pretty simple. Operating much like an auction house, the stock market enables buyers and sellers to negotiate prices and make trades.” This basically means you are buying a small part of a company for a price determined on supply and demand. [More Info Here... :smile:](https://www.investopedia.com/terms/s/stockmarket.asp)"))
            await asyncio.sleep(1.5)
            await ctx.message.delete()

        elif args == "shares":
            await ctx.send(embed=em("Stock Shares",
                                    "✦ What are stocks and shares? - Stocks are a small percent of a company sold on the stock market in the form of shares. Investopedia defines stocks as the following, “A stock (also known as equity) is a security that represents the ownership of a fraction of a corporation. This entitles the owner of the stock to a proportion of the corporations assets and profits equal to how much stock they own. Units of stock are called shares. [More Info Here... :smile:](https://www.investopedia.com/terms/s/stockmarket.asp)"))
            await asyncio.sleep(1.5)
            await ctx.message.delete()

        elif args == "prices":
            await ctx.send(embed=em("Stock Prices",
                                    "✦ What determines stock prices? - Stock prices are purely based on supply and demand, this is why sometimes a company may be doing amazing yet their stock may be dropping. So when investing in stocks or other types of investments it is important to look at EVERYTHING. This includes how the company is doing, public opinion, and the charts. Nerdwallet explains stock price as such, “That supply and demand help determine the price for each security, or the levels at which stock market participants — investors and traders — are willing to buy or sell.” And they also mention how buying and selling works, “Buyers offer a “bid,” or the highest amount they’re willing to pay, which is usually lower than the amount sellers “ask” for in exchange. This difference is called the bid-ask spread. For a trade to occur, a buyer needs to increase his price or a seller needs to decrease hers.” [More Info Here... :smile:](https://www.investopedia.com/terms/s/stockmarket.asp)'"))
            await asyncio.sleep(1.5)
            await ctx.message.delete()

        elif args == "types":
            await ctx.send(embed=em("Stock Types",
                                    '✦ What types of stocks are there? - There are different groups of stock that serve different purposes in your portfolio. • Income/Dividend Stock - These stocks usually do not have crazy growth but rather high dividends yields which usually comes with higher payout ratios. These companies will usually payout every month, quarter, semi-annually, or yearly. • Cyclical Stock - These are stocks who will have ups and downs based on the economy and are more sensitive when there is an economic downturn. •Blue Chip Stocks -  Very safe stocks usually from big companies with large market caps. These companies will usually be a well known name like Walmart, Apple, or Coca Cola. These companies are more than likely to be financially sound and survive economic crashes. • Tech Stocks - Companies based around technology. These usually have the most growth but also come with an associated risk. Technology advances fast meaning if the company does not keep up it can fall out of favor. • Speculative Stocks - Usually extreme risk, these are companies that are new and usually don’t have much history or financial stability. These companies can bring immense profits as well as risk. • Defensive Stocks - Stocks that are extremely safe, these companies have been around for centuries sometimes and are impossible to stop. These stocks will do good and recover from crashes and sometimes even profit. Examples are prominent in the consumer staples sector, an example is Walmart. • Growth Stocks - Most do not pay out dividends as they would rather keep that money and reinvest it into their company for more growth. These stocks will bring good growth and profit is only made on capital gains. [More Info Here... :smile:](https://www.investopedia.com/terms/s/stockmarket.asp)'))
            await asyncio.sleep(1.5)
            await ctx.message.delete()
        elif args == "brokers":
            await ctx.send(embed=em("Brokerages",
                                    '✦ What is a broker and brokerage? - A brokerage account is what will allow you to buy and sell stocks. Without a broker you cannot trade, when you decide to buy a stock it is sent to the broker (this used to be a real person on the floors of the NYSE, now it is all automatic), they will buy it for you and be the middleman. ✦ Can you invest in the stock market under the age of 18? - Yes, you can invest in the stock market under the age of 18, but only with the permission and having a parent signed on with you. In the UK you will need to open what is called a junior stocks and shares ISA, in the US you need what is called a custodial account. Both of these are accounts that belong to your parents until you are 18 and then owner ship is transferred to you, this will allow you to access the stock market and invest. You can find these by looking it up on google or going to your bank, as they will most likely help you set one up or recommend one. ✦ What are some good and trust worthy brokerage accounts? - Brokerages will depend on your location for the EU, typically Trading 212, Interactive Brokers, and EToro are used. For the US brokers like Webull, Robinhood (which is not a good choice as it is being investigated by the SEC, is very unreliable, and has a 10 million dollar lawsuit), Charles Schwab, E*TRADE, Think Or Swim, TD Ameritrade, are all great brokers. When choosing your broker it is a good idea to look at them all to see which one applies to what you are looking for. ✦ What is paper trading? - Paper trading is the act of trading with simulated money, this is most commonly used for practice. Investopedia says the following, "A paper trade is a simulated trade that allows an investor to practice buying and selling without risking real money." [More Info Here... :smile:](https://www.investopedia.com/terms/s/stockbroker.asp)'))
            await asyncio.sleep(1.5)
            await ctx.message.delete()
        else:
            await ctx.send(embed=em("Please use these commands for help on stocks!",
                                    "M.stock market, M.stock shares, M.stock prices, M.stock types, M.stock brokers", discord.Color.red()))
            await asyncio.sleep(1.5)
            await ctx.message.delete()

    @commands.command(name="index-funds", aliases=["etfs", "etf", "funds"])
    async def index_and_etf(self, ctx):
        embed = discord.Embed(title="Index Funds And ETF'S",
                              description='- ETFs and Index Funds are both great ways to diversify investments, but how are they different? The main and biggest differences for the investor is cost, ETFs and Index Funds will have different costs associated with them for the investor. Index Funds are rebalanced daily which come in the form of commissions and other costs. ETFs on the other hand have another system as defined by Investopedia, " ETFs have a unique process called creation/redemption in-kind (meaning shares of ETFs can be created and redeemed with a like basket of securities) that avoids these transaction costs." Index Funds also have the cost of cash drag, which  ETFs do not have to deal with. However an advantage that Index Funds have over ETFs is when it comes to dividends. Index Funds will immediately reinvest their dividends compared to ETFs which pool them up and pay them out at the end of each quarter. ETFs also have lower management fees. However the biggest cost in ETFs is the shareholder transaction cost, which is usually 0 for Index Funds. \n[Index Funds](https://www.investopedia.com/terms/i/indexfund.asp) \n[ETF](https://www.investopedia.com/terms/e/etf.asp)', color=discord.Color.green())
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="freetrade")
    async def freetrade(self, ctx):
        embed = discord.Embed(title="Get A Free Stock On FreeTrade!",
                              description="[Mark Tilbury's Promo Code Here... :smile:](https://freetrade.app.link/DiVJxPU22bb?_p=c11c32dc9e0b7af1e61890f4e0)", color=discord.Color.green())
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="public")
    async def public(self, ctx):
        embed = discord.Embed(title="Get A Free Stock On Public!",
                              description="[Mark Tilbury's Promo Code Here... :smile:](https://public.com/mark)", color=discord.Color.green())
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="free-stocks")
    async def free_stocks(self, ctx):
        embed = discord.Embed(title="Free Stocks Offered By Mark",
                              description="[FreeTrade Promo Code](https://freetrade.app.link/DiVJxPU22bb?_p=c11c32dc9e0b7af1e61890f4e0)\n[Public Promo Code](https://public.com/mark)", color=discord.Color.green())
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="link-tree")
    async def link_tree(self, ctx):
        embed = discord.Embed(title="Mark's Link Tree!",
                              description="[Link to it here... :smile:](https://marktilbury.net/clickhere)", color=discord.Color.green())
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="trading-patterns")
    async def trading_patterns(self, ctx):
        embed = discord.Embed(title="Trading Patterns",
                              description="Throughout the trading scheme, we see many trading patterns which can somewhat predict what is going to happen next with a stock. We use these to be smart, and notice when it is the right time to buy or sell, it is essential to know some of these key features. [Link to key trading patterns](https://www.investopedia.com/articles/technical/112601.asp)\n[A PDF for analyzing chart patterns](http://i.investopedia.com/inv/pdf/tutorials/AnalyzingChartPatterns.pdf)", color=discord.Color.green())
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="dropshipping", aliases=["drop-shipping"])
    async def drop_shipping(self, ctx, args=""):
        if args == "":
            embed = discord.Embed(title="Drop Shipping Commands",
                                  description="M.drop-shipping-definition\nM.drop-shipping-guide\nM.drop-shipping-profits", color=discord.Color.green())
            await ctx.send(embed=embed)
            await asyncio.sleep(1.5)
            await ctx.message.delete()

        elif args == "definition":
            embed = discord.Embed(title="What is dropshipping?",
                                  description="Dropshipping is a business model that you can use to run your store without ever holding any inventory. Once you've made a sale, your supplier will ship your products from their warehouse, straight to your customer's doorstep meaning that you'll never need to worry about stoing, packaging, or shipping your products. For example, you can sell an item for $20, give $5 and the address to your supplier, and your supplier will ship it directly to your customer, and you make $15 profit. Written by Frog#1582\n[More Info Here... :smile:](https://www.shopify.co.uk/blog/what-is-dropshipping#definition)", color=discord.Color.green())
            await ctx.send(embed=embed)
            await asyncio.sleep(1.5)
            await ctx.message.delete()

        elif args == "guide":
            embed = discord.Embed(title="How does dropshipping work?",
                                  description="How Does Dropshipping Work? Dropshipping is a simple business model. Once a customer places an order from your store, you’ll simply purchase the product from your supplier, and instruct them to ship the product directly to your customer’s door. That means you can run your own business from anywhere in the world. Written by Frog#1582\n[More Info Here... :smile:](https://www.shopify.co.uk/blog/what-is-dropshipping#definition)", color=discord.Color.green())
            await ctx.send(embed=embed)
            await asyncio.sleep(1.5)
            await ctx.message.delete()

        elif args == "profits":
            embed = discord.Embed(title="Is dropshipping profitable?",
                                  description="Is Dropshipping Profitable? Yes it is profitable, but you must put in the effort to research products, set up website, distribute well, and eventually scale your business. Distributing is very important! Written by Frog#1582\n[More Info Here... :smile:](https://www.shopify.co.uk/blog/what-is-dropshipping#benefits)", color=discord.Color.green())
            await ctx.send(embed=embed)
            await asyncio.sleep(1.5)
            await ctx.message.delete()

        elif args == "products":
            embed = discord.Embed(title="Do I need to purchase products for my online store?",
                                  description="No, the beauty of dropshipping is that you don’t need to hold any inventory yourself. You simply order it from your supplier once a customer has bought from you. That said, it’s a good idea to buy sample products from your suppliers before uploading them to your online store to make sure you are happy with the quality of the product. In fact, I would insist that you buy sample products! Written by Frog#1582", color=discord.Color.green())
            await ctx.send(embed=embed)
            await asyncio.sleep(1.5)
            await ctx.message.delete()

        elif args == "setup":
            pass

        elif args == "links":
            pass

        else:
            return await ctx.send(embed=discord.Embed(title="Please use these commands for help on dropshipping!",
                                                      description="M.dropshipping, M.dropshipping definition, M.dropshipping guide, M.dropshippinh profits, M.dropshipping products, M.dropshipping setup, M.dropshipping links", color=discord.Color.green()))

    @commands.command(name="crypto", aliases=["crypto-currency"])
    async def crypto_currency(self, ctx, args):
        if args == "":
            pass
        else:
            pass

    @commands.command(name="digital-marketing", aliases=["marketing"])
    async def digital_marketing(self, ctx, args):
        if args == "":
            pass
        else:
            pass

    @commands.command(name="real-estate")
    async def real_estate(self, ctx, args):
        if args == "":
            pass
        else:
            pass

    @commands.command(name="suggestion", aliases=["suggest", "s"])
    async def server_suggestion(self, ctx, *, suggestion: str):
        now = datetime.now()
        emojis = ["👀", "😄", "😇", "🤩", "😎", "👌", "👍", "👏"]
        channel = self.bot.get_channel(806584030908645486)
        if not ctx.guild:
            return

        await ctx.message.delete()

        embed = discord.Embed(color=696969)
        embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        embed.set_thumbnail(
            url="https://yt3.ggpht.com/ytc/AAUvwnhl2_dBWn3rL1fe5j7O0qDMKuAK-eorFyMk1NyiVQ=s900-c-k-c0x00ffffff-no-rj")
        embed.add_field(name=f"Suggestion:", value=f"{suggestion}\n\n", inline=True)
        embed.add_field(name=f"Status", value="This is still awaiting a response from a staff member!", inline=False)
        embed.set_footer(text="@Copyright Alfie Phillips")
        message = await channel.send(embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("❌")

    @commands.command(name="accept")
    @commands.has_role("Admin")
    async def accept(self, ctx, message_id: int, *, reason="None"):
        if not ctx.guild:
            return

        channel = self.bot.get_channel(806584030908645486)
        try:
            message = await channel.fetch_message(message_id)
            await ctx.message.delete()

            author = message.embeds[0].author
            suggestion = message.embeds[0].fields[0].value
            name = author.name
            icon_url = author.icon_url
            em = discord.Embed(color=3340850)
            em.set_author(name=f"{name}", icon_url=f"{icon_url}")
            em.set_thumbnail(
                url="https://yt3.ggpht.com/ytc/AAUvwnhl2_dBWn3rL1fe5j7O0qDMKuAK-eorFyMk1NyiVQ=s900-c-k-c0x00ffffff-no-rj")
            em.add_field(name=f"Suggestion:", value=f"{suggestion}\n\n", inline=True)
            em.add_field(name=f"Status", value="Accepted ✅", inline=False)
            em.add_field(name=f"Staff answer by @{ctx.author.name}", value=f"{reason}")
            em.set_footer(text="@Copyright Alfie Phillips")
            return await message.edit(embed=em)

        except:
            await ctx.message.delete()
            return await ctx.send(f"{ctx.author.mention}. Message with id: {str(message_id)} was not found!")

    @commands.command(name="decline")
    @commands.has_role("Admin")
    async def decline(self, ctx, message_id: int, *, reason="None"):
        if not ctx.guild:
            return

        channel = self.bot.get_channel(806584030908645486)
        try:
            message = await channel.fetch_message(message_id)
            await ctx.message.delete()

            author = message.embeds[0].author
            suggestion = message.embeds[0].fields[0].value
            name = author.name
            icon_url = author.icon_url
            em = discord.Embed(color=16718080)
            em.set_author(name=f"{name}", icon_url=f"{icon_url}")
            em.set_thumbnail(
                url="https://yt3.ggpht.com/ytc/AAUvwnhl2_dBWn3rL1fe5j7O0qDMKuAK-eorFyMk1NyiVQ=s900-c-k-c0x00ffffff-no-rj")
            em.add_field(name=f"Suggestion:", value=f"{suggestion}\n\n", inline=True)
            em.add_field(name=f"Status", value="Declined ❌", inline=False)
            em.add_field(name=f"Staff answer by @{ctx.author.name}", value=f"{reason}")
            em.set_footer(text="@Copyright Alfie Phillips")
            await message.edit(embed=em)

        except:
            await ctx.message.delete()
            return await ctx.send(f"{ctx.author.mention}. Message with id: ({str(message_id)}) was not found!")


def setup(bot):
    bot.add_cog(Commands(bot))
