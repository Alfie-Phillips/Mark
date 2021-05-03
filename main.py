import asyncio
import datetime
import os

import discord
from aiohttp import ClientSession
from config import TOKEN, MONGO_URI
from discord.ext import commands
from discord.ext.commands.errors import *
from pymongo import MongoClient

from cogs.utils.context import TheContext

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"

initial_cogs = [
    'jishaku',
    'cogs.commands',
    'cogs.moderation',
    'cogs._help',
    'cogs.game',
    'cogs.levels'
]

cluster = MongoClient(MONGO_URI)
db = cluster["Users"]


class Mark(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=kwargs.pop('command_prefix', ('m.', 'M.', 'Mark.', 'mark.')),
                         intents=discord.Intents.all(),
                         case_insensitive=True,
                         **kwargs)
        self.session = ClientSession(loop=self.loop)
        self.start_time = datetime.datetime.utcnow()
        self.clean_text = commands.clean_content(escape_markdown=True, fix_channel_mentions=True)

        """ Listening for events """

    async def on_connect(self):
        print("Bot is connected...")

    async def on_ready(self):
        print(f'Successfully logged in as {self.user}\nSharded to {len(self.guilds)} guilds')
        self.guild = self.get_guild(806526222884143116)
        await self.change_presence(activity=discord.Game(name='Use the prefix "M."'))

        for ext in initial_cogs:
            self.load_extension(ext)
        print("All extensions have loaded!")

    async def on_member_join(self, member):
        await self.wait_until_ready()
        if member.guild.id == 806526222884143116:
            await member.send('Welcome to the Mark Tilbury Server, we hope you have a great time here!')

    async def on_message(self, message):
        await self.wait_until_ready()

        if message.author.bot:
            return ""

        print(f"{message.channel}: {message.author}: {message.clean_content}")

        if not message.guild:
            return ""

        await self.process_commands(message)

    async def on_raw_reaction_add(self, payload):
        if payload.channel_id == 806584030908645486:
            channel = self.get_channel(806584030908645486)
            mod_channel = self.get_channel(806530966105096195)
            message = await channel.fetch_message(payload.message_id)
            author = message.embeds[0].author
            suggestion = message.embeds[0].fields[0].value
            name = author.name
            icon_url = author.icon_url
            em = discord.Embed(color=696969)
            em.set_author(name=f"{name}", icon_url=f"{icon_url}")
            em.set_thumbnail(
                url="https://yt3.ggpht.com/ytc/AAUvwnhl2_dBWn3rL1fe5j7O0qDMKuAK-eorFyMk1NyiVQ=s900-c-k-c0x00ffffff-no-rj")
            em.add_field(name=f"New Suggestion!", value=f"{suggestion}\n\n", inline=True)
            em.add_field(name=f"Status", value="Undecided", inline=False)
            em.set_footer(text="@Copyright Alfie Phillips")
            for reaction in message.reactions:
                if reaction.emoji == "✅":
                    if int(reaction.count) == 2:
                        return await mod_channel.send(embed=em)

                elif reaction.emoji == "❌":
                    if int(reaction.count) == 10:
                        return await message.delete()

    async def process_commands(self, message):
        if message.author.bot:
            return ""

        ctx = await self.get_context(message=message)

        if ctx.command is None:
            return ""

        if ctx.command.name in ['help', 'member_count', 'server_messages', 'messages', 'users', 'source']:
            if ctx.channel.id not in [741634902851846195, 806528778846994463]:
                return await message.channel.send("**Please use the <#741634902851846195> channel**")

        return await self.invoke(ctx)

    async def on_command_error(self, ctx, exception):
        await self.wait_until_ready()

        error = getattr(exception, 'original', exception)

        if hasattr(ctx.command, 'on_error'):
            return await ctx.send(str(error))

        elif isinstance(error, CheckFailure):
            return await ctx.send(str(error))

        if isinstance(error, (BadUnionArgument, PrivateMessageOnly,
                              NoPrivateMessage, MissingRequiredArgument, ConversionError)):
            return await ctx.send(str(error))

        elif isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(title="Slow it down!", description=f"Try again in {error.retry_after:.2f}s.")
            await ctx.send(embed=em)

        elif isinstance(error, BotMissingPermissions):
            await ctx.send('I am missing these permissions to do this command:'
                           f'\n{self.lts(error.missing_perms)}')

        elif isinstance(error, MissingPermissions):
            await ctx.send('You are missing these permissions to do this command:'
                           f'\n{self.lts(error.missing_perms)}')

        elif isinstance(error, (BotMissingAnyRole, BotMissingRole)):
            await ctx.send(f'I am missing these roles to do this command:'
                           f'\n{self.lts(error.missing_roles or [error.missing_role])}')

        elif isinstance(error, (MissingRole, MissingAnyRole)):
            await ctx.send(f'You are missing these roles to do this command:'
                           f'\n{self.lts(error.missing_roles or [error.missing_role])}')

        elif isinstance(error, BadArgument) and ctx.command.name in ('rep', 'report'):
            await ctx.send(f"Can't find that member. Please try again.")

        else:
            raise error

    """ Bot Functions """

    async def get_context(self, message, *, cls=TheContext):
        return await super().get_context(message=message, cls=cls or TheContext)

    def em(self, **kwargs):
        return discord.Embed(**kwargs)

    @staticmethod
    def lts(list_: list):
        return ', '.join([obj.name if isinstance(obj, discord.Role) else str(obj).replace('_', ' ') for obj in list_])

    @classmethod
    async def setup(cls, **kwargs):
        bot = cls()
        try:
            await bot.start(TOKEN, **kwargs)
        except KeyboardInterrupt:
            await bot.close()


if __name__ == "__main__":
    # keep_alive()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Mark.setup())
