import asyncio
import discord
from discord.ext import commands, tasks
from discord.utils import find
import os
import utils
from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageFilter #Used for !owner get-info and will be used for DMS on member_join
import random
import sqlite3
from itertools import cycle


class Contest(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        #self.poem_contest.start()


    def cog_unload(self):
        self.poem_contest.cancel()

    DIR = "d:\CODING\DISCORD BOT\Bot\\"
    db = sqlite3.connect(os.path.join(DIR, "Poems.db"))
    SQL = db.cursor()
    SQL.execute('create table if not exists Poems("Num" integer primary key autoincrement, "user_id" INTEGER NOT NULL, "user_name" TEXT, "title" TEXT,"poem" TEXT, "votes" INTEGER)')






    DIR_Accounts="d:\CODING\DISCORD BOT\Bot\\"
    dbAccounts = sqlite3.connect(os.path.join(DIR_Accounts, "BankAccounts.db"))
    SQLAccounts = dbAccounts.cursor()

    DIR_guilds="d:\CODING\DISCORD BOT\Bot\\"
    db_guilds=sqlite3.connect(os.path.join(DIR_guilds,"Guild.db"))
    SQL_guilds=db_guilds.cursor()

    SQL_guilds.execute('select guild_id from Guilds where wantsPoem=1')
    result=SQL_guilds.fetchall()



    poem_themes=cycle(['Death','Love','Friendship','24 hours','Day or Night?']) #Poem Themes, these are just examples ofc.

    @tasks.loop(hours=48) #Poem Contest occurs every 48 hours
    async def poem_contest(self):
        print("Poem Contest Started")        
        theme=next(Contest.poem_themes)
        print("ok1")
        Contest.SQL_guilds.execute('select guild_id from Guilds where wantsPoem=1')
        result=Contest.SQL_guilds.fetchall()
        print(result)
        if len(result)==0:
            print("restarting in 5 minutes")
            guild=self.bot.get_guild(717447897263636542)
            announcements = find(lambda x: x.name == 'z-announcements',  guild.text_channels)
            embed=discord.Embed(
                title="How unfortunate! No server enabled the Poem Contest Feature",
                description="A miracle may happen in 5 minutes!",
                color=0x3cd3f6
            )
            await announcements.send(embed=embed)
            await asyncio.sleep(300)
            self.poem_contest.restart()
        result=[i[0] for i in result]
        print("ok2")
        for guild_id in result:
            guild=self.bot.get_guild(guild_id)
            print(guild)
            weather_msg = find(lambda x: x.name == 'z-announcements',  guild.text_channels)
            await weather_msg.send(f"Even started! The theme is {theme}. Good luck!")
        print("ok3")
        #These 4 lines create a Poem Table (SQL)
        DIR = "d:\CODING\DISCORD BOT\Bot\\"
        db = sqlite3.connect(os.path.join(DIR, "Poems.db"))
        SQL = db.cursor()
        SQL.execute('create table if not exists Poems("Num" integer primary key autoincrement, "user_id" INTEGER NOT NULL, "user_name" TEXT, "title" TEXT,"poem" TEXT, "votes" INTEGER)')
        print("ok4")
        for guild_id in result:
            guild=self.bot.get_guild(guild_id)
            weather_msg = find(lambda x: x.name == 'z-announcements',  guild.text_channels)
            await weather_msg.send("Waiting 48 hours!")
        print("ok5")
        await asyncio.sleep(172800)#48 hours
        SQL.execute("SELECT user_name, max(votes) FROM Poems;")
        result = SQL.fetchall()
        winner=result[0][0] #Winner of the contest
        print("ok6")
        for guild_id in result:
            guild=self.bot.get_guild(guild_id)
            announcements = find(lambda x: x.name == 'z-announcements',  guild.text_channels)
            await announcements.send("And the winner of the contest is...") #I know that ctx here is not gonna work (I think?). But you do get what I want
            await asyncio.sleep(2)
            await announcements.send(f'{winner}!!!!!')
            await asyncio.sleep(1)
            await announcements.send("Even ended! it will restart in 30 seconds")
        #These 3 commands reset everything to restart the loop
        SQL.execute("DROP TABLE Poems") #Deletes the Poems table
        Contest.SQLAccounts.execute('update Accounts set PoetChoice = ""') #Set everyone's vote to ""
        Contest.SQLAccounts.execute('update Accounts set voted = 0') #No one voted
        Contest.SQLAccounts.execute(f'update Accounts set balance = balance + 1000 where user_name = ?', (str(winner)))

        Contest.dbAccounts.commit()
        

    @poem_contest.before_loop
    async def before_poem_contest(self):
        await self.bot.wait_until_ready()

    @commands.command()
    async def brute_start(self,ctx):
        guild=self.bot.get_guild(717447897263636542)
        announcements = find(lambda x: x.name == 'z-announcements',  guild.text_channels)
        await ctx.send("Brute force mode enabled to start Poem Contest")
        self.poem_contest.restart()

    @commands.command()
    async def brute_stop(self,ctx):
        guild=self.bot.get_guild(717447897263636542)
        announcements = find(lambda x: x.name == 'z-announcements',  guild.text_channels)
        Contest.SQL.execute("DROP TABLE Poems") #Deletes the Poems table
        Contest.SQLAccounts.execute('update Accounts set PoetChoice = ""') #Set everyone's vote to ""
        Contest.SQLAccounts.execute('update Accounts set voted = 0') #No one voted
        await ctx.send("Brute force mode enabled to cancel Poem Contest")
        self.poem_contest.cancel()

    @commands.group(name="poem",invoke_without_command=False)
    async def poem(self,ctx):
        if ctx.guild is None:
            pass
        else:
            enabled,error_msg=utils.enabledPoem(ctx,Contest.SQL_guilds,Contest.db_guilds,ctx.guild.id)
            if enabled:
                pass
            else:
                await error_msg
                return



    @poem.command(name="send")
    @commands.dm_only() #Command can only be run in a DM
    async def send(self,ctx,title,*,poem): #User sends a DM to the bot to enter the contest : he sends his poem

        lst=[g for g in self.bot.guilds if g.get_member(ctx.author.id)]
        
        if len(lst)>0:

            DIR_guilds="d:\CODING\DISCORD BOT\Bot\\"
            db_guilds=sqlite3.connect(os.path.join(DIR_guilds,"Guild.db"))
            SQL_guilds=db_guilds.cursor()

            canPlay=False
            for i in lst:
                SQL_guilds.execute('select wantsPoem from Guilds where guild_id = ?',(i.id,))
                result=SQL_guilds.fetchone()
                if result[0]==1:
                    canPlay=True
                    available_server=i.name
                    break

            if canPlay:
                user_id=ctx.author.id
                user_name=str(ctx.author)
                default_vote=0


                Contest.SQL.execute(f'select user_id from Poems where user_id="{user_id}"')
                data=Contest.SQL.fetchall()
                if not data:
                    await ctx.author.send("Are you sure of this action? send `!yes` or `!no`")

                    def yes(m):
                        return m.author.id == ctx.author.id

                    yesAnswer = await self.bot.wait_for('message', check=yes)
                    
                    if yesAnswer.content=="!yes":
                        Contest.SQL.execute(f'insert into Poems(user_id, user_name, title, poem, votes) values(?,?,?,?,?)', (user_id,user_name,title,poem,default_vote))
                        Contest.db.commit()
                        await ctx.author.send(f"I received the Poem. Good luck!\n\
                            Since not all servers enabled the Poem Contest Feature, I'll help you out\n\
                            You can use Poem commands in the {available_server} server")
                    
                    
                    else:
                        await ctx.author.send("Action stopped")
                

                else:
                    await ctx.author.send("You already sent your poem")
            
            else:
                await utils.embed(ctx, ctx, "None of the servers you're in has the Poem Contest Feature enabled","Tell them to enable it with [prefix]enable")

        else:
            await utils.embed(ctx,ctx,"You aren't in a server that uses me...","This is my invite link : ")

    @poem.command(name="delete")
    @commands.dm_only()
    async def delete(self,ctx):
        USER_ID=ctx.author.id
        USER_NAME=str(ctx.author)
        Contest.SQL.execute('select user_id from Poems where user_id=?',(USER_ID,))
        data=Contest.SQL.fetchall()
        if len(data)==0:
            await utils.error_embed(ctx,"You never sent a poem","You can send it using `z!poem send Title Content`")
        else:
            Contest.SQL.execute('delete from Poems where user_id=?',(USER_ID,))
            Contest.db.commit()
            Contest.SQLAccounts.execute('update Accounts set poetChoice=?,voted=0 where poetChoice=?',("",USER_NAME,))
            Contest.dbAccounts.commit()
            await utils.embed(ctx,ctx,"I successfully deleted your poem","You can send a new one using `z!poem send Title Content`")

    @poem.command(name="list")
    @utils.appropriate_channel()
    async def list(self,ctx): #Lists all the poems, with their author, title and number of votes

        enabled,error_msg=utils.enabledPoem(ctx,Contest.SQL_guilds,Contest.db_guilds,ctx.guild.id)

        if enabled:
            Contest.SQL.execute("SELECT * from Poems")
            result=Contest.SQL.fetchall()
            poem_list=discord.Embed(
                title="Poem Contest",
                description="Nothing here",
                color=discord.Color.green()
            )
            

            for i in result:
                poem_list.add_field(name='\u200b',value=f' Author=**{i[2]}**------Title=**"{i[3]}"**------Number of votes=**{i[5]}**')
            
            await ctx.send(embed=poem_list)

        else:
            await error_msg

    @poem.command(nmae="read")
    @utils.appropriate_channel()
    async def read(self,ctx,*member): #to read the entirety of a poem

        enabled,error_msg=utils.enabledPoem(ctx,Contest.SQL_guilds,Contest.db_guilds,ctx.guild.id)

        if enabled:
            member=" ".join(member)
            print(member)
            DIR = "d:\CODING\DISCORD BOT\Bot\\"
            db = sqlite3.connect(os.path.join(DIR, "Poems.db"))
            SQL = db.cursor()


            SQL.execute("select * from Poems where user_name=?", (member,))
            result=SQL.fetchone()
            poem=discord.Embed(
                title=f'{result[2]}\' poem',
                description=f"Title: **{result[3]}**",
                color=discord.Color.blue()
            )
            poem.set_footer(text=result[4])
            await ctx.send(embed=poem)
        else:
            await error_msg

    @poem.command(name="vote")
    @utils.appropriate_channel()
    async def vote(self,ctx,*member): #Member votes for a poem. (adds 1 to the number of votes of the poem)
        
        DIR = "d:\CODING\DISCORD BOT\Bot\\"
        db = sqlite3.connect(os.path.join(DIR, "Poems.db"))
        SQL = db.cursor()
        USER_NAME=" ".join(member)
        print(USER_NAME)

        dbAccounts = sqlite3.connect(os.path.join(DIR, "BankAccounts.db"))
        SQLAccounts = dbAccounts.cursor()

        SQLAccounts.execute("select voted from Accounts where user_id=?", (ctx.author.id,))
        hasVoted=SQLAccounts.fetchone()
        
        if hasVoted[0]==0:
            voted=1
            SQL.execute("select user_name from Poems where user_name=?", (USER_NAME,))
            data=SQL.fetchall()
            vote=1
            if not data:
                await ctx.send("This person didn't participate")
            else:
                SQL.execute(f'update Poems set votes = votes + ? where user_name = ?', (vote,USER_NAME))
                db.commit()
                SQLAccounts.execute(f'update Accounts set voted = ? where user_id = ?', (voted,ctx.author.id))
                dbAccounts.commit()
                SQLAccounts.execute(f'update Accounts set poetChoice = ? where user_id = ?', (USER_NAME,ctx.author.id))
                dbAccounts.commit()
                await ctx.send(f'{ctx.author.mention},you voted for {USER_NAME}!')
        else:
            print(hasVoted)
            await ctx.send("You already voted! Revote using `!delVote` to remove your current vote")

    @poem.command(name="delVote")
    @utils.appropriate_channel()
    async def delVote(self,ctx): #Remove the user's vote (to stop voting, or to change his vote)

        DIR = "d:\CODING\DISCORD BOT\Bot\\"
        db = sqlite3.connect(os.path.join(DIR, "Poems.db"))
        SQL = db.cursor()


        dbAccounts = sqlite3.connect(os.path.join(DIR, "BankAccounts.db"))
        SQLAccounts = dbAccounts.cursor()

        SQLAccounts.execute("select voted from Accounts where user_id=?", (ctx.author.id,))
        hasVoted=SQLAccounts.fetchone()

        if hasVoted[0]==1:
            removeVote=1
            SQLAccounts.execute("select poetChoice from Accounts where user_id=?", (ctx.author.id,))
            poetChoice=SQLAccounts.fetchone()
            SQL.execute(f'update Poems set votes = votes - ? where user_name = ? and votes>0', (1,poetChoice[0]))
            db.commit()
            SQLAccounts.execute(f'update Accounts set voted = ? where user_id = ?', (0,ctx.author.id))
            dbAccounts.commit()
            SQLAccounts.execute(f'update Accounts set poetChoice = ? where user_id = ?', ("",ctx.author.id))
            dbAccounts.commit()

            await ctx.send(f'We removed your vote for {poetChoice[0]}\'s poem. You can now vote again!')

        else:
            await ctx.send("You can't use that command since you haven't voted yet!")

def setup(bot):
    bot.add_cog(Contest(bot))