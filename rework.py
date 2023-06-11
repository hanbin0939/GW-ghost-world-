import discord
from dotenv import load_dotenv
from discord.commands import Option
from discord.ext import commands
from config.data import *
from discord.shard import EventItem

load_dotenv()

bot = commands.Bot(command_prefix='%',intents=discord.Intents.all(),owner_ids=[759072684461391893])
cogs_path = 'cogs'
cogs_list = ["music",
             "mp3"
             ]

for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')

@bot.event
async def on_ready():
    print("Bot Ready!")
    await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="Emaegency alart (DDOS)"))
    
bot.run(token)