import discord
from discord.ext import commands
import utils

class Help(commands.Cog):

    def __init__(self,bot):
        self.bot=bot
        
    @commands.command()
    @utils.appropriate_channel()
    async def help(self,ctx):
        pass

    @commands.group(name="help",invoke_without_command=True)
    @utils.appropriate_channel()
    async def help(self,ctx):
        
        general_help=discord.Embed(
            title="General Help for zola",
            description="Everything you need to know",
            color=discord.Color.green()
        )
        general_help.add_field(name="Basic commands", value="Bot info ℹ️ - `z!about`\nServer info - `z!info`",inline=False)
        general_help.add_field(name="👑 Moderators, Admins & Owner 👑", value="Use my Big3 commands with `z!help big3`",inline=False)
        general_help.add_field(name="Do you dream of wealth?", value="Use my economy commands. More info with `z!help economy`",inline=False)
        general_help.add_field(name="<a:froggydefault:744347632754884639>Games<a:froggydefault:744347632754884639>", value="-Play the **Flag game** 🇫🇷. More info with `z!help flag`\n-Play the **Yam Game** 🎲. More info with `z!help yam`\n-Participate to a **Multiserver Poem Contest** ✍️! More info with `z!help poem`",inline=False)
        await ctx.send(embed=general_help)


    @help.command(name="big3")
    async def big3(self,ctx):
        big3_help=discord.Embed(
            title="Big3 help"
        )
        await ctx.send(embed=big3_help)
    
    @help.command(name="economy")
    async def economy(self,ctx):
        economy_help=discord.Embed(
            title="Economy help"
        )
        await ctx.send(embed=economy_help)



    """----------------GAME HELP-----------------------"""

    @help.command(name="flag")
    async def flag(self,ctx):
        flag_help=discord.Embed(
            title="Flag help"
        )
        await ctx.send(embed=flag_help)

    @help.command(name="yam")
    async def yam(self,ctx):
        yam_help=discord.Embed(
            title="Yam help"
        )
        await ctx.send(embed=yam_help)
    
    @help.command(name="poem")
    async def poem(self,ctx):
        poem_help=discord.Embed(
            title="Poem help"
        )
        await ctx.send(embed=poem_help)

def setup(bot):
    bot.add_cog(Help(bot))
