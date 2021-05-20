# Imports here...

from discord.ext.commands import check


def in_discord():
    def predicate(ctx):
        return ctx.guild.id == 734739379364429844 # Checking if user is in the discord server.

    return check(predicate)


