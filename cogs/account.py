import discord
from discord.ext import commands
import os
import asyncio
import aiosqlite

DATABASE = 'data.db'



class Modal(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Modal system activated!")
        setattr(self.bot,"db",await aiosqlite.connect(DATABASE))
        async with self.bot.db.cursor() as cursor:
            await cursor.execute('CREATE TABLE IF NOT EXISTS data (real_name TEXT, name TEXT, mail TEXT, content TEXT, guild INTEGER, id INTEGER ,level INTEGER ,xp INTEGER)')
    
    

    @discord.slash_command(description = "this command is not work...")
    async def account_info(self,ctx,member: discord.Member):
        if member is None:
            member = ctx.auhtor
        async with self.bot.db.cursor()as cursor:
            await cursor.execute("SELECT name FROM data WHERE guild = ? AND id = ?",(member.id, ctx.guild.id))
            name = await cursor.fetchone()

    

    @discord.slash_command(description = "Create the Ghost_world account")
    async def create_account(self, ctx: discord.ApplicationContext):
        class Resister_Modal(discord.ui.Modal):
            def __init__(self, bot, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.bot = bot
                self.add_item(discord.ui.InputText(label="Name"))
                self.add_item(discord.ui.InputText(label="your mail"))
                self.add_item(discord.ui.InputText(label="statues", style=discord.InputTextStyle.long))

            async def callback(self, interaction:discord.Interaction):
                async with self.bot.db.cursor() as cursor:
                    await cursor.execute("SELECT content FROM data WHERE guild = ? AND real_name = ?",(interaction.guild_id, interaction.user.name))
                    data = await cursor.fetchone()
                    if data is None:
                        await cursor.execute('INSERT INTO data (real_name, name, mail, content, guild, id, level, xp) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',(interaction.user.name ,self.children[0].value, self.children[1].value, self.children[2].value ,interaction.guild_id, interaction.user.id, 1, 0))
                        await self.bot.db.commit()
                        await interaction.response.send_message("rester complete")
                    if data:
                        await interaction.response.send_message("!You already have account!")
        modal = Resister_Modal(self.bot, title="Resister GW account.")
        await ctx.send_modal(modal)
        print(f"{ctx.user.name} is resister the GW")

def setup(bot):
    bot.add_cog(Modal(bot))
