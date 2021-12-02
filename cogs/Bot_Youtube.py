import discord
import asyncio
from discord.ext import commands
from Bot_Helper import join_channel, get_yt_audio_source

RESPONSE_MISSING_KEYWORD = "Enter a Keyword or URL after the 'play - command' (!play Michael Jackson Beat it)"
RESPONSE_NOAUDIO = "There is no Audio being played!"
RESPONSE_PAUSED_AUDIO = "I already paused the Audio!"
RESPONSE_RESUMED_AUDIO = "There is no need to resume the Audio!"


# ----------------------------------------------------------------------------------------------------
# Class Bot_Youtube extends commands.Cog
#
# class handles all commands, which use youtube services
# ----------------------------------------------------------------------------------------------------
class Bot_Youtube(commands.Cog):

    # ----------------------------------------------------------------------------------------------------
    # CONSTRUCTOR
    #
    # parameters:
    #       self
    #       bot - the discord bot, that is connected to the server
    #       queueList - list with all the keywords, that will be / have been played
    #       active_playlist - boolean to determine, whether the queue has come to and end
    # ----------------------------------------------------------------------------------------------------
    def __init__(self, bot):
        self.bot = bot
        self.queueList = []
        self.active_playlist = False

    # ----------------------------------------------------------------------------------------------------
    # parameters:
    #       self
    #       val - new value of active_playlist
    #
    # Setter for active_playlist (also clears the queueList)
    # ----------------------------------------------------------------------------------------------------
    def stop_current_playlist(self):
        self.active_playlist = False
        self.queueList.clear()

    # ----------------------------------------------------------------------------------------------------
    # parameters:
    #       self
    #       ctx - context
    #       source - source to be played immediately
    #       index - index of the next keyword
    #
    # Recursive Method (recursion in lambda) plays the whole queue until it reaches an end
    # ----------------------------------------------------------------------------------------------------
    def play_queue(self, ctx, source, index):
        play_next = lambda e: self.play_queue(
            ctx,
            asyncio.run(get_yt_audio_source(self.queueList[index])),
            index + 1) if index + 1 <= len(self.queueList) else self.stop_current_playlist()

        ctx.voice_client.play(source, after=play_next)

    # ----------------------------------------------------------------------------------------------------
    # parameters:
    #       self
    #       ctx - context
    #       * - keyword - keyword to search for
    #
    # Discord Command to play youtube audio (searching from keyword) and building the queueList
    # ----------------------------------------------------------------------------------------------------
    @commands.command()
    async def play(self, ctx, *, keyword=None):
        if await join_channel(ctx):

            if self.active_playlist and not (keyword is None):
                self.queueList.append(keyword)
                print("{} added to playlist".format(keyword))
            else:
                self.active_playlist = True
                source = await get_yt_audio_source(keyword)
                self.play_queue(ctx, source, 0)

    # ----------------------------------------------------------------------------------------------------
    # parameters:
    #       self
    #       ctx - context
    #
    # Discord Command to stop youtube audio and clean the queueList
    # ----------------------------------------------------------------------------------------------------
    @commands.command()
    async def stop(self, ctx):
        if not (ctx.voice_client is None) and ctx.voice_client.is_playing():
            self.stop_current_playlist()
            ctx.voice_client.stop()
        else:
            await ctx.send(RESPONSE_NOAUDIO)

    # ----------------------------------------------------------------------------------------------------
    # parameters:
    #       self
    #       ctx - context
    #
    # Discord Command to skip the audio, which is currently being played
    # ----------------------------------------------------------------------------------------------------
    @commands.command()
    async def skip(self, ctx):
        if not (ctx.voice_client is None) and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
        else:
            await ctx.send(RESPONSE_NOAUDIO)

    # ----------------------------------------------------------------------------------------------------
    # parameters:
    #       self
    #       ctx - context
    #
    # Discord Command to pause the audio, which is currently being played
    # ----------------------------------------------------------------------------------------------------
    @commands.command()
    async def pause(self, ctx):
        if not (ctx.voice_client is None) and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
        else:
            await ctx.send(RESPONSE_PAUSED_AUDIO)

    # ----------------------------------------------------------------------------------------------------
    # parameters:
    #       self
    #       ctx - context
    #
    # Discord Command to resume the audio, which is currently being played
    # ----------------------------------------------------------------------------------------------------
    @commands.command()
    async def resume(self, ctx):
        if not (ctx.voice_client is None) and not (ctx.voice_client.is_playing()):
            ctx.voice_client.resume()
        else:
            await ctx.send(RESPONSE_RESUMED_AUDIO)


def setup(bot):
    bot.add_cog(Bot_Youtube(bot))
