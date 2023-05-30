import discord
from discord.ext import commands
import wavelink

bot = discord.Bot()

async def connect_nodes():
  """Connect to our Lavalink nodes."""
  await bot.wait_until_ready() # wait until the bot is ready

  await wavelink.NodePool.create_node(
    bot=bot,
    host='fsn.lavalink.alexanderof.xyz',
    port=2333,
    password = "lavalink",
  ) # create a node
    
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot # create a node
    
    @commands.Cog.listener('on_ready')
    async def on_ready(self):
        node: wavelink.Node = wavelink.NodePool.cr(host='fsn.lavalink.alexanderof.xyz',port=2333, password='lavalink')
        await wavelink.NodePool.connect(client=self.bot, nodes=[node])

    @commands.Cog.listener('on_wavelink_node_ready')
    async def on_node_ready(self, node):
        print(f"Wavelink node '{node.identifier}' is ready.")

    @commands.command()
    async def connect(self, ctx, *, channel: discord.VoiceChannel=None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise discord.DiscordException('No channel to join. Please call the command in a voice channel.')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        await ctx.send(f'Connecting to **`{channel.name}`**')
        await player.connect(channel.id)

    @commands.command()
    async def play(self, ctx, *, query: str):
        tracks = await self.bot.wavelink.get_tracks(f'ytsearch:{query}')

        if not tracks:
            return await ctx.send('Could not find any songs with that query.')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect)

        await ctx.send(f'Added {str(tracks[0])} to the queue.')
        await player.play(tracks[0])

def setup(bot):
    bot.add_cog(Music(bot))
