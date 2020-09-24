#Imports
from command import get_weather #Import weather features
from discord.ext import commands, tasks #Not used a lot so far, basic of a discord bot
from discord.ext.commands.cooldowns import BucketType
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
from utils import appropriate_channel
import utils
from cogs.poems import Contest
import asyncpg
import datetime


lock = asyncio.Lock() #For equality in the game, basically it is Synchronization Primitives. For further info go to https://docs.python.org/3/library/asyncio-sync.html

client = commands.Bot(command_prefix='z!') #The basic's basic of a Python Discord Bot
prefix = "z!" #Default prefix, used in !owner prefix
client.launch_time = datetime.datetime.utcnow()
client.remove_command("help")

async def db_connection():
    client.pg_con = await asyncpg.create_pool(database="zola",user="postgres",password="Python196819712004")
        

if os.path.isfile('data.json'):
    with open('data.json', 'r') as file:
        client.data = json.loads(file.read())
        if not client.data:
            client.data = {}
else:
    client.data = {}
  


def is_fuser():
    def predicate(ctx):
        return ctx.message.author.id==358629457025826816
    return commands.check(predicate)


@tasks.loop(minutes=5)
async def update_guilds():
    await client.wait_until_ready()
    print("Started updating Channels")
    #Load Json Files
    startupCheck('flag-info.json', json.dumps([{}])) 
    startupCheck('Ownersguilds.json', json.dumps([{}]))

    str_data_flag = open('flag-info.json').read()
    str_data_Owners = open('Ownersguilds.json').read()

    json_flag = json.loads(str_data_flag)
    json_Owners=json.loads(str_data_Owners)

    DIR_guilds=os.path.dirname(__file__)
    db_guilds=sqlite3.connect(os.path.join(DIR_guilds,"Guild.db"))
    SQL_guilds=db_guilds.cursor()
    SQL_guilds.execute('create table if not exists Guilds("Num" integer primary key autoincrement,"guild_id" INTEGER NOT NULL, "guild_name" TEXT, "prefix" TEXT, "wantsWelcome" INTEGER, "wantsPoem" INTEGER, "wantsCrosschat" INTEGER, "location" TEXT)')
    
    for guild in client.guilds:
        if guild.id==336642139381301249:
            channel = discord.utils.get(guild.text_channels, name='testing')

        else:

            SQL_guilds.execute('select wantsWelcome from Guilds where guild_id = ? ',(guild.id,))
            wantsWelcome=SQL_guilds.fetchone()
            name="wantsWelcome"
            if wantsWelcome is None:
                utils.none_to_zero(SQL_guilds,db_guilds,guild.id,name)
            wantsWelcome=wantsWelcome[0]

            
            SQL_guilds.execute('select wantsPoem from Guilds where guild_id = ? ',(guild.id,))
            wantsPoem=SQL_guilds.fetchone()
            name="wantsPoem"
            if wantsWelcome is None:
                utils.none_to_zero(SQL_guilds,db_guilds,guild.id,name)
            #wantsPoem=wantsPoem[0]

            SQL_guilds.execute('select wantsCrosschat from Guilds where guild_id = ? ',(guild.id,))
            wantsCrosschat=SQL_guilds.fetchone()
            name="wantsCrosschat"
            if wantsWelcome is None:
                utils.none_to_zero(SQL_guilds,db_guilds,guild.id,name)
            wantsCrosschat=wantsCrosschat[0]

            if not find(lambda x: x.name == 'ZolaBOT',  guild.categories):
                await guild.create_category_channel('ZolaBOT')

            category = get(guild.categories, name='ZolaBOT')

            if not find(lambda x: x.name == 'zola',  guild.text_channels):
                await guild.create_text_channel('zola', category=category)
            
            if wantsCrosschat==1 and not find(lambda x: x.name == 'cross-chat',  guild.text_channels):
                await guild.create_text_channel('cross-chat', category=category)

            if not find(lambda x: x.name == 'z-announcements',  guild.text_channels):
                await guild.create_text_channel('z-announcements', category=category)
            
            if wantsWelcome==1 and not find(lambda x: x.name == 'zwelcome',  guild.text_channels):
                await guild.create_text_channel('zwelcome', category=category)
            
            channel = discord.utils.get(guild.text_channels, name='zola')
        


        if str(guild.id) not in json_flag[0]:
            print(f'{channel} with id {channel.id} in {guild}')
            json_flag[0][guild.id] = {"prefix": ("z!"),
                                        "flag_game": { 
                                            channel.id: jeu(1, 1, 0, {}, False, False, False, "",[]).getAttributes()},
                                        }

        if str(guild.id) not in json_Owners[0]:
            json_Owners[0][guild.id] = {
                "HasPerms": 
                    Owners([str(x.id) for x in guild.members if x.guild_permissions.administrator]).getAttributes()
            }
    
        GUILD_ID=guild.id
        GUILD_NAME=str(guild)
        DEFAULT_CHANNEL=(discord.utils.get(guild.text_channels, name='zola')).id

        SQL_guilds.execute('select * from Guilds where guild_id = ?',(GUILD_ID,))
        doesExists=SQL_guilds.fetchone()
        if doesExists is None:
            wants=0
            execute = ('insert into Guilds(guild_id, guild_name, prefix, wantsWelcome, wantsPoem, wantsCrosschat) values(?,?,?,?,?,?)')
            val = (GUILD_ID, GUILD_NAME, prefix, wants, wants, wants)
            SQL_guilds.execute(execute, val)
            db_guilds.commit()
        """
        await client.pg_con.execute(f'''
                                    CREATE TABLE IF NOT EXISTS {GUILD_ID}  (
                                                                            index serial PRIMARY KEY,
                                                                            name text,
                                                                            value text
                                                                            )
                                    ''')        
        elems=[('guild_name',GUILD_NAME),('prefix',prefix),('wantsWelcome',wants),('wantsPoem',wants),('wantsCrosschat',wants),('game_channel',str(DEFAULT_CHANNEL))]#,('niveau','1'),('nbTours','1'),('tourNumero','1'),('scores',{}),(bool1,)]
        
        for val1,val2 in elems:
            await utils.create_record_db(client.pg_con,GUILD_ID,"guild_name",GUILD_NAME)
        """
        
    json.dump(json_flag, open('flag-info.json', 'w'), indent=2)
    json.dump(json_Owners, open('Ownersguilds.json', 'w'), indent=2)



