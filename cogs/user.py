import discord
from discord.ext import commands
from discord.commands import Option
import datetime
global_blacklist_user = [800186598779256852 , 692642438304759819]

blacklisted_users = [692642438304759819]
specific_server_id = 1069174895893827604
class user(commands.Cog):

    new_member_role_name = "DEV Role"
    rules_message_id = 1084676435786084422

    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self,member):
        channel = self.bot.get_channel(1083242633310261298) # Where ID is your welcome channel's ID
        guild = self.bot.get_guild(1069174895893827604)
        role = guild.get_role(1072660369274843257)
        await member.add_roles(role)
        embed = discord.Embed(title="welcome",description='만나서 반가워요!! XD',color=0x1700ff)
        embed.set_thumbnail(url=member.avatar.url)
        await member.send(f"{member.mention} welcome to server!")
        await channel.send(f'{member.mention} 님 {member.guild.name} 서버에 오신것을 환영합니다!!!',embed=embed)

    @discord.slash_command(aliases=['추방'])
    @commands.has_permissions(administrator=True)
    async def kick_user(self, ctx, nickname: discord.Member, password:Option(str,"비밀번호")):
        if password == "ghost_0939":
            await nickname.kick()
            await ctx.respond(f"{nickname} 님이 추방되었습니다.")
        else:
            await ctx.respond("Password Wrong")

    @discord.slash_command(aliases=['차단'])
    @commands.has_permissions(administrator=True)
    async def ban_user(self, ctx, nickname: discord.Member, password:Option(str,"비밀번호")):
        if password == "ban_087860":
            await nickname.ban()
            await ctx.respond(f"{nickname} 님이 차단되었습니다.")
        else:
            await ctx.respond("warning! No Access allowed")

    @commands.command()
    async def profile(self,ctx):
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

    @discord.slash_command()
    async def profile(self,ctx):
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
    @discord.slash_command()
    @commands.is_owner()
    async def send_user(self, ctx, user:discord.Member, send_message:Option(str,"message")):
        member = ctx.author
        await user.send(f"{send_message} send bt {member}")

    @commands.Cog.listener()
    async def on_message(self,message):
        if message.guild is not None and message.guild.id == specific_server_id:
            if message.author.id in blacklisted_users:
                await message.delete()
            else:
                await self.bot.process_commands(message)
        else:
            await self.bot.process_commands(message)

        if message.author.id in global_blacklist_user:
            await message.delete()
        else:
            await self.bot.process_commands(message)


def setup(bot):
    bot.add_cog(user(bot))