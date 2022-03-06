import asyncio
import datetime
import os
import discord
import logging
import string
import random

from discord.ext import commands
from discord.ext.commands.errors import *
from discord_components import Button, DiscordComponents
from discord import Forbidden
from discord.utils import get

from aiohttp import ClientSession
from envconfig import *
from pymongo import MongoClient
from cogs.utils.context import TheContext
from captcha.image import ImageCaptcha

from discord_components.interaction import Interaction

# Log options
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

# Database setup
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
        self.guild = self.get_guild(734739379364429844)
        self.logger = logging.Logger("logger", level="DEBUG")

        logging.basicConfig(level=logging.INFO)

        "Listening for events"

    async def on_connect(self):
        """
        Connecting to discord servers.
        """

        self.logger.info("Bot has connected.")

    async def on_ready(self):
        """
        When the bot has loading all components and extensions.
        """

        # Initialize discord components
        DiscordComponents(bot=self)

        # Changing the current bot status
        self.logger.info(f'Successfully logged in as {self.user}\nSharded to {len(self.guilds)} guilds')
        await self.change_presence(activity=discord.Game(name='Use the prefix "M."'))

        # Load our extensions to register commands in each specific sector
        for ext in initial_cogs:
            self.load_extension(ext)
        self.logger.info("All extensions have loaded!")

        # Send a new verification message on every reinstation of the bot
        embed = self.em(title="Verification", description="This is to make sure you are not a bot!", color=0x00ff00)
        button = Button(label="Verify")

        channel = self.get_channel(int(VERIFICATION_CHANNEL))

        return await channel.send(embed=embed, components=[button])

    async def on_button_click(self, interaction: Interaction):
        if interaction.responded:
            return
        
        member_id = interaction.user.id
        member = get(self.get_all_members(), id=member_id)
        role = interaction.guild.get_role(int(MEMBER_ROLE_ID))

        if interaction.component.label == "Verify":
            """
            Sends the user an image of a random string
            to verify themselves on the server.
            """

            # Create the directory for the captcha images
            if not os.path.exists(os.getcwd() + "/captchas"):
                os.mkdir(os.getcwd() + "/captchas")

            # Check user is already verified on the server
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

            try:
                # Try to send the user a message
                await member.send(embed=message)
                await member.send(file=discord.File(fp=os.getcwd() + "/captchas/" + str(chars) + ".png"))
                await interaction.send("Please check your DMs!")
            except Forbidden:
                # If the user has DMs disabled, alert an error to them
                return await interaction.send("I can't DM you! Please enable DMs in your privacy settings.\n\nIf you need help, use this link: https://bit.ly/3uclaR9")

            # Await a reply from the user
            reply = await self.wait_for("message", check=lambda message: message.author == interaction.author)

            # Remove the captcha image to save storage
            os.remove(os.getcwd() + "/captchas/" + str(chars) + ".png")
                
            if reply.content != chars:
                # Verification has failed
                return await member.send("Verification failed! Please try again!")

            else:
                # Add new role
                await member.send("You have been verified!")
                return await member.add_roles(role)

    async def on_member_join(self, member: discord.member):
        """
        Checks to run when a new member joins the server.
        """

        account_name = (member.name).lower().strip(" ")
        display_name = (member.display_name).lower().strip(" ")

        # Check if the user's name is mark tilbury
        if "marktilbury" in account_name or "marktilbury" in display_name:
            await member.send("You must not have the name Mark Tilbury to join this server!")
            return await member.kick()

        team_names = ["curtistilbury", "LD", "dawoud", "profitset", "bloberto", "alistair<T>()", "opengl", "roni", "расплатаздесь"]

        for name in team_names:
            if name in account_name or name in display_name:
                await member.send("You must not have the name of a team member to join this server!")
                return await member.kick()

        channel = self.get_channel(int(WELCOME_CHANNEL))
        member_count = len([member for member in self.guild.members if not member.bot])
        
        # Define random greetings to send when a new user joins the server
        greetings = [
            f"Welcome to the server, {member.mention}!",
            f"Howdy {member.mention}! Welcome to the Mark Tilbury Discord!",
            f"{member.mention} has joined the server!",
            f"{member.mention} has slid into the server.",
            f"Welcome {member.mention}.",
            f"Welcome to our discord {member.mention}. You are our {str(member_count)}th member!",
        ]

        return await channel.send(random.choice(greetings))

    async def on_message(self, message):
        """
        On every message sent by a normal user.
        """
        await self.wait_until_ready()
        
        # Do not respond to another bot
        if message.author.bot:
            return

        
        """
        A common question that will now recieve an automated response.
        """

        if "mark" in message.content.lower() and "twitter" in message.content.lower():
            return await message.channel.send("If the message above is imposing that Mark has a twitter, please report the user to our staff team. Mark **DOES NOT** have a Twitter account.") 

        self.logger.info(f"{message.channel}: {message.author}: {message.clean_content}")

        if not message.guild:
            return

        # Process the commands
        await self.process_commands(message)

    async def on_raw_reaction_add(self, payload):
        """
        On every reaction add in a server
        """

        if payload.channel_id == int(SUGGESTION_CHANNEL):
            channel = self.get_channel(int(SUGGESTION_CHANNEL))
            mod_channel = self.get_channel(int(MODERATOR_CHANNEL))

            # Find the message in the 'server-suggestions' channel
            message = await channel.fetch_message(payload.message_id)

            # Grab the field values of the corresponding message
            author = message.embeds[0].author
            suggestion = message.embeds[0].fields[0].value
            name = author.name
            icon_url = author.icon_url

            # Create a new embed message to replace the old one
            embed = em(color=696969)
            embed.set_author(name=f"{name}", icon_url=f"{icon_url}")
            embed.set_thumbnail(
                url="https://yt3.ggpht.com/ytc/AAUvwnhl2_dBWn3rL1fe5j7O0qDMKuAK-eorFyMk1NyiVQ=s900-c-k-c0x00ffffff-no-rj")
            embed.add_field(name=f"New Suggestion!", value=f"{suggestion}\n\n", inline=True)
            embed.add_field(name=f"Status", value="Undecided", inline=False)
            embed.add_field(name="Message ID", value=f"{payload.message_id}", inline=False)
            embed.set_footer(text="@Copyright Alfie Phillips")

            # Check if the reaction added is a valid emoji
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

        # Validate the command
        if ctx.command.name in ['member_count', 'server_messages', 'messages', 'users', 'source', 'lb', 'glb', 'hilo', "remind"]:
            if ctx.channel.id not in [741634902851846195, 741641800183447602]:
                return await message.channel.send("**Please use the <#741634902851846195> channel**")

        return await self.invoke(ctx)

    async def on_command_error(self, ctx, exception):
        await self.wait_until_ready()

        """
        Error handling for unhandled exceptions
        """

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
