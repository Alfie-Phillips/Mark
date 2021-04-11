from discord import Member
from discord.ext.commands import check

def in_discord():
    def predicate(ctx):
        return ctx.guild.id == 734739379364429844
    return check(predicate)