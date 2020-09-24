from command import get_weather #Import weather features
from discord.ext import commands, tasks #Not used a lot so far, basic of a discord bot
from discord.utils import get,find #Used to find channels and their IDs
from discord import Member #To use the Member Object
import discord, asyncio,os,random,json, re, requests #Lots of modules used here
from create_list import startupCheck #Check if a json list exists
from jeu import jeu, MauvaisIndice #Import the flag game
from forOwners import Owners #To create the OwnerGuilds json
from covid19 import latest, ranked_locations, country_data, check_server #Covid feature
from country_reverse import flags, capitals, lat_long, plot_map #Dict for Covid feature
from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageFilter #Used for !owner get-info and will be used for DMS on member_join
from io import BytesIO #Used for Member.avatar_url so far
import sqlite3 #Database for Bank Accounts
from itertools import cycle
from PyDictionary import PyDictionary
from newsapi import NewsApiClient
from fuzzywuzzy import fuzz
import utils
import importlib


class General(commands.Cog):

    
    async def partieProMessage(self,j: jeu, message): #Pro Embed Message for the Flag game, probably will be in another file
        embed = discord.Embed(title="Launching the pro-game", color=0x00ff00)
        embed.add_field(name="Game Details : ", value=str(j), inline=False) #For str(j), go to jeu.py
        await message.channel.send(embed=embed) #Sending the message as an embed


    async def risktakerMessage(self,message): #Same thing here, Risktaker option for the flag game
        embed=discord.Embed(
            title="I can tell that you are a brave man",
            description="This mode reminds me of casino games, may Fortune be with you",
            color=discord.Color.green()
        )
        embed.add_field(name="Game Details : ",value="Random level from 1 to 4\nNumber of rounds : 10\nGood luck!")
        await message.channel.send(embed=embed) #Sending the message as an embed






    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(utils.owner)
    async def reload(self, ctx):
        utils.author_init(self,ctx)

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                self.bot.reload_extension(f'cogs.{filename[:-3]}')
        importlib.reload(utils)
        await utils.embed(ctx, ctx,'Reloaded all cogs successfully.', None)


    """
    @commands.command()
    async def help()

    """
    @commands.command(aliases=['commands'])
    async def help_vouch(self, ctx):
        utils.author_init(self,ctx)

        embed=discord.Embed(
        title="Command Usage",
        description="😀Everything you need to properly vouch with zola😀",
        color=discord.Color.green()
        )
        embed.add_field(name=f"`$vouch`🤚", value=f"Vouch for a user. Usage: `$vouch @user Message here`", inline=False)
        embed.add_field(name=f"`$myvouches`📜", value=f"Display all vouches a user has. Usage: `$vouches @user`", inline=False)
        embed.add_field(name=f"`$delmyvouch`✂️", value=f"Delete the vouch. Usage: `$delmyvouch @user`", inline=False)
        embed.add_field(name=f"`$top`🏅", value=f"Display the top 10 users with the most vouches.", inline=False)
        await ctx.send(embed=embed)



    @commands.Cog.listener()
    async def on_message(self, message):
        utils.author_init(self,message)

        # Update username
        if message.author.id != self.bot.user.id and str(message.author) != self.bot.data[str(message.author.id)]["Username"]:
            self.bot.data[str(message.author.id)]["Username"] = str(message.author)
            utils.write(self)

        lock = asyncio.Lock()

        async with lock:
            if not str(message.author)=="ɀola#2251":

                if not message.guild:
                    pass
                        
                else:
                    str_data_flag = open('flag-info.json').read() #Opens the game json file
                    json_flag = json.loads(str_data_flag) #Loads the file

                    str_data_Owners = open('Ownersguilds.json').read() #Opens the Owner guilds json file
                    json_Owners=json.loads(str_data_Owners) #Loads the file



                    lst=message.content.split(" ") #See below the usage
                    current_guild=message.guild #Little shortcut here, don't know if I'm gonna keep it


                    prefix=json_flag[0][str(message.guild.id)]["prefix"]

                    if message.content.startswith(prefix):
                        text = message.content[len(prefix):]

                        if (message.channel.name=="zola" and not message.guild.id==336642139381301249) or (message.guild.id==336642139381301249 and (message.channel.name=="testing" or message.channel.name=="playground")):

                            attributs = json_flag[0][str(message.guild.id)]["flag_game"][str(message.channel.id)]
                            j = jeu(int(attributs[0]), int(attributs[1]), int(attributs[2]), attributs[3], attributs[4], attributs[5],                
                                attributs[6],attributs[7],attributs[8])

                            
                            Owners_attributs = json_Owners[0][str(message.guild.id)]["HasPerms"]
                            own = Owners(Owners_attributs[0])
                            """
                            if lst[0]==prefix+"covid":
                                if check_server():
                                    if lst[1]=="latest":
                                        await message.channel.send(embed=latest())
                                    elif lst[1]=="rank":
                                        await message.channel.send(embed=ranked_locations(lst[2]))
                                    elif lst[1]=="country":
                                        lst.pop(0)
                                        lst.pop(0)
                                        value=" ".join(lst)
                                        value=value.lower()
                                        value=value.capitalize()
                                        ranked_embed,file=country_data(value)
                                        await message.channel.send(embed=ranked_embed,file=file)
                                    else:
                                        not_recognised=discord.Embed(
                                            title="What is this command?",
                                            description="I don't know that... please refer to ```{}help covid```".format(prefix),
                                            colour=discord.Colour.red()
                                        )
                                        bot_answer = await message.channel.send(embed=not_recognised)
                                        await asyncio.sleep(3)
                                        await message.delete()
                                        await bot_answer.delete()
                                else:
                                    latest_embed=discord.Embed(
                                        title="Maintenance - Updating Info",
                                        description="Data Server is temporarely unavailable. Please try again later",
                                        colour=discord.Colour.green()
                                    )
                                    await message.channel.send(embed=latest_embed)
                            """
                            if lst[0]==prefix+'owner' and (str(message.author.id) in own.Perms):
                                if lst[1]=="prefix":
                                    if len(lst) == 3:
                                        if not lst[2].isalpha():

                                            json_flag[0][str(current_guild.id)]["prefix"] = lst[2]
                                            await message.channel.send("This is the new prefix : '%s'" % json_flag[0][str(message.guild.id)]["prefix"])

                                            DIR_guilds="d:\CODING\DISCORD BOT\Bot\\"
                                            db_guilds=sqlite3.connect(os.path.join(DIR_guilds,"Guild.db"))
                                            SQL_guilds=db_guilds.cursor()
                                            SQL_guilds.execute(f'update Guilds set prefix = ? where guild_id = ?', (current_guild.id, lst[2],))

                                            if not message.guild.id==336642139381301249:    weather_msg = find(lambda x: x.name == 'zola',  current_guild.text_channels)
                                            else:  weather_msg = find(lambda x: x.name == 'testing',  current_guild.text_channels) 
                                            if weather_msg and weather_msg.permissions_for(current_guild.me).send_messages:
                                                new_prefix=discord.Embed(
                                                    title="My Prefix was changed by the owner",
                                                    description="My prefix is now '%s'" % json_flag[0][str(message.guild.id)]["prefix"],
                                                    colour=discord.Colour.green()
                                                )
                                                await weather_msg.send(embed=new_prefix)
                                        else:
                                            await message.channel.send("It is preferable to use a non-alpha prefix for moderation purpose")
                                    else:
                                        await message.channel.send("**%s** ? That's not a prefix" % text)

                                elif lst[1]=="clear":
                                    if not message.guild.id==336642139381301249:    deleted = await message.channel.purge()
                                    bot_answer = await message.channel.send("I deleted **" + str(len(deleted)) +"** messages")
                                    await asyncio.sleep(3)
                                    if not message.guild.id==336642139381301249:    await bot_answer.delete()

                                elif lst[1]=="allow":
                                    id_input=" ".join(lst[2:])
                                    if len(lst)>=3:
                                        name= await self.bot.fetch_user(id_input)
                                        if id_input.isdigit():
                                            if lst[2] in own.Perms:
                                                await message.channel.send("**"+str(name) + "** is already an Owner!")
                                            else:
                                                json_Owners[0][str(message.guild.id)]["HasPerms"][0].append(id_input)
                                                json.dump(json_Owners, open('Ownersguilds.json', 'w'), indent=2)
                                                await message.channel.send("List Updated, added **"+str(name) + "** . He can now use the `!owner` commands")
                                                howner_allowed1,howner_allowed2=help_owner_allowed(prefix,current_guild)
                                                await name.send(embed=howner_allowed1)
                                                await name.send(embed=howner_allowed2)

                                        else:
                                            await message.channel.send("That's not a User ID. Why don't I accept Discord names? Because members usually changes their names regularly and that would use too much RAM for nothing...")
                                            
                                    else:
                                        await message.channel.send("Please retry")
                                        
                                
                                
                                elif lst[1]=="demote":
                                    if len(lst)==3:
                                        if lst[2].isdigit():
                                            name= await self.bot.fetch_user(lst[2])
                                            if lst[2] not in own.Perms:
                                                await message.channel.send("You can't demote **"+str(name) + "** because he is not even an Owner" )
                                            elif lst[2]=="358629457025826816" and str(message.author.id)!=lst[2]:
                                                await message.channel.send("Are you crazy? You want to demote my Father?! How dare you!")
                                            elif lst[2]==str(message.author.id):
                                                await message.channel.send("You can't demote yourself")
                                            else:
                                                json_Owners[0][str(message.guild.id)]["HasPerms"][0].remove(lst[2])
                                                json.dump(json_Owners, open('Ownersguilds.json', 'w'), indent=2)
                                                await message.channel.send("List Updated, **"+str(name) + "** has been demoted. Hope he'll understand.")
                                            #send DM of help_owner to the new guy
                                        else:
                                            await message.channel.send("That's not a User ID. Why don't I accept Discord names? Because members usually changes their names regularly and that would use too much RAM for nothing...")

                                elif lst[1]=="get-info":
                                    if len(lst)==3:
                                        if lst[2].isdigit():
                                            await message.channel.send("One second my friend, I am creating the perfect output")
                                            user= message.guild.get_member(int(lst[2]))
                                            font_list=["Fitamint Script.ttf"]
                                            img = Image.open("info-img.png")
                                            draw = ImageDraw.Draw(img)
                                            font = ImageFont.truetype("Gobold Bold.otf", 100)
                                            fontbig = ImageFont.truetype(random.choice(font_list), 400)
                                            response=requests.get(user.avatar_url)
                                            avatar=Image.open(BytesIO(response.content))
                                            avatar=avatar.resize((700,700))

                                            draw.text((200, 0), "Information:", (255, 255, 255), font=fontbig) #draws Information
                                            draw.text((50, 500), "Username:     {}#{}".format(user.name,user.discriminator), (255,0,255), font=font) #draws the Username of the user
                                            draw.text((50, 700), "ID:     {}".format(user.id), (240,128,128), font=font) #draws the user ID
                                            if user.status.value=="online":
                                                draw.text((50, 900), "User Status:     Online", (0, 255, 0), font=font) #draws green
                                                color=discord.Colour.green()
                                            elif user.status.value=="offline":
                                                draw.text((50, 900), "User Status:     Offline", (255, 255, 255), font=font) #draws white
                                                color=discord.Colour.light_grey()
                                            elif user.status.value=="dnd":
                                                draw.text((50, 900), "User Status:     Do not Disturb", (255, 0, 0), font=font) #draws red
                                                color=discord.Colour.red()
                                            elif user.status.value=="idle":
                                                draw.text((50, 900), "User Status:     Idle", (255, 255, 0), font=font) #draws yellow
                                                color=0xffd60a
                                            draw.text((50, 1100), "Account created:     {}".format(user.created_at), (173,255,47), font=font) #When the account was created 
                                            draw.text((50, 1300), "Nickname:     {}".format(user.display_name), (210,105,30), font=font) # Nickname of the user
                                            draw.text((50, 1500), "Users' Top Role:     {}".format(user.top_role), ImageColor.getcolor(str(user.top_role.color),"RGB"), font=font) #draws the top rome
                                            draw.text((50, 1700), "User Joined:     {}".format(user.joined_at), (0,250,154), font=font) #draws info about when the user joined

                                            mask_im = Image.new("L", avatar.size, 0)
                                            draw = ImageDraw.Draw(mask_im)
                                            draw.ellipse((0, 0, 700, 700), fill=255)
                                            mask_im.save('mask_circle.jpg', quality=95)

                                            mask_im_blur = mask_im.filter(ImageFilter.GaussianBlur(10))
                                            mask_im_blur.save('mask_circle_blur.jpg', quality=95)

                                            img.paste(avatar,(1600,100),mask_im_blur)
                                            img.save('info-img2.png')
                                            file=discord.File('info-img2.png')
                                            embed=discord.Embed(
                                                title="Here you go my friend!",
                                                color=color
                                            )
                                            embed.set_image(url='attachment://info-img2.png')
                                            await message.channel.send(embed=embed,file=file)

                                else:
                                    await message.channel.send("Command not found")


                            elif lst[0]==prefix+'owner' and not (message.author.id in own.Perms):
                                await message.channel.send("Do you have permissions to use this command? No? I thought so...")
                            




                            
                            
                            if j.partieEnPrepOuCommencee:
                                country_real_temp = os.path.splitext(j.country_name)[0]
                                try:
                                    country_real=flags[country_real_temp]
                                except:
                                    await j.prochainTourOuFin(message, json_flag)
                                DIR = "d:\CODING\DISCORD BOT\Bot\\"
                                db = sqlite3.connect(os.path.join(DIR, "BankAccounts.db"))
                                SQL = db.cursor()
                                if text.startswith('flag'):
                                    j.nbTours = j.tourNumero
                                    await j.prochainTourOuFin(message, json_flag)

                                elif j.tourNumero < j.nbTours + 1:
                                    essai = j.decode(text)
                                    if essai == j.decode(country_real):

                                        await message.add_reaction("😄")
                                        name = str(message.author)
                                        SQL.execute(f'select user_name from Accounts where user_name="{name}"')
                                        if not name in j.scores:
                                            j.scores[name] = 0
                                        if j.niveau==0:
                                            j.scores[name]+=3 * 10
                                            SQL.execute('update Accounts set balance = balance + ? where user_name = ?', (3 * 10,name))
                                        else:
                                            j.scores[name] += j.niveau * 10
                                            SQL.execute('update Accounts set balance = balance + ? where user_name = ?', (j.niveau * 10,name))

                                        db.commit()
                                        leaderboard = '\n'.join(
                                            [k + " : %i point" % j.scores[k] + ("s" if j.scores[k] > 1 else "") for k in j.scores])
                                        embed = discord.Embed(title="The country was \"%s\"" % country_real,
                                                            color=0x00ff00)
                                        if len(leaderboard) > 0:
                                            embed.add_field(name="Leaderboard", value=leaderboard, inline=False)
                                        SQL.execute('update Accounts set advice1 = 0') 
                                        db.commit()
                                        SQL.execute('update Accounts set advice2 = 0')
                                        db.commit()


                                        await message.channel.send(embed=embed)
                                    
                                        j.tourCommence = False

                                        await j.prochainTourOuFin(message, json_flag)




                                    elif essai == "giveup":
                                        await message.add_reaction("😢")
                                        leaderboard = '\n'.join(
                                            [k + " : %i point" % j.scores[k] + ("s" if j.scores[k] > 1 else "") for k in j.scores])
                                        embed = discord.Embed(title="The country was \"%s\"" % country_real,
                                                            color=0x00ff00)
                                        if len(leaderboard) > 0:
                                            embed.add_field(name="Leaderboard", value=leaderboard, inline=False)
                                        SQL.execute('update Accounts set advice1 = 0') 
                                        db.commit()
                                        SQL.execute('update Accounts set advice2 = 0')
                                        db.commit()
                                        await message.channel.send(embed=embed)
                                        await j.prochainTourOuFin(message, json_flag)

                                    elif essai=="advice1":

                                        SQL.execute("select advice1 from Accounts where user_id=?", (message.author.id,))
                                        hasVoted=SQL.fetchone()
                                        if hasVoted[0]==0:
                                            SQL.execute("select balance from Accounts where user_id=?", (message.author.id,))
                                            balance=SQL.fetchone()
                                            bot_msg=await message.channel.send(f"Are you sure of this action {message.author.mention}? You have a balance of {balance[0]} zolos and you will lose {(j.niveau*10)//3} points! Send `!yes` or `!no` (Advice is sent via DM)")
                                            def yes(m):
                                                return m.author.id == message.author.id

                                            yesAnswer = await self.bot.wait_for('message', check=yes)
                                            
                                            if yesAnswer.content=="!yes":
                                                if balance[0]>=3:
                                                    SQL.execute('update Accounts set balance = balance - 3 where user_id = ?', (message.author.id,))
                                                    db.commit()
                                                    SQL.execute('update Accounts set advice1 = 1 where user_id = ?', (message.author.id,))
                                                    db.commit()
                                                    get_user=self.bot.get_user(message.author.id)
                                                    capital=capitals[country_real]
                                                    await get_user.send(f'The Capital of this Country is : {capital}')
                                                    


                                                else:
                                                    await message.channel.send("You don't have enough money!")
                                                
                                            
                                            else:
                                                await message.channel.send("Action stopped")
                                                
                                        else:
                                            await message.channel.send("You already asked for this advice.")
                                        if not message.guild.id==336642139381301249:    await bot_msg.delete()
                                        if not message.guild.id==336642139381301249:    await message.delete()

                                    elif essai=="advice2":

                                        SQL.execute("select advice1 from Accounts where user_id=?", (message.author.id,))
                                        hasVoted=SQL.fetchone()
                                        if hasVoted[0]==1:
                                            SQL.execute("select balance from Accounts where user_id=?", (message.author.id,))
                                            balance=SQL.fetchone()
                                            bot_msg=await message.channel.send(f"Are you sure of this action {message.author.mention}? You have a balance of {balance[0]} zolos and you will lose {(j.niveau *10)//2} points! Send `!yes` or `!no` (Advice is sent via DM)")
                                            def yes(m):
                                                return m.author.id == message.author.id

                                            yesAnswer = await self.bot.wait_for('message', check=yes)
                                            
                                            if yesAnswer.content=="!yes":
                                                SQL.execute(f'select user_name from Accounts where user_name="{str(message.author)}"')
                                                SQL.execute("select balance from Accounts where user_id=?", (message.author.id,))
                                                balance=SQL.fetchone()
                                                if balance[0]>=5:
                                                    SQL.execute(f'update Accounts set balance = balance - 5 where user_id = ?', (message.author.id,))
                                                    db.commit()
                                                    SQL.execute(f'update Accounts set advice1 = 1 where user_id = ?', (message.author.id,))
                                                    db.commit()
                                                    get_user=self.bot.get_user(message.author.id)
                                                    longitude=lat_long[country_real][0]
                                                    latitude=lat_long[country_real][1]
                                                    plot_map(longitude,latitude)
                                                    file=discord.File("D:/CODING/DISCORD BOT/Bot/advice.png",filename='advice.png')
                                    
                                                    flag=discord.Embed(
                                                        title="Here is the Location",
                                                        description="Hope it may help you!",
                                                        colour=discord.Colour.green()
                                                    )
                                                    flag.set_image(url='attachment://advice.png')
                                                    
                                                    await get_user.send(embed=flag,file=file)


                                                else:
                                                    await message.channel.send("You don't have enough money!")
                                            
                                            
                                            else:
                                                await message.channel.send("Action stopped")
                                        else:
                                            await message.channel.send("You have to ask for advice1 first!")
                                        if not message.guild.id==336642139381301249:    await bot_msg.delete()
                                        if not message.guild.id==336642139381301249:    await message.delete()


                                    elif essai=="yes" or essai=="no" or essai=="bal":
                                        pass

                                    else:
                                        ratio=fuzz.ratio(essai, j.decode(country_real))
                                        if int(ratio)>60:
                                            await message.channel.send(f"You\'re so close! Ratio is {ratio}")
                                        else:
                                            await message.channel.send(f"Your answer is {ratio} % similar to the actual answer!")
                                            await message.add_reaction("😬")




                            else:             
                                print(text)       
                                if text.startswith('flag'):                    
                                    erreur = False
                                    try:
                                        textList = re.findall('flag(?:s)?(.*)', text)[0].split()
                                    except:
                                        wrong_flag_usage=discord.Embed(
                                            title="Uh oh, wrong usage of "+ prefix + "flag",
                                            description="I don't know this command, please refer to ```{}help flag```".format(prefix),
                                            colour=discord.Colour.red()
                                        )
                                        bot_answer = await message.channel.send(embed=wrong_flag_usage)
                                        await asyncio.sleep(3)
                                        if not message.guild.id==336642139381301249:    await message.delete()
                                        if not message.guild.id==336642139381301249:    await bot_answer.delete()
                                        erreur = True

                                    j = jeu(1, 1, 0, {}, False, False, False, "",[])

                                    if not erreur and len(textList) == 0:
                                        j = jeu(0, 1, 0, {}, False, False, False, "",[])


                                    elif not erreur and len(textList)==1 and textList[0]=='risktaker':
                                        j = jeu(0, 10, 0, {}, False, False, False, "",[])
                                        await General.risktakerMessage(self,message)


                                    elif not erreur and len(textList) == 2:
                                        
                                        directory = 'D:\\CODING\\DISCORD BOT\\Bot\\Images\\'+str(textList[0])
                                        number_of_files = len([item for item in os.listdir(directory) if os.path.isfile(os.path.join(directory, item))])
                                        if textList[1].isdigit() :
                                            if int(textList[1])<=number_of_files:
                                                try:
                                                    j = jeu(int(textList[0]), int(textList[1]), 0, {}, False, False, False,
                                                            "",[])
                                                    await General.partieProMessage(self,j, message)
                                                    
                                                except MauvaisIndice as inst:
                                                    await message.channel.send(inst)
                                                    erreur = True
                                            else:
                                                erreur=True
                                                exceeded_rounds=discord.Embed(
                                                    title="Too many rounds for the selected level",
                                                    description="For further information, please refer to ```{}help flag```".format(prefix),
                                                    colour=discord.Colour.green()
                                                )
                                                await message.channel.send(embed=exceeded_rounds)
                                        elif textList[1]=="max" or textList[1]=="MAX":
                                            await message.channel.send(f"MAX is {number_of_files} rounds")
                                            try:
                                                j = jeu(int(textList[0]), int(number_of_files), 0, {}, False, False, False,
                                                        "",[])
                                                await General.partieProMessage(self,j, message)
                                            except MauvaisIndice as inst:
                                                await message.channel.send(inst)
                                                erreur = True

                                        """
                                        except:
                                            print(str(textList))
                                            erreur=True
                                            wrong_level=discord.Embed(
                                                title="This level doesn't exist",
                                                description="For further information, please refer to ```{}help flag```".format(prefix),
                                                colour=discord.Colour.green()
                                            )
                                            await message.channel.send(embed=wrong_level)
                                        """

                                    if not erreur:
                                        j.countries_picked=[]
                                        print(j.countries_picked)
                                        j.partieEnPrepOuCommencee = True
                                        j.partieCommencee = True
                                        j.country_name = j.pickCountry()
                                        j.countries_picked.append(j.country_name)
                                        file=discord.File("D:/CODING/DISCORD BOT/Bot/Images/"+j.country_name, filename=j.country_name)
                                    
                                        flag=discord.Embed(
                                            title="Guess the Country",
                                            description="Be quick, otherwise your opponent might win :)",
                                            colour=discord.Colour.green()
                                        )
                                        flag.set_image(url='attachment://'+j.country_name)
                                        
                                        await message.channel.send(embed=flag,file=file)

                                        j.tourNumero += 1
                                        j.tourCommence = True



                                json_flag[0][str(message.guild.id)]["flag_game"][message.channel.id] = j.getAttributes()
                                json.dump(json_flag, open('flag-info.json', 'w'), indent=2)

                        


                        else:
                            if text.startswith("clear"):
                                if not message.guild.id==336642139381301249:    deleted = await message.channel.purge()
                                await message.channel.send("I deleted " + str(len(deleted)) +" messages")

                            else:

                                if not message.guild.id==336642139381301249:    await message.delete()
                                if not message.guild.id==336642139381301249:    weather_mention = find(lambda x: x.name == 'zola',  current_guild.text_channels)
                                else:  weather_mention = find(lambda x: x.name == 'testing',  current_guild.text_channels) 
                                warning_not_approp_channel=discord.Embed(
                                    title="Not appropriate channel",
                                    description="Please go to " + weather_mention.mention +" to use the Bot",
                                    colour=discord.Colour.red()
                                )
                                warning_not_approp_channel.set_thumbnail(url="https://lh3.googleusercontent.com/proxy/cW4ghwjowM1S8gnVJWUhSo0xAjUjKB1UHmSrPt5OAy2NfotInypwNcqVC3gsr8MgJam4p7o-TpJ4vFAKgkEyWqIWAExyvTXhwdHmEihwTNrsCOBQzBbQmy1_51WNHW0")
                                bot_msg_warning = await message.channel.send(embed=warning_not_approp_channel)
                                await asyncio.sleep(3)
                                if not message.guild.id==336642139381301249:    await bot_msg_warning.delete()


                    
                    elif message.channel.name=="cross-chat" and not str(message.author)=="ɀola#2251": #Cross chat feature
                        text = message.content #Little shortcut here
                        pfp = message.author.avatar_url #Little shortcut here
                        for guild in self.bot.guilds: #That's the basic of the cross chat feature
                            send_msg=discord.Embed(
                                title=text,
                                description="Sent by " + str(message.author) + " from the \"" + str(message.guild) + "\" server",
                                colour=discord.Colour.green()
                            )
                            send_msg.set_thumbnail(url=pfp)
                            cross_chat = find(lambda x: x.name == 'cross-chat',  guild.text_channels)
                            try:
                                await cross_chat.send(embed=send_msg)
                            except:
                                print(f'Did not find channel {cross_chat} in guild {guild}')
                        await message.delete()
        #await self.bot.process_commands(message)
    

def setup(bot):
    bot.add_cog(General(bot))