@client.event
async def on_ready(): #When I run the bot
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(
       activity=discord.Activity(name=f"{len(client.guilds)} servs. Use {prefix}help", #len(client.guilds) --> Looks for the number of server that has the bot
                                  type=discord.ActivityType.watching))



update_guilds.start()


@client.event
async def on_member_join(member):
    if member.guild.id==336642139381301249:
        pass
    else:
        print(member.id, "est arrivé dans", member.guild.name, "Initialisation de l'XP à zero") #Idk if I'm gonna keep it.
        #rule_mention = find(lambda x: x.name == 'bot-rules',  member.guild.name.text_channels) No idea why this is here. Need to check that

        #DM To the New Member. Using the PIL Module.
        response=requests.get(str(member.guild.icon_url))
        servIcon=Image.open(BytesIO(response.content))
        servIcon=servIcon.resize((2024,2024))
        draw = ImageDraw.Draw(servIcon)
        font = ImageFont.truetype("Gobold Bold.otf", 300)
        draw.text((200, 1212), "Welcome to", (255, 255, 0), font=font)
        #draw.text(((2024-w)/2,1512),msg, (0, 255, 0), font=font)
        draw.text((200,1212),"Welcome to\n"+str(member.guild),(255,255,0),font=font,align="center")
        responseAvatar=requests.get(member.avatar_url)
        avatar=Image.open(BytesIO(responseAvatar.content))
        avatar=avatar.resize((700,700))
        mask_im = Image.new("L", avatar.size, 0)
        draw = ImageDraw.Draw(mask_im)
        draw.ellipse((0, 0, 700, 700), fill=255)
        mask_im.save('mask_circle.jpg', quality=95)
        servIcon.paste(avatar,(680,512),mask_im)
        servIcon.save('servIcon.png')

        file=discord.File('servIcon.png')
        embed=discord.Embed(
            title="Hello {}! Welcome to {} server!".format(str(member),str(member.guild)),
            color=discord.Colour.green()
        )
        embed.set_image(url='attachment://servIcon.png')
        await member.send(embed=embed,file=file)
        
        #Not done
        """
        general = find(lambda x: x.name == 'general',  guild.text_channels)
        if weather_msg and weather_msg.permissions_for(guild.me).send_messages:
            await weather_msg.send('{} just joined the server. Hope he'll enjoy his stay!}'.format(str(member)))
        """
        #await member.send("Hello {member.id}! Welcome to {member.guild.name}! Please read {rule_mention.mention}")

        str_data_flag = open('flag-info.json').read()
        json_flag = json.loads(str_data_flag)
        if not member.id in json_flag[0]["joueurs"]:
            json_flag[0]["joueurs"][member.id] = {"XP": 0}
        json.dump(json_flag, open('flag-info.json', 'w'), indent=2)

    DIR = os.path.dirname(__file__)
    db = sqlite3.connect(os.path.join(DIR, "BankAccounts.db"))
    SQL = db.cursor()
    USER_ID=member.id
    USER_NAME=str(member)
    START_BALANCE=0
    voted=0
    poet=""
    no_advice=0

    SQL.execute('create table if not exists Accounts("Num" integer primary key autoincrement, "user_id"	INTEGER NOT NULL, "user_name" TEXT, "balance" INTEGER)')

    SQL.execute(f'select balance from Accounts where user_id="{USER_ID}"')

    result_userID=SQL.fetchone()
    if result_userID is None:
        execute = ('insert into Accounts(user_id, user_name, balance, voted, poetChoice, advice1, advice2) values(?,?,?,?,?,?,?)')
        val = (USER_ID, USER_NAME, START_BALANCE, voted, poet, no_advice, no_advice)
        SQL.execute(execute, val)
        db.commit()
        print(f'NEW: {USER_NAME} has a balance of 0')
    db.close()


