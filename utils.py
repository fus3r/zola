import discord
import sqlite3
import os
import json
from discord.ext import commands
import asyncpg
from typing import Callable, Union, Dict, Optional, Iterator, List, Sequence, SupportsInt, Union
import datetime

prefix = 'z!'
footer_text = f'type {prefix}help to see my commands'
embed_color = 0x3cd3f6
error_embed_color = 0xff0000

def appropriate_channel(): #Appropriate channels for other commands
        def predicate(ctx):
            if ctx.guild.id==336642139381301249:
                weather_channel=discord.utils.get(ctx.guild.text_channels, name='testing')
                playground=discord.utils.get(ctx.guild.text_channels, name='playground')
            else:
                weather_channel=discord.utils.get(ctx.guild.text_channels, name='zola')
            return ctx.channel.id==weather_channel.id or ctx.channel.id==playground
        return commands.check(predicate)



def write(self):
    with open('data.json', 'w') as file:
        file.write(json.dumps(self.bot.data, indent=4, sort_keys=True))


async def embed(ctx, where, title: str, description: str):
    _embed = discord.Embed(title=title, description=description, color=embed_color)
    _embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    _embed.set_footer(text=footer_text)
    return await where.send(embed=_embed)



async def error_embed(ctx, title: str, description: str):
    _embed = discord.Embed(title=":x: " + title, description=description, color=error_embed_color)
    _embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    _embed.set_footer(text=footer_text)
    return await ctx.send(embed=_embed)





def author_init(self,ctx):

    DIR = os.path.dirname(__file__)
    db = sqlite3.connect(os.path.join(DIR, "BankAccounts.db"))
    SQL = db.cursor()
    USER_ID=ctx.author.id
    USER_NAME=str(ctx.author)
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


    if ctx.author.id != self.bot.user.id and not str(ctx.author.id) in self.bot.data:
        #print(f'User {ctx.author} in {ctx.guild.name} has no vouch data, creating fresh vouch data for them.')
        self.bot.data[str(ctx.author.id)] = {"Username": str(ctx.author), "Vouches": {}, "Scam":{}}
        write(self)
        return False
    
    
    return True

def owner(ctx):
    return ctx.author.id == 349902688961691648


def none_to_zero(SQL,db,guild_id,option):
    SQL.execute(f'update Guilds set {option} = 0 where guild_id = ?', (guild_id,))
    db.commit()


def guild_prefix(SQL,db,guild_id):
    SQL.execute('select prefix from Guilds where guild_id = ?',(guild_id,))
    prefix=SQL.fetchone()
    return prefix[0]



def enabledPoem(ctx,SQL,db,guild_id):
    SQL.execute('select wantsPoem from Guilds where guild_id = ?',(guild_id,))
    result=SQL.fetchone()
    if result[0]==1:
        return True, ""
    else:
        return False,embed(ctx,ctx,"This server didn't enable the Poem Contest Feature",f"Mods,Admins and Owners can activate it using {guild_prefix(SQL,db,guild_id)}")


async def create_record_db(cursor,GUILD_ID,val1,val2):
    exist = await cursor.fetch(f"SELECT * FROM {GUILD_ID} WHERE name=$1",val1)
    if not exist:
        await cursor.execute(f"INSERT INTO {GUILD_ID} (name,value) VALUES ($1,$2)",val1,val2)




def bold(text: str, escape_formatting: bool = True) -> str:
    return "**{}**".format(text)

def humanize_timedelta(*, timedelta: Optional[datetime.timedelta] = None, seconds: Optional[SupportsInt] = None) -> str:
    try:
        obj = seconds if seconds is not None else timedelta.total_seconds()
    except AttributeError:
        raise ValueError("You must provide either a timedelta or a number of seconds")

    seconds = int(obj)
    periods = [
        (("year"), ("years"), 60 * 60 * 24 * 365),
        (("month"), ("months"), 60 * 60 * 24 * 30),
        (("day"), ("days"), 60 * 60 * 24),
        (("hour"), ("hours"), 60 * 60),
        (("minute"), ("minutes"), 60),
        (("second"), ("seconds"), 1),
    ]

    strings = []
    for period_name, plural_period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            if period_value == 0:
                continue
            unit = plural_period_name if period_value > 1 else period_name
            strings.append(f"{period_value} {unit}")

    return ", ".join(strings)

