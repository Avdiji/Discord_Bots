import discord
from discord.ext import commands


# ----------------------------------------------------------------------------------------------------
# Class Bot_Akhi extends commands.Cog
#
# class handles all commands, which are Islam-related
# ----------------------------------------------------------------------------------------------------
class Bot_Akhi(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Bot_Akhi(bot))
