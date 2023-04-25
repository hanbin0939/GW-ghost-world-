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
    await asyncio.sleep(3)
    async with bot.db.cursor() as cursor:
        await cursor.execute('''CREATE TABLE IF NOT EXISTS levels (level INTEGER, xp INTEGER, user INTEGER, guild INTEGER)''')

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    author = message.author
    guild = message.guild
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT xp FROM levels WHERE user =? AND guild =?",(str(author.id),str(guild.id)))
        xp = await cursor.fetchone()
        await cursor.execute("SELECT xp FROM levels WHERE user =? AND guild =?",(str(author.id),str(guild.id)))
        level = await cursor.fetchone()

        if not xp or not level:
            await cursor.execute("INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)", (0, 0, str(author.id), str(guild.id)))
        try:
            xp = xp[0]
            level = level[0]
        except TypeError:
            xp = 0
            level = 0
        if level < 5:
            xp += random.randint(1,3)
            await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?",(str(xp),str(author.id),str(guild.id)))
        else:
            rand = random.randint(1, (level//4))
            if rand == 1:
                xp += random.randint(1,3)
                await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?",(str(xp),str(author.id),str(guild.id)))
        if xp >= 100:
            level += 1
            await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND guild = ?",(str(xp),str(author.id),str(guild.id)))
            await cursor.execute("UPDATE levels SET xp = ? WHERE user = ? AND GUILDS = ?",(0,str(author.id),str(guild.id)))
            await message.channel.send(f"{author.mention} 님이 **{level}** 이 되었습니다!!")
    await bot.db.commit()

@bot.slash_command(aliases=['lvl','rank','r'])
async def level(ctx,member: discord.Member = None):
    if member is None:
        member = ctx.author
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?",(member.id,ctx.guild.id,))
        xp = await cursor.fetchone()
        await cursor.execute("SELECT level FROM levels WHERE user = ? AND guild = ?",(member.id,ctx.guild.id,))
        level = await cursor.fetchone()

        if not xp or not level:
            await cursor.execute("INSERT INTO levels (level, xp, user, guild) VALUES (?, ?, ?, ?)", (0, 0, str(member.id), str(ctx.guild.id),))
        try:
            xp = xp[0]
            level = level[0]
        except TypeError:
            xp = 0
            level = 0
        await ctx.respond(f"{member.name}'s level is{level}\nXP:{xp}")


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