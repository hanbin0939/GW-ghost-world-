import discord
from discord.ext import commands
import json
import os
from config.data import token
import datetime
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
os.chdir(r'C:\Users\hero7\OneDrive\바탕 화면\GW-ghost-world-')
@client.event
async def on_ready():
    print(f"{len(client.guilds)} server joined\n")

    
@client.slash_command()
async def my_info(ctx,member:discord.Member = None):
    member = ctx.author
    roles = [role for role in member.roles[1:]]
    embed = discord.Embed(title=f"{ctx.author}",color=0x929292)
    embed.add_field(name="**•ID•**", value=f"{member.id}", inline=True)
    embed.add_field(name="**•Status•**", value=str(member.status).replace("dnd", "Do Not Disturb"), inline=True)
    embed.set_thumbnail(url=f"{member.avatar.url}")
    embed.add_field(name=f"**•Roles• ({len(ctx.author.roles) - 1})**", value='• '.join([role.mention for role in roles]), inline=False)
    embed.add_field(name="**•Account Created At•**", value=f"{member.created_at.date()}".replace("-", "/"), inline=True)
    embed.add_field(name="**•Joined Server At•**", value=f"{member.joined_at.date()}".replace("-", "/"), inline = True)
    embed.set_footer(icon_url = f"{ctx.author.avatar.url}", text = f"Requested by {ctx.author}")
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.respond(embed=embed)



client.run(token)