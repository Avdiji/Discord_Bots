import discord
from discord.ext import commands


# ----------------------------------------------------------------------------------------------------
# - Script implements commands, which ease the discord users life (hopefully)
# - Script also implements commands to be used by other discord bots
# ----------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------
# parameters:
#       ctx - context
#
# Function makes the bot join to a specific discord voice channel
# ----------------------------------------------------------------------------------------------------
async def joinChannel(ctx):
    if ctx.author.voice is None:
        await ctx.send(RESPONSE_COMMAND_AUTHOR_NOVOICECHANNEL)
    else:
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

async def test(ctx):
    await ctx.send("Test")