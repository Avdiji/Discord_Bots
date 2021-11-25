import discord
from discord.ext import commands


# ----------------------------------------------------------------------------------------------------
# Class Bot_Youtube extends commands.Cog
#
# class handles all commands, which use youtube services
# ----------------------------------------------------------------------------------------------------
class Bot_Youtube(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Bot_Youtube(bot))
