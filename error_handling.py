import traceback
import sys

from discord.ext import commands
import asyncio
import utils


class ErrorHandling(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error,commands.CommandOnCooldown) or isinstance(error,commands.MaxConcurrencyReached):
            return
            # await utils.error_embed(ctx, 'Invalid command', f'Use `{utils.prefix}help` to see the available commands.')
    
        if isinstance(error, commands.CommandNotFound):
            """
            msg=await utils.error_embed(ctx, 'Invalid command', f'Use `{utils.prefix}help` to see the available commands.')
            await asyncio.sleep(2)
            await ctx.message.delete()
            await msg.delete()
            """
            return
        


        if isinstance(error, commands.CheckFailure):
            return
        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'vouch' or ctx.command.qualified_name == 'myvouches' or ctx.command.qualified_name == 'delvouc h':
                return

            await utils.error_embed(ctx, ctx,'Invalid command argument', f'Please refer to `{utils.prefix}help_vouch` to see command usage.')
        else:
            #print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            await utils.error_embed(ctx, 'Something went wrong', f'```md\n{type(error)} {error}```')


def setup(bot):
    bot.add_cog(ErrorHandling(bot))
