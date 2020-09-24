import asyncio
import discord
from discord.ext import commands
import os
import utils
from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageFilter #Used for !owner get-info and will be used for DMS on member_join
import random
import sqlite3
from discord.ext.commands.cooldowns import BucketType

class Yam(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    
    def shot(self,nb):
        result=[]
        for x in range(nb):
            result.append(random.randint(1,6))
        return result


    def fiesta(self,sentence,yes,small):
        happy=discord.Embed(
            title="🎉"+sentence+"🎉",
            color=0xfff700
        )
        if yes and small:
            happy.set_thumbnail(url="https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/birthday-party-for-cute-child-royalty-free-image-700712598-1552358033.jpg")
            happy.add_field(name="Not bad at all my friend",value="May Fortune be with you, always, not only now, ALWAYS")
        elif yes and not small:
            happy.set_image(url="https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/birthday-party-for-cute-child-royalty-free-image-700712598-1552358033.jpg")
            happy.add_field(name="Not bad at all my friend",value="May Fortune be with you, always, not only now, ALWAYS")
        else:
            happy.set_thumbnail(url="https://live.staticflickr.com/7295/12357485995_ea9d9dfdee_n.jpg")
            happy.add_field(name="Usually, I do better...",value="but I guess &ome people are luckier than others...")
        return happy


    def draw(self,seq,round,USER_ID,GUILD_ID):
        x=-60
        y=150
        for i in seq:
            x+=120
            for_player = Image.open(f'yam_images/{USER_ID}{GUILD_ID}.jpg')
            dice1 = Image.open(f'yam_images/{i}.png')
            dice1=dice1.resize((75,75))
            for_player.paste(dice1,(x,y))
            for_player.save(f"yam_images/{USER_ID}{GUILD_ID}.jpg",quality=95)

        file=discord.File(f'yam_images/{USER_ID}{GUILD_ID}.jpg')
        embed=discord.Embed(
            title=f"This is what you got for round {round}",
            color=discord.Colour.red()
        )
        embed.set_image(url=f'attachment://{USER_ID}{GUILD_ID}.jpg')
        return embed,file

    def end_game(self,ctx,score,user_id):
        sc=discord.Embed(
        title=f'You have a score of {score} zolos',
        color=discord.Color.green() 
        )
        
        
        DIR = "d:\CODING\DISCORD BOT\Bot\\"
        db = sqlite3.connect(os.path.join(DIR, "BankAccounts.db"))
        SQL = db.cursor()
        SQL.execute('update Accounts set balance = balance + ? where user_id = ?', (score,user_id))
        db.commit()
        return sc


    async def delete_msgs(self,ctx):
        pass



    async def check(self,ctx,result,small):
        if result.count(result[0])==5: #Yam Check
            to_send=f'You Made A YAM of {result[0]}!'
            msg_sent = await ctx.send(embed=Yam.fiesta(self,to_send,True,small))
            score=100*int(result[0])
            return result,score, msg_sent

        if len(set(result))==2:
            if all(result.count(i)>=2 for i in set(result)):
                to_send='You Made a FULL!!'
                msg_sent = await ctx.send(embed=Yam.fiesta(self,to_send,True,small))
                score=80
                return result,score, msg_sent

        result.sort()

        lst1=[1,2,3,4]
        lst2=[2,3,4,5]
        lst3=[3,4,5,6]

        if result==[1,2,3,4,5] or result==[2,3,4,5,6]: #Long Suite Check
            to_send="YOU GOT A LONG SUITE (and of course, a little suite inside it)!"
            msg_sent = await ctx.send(embed=Yam.fiesta(self,to_send,True,small))
            score=75
            return result,score, msg_sent



        elif all(i in result for i in lst1) or all(i in result for i in lst2) or all(i in result for i in lst3):  #Small Suite Check
            to_send="YOU GOT A SMALL SUITE!"
            msg_sent = await ctx.send(embed=Yam.fiesta(self,to_send,True,small))
            score=40
            return result,score, msg_sent

        doubles=[]

        #if any(result.count(i)==3 for i in result): 
        for i in set(result):
            if result.count(i)==3:  #Broland Check
                to_send=f"You Made a BROLAND of {i}!"                        
                msg_sent = await ctx.send(embed=Yam.fiesta(self,to_send,True,small))
                score=30*int(i)
                return result,score, msg_sent
            if result.count(i)==4:  #Carré Check
                to_send=f"You Made a CARRE of {i}!"
                msg_sent = await ctx.send(embed=Yam.fiesta(self,to_send,True,small))
                score=75*int(i)
                return result,score, msg_sent
            if result.count(i)==2:  #Regular Double Check
                doubles.append(i)
                
        if len(doubles)>0:
            if len(doubles)==1:
                to_send=f'You got a double of {doubles[0]}'
                score=5
            else:
                to_send=f'You got a double of {doubles[0]} and {doubles[1]}'
                score=10
            msg_sent = await ctx.send(embed=Yam.fiesta(self,to_send,False,small))
        
        else:
            score=0
            unlucky=discord.Embed(
                title="Noob, nothing here for ya",
                color=discord.Color.dark_grey()
            )
            unlucky.set_image(url="https://fr.web.img5.acsta.net/newsv7/20/06/08/11/19/4857459.jpg")
            msg_sent = await ctx.send(embed=unlucky)


        return result,score, msg_sent


    async def wanna_keep(self,ctx,result):
            to_delete=await ctx.send("What do you want to keep? Reply with `!keep numbers with spaces between them`")

            def is_player(m):
                return m.author.id == ctx.author.id and m.guild.id==ctx.guild.id

            reply=await self.bot.wait_for('message', check=is_player)
            if not ctx.guild.id==336642139381301249:    await reply.delete()
            reply_split=reply.content[5:]
            if reply_split=="all" or reply_split=="end":
                return False

            for i in reply_split:
                if i.isalpha():
                    await ctx.send("Ok, you don't wanna play the game anymore, neeeever minddd")
                    return False
            try:
                toKeep=reply_split.split()
                print(toKeep)
                toKeep=[int(i) for i in toKeep]
                print(toKeep)
            except:
                await ctx.send("Wut, here's an example : `!keep 1 3 3`")
            for i in toKeep:
                if i not in result and len(toKeep)>0:
                    await ctx.send(f'{i} not in your shot, I\'ll remove it, your mistake.')
                    toKeep.remove(i)
                
            return toKeep,to_delete

    @discord.ext.commands.max_concurrency(1,per=BucketType.channel,wait=False)
    @commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command()
    @utils.appropriate_channel()
    async def yam(self,ctx):
        USER_ID=ctx.author.id
        GUILD_ID=ctx.guild.id
        background = Image.open("yam_images/original.jpg")
        for_player = background.copy()
        for_player.save(f"yam_images/{USER_ID}{GUILD_ID}.jpg")


        seq=Yam.shot(self,5)
        msg,file=Yam.draw(self,seq,1,USER_ID,GUILD_ID)
        msg1=await ctx.send(embed=msg,file=file)
        result,sc,msg_sent1=await Yam.check(self,ctx,seq,True)
        y,to_delete1=await Yam.wanna_keep(self,ctx,result)

        if y:
            seq=Yam.shot(self,5-len(y))
            for z in y:
                seq.append(z)
            msg,file=Yam.draw(self,seq,2,USER_ID,GUILD_ID)
            msg2=await ctx.send(embed=msg,file=file)
            result,sc,msg_sent2=await Yam.check(self,ctx,seq,True)
            y,to_delete2=await Yam.wanna_keep(self,ctx,result)

            if y:
                seq=Yam.shot(self,5-len(y))
                for z in y:
                    seq.append(z)
                msg,file=Yam.draw(self,seq,3,USER_ID,GUILD_ID)
                msg3=await ctx.send(embed=msg,file=file)
                result,sc,msg_sent3=await Yam.check(self,ctx,seq,False)
                msg4=await ctx.send(embed=Yam.end_game(self,ctx,sc,USER_ID))
                os.remove(f"yam_images/{USER_ID}{GUILD_ID}.jpg")

                if not ctx.guild.id==336642139381301249:    await msg1.delete()
                if not ctx.guild.id==336642139381301249:    await msg2.delete()
                #await msg3.delete()
                #await msg4.delete()
                if not ctx.guild.id==336642139381301249:    await msg_sent1.delete()
                if not ctx.guild.id==336642139381301249:    await msg_sent2.delete()
                #await msg_sent3.delete()
                if not ctx.guild.id==336642139381301249:    await to_delete1.delete()
                if not ctx.guild.id==336642139381301249:    await to_delete2.delete()



            else:
                msg3=await ctx.send(embed=Yam.end_game(self,ctx,sc,USER_ID))
                os.remove(f"yam_images/{USER_ID}{GUILD_ID}.jpg")
                if not ctx.guild.id==336642139381301249:    await msg1.delete()
                if not ctx.guild.id==336642139381301249:    await msg2.delete()
                #await msg3.delete()
                if not ctx.guild.id==336642139381301249:    await msg_sent1.delete()
                #await msg_sent2.delete()
                if not ctx.guild.id==336642139381301249:    await to_delete1.delete()
                if not ctx.guild.id==336642139381301249:    await to_delete2.delete()

        else:
            msg2=await ctx.send(embed=Yam.end_game(self,ctx,sc,USER_ID))
            os.remove(f"yam_images/{USER_ID}{GUILD_ID}.jpg")
            if not ctx.guild.id==336642139381301249:    await to_delete1.delete()
        if not ctx.guild.id==336642139381301249:    await ctx.message.delete()

    @yam.error
    async def yam_error(self,ctx,error):
        if isinstance(error,commands.MaxConcurrencyReached):
            await utils.error_embed(ctx,str(error),"Patience, my friend")
        elif isinstance(error,commands.CommandOnCooldown):
            if ctx.message.author.guild_permissions.administrator or ctx.message.author.id==358629457025826816:
                await ctx.reinvoke()
                return
            await utils.error_embed(ctx,str(error),"Patience, my friend")

def setup(bot):
    bot.add_cog(Yam(bot))