"""
@client.event
async def on_member_remove(member):
    pass
"""



@client.event
async def on_guild_join(guild): #When a bot joins a server
    await client.change_presence(
        activity=discord.Activity(name=f"{len(client.guilds)} servers. Use {prefix}help", #Since the bot used to watch x servers. He watches now x+1 servers. We update that variable.
                                type=discord.ActivityType.watching))
    

    DIR_guilds=os.path.dirname(__file__)
    db_guilds=sqlite3.connect(os.path.join(DIR_guilds,"Guild.db"))
    SQL_guilds=db_guilds.cursor()
    SQL_guilds.execute('create table if not exists Guilds("Num" integer primary key autoincrement,"guild_id" INTEGER NOT NULL, "guild_name" TEXT, "wantsWelcome" INTEGER, "wantsPoem" INTEGER, "wantsCrosschat" INTEGER, "location" TEXT)')

    GUILD_ID=guild.id
    GUILD_NAME=str(guild)
    wants=0
    default_location="zola"
    execute = ('insert into Guilds(guild_id, guild_name, wantsWelcome, wantsPoem, wantsCrosschat, location) values(?,?,?,?,?,?)')
    val = (GUILD_ID, GUILD_NAME, wants, wants, wants, default_location)
    SQL_guilds.execute(execute, val)
    print(f'Working for guild {str(guild)}')
    db_guilds.commit()


    #Very important notice: Let's say the bot was before in this server. The category and 2 text channels would be there. Since not a lot of important stuff is there (only commands and some old chat), the bot deletes them.
    if find(lambda x: x.name == 'ZolaBOT',  guild.categories):
        category=discord.utils.get(guild.categories,name="ZolaBOT")
        await category.delete()
    """
    if find(lambda x: x.name == 'cross-chat',  guild.text_channels):
        channel=discord.utils.get(guild.text_channels, name='cross-chat')
        await channel.delete()
    """
    if find(lambda x: x.name == 'zola',  guild.text_channels):
        channel=discord.utils.get(guild.text_channels, name='zola')
        await channel.delete()

    if find(lambda x: x.name == 'z-welcome',  guild.text_channels):
        channel=discord.utils.get(guild.text_channels, name='z-welcome')
        await channel.delete()

    #He recreates thel here.
    if not find(lambda x: x.name == 'ZolaBOT',  guild.categories):
        await guild.create_category_channel('ZolaBOT')
    category = get(guild.categories, name='ZolaBOT')
    await guild.create_text_channel('zola', category=category)
    #await guild.create_text_channel('z-welcome', category=category)
    #await guild.create_text_channel('cross-chat', category=category)
    #await guild.create_text_channel('bot-rules', category=category)


    #Sends a welcome message in the weather channel (name will change ofc)
    weather_msg = find(lambda x: x.name == 'zola',  guild.text_channels)
    if weather_msg and weather_msg.permissions_for(guild.me).send_messages:
        await weather_msg.send('Hello {}! I am zola, still in alpha. Please use me in this specific channel'.format(guild.name))
    
    #Load the Owner Guild JSON File
    str_data_Owners = open('Ownersguilds.json').read()
    json_Owners=json.loads(str_data_Owners)

    #Load the Guild (Game) JSON File
    str_data_flag = open('flag-info.json').read()
    json_flag = json.loads(str_data_flag)

    i = 0
    while True:
        if isinstance(guild.channels[i], discord.TextChannel):
            break
        else:
            i += 1

    if guild.id not in json_flag[0]:
        json_flag[0][guild.id] = {"prefix": "!",
                                    "flag_game": {
                                        channel.id: jeu(1, 1, 0, {}, False, False, False, "",[]).getAttributes() for
                                        channel in guild.text_channels},
                                    }
    if guild.id not in json_Owners[0]: 
        json_Owners[0][guild.id] = {
                "HasPerms": 
                    Owners([str(x.id) for x in guild.members if x.guild_permissions.administrator]).getAttributes()
            }

    json.dump(json_flag, open('flag-info.json', 'w'), indent=2)
    json.dump(json_Owners, open('Ownersguilds.json', 'w'), indent=2)

    howner1,howner2=help_owner(prefix,guild)

    for member in guild.members:
        if member.guild_permissions.administrator and member!=guild.me:
            await member.send(embed=howner1)
            await member.send(embed=howner2)


