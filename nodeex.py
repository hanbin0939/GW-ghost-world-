import discord
from discord.ext import commands
import wavelink
from config.data import token

bot = commands.Bot(command_prefix='%',intents=discord.Intents.all(),owner_ids=[759072684461391893])

async def connect_nodes():
  """Connect to our Lavalink nodes."""
  await bot.wait_until_ready() # wait until the bot is ready

  await wavelink.NodePool.create_node(
    bot=bot,
    host='narco.buses.rocks',
    port=2269,
    password = "glasshost1984",
  ) # create a node


@bot.slash_command(name="play")
async def play(ctx, search: str):
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


@bot.event
async def on_ready():
  await connect_nodes() # connect to the server
  await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="this bot is beta testing"))

@bot.event
async def on_wavelink_node_ready(node: wavelink.Node):
  print(f"{node.identifier} is ready.") # print a message

bot.run(token)