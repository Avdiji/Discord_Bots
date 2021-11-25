import os
import discord
from discord.ext import commands

TOKEN_PATH = "./.env"
TOKEN_KEY = "TOKEN_BOT"

COGS_PATH = "./cogs"

bot = commands.Bot(command_prefix='!')


# ----------------------------------------------------------------------------------------------------
# parameters:
#       token_path - path to the .env file with the token
#       token_key - key of the specific token
#
# Function extracts the token from the file with the token_path with the given token_key
# ----------------------------------------------------------------------------------------------------
def getToken(token_path, token_key):
    file = open(token_path, 'r')
    for line in file:
        if token_key in line:
            return line.split("=")[1]
    return None


# ----------------------------------------------------------------------------------------------------
# parameters:
#       cogs_path - path to the folder, that contains all the extensions
#
# Function extracts the token from the file with the token_path with the given token_key
# ----------------------------------------------------------------------------------------------------
def loadAllExtensions(cogs_path):
    for filename in os.listdir(cogs_path):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")


# ----------------------------------------------------------------------------------------------------
# Function prints, when the bot has successfully started
# ----------------------------------------------------------------------------------------------------
@bot.event
async def on_ready():
    print("logged in as {0.user}".format(bot))


# ----------------------------------------------------------------------------------------------------
# parameters:
#       ctx - context
#       extension - extension to be loaded
#
# Function loads an extension to the corresponding context
# ----------------------------------------------------------------------------------------------------
@bot.command()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")


# ----------------------------------------------------------------------------------------------------
# parameters:
#       ctx - context
#       extension - extension to be loaded
#
# Function unloads an extension from the corresponding context
# ----------------------------------------------------------------------------------------------------
@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")


loadAllExtensions(COGS_PATH)
bot.run(getToken(TOKEN_PATH, TOKEN_KEY))
