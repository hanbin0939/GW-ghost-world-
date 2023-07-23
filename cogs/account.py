import discord
from discord.ext import commands
import random
import aiosqlite

DATABASE = 'data.db'


class Modal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("level system activated!")
        setattr(self.bot, "db", await aiosqlite.connect(DATABASE))
        async with self.bot.db.cursor() as cursor:
            await cursor.execute(
                'CREATE TABLE IF NOT EXISTS data (real_name TEXT, name TEXT, mail TEXT, content TEXT, guild INTEGER, id INTEGER ,level INTEGER ,xp INTEGER, chat_xp INTEGER)')

    @discord.slash_command(description="this command is not work...")
    async def account_info(self, ctx, member: discord.Member):
        if member is None:
            member = ctx.auhtor
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT name FROM data WHERE guild = ? AND id = ?", (member.id, ctx.guild.id))

    @commands.Cog.listener("on_message")
    async def on_message(self, message):
        if message.guild is None:
            return
        author = message.author
        guild = message.guild
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT chat_xp, level FROM data WHERE guild = ? AND id = ?", (guild.id, author.id))
            data = await cursor.fetchone()
        if not data:
            await message.delete()
            await author.send("You need to resister GW account")
            '''
        else:
            chat_xp = data[0]
            level = data[1]
        if level < 4:
            chat_xp += 30
        else:
            rand = random.randint(1, (level // 4))
            if rand == 1:
                chat_xp += random.randint(1, 4) * 4

        if chat_xp >= 1000:
            level += 1
            chat_xp = 0
            await message.channel.send(f"{author.mention} 님이 **{level} Level** 이 되었습니다!!")
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("UPDATE data SET chat_xp = ?, level = ? WHERE guild = ? AND id = ?",
                                 (chat_xp, level, str(guild.id), str(author.id)))
                                 '''
    @discord.slash_command()
    @commands.is_owner()
    async def force_create_bot_account(self,ctx, member,bot_name,id):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute(
                'INSERT INTO data (real_name, name, mail, content, guild, id, level, xp, chat_xp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (member, bot_name, None,
                 None, ctx.guild.id, id, 1, 0, 0))
            await self.bot.db.commit()
            await ctx.respond("rester complete")

    @discord.slash_command()
    @commands.is_owner()
    async def force_create_account(self,ctx, member,user_name,email,id):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute(
                'INSERT INTO data (real_name, name, mail, content, guild, id, level, xp, chat_xp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (member, user_name, email,
                 'Force Account', ctx.guild.id, id, 1, 0, 0))
            await self.bot.db.commit()
            await ctx.respond("rester complete")
    @discord.slash_command(description="Create the Ghost_world account")
    async def create_account(self, ctx: discord.ApplicationContext):
        class Resister_Modal(discord.ui.Modal):
            def __init__(self, bot, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.bot = bot
                self.add_item(discord.ui.InputText(label="Name", style=discord.InputTextStyle.short))
                self.add_item(discord.ui.InputText(label="your mail"))
                self.add_item(discord.ui.InputText(label="자신을 소개해보세요!!!", style=discord.InputTextStyle.long))

            async def callback(self, interaction: discord.Interaction):
                async with self.bot.db.cursor() as cursor:
                    await cursor.execute("SELECT content FROM data WHERE guild = ? AND real_name = ?",
                                         (interaction.guild_id, interaction.user.name))
                    data = await cursor.fetchone()
                    if data is None:
                        await cursor.execute(
                            'INSERT INTO data (real_name, name, mail, content, guild, id, level, xp, chat_xp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                            (interaction.user.name, self.children[0].value, self.children[1].value,
                             self.children[2].value, interaction.guild_id, interaction.user.id, 1, 0, 0))
                        await self.bot.db.commit()
                        await interaction.response.send_message("rester complete")
                    if data:
                        await interaction.response.send_message("!You already have account!")

        modal = Resister_Modal(self.bot, title="Resister GW account.")
        await ctx.send_modal(modal)
        print(f"{ctx.user.name} is resister the GW")


def setup(bot):
    bot.add_cog(Modal(bot))
