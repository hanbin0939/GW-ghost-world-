import os
import discord
from discord.ext import commands

folder_path = "./my_folder"
file_name = "bug_report.txt"

class MyModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="What is bot name??"))
        self.add_item(discord.ui.InputText(label="세부사항", style=discord.InputTextStyle.long))

    async def callback(self,interaction: discord.Interaction):
        with open(file_path,'w')as file:
            nickname = interaction.user.name
            bot_name =self.children[0].value
            des = self.children[1].value
            file.write(f"{nickname} is report {bot_name} 's error'.\ndescription -> {des}")
            await interaction.response.send_message("오류신고가 완료되었습니다!!")
            new_file_path = f"{nickname}_bug_report.txt"
        os.rename(file,new_file_path)

file_path = os.path.join(folder_path, file_name)
class Report(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("운영체제", os.name)

        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        


    @discord.slash_command()
    async def bug_report(self,ctx: discord.ApplicationContext):
        """Shows an example of a modal dialog being invoked from a slash command."""
        modal = MyModal(title="Modal via Slash Command")
        await ctx.send_modal(modal)
        

def setup(bot):
    bot.add_cog(Report(bot))