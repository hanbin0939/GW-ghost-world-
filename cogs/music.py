import discord
from discord.ext import commands
import wavelink

async def connect_nodes(self):
        await self.bot.wait_until_ready() # wait until the bot is ready

        await wavelink.NodePool.create_node(
        bot=self.bot,
        host='fsn.lavalink.alexanderof.xyz',
        port=2333, 
        password = "lavalink",
        )

class Music(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.queue = []

    @commands.Cog.listener()
    async def on_ready(self):
        await connect_nodes(self)

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self,node: wavelink.Node):
        print(f"{node.identifier} is ready.") # print a message

    @discord.slash_command(name="play")
    async def play(self,ctx, search: str):
        vc = ctx.voice_client # define our voice client

        if not vc: # check if the bot is not in a voice channel
            vc = await ctx.author.voice.channel.connect(cls=wavelink.Player) # connect to the voice channel

        if ctx.author.voice.channel.id != vc.channel.id: # check if the bot is not in the voice channel
            return await ctx.respond("You must be in the same voice channel as the bot.") # return an error message

        song = await wavelink.YouTubeTrack.search(query=search, return_first=True) # search for the song

        if not song: # check if the song is not found
            return await ctx.respond("No song found.") # return an error message

        await vc.play(song) # play the song
        await ctx.respond(f"Now playing: `{vc.source.title}`") # return a message
        
    @discord.slash_command()
    async def stop(self,ctx):
        vc = ctx.voice_client
        await vc.stop()
        await ctx.respond(f"Sucessfully stoped")

def setup(bot):
    bot.add_cog(Music(bot))