import asyncio
import discord
from discord.ext import commands, tasks
from discord.utils import find
import os
import utils
import random
import sqlite3


class Economy(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #@commands.cooldown(1, 30, commands.BucketType.user)
    @commands.command(pass_context=True, brief="Shows the user's balance")
    async def bal(self,ctx):
        DIR = "d:\CODING\DISCORD BOT\Bot\\"
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
        
        await ctx.send(f'{ctx.message.author.mention} has a balance of {result_userID[0]} zolos')
    

    """
    @bal.error
    async def bal_error(self,ctx, error):
        if isinstance(error,commands.CommandOnCooldown):
            if ctx.message.author.guild_permissions.manage_guild:
                await ctx.reinvoke()
                return
            await ctx.send(error)
    """

def setup(bot):
    bot.add_cog(Economy(bot))