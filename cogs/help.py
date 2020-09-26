import discord
from discord.ext import commands
import utils
import sqlite3
import os

class Help(commands.Cog):

    def __init__(self,bot):
        self.bot=bot

    DIR_guilds="d:\CODING\DISCORD BOT\Bot\\"
    db_guilds=sqlite3.connect(os.path.join(DIR_guilds,"Guild.db"))
    SQL_guilds=db_guilds.cursor()

    @commands.command()
    @utils.appropriate_channel()
    async def help(self,ctx):
        pass

    @commands.group(name="help",invoke_without_command=True)
    @utils.appropriate_channel()
    async def help(self,ctx):
        Help.SQL_guilds.execute('select prefix from Guilds where guild_id=?',(ctx.guild.id,))
        prefix=Help.SQL_guilds.fetchone()
        _="".join(prefix)
        general_help=discord.Embed(
            title="General Help for zola",
            description="Everything you need to know",
            color=discord.Color.green()
        )
        general_help.add_field(name="ℹ️ Basic commands ℹ️", value=f"Bot info - `{_}about`\nServer info - `{_}info`",inline=False)
        general_help.add_field(name="👑 Moderators, Admins & Owner 👑", value=f"Use my Big3 commands <:verycool:739613733474795520> with `{_}help big3`",inline=False)
        general_help.add_field(name="🤑 Do you dream of wealth? 🤑", value=f"Use my economy commands. More info with `{_}help economy`",inline=False)
        general_help.add_field(name="<a:rooCool:747680120763973654>Useful/Fun commands<a:rooCool:747680120763973654>", value=f"**Weather App** - More info with `{_}help weather`\n**Dictionnary** - More info with `{_}help define`\n**News in EN-FR-ES** - More info with `{_}info news`",inline=False),
        general_help.add_field(name="<a:froggydefault:744347632754884639>Games<a:froggydefault:744347632754884639>", value=f"-Play the **Flag game** 🇫🇷. More info with `{_}help flag`\n-Play the **Yam Game** 🎲. More info with `{_}help yam`\n-Participate to a **Multiserver Poem Contest** ✍️! More info with `{_}help poem`",inline=False)
        general_help.add_field(name="Customizable commands",value=f"__*NOTE*__: Check if they are activated or not using `{_}enable`\nOnly the Big3 can make changes but any user can give a suggestion\n-**Welcome message** (`{_}help welcome`)\n-**Poem Contest** (`{_}help poem`)\n-**Cross-chat**(`{_}help crosschat`)")
        general_help.set_thumbnail(url="https://pngimg.com/uploads/question_mark/question_mark_PNG129.png")
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
