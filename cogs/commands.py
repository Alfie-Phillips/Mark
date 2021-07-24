import asyncio
from datetime import datetime

import discord
from discord.ext import commands

import random
import inspect
import uuid

from flask import helpers
from .utils.helpers import to_pages_by_lines

from main import db

collection = db["Points"]
reminders = db["Reminders"]
suggestion_channel = 747165320510308393


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

    @commands.command(name="ping", help="Test the bots ping.")
    async def ping(self, ctx):
        embed = discord.Embed(title="My Current Ping!", description=f"{round(self.bot.latency * 1000, 1)}ms!", color=discord.Color.green())
        await ctx.send(embed=embed)
        await asyncio.sleep(1.5)
        await ctx.message.delete()

    @commands.command(name="nick", help="Give yourself a nickname.")
    async def nick(self, ctx, name):
        user_id = {
            "id": ctx.author.id
        }


        try:
            user = collection.find_one(user_id)
            nickname = user['nickname']

            if nickname != None:
                if name == nickname:
                    return await ctx.send("You can't change your nickname to your current nickname, pick a different one!")
                elif name == ctx.author.name:
                    return await ctx.send("You can't change your nickname to your current discord name, what is the point?")
        except:
            return await ctx.send("You have not created an account yet!")

        collection.update_one({"id": ctx.author.id}, {"$set": {"nickname": name}})

        embed = discord.Embed(
            title="New Nickname!",
            description=f"I will now refer to you as {name}!",
            color=discord.Color.green()
        )

        embed.set_footer(text="@Copyright Alfie Phillips")

        return await ctx.send(embed=embed)

    @commands.command(name="users", help="Get all current users on the server.")
    async def users(self, ctx):
        """Information about users"""
        members = self.members()
        await ctx.send(f'***Users Description***'
                       f'```Online: {members["online"]}\n'
                       f'Idle: {members["idle"]}\n'
                       f'DND: {members["dnd"]}\n'
                       f'Offline: {members["offline"]}```')

    @commands.command(name="members", help="Member count.")
    async def member_count(self, ctx):
        """Member Count"""
        embed = discord.Embed(title=f"Members Of The Mark Tilbury Discord", description=f"{ctx.guild.member_count} members!", color=discord.Color.green())
        embed.set_footer(text="@Copyright Alfie Phillips")
        await ctx.send(embed=embed)


    def get_github_link(self, base_url: str, branch: str, command: str):
        obj = self.bot.get_command(command.replace('.', ' '))

        source = obj.callback.__code__
        module = obj.callback.__module__

        lines, firstlineno = inspect.getsourcelines(source)
        location = module.replace('.', '/')
        url = f'{base_url}/blob/{branch}/{location}.py#L{firstlineno}-L{firstlineno + len(lines) - 1}'
        return url

    @commands.command(name="source", help="Source code for this discord bot, and documentation for every line of code.")
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


    @commands.command(name="suggestion", aliases=["suggest"], help="Send a server suggestion through this command.")
    async def server_suggestion(self, ctx, *, suggestion: str):
        now = datetime.now()
        channel = self.bot.get_channel(suggestion_channel)
        if not ctx.guild:
            return

        await ctx.message.delete()

        embed = discord.Embed(color=696969)
        embed.set_author(name=f"{ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        embed.set_thumbnail(
            url="https://yt3.ggpht.com/ytc/AAUvwnhl2_dBWn3rL1fe5j7O0qDMKuAK-eorFyMk1NyiVQ=s900-c-k-c0x00ffffff-no-rj"
            )
        
        embed.add_field(name=f"Suggestion:", value=f"{suggestion}\n\n", inline=True)
        embed.add_field(name=f"Status", value="This is still awaiting a response from a staff member!", inline=False)
        embed.set_footer(text="@Copyright Alfie Phillips")
        message = await channel.send(embed=embed)
        
        await message.add_reaction("<:Yes:741648526089519134>")
        await message.add_reaction("<:No:741648556493897818>")

    @commands.command(name="revive", help="Revive the chat.")
    async def revive(self, ctx):
        choices = [
               "What is your favourite investment you have made?",
               "If you recieved all the money in the world, what would you do with it?",
               "What is something you've always wanted to do, but have yet to do?",
               "What is your biggest accomplishment?",
               "What was the worst investment you have ever made?",
               "Where do you see yourself in 15 years?",
               "What is your favourite social media platform?",
               "What is your biggest phobia?",
               "If you could time travel only once, what year would you go to and why?",
               "Does pineapple belong on pizza?",
               "What is your favourite song?",
               "Who is your favourite movie actor?",
               "What is your favourite movie/tv show?"
        ]
        return await ctx.send(random.choice(choices))

    @commands.command(name="remind", case_insensitive = True, aliases=["reminder", "remindme", "remind_me"])
    async def reminder(self, ctx, time, *, reminder):
        """
        The reminder command allows users to remind themselves of tasks they need to accomplish/things they might forget
        The max reminder time (if the bot stays online long enough) is 90 days and the min is 5 minutes
        """

        member = ctx.author
        randomId = uuid.uuid4()
        embed = discord.Embed(color=0x55a7f7, timestamp=datetime.utcnow())
        seconds = 0
        if reminder is None:
            embed.add_field(name='Warning', value='Please specify what do you want me to remind you about.')
        if time.lower().endswith("d"):
            seconds += int(time[:-1]) * 60 * 60 * 24
            counter = f"{seconds // 60 // 60 // 24} days"
        if time.lower().endswith("h"):
            seconds += int(time[:-1]) * 60 * 60
            counter = f"{seconds // 60 // 60} hours"
        elif time.lower().endswith("m"):
            seconds += int(time[:-1]) * 60
            counter = f"{seconds // 60} minutes"
        elif time.lower().endswith("s"):
            seconds += int(time[:-1])
            counter = f"{seconds} seconds"

        now = datetime.now()

        query = {
            "reminderId": randomId,
            "userId": ctx.author.id,
            "time": counter,
            "reminder": str(reminder),
            "timeCreated": f"{now.year}/{now.month}/{now.day}/{now.hour}:{now.minute}.{now.second}",
            "status": "DURING"
        }

        try:
            reminders.insert_one(query)
        except Exception as error:
            return await ctx.send("Error adding reminder, please inform a staff member!")

        if seconds == 0:
            embed.add_field(name='Warning',
                            value='Please specify a proper duration, send `reminder_help` for more information.')
        elif seconds < 300:
            embed.add_field(name='Warning',
                            value='You have specified a too short duration!\nMinimum duration is 5 minutes.')
        elif seconds > 7776000:
            embed.add_field(name='Warning', value='You have specified a too long duration!\nMaximum duration is 90 days.')
        else:
            await ctx.send(f"Alright, I will remind you about `{reminder}` in {counter}.")
            await asyncio.sleep(seconds)

            query = {
                "reminderId": randomId
            }

            value = {
                "$set": {
                    "status": "FINISHED"
                }
            }

            try:
                reminders.update_one(query, value)
            except Exception as error:
                return await ctx.send("Error updating reminder, please inform a staff member!")
            await member.send(f"Hi, you asked me to remind you about `{reminder}` {counter} ago.")
            return

        return await member.send(embed=embed)


def setup(bot):
    bot.add_cog(Commands(bot))
