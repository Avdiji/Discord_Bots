import discord
import youtube_dl
from discord import FFmpegOpusAudio
from discord.ext import commands

RESPONSE_BOT_NOVC = "Currently I'm not in a Voice Channel!"
RESPONSE_COMMAND_AUTHOR_NOVC = "You need to enter a Voice Channel to use that Command!"
RESPONSE_MISSING_KEYWORD = "Enter a Keyword or URL after the 'play - command' (!play Michael Jackson Beat it)"


# ----------------------------------------------------------------------------------------------------
# - Script implements commands, which ease the discord users life (hopefully)
# - Script also implements commands to be used by other discord bots
# ----------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------
# parameters:
#       ctx - context
#
# returns:
#       True if the Bot has successfully joined the voice - channel, else False
#
# Function makes the bot join to a specific discord voice channel
# ----------------------------------------------------------------------------------------------------
async def join_channel(ctx):
    if ctx.author.voice is None:
        await ctx.send(RESPONSE_COMMAND_AUTHOR_NOVC)
        return False
    else:
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)
        return True


# ----------------------------------------------------------------------------------------------------
# parameters:
#       ctx - context
#
# Function makes the bot leave to the discord voice channel (if possible)
# ----------------------------------------------------------------------------------------------------
async def leave_channel(ctx):
    if ctx.voice_client is None:
        await ctx.send(RESPONSE_BOT_NOVC)
    else:
        await ctx.voice_client.disconnect()


# ----------------------------------------------------------------------------------------------------
# parameters:
#       ctx - context
#       keyword - a keyword, which is being searched for to find the corresponding youtube video (audio)

# Function returns the audio source of a youtube video (depends on which keyword you type in)
# ----------------------------------------------------------------------------------------------------
async def get_yt_audio_source(keyword):
    YDL_OPTIONS = {"format": "bestaudio"}
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        video = ydl.extract_info(f"ytsearch:{keyword}", download=False)['entries'][0]
        url = video['url']
        source = await discord.FFmpegOpusAudio.from_probe(url, method="fallback")
        return source
