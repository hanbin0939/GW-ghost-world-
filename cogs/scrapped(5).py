import discord
from discord.ext import commands
from discord.utils import get
from youtube_dl import YoutubeDL
import youtube_dl

class VoiceError(Exception):
    pass


class YTDLError(Exception):
    pass

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, url):
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        
        vc = get(self.bot.voice_clients, guild=ctx.guild)
        if vc and vc.is_connected():
            await vc.move_to(ctx.author.voice.channel)
        else:
            vc = await ctx.author.voice.channel.connect()

        with YoutubeDL(YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                URL = info['formats'][0]['url']
                # Rest of your code that requires 'info' goes here
            except Exception as e:
                print(f"An error occurred: {e}")
                # Handle the exception here or notify user about the issue, do not proceed further with 'info' variable
            else:
                vc.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=URL))
                vc.source = discord.PCMVolumeTransformer(vc.source)
                vc.source.volume = 0.5

    @commands.command()
    async def leave(self, ctx):
        vc = get(self.bot.voice_clients, guild=ctx.guild)
        if vc and vc.is_connected():
            await vc.disconnect()
        else:
            await ctx.send("I'm not in a voice channel. You must be in the same channel as me to use this command.")
def setup(bot):
    bot.add_cog(Music(bot))