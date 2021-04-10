from discord.ext.commands.errors import *
from discord.ext import commands
import discord

from aiohttp import ClientSession
import datetime
import asyncio
import os
from config import TOKEN
from datetime import timedelta

from cogs.utils.context import TheContext

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"

initial_cogs = [
    'jishaku',
    'cogs.commands',
    'cogs.reporting'
]

print("Bot is connecting...")

class Mark(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=kwargs.pop('command_prefix', ('m.', 'M.', 'Margeret.', 'Granny.')),
                        intents=discord.Intents.all(),
                        case_insensitive=True,
                        **kwargs)
        self.session = ClientSession(loop=self.loop)
        self.start_time = datetime.datetime.utcnow()
        self.clean_text = commands.clean_content(escape_markdown=True, fix_channel_mentions=True)

        """ Listening for events """

    async def on_connect(self):
        print("Bot is now connected...")

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

    async def process_commands(self, message):
        if message.author.bot:
            return ""

        ctx = await self.get_context(message=message)

        if ctx.command is None:
            return ""

        if ctx.command.name in ['help', 'member_count', 'server_messages', 'messages']:
            if ctx.channel.id not in [806528778846994463, 806535704334303263]:
                return await message.channel.send("**Please use the <#806528778846994463> channel**")

        return await self.invoke(ctx)

        async def on_command_error(self, ctx, exception):
            await self.wait_until_ready()

            error = getattr(exception, 'original', exception)

            if hasattr(ctx.command, 'on_error'):
                return ""

            elif isinstance(error, CheckFailure):
                return ""

            if isinstance(error, (BadUnionArgument, PrivateMessageOnly,
                            NoPrivateMessage, MissingRequiredArgument, ConversionError)):
                return await ctx.send(str(error))

            elif isinstance(error, commands.CommandOnCooldown):
                    em = discord.Embed(title=f"Slow it down bro!",description=f"Try again in {error.retry_after:.2f}s.")
                    return await ctx.send(embed=em)

            elif isinstance(error, BotMissingPermissions):
                return await ctx.send('I am missing these permissions to do this command:'
                                f'\n{self.lts(error.missing_perms)}')

            elif isinstance(error, MissingPermissions):
                return await ctx.send('You are missing these permissions to do this command:'
                                f'\n{self.lts(error.missing_perms)}')

            elif isinstance(error, (BotMissingAnyRole, BotMissingRole)):
                return await ctx.send(f'I am missing these roles to do this command:'
                                f'\n{self.lts(error.missing_roles or [error.missing_role])}')

            elif isinstance(error, (MissingRole, MissingAnyRole)):
                return await ctx.send(f'You are missing these roles to do this command:'
                                f'\n{self.lts(error.missing_roles or [error.missing_role])}')

            elif isinstance(error, BadArgument) and ctx.command.name in ('rep', 'report'):
                return await ctx.send(f"Can't find that member. Please try again.")

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
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Mark.setup())
        
        

