import discord
from discord.ext import commands
from discord.utils import get,find
import sqlite3
import os


DIR_guilds="d:\CODING\DISCORD BOT\Bot\\"
db_guilds=sqlite3.connect(os.path.join(DIR_guilds,"Guild.db"))
SQL_guilds=db_guilds.cursor()

class Wants(commands.Cog):
    
    def __init__(self,bot):
        self.bot=bot
        



    def update_db(result,guild_id,option,msg_option,enable):
        SQL_guilds.execute('select prefix from Guilds where guild_id = ?', (guild_id,))
        prefix=SQL_guilds.fetchone()
        prefix=prefix[0]

        if result==0 and enable:
            SQL_guilds.execute(f'update Guilds set {option} = 1 where guild_id = ?', (guild_id,))
            db_guilds.commit()
            embed=discord.Embed(
                title=f'{msg_option} is now enabled',
                description=f"You can disable it whenever you want with `{prefix}disable option",
                color=discord.Color.green()
            )
            
            return embed, True
        elif result==1 and enable:
            embed=discord.Embed(
                title=f'{msg_option} is already enabled!',
                description=f"You can disable it whenever you want with `{prefix}disable option",
                color=discord.Color.red()
            )
            return embed, True
        elif result==1 and not enable:
            SQL_guilds.execute(f'update Guilds set {option} = 0 where guild_id = ?', (guild_id,))
            db_guilds.commit()
            embed=discord.Embed(
                title=f'{msg_option} is now disabled',
                description=f"You can enable it whenever you want with `{prefix}enable option",
                color=discord.Color.green()
            )
            
            return embed, False
        elif result==0 and not enable:
            embed=discord.Embed(
                title=f'{msg_option} is already disabled!',
                description=f"You can enable it whenever you want with `{prefix}enable option",
                color=discord.Color.red()
            )
            return embed, False
  
    def options_status(result,message):
        if result==1:
            name="✅"+message+"✅"
            value="is Active🟢"
        else:
            name="❌"+message+"❌"
            value="is Disabled🔴"
        return name,value



    @commands.group(name="enable",invoke_without_command=True)
    #@commands.has_permissions(manage_guild=True)
    async def enable(self,ctx):
    
        GUILD_ID=ctx.guild.id
        SQL_guilds.execute('select * from Guilds where guild_id = ?',(GUILD_ID,))
        result=SQL_guilds.fetchone()
        print(result)

        wantsWelcome=result[4]
        Welcome_msg="Welcome Feature"
        Welcome_name,Welcome_value=Wants.options_status(wantsWelcome,Welcome_msg)
        
        wantsPoem=result[5]
        Poem_msg="Poem Contest Feature"
        Poem_name,Poem_value=Wants.options_status(wantsPoem,Poem_msg)

        wantsCrosschat=result[6]
        Crossc_msg="Cross-chat Feature"
        Crossc_name,Crossc_value=Wants.options_status(wantsCrosschat,Crossc_msg)


        embed=discord.Embed(
            title="Zola Options",
            description="Check if they are enabled or not in your server",
            color=0x048df6
        )
        embed.add_field(name=Welcome_name,value=Welcome_value,inline=False)
        embed.add_field(name='\u200b',value="\u200b", inline=False)
        embed.add_field(name=Poem_name,value=Poem_value,inline=False)
        embed.add_field(name='\u200b',value="\u200b", inline=False)
        embed.add_field(name=Crossc_name,value=Crossc_value,inline=False)
        await ctx.send(embed=embed)
        
    
    @enable.command(name="Welcome")
    @commands.has_permissions(manage_guild=True)
    async def Welcome(ctx):
        GUILD_ID=ctx.guild.id
        guild=ctx.guild
        SQL_guilds.execute('select wantsWelcome from Guilds where guild_id= ?', (GUILD_ID,))
        wantsWelcome = SQL_guilds.fetchone()
        option="wantsWelcome"
        msg_option="Welcome Feature"
        #Create in case a if is None
        embed,isEnable=Wants.update_db(wantsWelcome[0],GUILD_ID,option,msg_option,True)
        await ctx.send(embed=embed)

        category = get(guild.categories, name='ZolaBOT')
        if isEnable and not find(lambda x: x.name == 'zwelcome',  guild.text_channels):
            await guild.create_text_channel('zwelcome', category=category)

    @enable.command(name="Poem")
    @commands.has_permissions(manage_guild=True)
    async def Poem(ctx):
        GUILD_ID=ctx.guild.id
        SQL_guilds.execute('select wantsPoem from Guilds where guild_id= ?', (GUILD_ID,))
        wantsPoem = SQL_guilds.fetchone()
        option="wantsPoem"
        msg_option="Poem Contest Feature"
        #Create in case a if is None
        embed,isEnable=Wants.update_db(wantsPoem[0],GUILD_ID,option,msg_option,True)
        await ctx.send(embed=embed)

    @enable.command(name="cross_chat")
    @commands.has_permissions(manage_guild=True)
    async def cross_chat(ctx):
        GUILD_ID=ctx.guild.id
        guild=ctx.guild
        SQL_guilds.execute('select wantsCrosschat from Guilds where guild_id= ?', (GUILD_ID,))
        wantsCrosschat = SQL_guilds.fetchone()
        option="wantsCrosschat"
        msg_option="Cross-chat Feature"
        #Create in case a if is None
        embed,isEnable=Wants.update_db(wantsCrosschat[0],GUILD_ID,option,msg_option,True)
        await ctx.send(embed=embed)
        category = get(guild.categories, name='ZolaBOT')
        if isEnable and not find(lambda x: x.name == 'cross-chat',  guild.text_channels):
            await guild.create_text_channel('cross-chat', category=category)






    @commands.group(name="disable",invoke_without_command=True)
    #@commands.has_permissions(manage_guild=True)
    async def disable(self,ctx):
        GUILD_ID=ctx.guild.id
        SQL_guilds.execute('select * from Guilds where guild_id = ?',(GUILD_ID,))
        result=SQL_guilds.fetchone()
        print(result)

        wantsWelcome=result[4]
        Welcome_msg="Welcome Feature"
        Welcome_name,Welcome_value=Wants.options_status(wantsWelcome,Welcome_msg)
        
        wantsPoem=result[5]
        Poem_msg="Poem Contest Feature"
        Poem_name,Poem_value=Wants.options_status(wantsPoem,Poem_msg)

        wantsCrosschat=result[6]
        Crossc_msg="Cross-chat Feature"
        Crossc_name,Crossc_value=Wants.options_status(wantsCrosschat,Crossc_msg)


        embed=discord.Embed(
            title="Zola Options",
            description="Check if they are enabled or not in your server",
            color=0x048df6
        )
        embed.add_field(name=Welcome_name,value=Welcome_value,inline=False)
        embed.add_field(name='\u200b',value="\u200b", inline=False)
        embed.add_field(name=Poem_name,value=Poem_value,inline=False)
        embed.add_field(name='\u200b',value="\u200b", inline=False)
        embed.add_field(name=Crossc_name,value=Crossc_value,inline=False)
        await ctx.send(embed=embed)
        
    
    @disable.command(name="Welcome")
    @commands.has_permissions(manage_guild=True)
    async def Welcome(self,ctx):
        GUILD_ID=ctx.guild.id
        SQL_guilds.execute('select wantsWelcome from Guilds where guild_id= ?', (GUILD_ID,))
        wantsWelcome = SQL_guilds.fetchone()
        option="wantsWelcome"
        msg_option="Welcome Feature"
        #Create in case a if is None
        embed,isEnable=Wants.update_db(wantsWelcome[0],GUILD_ID,option,msg_option,False)
        await ctx.send(embed=embed)

    @disable.command(name="Poem")
    @commands.has_permissions(manage_guild=True)
    async def Poem(self,ctx):
        GUILD_ID=ctx.guild.id
        SQL_guilds.execute('select wantsPoem from Guilds where guild_id= ?', (GUILD_ID,))
        wantsPoem = SQL_guilds.fetchone()
        option="wantsPoem"
        msg_option="Poem Contest Feature"
        print(wantsPoem[0])
        embed,isEnable=Wants.update_db(wantsPoem[0],GUILD_ID,option,msg_option,False)
        await ctx.send(embed=embed)

    @disable.command(name="cross_chat")
    @commands.has_permissions(manage_guild=True)
    async def cross_chat(self,ctx):
        GUILD_ID=ctx.guild.id
        SQL_guilds.execute('select wantsCrosschat from Guilds where guild_id= ?', (GUILD_ID,))
        wantsCrosschat = SQL_guilds.fetchone()
        option="wantsCrosschat"
        msg_option="Cross-chat Feature"
        #Create in case a if is None
        embed,isEnable=Wants.update_db(wantsCrosschat[0],GUILD_ID,option,msg_option,False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Wants(bot))