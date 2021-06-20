import asyncio
from datetime import datetime

import discord
from discord.ext import commands

class Advice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command(name="stock", help="market, shares, prices, types, brokers")
    async def stock(self, ctx, args=""):
        def em(title, description):
            embed = discord.Embed(title=title, description=description, color=discord.Color.green())
            embed.set_footer(text="@Copyright Alfie Phillips")
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

    @commands.command(name="index-funds", aliases=["etfs", "etf", "funds"], help="Information on index funds.")
    async def index_and_etf(self, ctx):
        embed = discord.Embed(title="Index Funds And ETF'S",
                              description='- ETFs and Index Funds are both great ways to diversify investments, but how are they different? The main and biggest differences for the investor is cost, ETFs and Index Funds will have different costs associated with them for the investor. Index Funds are rebalanced daily which come in the form of commissions and other costs. ETFs on the other hand have another system as defined by Investopedia, " ETFs have a unique process called creation/redemption in-kind (meaning shares of ETFs can be created and redeemed with a like basket of securities) that avoids these transaction costs." Index Funds also have the cost of cash drag, which  ETFs do not have to deal with. However an advantage that Index Funds have over ETFs is when it comes to dividends. Index Funds will immediately reinvest their dividends compared to ETFs which pool them up and pay them out at the end of each quarter. ETFs also have lower management fees. However the biggest cost in ETFs is the shareholder transaction cost, which is usually 0 for Index Funds. \n[Index Funds](https://www.investopedia.com/terms/i/indexfund.asp) \n[ETF](https://www.investopedia.com/terms/e/etf.asp)', color=discord.Color.green())
        embed.set_footer(text="@Copyright Alfie Phillips")
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="freetrade", help="Promo code for freetrade.")
    async def freetrade(self, ctx):
        embed = discord.Embed(title="Get A Free Stock On FreeTrade!",
                              description="[Mark Tilbury's Promo Code Here... :smile:](https://freetrade.app.link/DiVJxPU22bb?_p=c11c32dc9e0b7af1e61890f4e0)", color=discord.Color.green())
        embed.set_footer(text="@Copyright Alfie Phillips")
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="public", help="Promo code for public.")
    async def public(self, ctx):
        embed = discord.Embed(title="Get A Free Stock On Public!",
                              description="[Mark Tilbury's Promo Code Here... :smile:](https://public.com/mark)", color=discord.Color.green())
        embed.set_footer(text="@Copyright Alfie Phillips")
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="free-stocks", help="Free available stocks.")
    async def free_stocks(self, ctx):
        embed = discord.Embed(title="Free Stocks Offered By Mark",
                              description="[FreeTrade Promo Code](https://freetrade.app.link/DiVJxPU22bb?_p=c11c32dc9e0b7af1e61890f4e0)\n[Public Promo Code](https://public.com/mark)", color=discord.Color.green())
        embed.set_footer(text="@Copyright Alfie Phillips")
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="dropshipping", aliases=["drop-shipping"], help="definition, guide, profits, products")
    async def drop_shipping(self, ctx, args=""):

        if args == "definition":
            embed = discord.Embed(title="What is dropshipping?",
                                  description="Dropshipping is a business model that you can use to run your store without ever holding any inventory. Once you've made a sale, your supplier will ship your products from their warehouse, straight to your customer's doorstep meaning that you'll never need to worry about stoing, packaging, or shipping your products. For example, you can sell an item for $20, give $5 and the address to your supplier, and your supplier will ship it directly to your customer, and you make $15 profit. Written by Frog#1582\n[More Info Here... :smile:](https://www.shopify.co.uk/blog/what-is-dropshipping#definition)", color=discord.Color.green())
            embed.set_footer(text="@Copyright Alfie Phillips")
            await ctx.send(embed=embed)
            await asyncio.sleep(1.5)
            await ctx.message.delete()

        elif args == "guide":
            embed = discord.Embed(title="How does dropshipping work?",
                                  description="How Does Dropshipping Work? Dropshipping is a simple business model. Once a customer places an order from your store, you’ll simply purchase the product from your supplier, and instruct them to ship the product directly to your customer’s door. That means you can run your own business from anywhere in the world. Written by Frog#1582\n[More Info Here... :smile:](https://www.shopify.co.uk/blog/what-is-dropshipping#definition)", color=discord.Color.green())
            embed.set_footer(text="@Copyright Alfie Phillips")
            await ctx.send(embed=embed)
            await asyncio.sleep(1.5)
            await ctx.message.delete()

        elif args == "profits":
            embed = discord.Embed(title="Is dropshipping profitable?",
                                  description="Is Dropshipping Profitable? Yes it is profitable, but you must put in the effort to research products, set up website, distribute well, and eventually scale your business. Distributing is very important! Written by Frog#1582\n[More Info Here... :smile:](https://www.shopify.co.uk/blog/what-is-dropshipping#benefits)", color=discord.Color.green())
            
            embed.set_footer(text="@Copyright Alfie Phillips")
            await ctx.send(embed=embed)
            await asyncio.sleep(1.5)
            await ctx.message.delete()

        elif args == "products":
            embed = discord.Embed(title="Do I need to purchase products for my online store?",
                                  description="No, the beauty of dropshipping is that you don’t need to hold any inventory yourself. You simply order it from your supplier once a customer has bought from you. That said, it’s a good idea to buy sample products from your suppliers before uploading them to your online store to make sure you are happy with the quality of the product. In fact, I would insist that you buy sample products! Written by Frog#1582", color=discord.Color.green())
            embed.set_footer(text="@Copyright Alfie Phillips")
            await ctx.send(embed=embed)
            await asyncio.sleep(1.5)
            await ctx.message.delete()

        else:
            embed = discord.Embed(title="Please use these commands for help on dropshipping!", 
                                    description="M.dropshipping, M.dropshipping definition, M.dropshipping guide, M.dropshippinh profits, M.dropshipping products, M.dropshipping setup, M.dropshipping links", color=discord.Color.green())
            
            return await ctx.send(embed=embed)


    @commands.command(name="crypto", aliases=["crypto-currency"], help="Help on cryptocurrency.")
    async def crypto_currency(self, ctx, args):
        if args == "":
            pass
        else:
            pass

    @commands.command(name="digital-marketing", aliases=["marketing"], help="Help on digital marketing.")
    async def digital_marketing(self, ctx, args):
        if args == "":
            pass
        else:
            pass

    @commands.command(name="real-estate", help="Help on real estate.")
    async def real_estate(self, ctx, args):
        if args == "":
            pass
        else:
            pass


def setup(bot):
    bot.add_cog(Advice(bot))