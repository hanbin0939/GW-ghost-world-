import discord
import random
from discord.ext import commands
import asyncio
from config.data import token
import datetime
import aiosqlite
from easy_pil import*
bot = commands.Bot(command_prefix='&')

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
        if level <= 5:
            xp += random.randint(1,4) * 7

        if level == 6:
            xp += random.randint(1,4) * 5

        if level == 7:
            xp += random.randint(1,4) * 4
        
        if level == 8:
            xp += random.randint(1,4) * 4

        if level == 9:
            xp += random.randint(1,4) * 4
        if level == 10:
            xp += random.randint(1,4) * 4

        if level == 11 :
            xp += random.randint(1,4) * 3
        if level == 12:
            xp += random.randint(1,4) * 3

        else:
            xp += random.randint(1,3)

        
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
            level = 0

        if level == 1:
            embed = discord.Embed(title=f"{member.name}",description=f"your level is *level {level}*",color=0xAEAEAE)
            embed.set_footer(text=f"tear : Grunt\ncurrent EXP : {xp}")
            embed.set_thumbnail(url="attachment://image.png")
            with open("image/Grunt.png", "rb") as f:
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

        if level == 8:
            embed = discord.Embed(title=f"{member.name}",description=f"your level is *Level {level}*",color=0xEC0A0A)
            embed.set_thumbnail(url="attachment://image.jpg")
            embed.set_footer(text=f"tier : hank\nEXP : {xp}")
            with open("image/hank.jpg", "rb") as f:
                await ctx.respond(embed=embed, file=discord.File(f, 'image.jpg'))
        if level == 9:
            embed = discord.Embed(title=f"{member.name}",description=f"your level is *Level {level}*",color=0x007025)
            embed.set_thumbnail(url="attachment://image.png")
            embed.set_footer(text=f"tier : tricky\nEXP : {xp}")
            with open("image/tricky.png", "rb") as f:
                await ctx.respond(embed=embed, file=discord.File(f, 'image.png'))
        if level == 10:
            embed = discord.Embed(title=f"{member.name}",description=f"your level is *Level {level}*",color=0x100000)
            embed.set_thumbnail(url="attachment://image.png")
            embed.set_footer(text=f"tier : auditor\nEXP : {xp}")
            with open("image/Auditor.png", "rb") as f:
                await ctx.respond(embed=embed, file=discord.File(f, 'image.png'))
        if level == 11:
            embed = discord.Embed(title=f"{member.name}",description=f"your level is *Level {level}*",color=0xFF0000)
            embed.set_thumbnail(url="attachment://image.png")
            embed.set_footer(text=f"tier : Demon\nEXP : {xp}")
            with open("image/DemonFNMIcon.png", "rb") as f:
                await ctx.respond(embed=embed, file=discord.File(f, 'image.png'))
        if level == 12:
            embed = discord.Embed(title=f"{member.name}",description=f"your level is *Level {level}*",color=0xFF0000)
            embed.set_thumbnail(url="attachment://image.png")
            embed.set_footer(text=f"tier : evil dual\nEXP : {xp}")
            with open("image/evildual.png", "rb") as f:
                await ctx.respond(embed=embed, file=discord.File(f, 'image.png'))
        if level == 13:
            embed = discord.Embed(title=f"{member.name}",description=f"your level is *Level {level}*",color=0xFF0000)
            embed.set_thumbnail(url="attachment://image.png")
            embed.set_footer(text=f"tier : hell clown\nEXP : {xp}")
            with open("image/hell.png", "rb") as f:
                await ctx.respond(embed=embed, file=discord.File(f, 'image.png'))
        if level == 14:
            embed = discord.Embed(title=f"{member.name}",description=f"your level is *Level {level}*",color=0x555454)
            embed.set_thumbnail(url="attachment://image.png")
            embed.set_footer(text=f"tier : Dual\nEXP : {xp}")
            with open("image/dual.png", "rb") as f:
                await ctx.respond(embed=embed, file=discord.File(f, 'image.png'))
        if level == 15:
            embed = discord.Embed(title=f"{member.name}",description=f"your level is *Level {level}*",color=0xD70000)
            embed.set_thumbnail(url="attachment://image.png")
            embed.set_footer(text=f"tier : MAG HANK\nEXP : {xp}")
            with open("image/mag_hank.png", "rb") as f:
                await ctx.respond(embed=embed, file=discord.File(f, 'image.png'))
        else:
            await ctx.respond(f"{member.name}'s level is{level}\nXP:{xp}")

@bot.slash_command(aliases=['lvl','rank','r'])
async def level_image(ctx,member: discord.Member = None):
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
            level = 0
        user_data = {
            "name" : f"{member.name}#{member.discriminator}",
            "xp" : xp,
            "level" : level,
            "next_level_xp" : 100,
            "percentage": xp,

        }

        background = Editor(Canvas((900,300),color="#141414"))
        profile_picture = await load_image_async(str(member.avatar.url))
        profile = Editor(profile_picture).resize((150,150)).circle_image()

        poppins = Font.poppins(size=40)
        poppins_small = Font.poppins(size=20)

        card_right_shape = [(600,0), (750, 300), (900, 300), (900,0)]

        background.polygon(card_right_shape,color="#FFFFFF")
        background.paste(profile, (30,30))

        background.rectangle((30,220),width=650,height=40,color="#FFFFFF",radius=20)
        background.bar((30,220),max_width=650, height=40, percentage=user_data["percentage"],color="#282828",radius=20,)
        background.text((200,40), user_data["name"], font= poppins, color="#FFFFFF")

        background.rectangle((200,100),width=350,height=2, fill="#FFFFFF")
        background.text(
            (200,130),
            f"levle - {user_data['level']} | XP - {user_data['xp']}/{user_data['next_level_xp']}",
            font=poppins_small,
            color="#FFFFFF"
        )

        file = discord.File(fp=background.image_bytes,filename="levelcard.png")
        await ctx.respond(file=file)

@bot.slash_command(aliases=['lb','lvlboard'])
async def leaderboard(ctx):
    async with bot.db.cursor() as cursor:
        await cursor.execute("SELECT xp FROM levels WHERE user = ? AND guild = ?",(ctx.guild.id))
        levelsys = await cursor.fetchone()
        if levelsys:
            if not levelsys[0] == 1:
                await ctx.reply("Level system disabled!!")
        await cursor.execute("SELECT level, xp, user FROM levels WHERE guild = ?",(ctx.guild.id))
        data = await cursor.fetchall()
        if data:
            em = discord.Embed(title="Level Leaderboard")
            count = 0
            for table in data:
                count += 1
                user = ctx.guild.get_member(table[2])
                em.add_field(name=f"{count}. {user.name}",value=f"Level-**{table[0]}** | XP-**{table[1]}**",inline=False)
            return await ctx.send(embed=em)
        return await ctx.respond("there has not users stored in leaderboard")


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