@client.event
async def on_guild_remove(guild): #When a server kicks the bot
    await client.change_presence(
        activity=discord.Activity(name=f"{len(client.guilds)} servers. Use {prefix}help", #Since the bot used to watch x servers. He watches now x-1 servers. We update that variable.
                                  type=discord.ActivityType.watching))
    """
    IMPORTANT
    We need to remove this guild from the Guild.json, let's try it here:

    str_data_flag = open('flag-info.json').read()
    json_flag = json.loads(str_data_flag)
    

    """



@client.command()
@is_fuser()
async def leave_dpy(ctx):
    toleave=client.get_guild(336642139381301249)
    await toleave.leave()



@client.command()
@appropriate_channel()
async def shop(ctx):
    pass

@client.command()
@appropriate_channel()
async def define(ctx,SearchWord):
    print(SearchWord)
    try:
        meaning=PyDictionary().meaning(SearchWord,disable_errors=True)

    except:
        await ctx.send("Word not found")

    if meaning:
        result=discord.Embed(
            title=f'Meaning of \"{SearchWord}\"',
            color=discord.Color.green()
        )

        url = 'https://en.wikipedia.org/w/api.php'
        data = {
            'action' :'query',
            'format' : 'json',
            'formatversion' : 2,
            'prop' : 'pageimages|pageterms',
            'piprop' : 'original',
            'titles' : SearchWord
        }
        response = requests.get(url, data)
        json_data = json.loads(response.text)
        try:
            if len(json_data['query']['pages']) >0:
                url=json_data['query']['pages'][0]['original']['source']
                print(url)
                result.set_image(url=url)
        except:
            print("no image")

        for i in meaning:
            for x in range(len(meaning[i])):
                result.add_field(name=f'Type : {i}',value=f'{x+1}) : {meaning[i][x]}',inline=False)
        await ctx.send(embed=result)
    else:
        await ctx.send("Word not found")

@client.command()
@appropriate_channel()
async def help(ctx):
    await ctx.send("Under Construction, patience my friend.")


