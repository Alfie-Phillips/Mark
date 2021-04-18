from discord.ext import commands
import discord
from urllib.parse import urlparse
import asyncio
import re

class Filtering(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if not ctx.guild:
            return False
    
    @commands.Cog.listener()
    async def on_message(self, message):
        await self.bot.wait_until_ready()
        if not message.guild:
            return

        await self._do_filtering(message)
        await self._do_parsing(message)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.bot.wait_until_ready()
        if not before.guild:
            return 
        
        await self._do_filtering(after)
        await self._do_parsing(after)

    async def _do_filtering(self, message: discord.Message):
        message_content = message.content.strip().lower()
        user = message.author
        valid_channels = [806530966105096195]
        mod_channel = self.bot.get_channel(806530966105096195)
        with open("bad-words.txt", 'r+') as f:
            words = [word.strip().lower() for word in f.readlines()]
        if message.channel.id in valid_channels:
            if message.author == self.bot.user:
                return
            await message.delete()
            await message.channel.send("I know this is a staff channel, but can you still please not use that?")
            return True
        if message.channel not in valid_channels:
            if message.author == self.bot.user:
                return
            for word in words:
                if word in message_content:
                    embed = discord.Embed(title="Bad Profanity Violation!", description="Your message contains profanity we do not allow on this server. Please refrain from doing this again!")
                    await user.send(embed=embed)
                    await message.delete()
                    warning_embed = discord.Embed(title=f"Violation by {str(user)} | USER ID: {str(user.id)}", description=f"Message: {message_content}")
                    await mod_channel.send(embed=warning_embed)
                    return True

    async def _do_parsing(self, message: discord.Message):
        user = message.author
        mod_channel = self.bot.get_channel(806530966105096195)
        urls = re.findall(r"(https?://[^\s]+)", message.content, flags=re.IGNORECASE)
        for url in urls:
            try:
                result = urlparse(url)
                if all([result.scheme, result.netloc]):
                    result = await self._blacklisted_url(result.netloc)
                    if result:
                        reply = discord.Embed(title="Blocked URL", description="You tried to send a blacklisted link! This is not allowed on the server.")
                        report = discord.Embed(title=f"USER: {user} | ID: {user.id} Blocked URL", description=f"Blocked Message: {message.content}")
                        await message.delete()
                        await user.send(embed=reply)
                        await mod_channel.send(embed=report)

                    return 

            except Exception as exception:
                print(exception)

    async def _blacklisted_url(self, netloc: str) -> bool:
        with open("blacklisted-urls.txt", 'r+') as f:
            urls = [url.strip().lower() for url in f.readlines()]
            for url in urls:
                if url in netloc:
                    return True
            return False

def setup(bot: commands.Bot):
    bot.add_cog(Filtering(bot=bot))