import discord
import random
from discord.ext import commands
import asyncio
from config.data import token
import datetime
import aiosqlite
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print("Ready")
    setattr(bot,"db",await aiosqlite.connect("level.db"))
    #await asyncio.sleep(1)
    async with bot.db.cursor() as cursor:
        await cursor.execute('''CREATE TABLE IF NOT EXISTS levels (level INTEGER, xp INTEGER, user INTEGER, guild INTEGER)''')


@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1083242633310261298) # Where ID is your welcome channel's ID
    guild = bot.get_guild(1069174895893827604)
    role = guild.get_role(1072660369274843257)
    await member.add_roles(role)
    embed = discord.Embed(title="welcome",description='만나서 반가워요!! XD',color=0x1700ff)
    embed.set_thumbnail(url=member.avatar.url)
    await channel.send(f'{member.mention} 님 {member.guild.name} 서버에 오신것을 환영합니다!!!',embed=embed)

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    author = message.author
    guild = message.guild
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT xp, level FROM levels WHERE user =? AND guild =?",(str(author.id),str(guild.id),))
        result = await cursor.fetchone()
        if not result:
            await cursor.execute("INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)", (0, 0, str(author.id), str(guild.id)))
            xp = 0
            level = 0
        else:
            xp = result[0]
            level = result[1]
        if level < 2:
            xp += random.randint(1, 5) * 10

        if level == 3:
            xp += random.randint(1,3) * 10
        
        if level == 4:
            xp += random.randint(1,3) * 5
        
        if level == 5:
            xp += random.randint(1,3) * 3

        if level == 6:
            xp += random.randint(1,3) * 2
        
        if level == 7:
            xp += random.randint(1,3)

        else:
            xp += random.randint(1,2)

        
        if xp >= 100:
            level += 1
            xp = 0
            await message.channel.send(f"{author.mention} 님이 **{level}** 이 되었습니다!!")

        await cursor.execute("UPDATE levels SET xp = ?, level = ? WHERE user = ? AND guild = ?",(xp, level, str(author.id), str(guild.id)))
    await bot.db.commit()



@bot.slash_command(aliases=['lvl','rank','r'])
async def level(ctx,member: discord.Member = None):
    if member is None:
        member = ctx.author
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?",(member.id,ctx.guild.id))
        xp = await cursor.fetchone()
        await cursor.execute("SELECT level FROM levels WHERE user = ? AND guild = ?",(member.id,ctx.guild.id))
        level = await cursor.fetchone()

        if not xp or not level:
            await cursor.execute("INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)", (0, 0, member.id, ctx.guild.id))
        try:
            xp = xp[0]
            level = level[0]
        except TypeError:
            xp = 0
            level = 1

        if level == 1:
            embed = discord.Embed(title=f"{member.name}",description=f"your level is *level {level}*",color=0xAEAEAE)
            embed.set_footer(text=f"tear : Rich\ncurrent EXP : {xp}")
            embed.set_thumbnail(url="attachment://image.png")
            with open("image/rich.png", "rb") as f:
                await ctx.respond(embed=embed, file=discord.File(f, "image.png"))

        if level == 2:
            embed = discord.Embed(title=f"{member.name}",description=f"your level is *Level {level}*",color=0x900000)
            embed.set_footer(text=f"tear : Jebus\ncurrent EXP : {xp}")
            embed.set_thumbnail(url="attachment://image.png")
            with open("image/jebus.png", "rb") as f:
                await ctx.respond(embed=embed, file=discord.File(f, "image.png"))

        if level == 3:
            embed = discord.Embed(title=f"{member.name}",description=f"your level is *Level {level}*",color=0xff0000)
            embed.set_footer(text=f"tear : Coolhank\ncurrent EXP : {xp}")
            embed.set_thumbnail(url="attachment://image.png")
            with open("image/coolhank.png", "rb") as f:
                await ctx.respond(embed=embed, file=discord.File(f, "image.png"))
        
        if level == 4:
            embed = discord.Embed(title=f"{member.name}",description=f"your level is *Level {level}*",color=0x474747)
            embed.set_footer(text=f"tear : Deimos\ncurrent EXP : {xp}")
            embed.set_thumbnail(url="attachment://image.png")
            with open("image/deimos.png", "rb") as f:
                await ctx.respond(embed=embed, file=discord.File(f, "image.png"))
        if level == 5:
            embed = discord.Embed(title=f"{member.name}",description=f"your level is *Level {level}*",color=0xFF66FF)
            embed.set_footer(text=f"tear : Wank\ncurrent EXP : {xp}")
            embed.set_thumbnail(url="attachment://image.png")
            with open("image/wank.png", "rb") as f:
                await ctx.respond(embed=embed, file=discord.File(f, "image.png"))
        if level == 6:
            embed = discord.Embed(title=f"{member.name}",description=f"your level is *Level {level}*",color=0x474747)
            embed.set_thumbnail(url="attachment://image.png")
            embed.set_footer(text=f"tier : sanford\nEXP : {xp}")
            with open("image/Sanford.png", "rb") as f:
                await ctx.respond(embed=embed, file=discord.File(f, "image.png"))
        if level == 7:
            embed = discord.Embed(title=f"{member.name}",description=f"your level is *Level {level}*",color=0xC30000)
            embed.set_thumbnail(url="attachment://image.png")
            embed.set_footer(text=f"tier : torture\nEXP : {xp}")
            with open("image/torture.png", "rb") as f:
                await ctx.respond(embed=embed, file=discord.File(f, "image.png"))
        #await ctx.respond(f"{member.name}'s level is{level}\nXP:{xp}")

'''
@bot.command(aliases=['lb','lvlboard'])
async def leaderboard(ctx):
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?",(ctx.guild.id))
        levelsys = await cursor.fetchone()
        if levelsys:
            if not levelsys[0] == 1:
                await ctx.reply("Level system disabled!!")
'''

@bot.slash_command()
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



bot.run(token)