@client.command()
@appropriate_channel()
async def news(ctx,language,*query):
    member=ctx.author
    query=" ".join(query)
    if language=="en":
        news_en=discord.Embed(
            title=f"Everything you need about {query}",
            description="You searched for results in English",
            color=discord.Color.red()
        )


        news_en.add_field(name="__**Command Index**__", value="📖 Shows this Menu\n\n🔴__**CNN NEWS**__\n\n🟢 __**BBC NEWS**__\n\n🔵__**The Washington Post**__",inline=False)
        news_en.set_author(name=f"Command Requested by: {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        m = await ctx.send(embed=news_en)
        await m.edit(embed=news_en)
        await m.add_reaction('📖')

        await m.add_reaction('🔴')
        await m.add_reaction('🟢')
        await m.add_reaction('🔵')

        def checkreact(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['📖','🔴', '🟢','🔵']
        while True:
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=checkreact)

            except TimeoutError:
                pass
            except asyncio.exceptions.TimeoutError:
                pass
            except asyncio.TimeoutError:
                bruh = discord.Embed(color=discord.Color.dark_red())
                bruh.add_field(name="__**What were you doing?**__", value="Don't stay more than 20 seconds ya lazy")
                try:
                    await m.edit(embed=bruh, delete_after=5)
                except discord.errors.NotFound:
                    pass

            except discord.errors.NotFound:
                pass 
            
            else:
                if str(reaction.emoji) == '🔴':                    
                    newsapi = NewsApiClient(api_key='efb3d9c3033045209138f4eb2047f013')
                    all_articles = newsapi.get_everything(q=query,
                                                    sources='cnn',
                                                    language='en',
                                                    sort_by='relevancy',
                                                    page_size=1,
                                                    page=1)
                    for i in all_articles["articles"]:
                        cnn=discord.Embed(
                            title=i["title"],
                            description=i["description"],
                            url=i["url"],
                            color=discord.Color.red()
                        )
                        cnn.set_author(name=(i["author"]))
                        cnn.set_image(url=i["urlToImage"])

                        cnn.set_footer(text=i["publishedAt"])
                        cnn.add_field(name="Content",value=i["content"])
                    await m.edit(embed=cnn)
                elif str(reaction.emoji) == '🟢':
                    newsapi = NewsApiClient(api_key='efb3d9c3033045209138f4eb2047f013')
                    all_articles = newsapi.get_everything(q=query,
                                                    sources='bbc-news',
                                                    language='en',
                                                    sort_by='relevancy',
                                                    page_size=1,
                                                    page=1)
                    for i in all_articles["articles"]:
                        bbc=discord.Embed(
                            title=i["title"],
                            description=i["description"],
                            url=i["url"],
                            color=discord.Color.red()
                        )
                        bbc.set_author(name=i["author"])
                        bbc.set_image(url=i["urlToImage"])
                        bbc.set_footer(text=i["publishedAt"])
                        bbc.add_field(name="Content",value=i["content"])
                    await m.edit(embed=bbc)
                elif str(reaction.emoji) == '🔵':
                
                    newsapi = NewsApiClient(api_key='efb3d9c3033045209138f4eb2047f013')
                    all_articles = newsapi.get_everything(q=query,
                                                    sources='the-washington-post',
                                                    language='en',
                                                    sort_by='relevancy',
                                                    page_size=1,
                                                    page=1)
                    for i in all_articles["articles"]:
                        wash=discord.Embed(
                            title=i["title"],
                            description=i["description"],
                            url=i["url"],
                            color=discord.Color.red()
                        )
                        wash.set_author(name=i["author"])
                        wash.set_image(url=i["urlToImage"])
                        wash.set_footer(text=i["publishedAt"])
                        wash.add_field(name="Content",value=i["content"])
                    await m.edit(embed=wash)
                else:
                    if str(reaction.emoji) == '📖':
                        await m.remove_reaction('📖', member)
                        default=discord.Embed(
                                    title=f"Everything you need about {query}",
                                    description="You searched for results in English",
                                    color=discord.Color.red()
                                )
                        default.add_field(name="__**Command Index**__", value="📖 Shows this Menu\n\n🔴__**CNN NEWS**__\n\n🟢 __**BBC NEWS**__\n\n🔵__**The Washington Post**__",inline=False)
                        default.set_author(name=f"Command Requested by: {ctx.author}", icon_url=f"{ctx.author.avatar_url}")                                     
                        await m.edit(embed=default)
    elif language=="fr":
        news_fr=discord.Embed(
            title=f"Everything you need about {query}",
            description="You searched for results in French",
            color=discord.Color.red()
        )


        news_fr.add_field(name="__**Command Index**__", value="📖 Shows this Menu\n\n🔴__**Le Monde**__\n\n🟢 __**Les échos**__\n\n🔵__**Libération**__",inline=False)
        news_fr.set_author(name=f"Command Requested by: {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        m = await ctx.send(embed=news_fr)
        await m.edit(embed=news_fr)
        await m.add_reaction('📖')

        await m.add_reaction('🔴')
        await m.add_reaction('🟢')
        await m.add_reaction('🔵')

        def checkreact(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['📖','🔴', '🟢','🔵']
        while True:
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=checkreact)

            except TimeoutError:
                pass
            except asyncio.exceptions.TimeoutError:
                pass
            except asyncio.TimeoutError:
                bruh = discord.Embed(color=discord.Color.dark_red())
                bruh.add_field(name="__**What were you doing?**__", value="Don't stay more than 20 seconds ya lazy")
                try:
                    await m.edit(embed=bruh, delete_after=5)
                except discord.errors.NotFound:
                    pass

            except discord.errors.NotFound:
                pass 
            
            else:
                if str(reaction.emoji) == '🔴':                    
                    newsapi = NewsApiClient(api_key='efb3d9c3033045209138f4eb2047f013')
                    all_articles = newsapi.get_everything(q=query,
                                                    sources='le-monde',
                                                    language='fr',
                                                    sort_by='relevancy',
                                                    page_size=1,
                                                    page=1)
                    for i in all_articles["articles"]:
                        ggle=discord.Embed(
                            title=i["title"],
                            description=i["description"],
                            url=i["url"],
                            color=discord.Color.red()
                        )
                        ggle.set_author(name=i["author"])
                        ggle.set_image(url=i["urlToImage"])
                        ggle.set_footer(text=i["publishedAt"])
                        ggle.add_field(name="Content",value=i["content"])
                    await m.edit(embed=ggle)
                elif str(reaction.emoji) == '🟢':
                    newsapi = NewsApiClient(api_key='efb3d9c3033045209138f4eb2047f013')
                    all_articles = newsapi.get_everything(q=query,
                                                    sources='les-echos',
                                                    language='fr',
                                                    sort_by='relevancy',
                                                    page_size=1,
                                                    page=1)
                    for i in all_articles["articles"]:
                        monde=discord.Embed(
                            title=i["title"],
                            description=i["description"],
                            url=i["url"],
                            color=discord.Color.red()
                        )
                        monde.set_author(name=i["author"])
                        monde.set_image(url=i["urlToImage"])
                        monde.set_footer(text=i["publishedAt"])
                        monde.add_field(name="Content",value=i["content"])
                    await m.edit(embed=monde)
                elif str(reaction.emoji) == '🔵':
                    newsapi = NewsApiClient(api_key='efb3d9c3033045209138f4eb2047f013')
                    all_articles = newsapi.get_everything(q=query,
                                                    sources='liberation',
                                                    language='fr',
                                                    sort_by='relevancy',
                                                    page_size=1,
                                                    page=1)
                    for i in all_articles["articles"]:
                        echos=discord.Embed(
                            title=i["title"],
                            description=i["description"],
                            url=i["url"],
                            color=discord.Color.red()
                        )
                        echos.set_author(name=i["author"])
                        echos.set_image(url=i["urlToImage"])
                        echos.set_footer(text=i["publishedAt"])
                        echos.add_field(name="Content",value=i["content"])
                    await m.edit(embed=echos)
                else:
                    if str(reaction.emoji) == '📖':
                        await m.remove_reaction('📖', member)
                        default=discord.Embed(
                                    title=f"Everything you need about {query}",
                                    description="You searched for results in French",
                                    color=discord.Color.red()
                                )
                        default.add_field(name="__**Command Index**__", value="📖 Shows this Menu\n\n🔴__**Le Monde**__\n\n🟢 __**Les échos**__\n\n🔵__**Libération**__",inline=False)
                        default.set_author(name=f"Command Requested by: {ctx.author}", icon_url=f"{ctx.author.avatar_url}")                                     
                        await m.edit(embed=default)
    elif language=="es":
        news_fr=discord.Embed(
            title=f"Everything you need about {query}",
            description="You searched for results in Spanish",
            color=discord.Color.red()
        )


        news_fr.add_field(name="__**Command Index**__", value="📖 Shows this Menu\n\n🔴__**El-Mundo**__\n\n🟢 __**CNN Spanish**__\n\n🔵__**La Nacion**__",inline=False)
        news_fr.set_author(name=f"Command Requested by: {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
        m = await ctx.send(embed=news_fr)
        await m.edit(embed=news_fr)
        await m.add_reaction('📖')

        await m.add_reaction('🔴')
        await m.add_reaction('🟢')
        await m.add_reaction('🔵')

        def checkreact(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['📖','🔴', '🟢','🔵']
        while True:
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=checkreact)

            except TimeoutError:
                pass
            except asyncio.exceptions.TimeoutError:
                pass
            except asyncio.TimeoutError:
                bruh = discord.Embed(color=discord.Color.dark_red())
                bruh.add_field(name="__**What were you doing?**__", value="Don't stay more than 20 seconds ya lazy")
                try:
                    await m.edit(embed=bruh, delete_after=5)
                except discord.errors.NotFound:
                    pass

            except discord.errors.NotFound:
                pass 
            
            else:
                if str(reaction.emoji) == '🔴':                    
                    newsapi = NewsApiClient(api_key='efb3d9c3033045209138f4eb2047f013')
                    all_articles = newsapi.get_everything(q=query,
                                                    sources='el-mundo',
                                                    language='es',
                                                    sort_by='relevancy',
                                                    page_size=1,
                                                    page=1)
                    for i in all_articles["articles"]:
                        ggle=discord.Embed(
                            title=i["title"],
                            description=i["description"],
                            url=i["url"],
                            color=discord.Color.red()
                        )
                        ggle.set_author(name=i["author"])
                        ggle.set_image(url=i["urlToImage"])
                        ggle.set_footer(text=i["publishedAt"])
                        ggle.add_field(name="Content",value=i["content"])
                    await m.edit(embed=ggle)
                elif str(reaction.emoji) == '🟢':
                    newsapi = NewsApiClient(api_key='efb3d9c3033045209138f4eb2047f013')
                    all_articles = newsapi.get_everything(q=query,
                                                    sources='cnn-es',
                                                    language='es',
                                                    sort_by='relevancy',
                                                    page_size=1,
                                                    page=1)
                    for i in all_articles["articles"]:
                        monde=discord.Embed(
                            title=i["title"],
                            description=i["description"],
                            url=i["url"],
                            color=discord.Color.red()
                        )
                        monde.set_author(name=i["author"])
                        monde.set_image(url=i["urlToImage"])
                        monde.set_footer(text=i["publishedAt"])
                        monde.add_field(name="Content",value=i["content"])
                    await m.edit(embed=monde)
                elif str(reaction.emoji) == '🔵':
                    newsapi = NewsApiClient(api_key='efb3d9c3033045209138f4eb2047f013')
                    all_articles = newsapi.get_everything(q=query,
                                                    sources='la-nacion',
                                                    language='es',
                                                    sort_by='relevancy',
                                                    page_size=1,
                                                    page=1)
                    for i in all_articles["articles"]:
                        echos=discord.Embed(
                            title=i["title"],
                            description=i["description"],
                            url=i["url"],
                            color=discord.Color.red()
                        )
                        echos.set_author(name=i["author"])
                        echos.set_image(url=i["urlToImage"])
                        echos.set_footer(text=i["publishedAt"])
                        echos.add_field(name="Content",value=i["content"])
                    await m.edit(embed=echos)
                else:
                    if str(reaction.emoji) == '📖':
                        await m.remove_reaction('📖', member)
                        default=discord.Embed(
                                    title=f"Everything you need about {query}",
                                    description="You searched for results in French",
                                    color=discord.Color.red()
                                )
                        default.add_field(name="__**Command Index**__", value="📖 Shows this Menu\n\n🔴__**El-Mundo**__\n\n🟢 __**CNN Spanish**__\n\n🔵__**La Nacion**__",inline=False)
                        default.set_author(name=f"Command Requested by: {ctx.author}", icon_url=f"{ctx.author.avatar_url}")                                     
                        await m.edit(embed=default)
    
    
    
    
    else:
        await ctx.send("I don't know this language OR I don't use it to retrieve news... Check `z!help` for further information")


@client.command()
@appropriate_channel()
async def weather(ctx,*city):
    if len(city)>=1:
        await ctx.send(embed=get_weather(" ".join(city)))
    else:
        print(city)
        await ctx.send("Whut")

@client.command()
@appropriate_channel()
async def flag(ctx,*args):
    pass


@client.group(name="covid")
async def covid(ctx):
    await ctx.send("Covid Platform")

@covid.command(name="latest")
async def latest(ctx):
    await ctx.send("Returns latest")




"""
@client.command()
@appropriate_channel()
async def help(ctx):
    pass

"""
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')  

client.loop.run_until_complete(db_connection())
client.run('NzMxNjE4MjY5NDI0Nzc5Mjg0.XwoqnA.PnaQuRayqxNCXs7n_LMIIYx2YGY') #Runs the bot