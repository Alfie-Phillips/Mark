import asyncio
import datetime
import os
import discord
import logging
import string
import random

from discord.ext import commands
from discord.ext.commands.errors import *

from aiohttp import ClientSession
from config import TOKEN, MONGO_URI
from pymongo import MongoClient
from cogs.utils.context import TheContext

from discord_components import Button, DiscordComponents
from captcha.image import ImageCaptcha


os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"

initial_cogs = [
    'jishaku',
    'cogs.commands',
    'cogs.advice',
    'cogs.moderation',
    'cogs._help',
    'cogs.game',
    'cogs.levels',
    'cogs.links',
    'cogs.admin'
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

        logging.basicConfig(level=logging.INFO)

        "Listening for events"

    async def on_connect(self):
        """
        Connecting to discord servers.
        """
        print("Bot is connected...")

    async def on_ready(self):
        """
        On bot load.
        """

        DiscordComponents(bot=self)

        print(f'Successfully logged in as {self.user}\nSharded to {len(self.guilds)} guilds')
        self.guild = self.get_guild(734739379364429844)
        await self.change_presence(activity=discord.Game(name='Use the prefix "M."'))

        for ext in initial_cogs:
            self.load_extension(ext)
        print("All extensions have loaded!")

        embed = discord.Embed(title="Verification", description="This is to make sure you are not a bot!", color=0x00ff00)

        channel = self.get_channel(937339343377428540)

        button = Button(label="Verify")

        return await channel.send(embed=embed, components=[button])

    async def on_button_click(self, interaction):
        member = interaction.user
        guild = self.get_guild(734739379364429844)
        role = guild.get_role(937338231672963114)

        if interaction.component.label == "Verify":
            """
            Sends the user an image of a random string
            to verify themselves on the server.
            """

            if not os.path.exists(os.getcwd() + "/captchas"):
                os.mkdir(os.getcwd() + "/captchas")


            if role in member.roles:
                return await interaction.send("You are already verified!")

            # Verification message
            message = discord.Embed(title="Verification", description="Please type the following string to verify yourself.", color=0x00ff00)
            message.set_footer(text="@Copyright Alfie Phillips")

            # Define the string length to use for verification
            STRING_LENGTH = random.randint(5, 7)

            chars = ""

            # Generate a random string
            for i in range(STRING_LENGTH):
                chars = chars + random.choice(string.ascii_lowercase + string.digits)
            
            # Create the image
            image = ImageCaptcha(width=280, height=80, font_sizes=(40, 50))
            image.write(chars, os.getcwd() + "/captchas/" + str(chars) + ".png")


            await interaction.send("Check your dms!")

            await member.send(embed=message)
            await member.send(file=discord.File(fp=os.getcwd() + "/captchas/" + str(chars) + ".png"))
            

            reply = await self.wait_for("message", check=lambda message: message.author == interaction.author)

            os.remove(os.getcwd() + "/captchas/" + str(chars) + ".png")
                
            if reply.content != chars:
                return await member.send("Verification failed! Please try again!")

            else:
                # Add new role
                await member.send("You have been verified!")
                return await member.add_roles(role)


    async def on_message(self, message):
        """
        On every message sent by a normal user.
        """
        await self.wait_until_ready()

        if message.author.bot:
            return

        
        """
        A common question that will now recieve an automated response.
        """
        if "mark" in message.content.lower() and "twitter" in message.content.lower():
            return await message.channel.send("Mark **DOES NOT** have a Twitter account. Please report and block the user on twitter.") 

        print(f"{message.channel}: {message.author}: {message.clean_content}")

        if not message.guild:
            return 

        await self.process_commands(message)

    async def on_raw_reaction_add(self, payload):
        """
        On every reaction add in a server
        """

        suggestionChannelId = 747165320510308393
        if payload.channel_id == suggestionChannelId:
            channel = self.get_channel(suggestionChannelId)
            mod_channel = self.get_channel(734883606555656334)
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
            em.add_field(name="Message ID", value=f"{payload.message_id}", inline=False)
            em.set_footer(text="@Copyright Alfie Phillips")
            for reaction in message.reactions:
                if str(reaction.emoji) not in ["<:Yes:741648526089519134>", "<:No:741648556493897818>"]:
                    await message.remove_reaction(reaction, payload.member)
                
    async def process_commands(self, message):
        """
        Process all commands with certain prefix.
        """
        if message.author.bot:
            return 

        ctx = await self.get_context(message=message)

        if ctx.command is None:
            return 

        if ctx.command.name in ['member_count', 'server_messages', 'messages', 'users', 'source', 'lb', 'glb', 'hilo', "remind"]:
            if ctx.channel.id not in [741634902851846195, 741641800183447602]:
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

    " Bot Functions "

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
