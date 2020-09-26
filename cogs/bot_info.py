import discord
from discord.ext import commands
from discord.utils import get,find
import utils
import time
import datetime
import math
import sqlite3
import os
from asyncio.subprocess import Process
from platform import python_version
from discord import __version__ as discord_version
from psutil import Process, virtual_memory


class Info(commands.Cog):
    
    def __init__(self,bot):
        self.bot=bot



    
    @commands.command()
    @utils.appropriate_channel()
    async def about(self,ctx):
        

        stats = discord.Embed(
            title="About me!",
            color=discord.Color.red()
            )
            
        stats.set_thumbnail(url=self.bot.user.avatar_url)


        DIR_guilds="d:\CODING\DISCORD BOT\Bot\\"
        db_guilds=sqlite3.connect(os.path.join(DIR_guilds,"Guild.db"))
        SQL_guilds=db_guilds.cursor()

        SQL_guilds.execute(f'select location from Guilds where guild_id="{ctx.guild.id}"')
        location=SQL_guilds.fetchone()
        print(location[0])
        channel_location = find(lambda x: x.name == location[0],  ctx.guild.text_channels) 
        proc = Process()
        with proc.oneshot():
            mem_total = virtual_memory().total / (1024 ** 2)
            mem_of_total = proc.memory_percent()
            mem_usage = mem_total * (mem_of_total / 100)

        channels = map(lambda m: len(m.channels), self.bot.guilds)

        delta_uptime = datetime.datetime.utcnow() - ctx.bot.launch_time
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        fields = [
            ("__*Developer*__", "<@358629457025826816>", False),
            ("__*Github<:github:744345792172654643>*__", "https://github.com/TheFuser", False),
            ("__*Language | Library*__",
             f"<:python:596577462335307777> Python {python_version()} | <:dpy:596577034537402378> Discord.py {discord_version}",
             False),

            ("__*<a:squirtleHype:739616791084400701> Support Server*__",
             "[Here!](https://discord.gg/FhxgvF)", True),

            ("__*<a:crabrave:739615014679347201> Invite Link*__",
             "Not set yet", True),
             #"[Here!](https://discord.com/oauth2/authorize?client_id=721397896704163965&scope=bot&permissions=470117623)", True),

            ("__*❗ Current Prefix*__", f'`{ctx.prefix}`', True),
            ("__*❗ My token*__ : <a:loading:747680523459231834>", 'Patience scammer', False),
            ("__*Discord Stats*__",
             "All Guilds: {}"
             "\nAll Channels: {}"
             "\nAll Emojis: {}"
             "\nAll Commands: {}"
             "\nAll Users: {:,}".format(len(self.bot.guilds), sum(list(channels)), len(self.bot.emojis),
                                    len(self.bot.commands),
                                    len(self.bot.users)), True),

            #("__*Line Count*__", lineCount(), True),
            ("__*Help Command*__", "Under Construction", True),
            ("__*Where can you use me*__?", channel_location.mention, False),
            ("__*Uptime*__", f"{days}d, {hours}h, {minutes}m, {seconds}s", False),
            ("__*Latency*__", f'{round(self.bot.latency * 1000)}ms', False),
            ("__*Memory Usage*__", f"{mem_usage:,.2f} / {mem_total:,.2f} MiB ({mem_of_total:.2f}%)", False)]

        for name, value, inline in fields:
            stats.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=stats)

    @commands.command()
    @utils.appropriate_channel()
    async def info(self,ctx):
        guild=ctx.guild

        if guild.description is None:   DESCRIPTION=""
        else:   DESCIPTION=guild.description


        BIRTH=guild.created_at
        passed = (ctx.message.created_at - guild.created_at).days
        created_at = ("Created on {date}. That's over {num} days ago!").format(
            date=guild.created_at.strftime("%d %b %Y %H:%M"),
            num=passed,
        )

        online = len([m.status for m in guild.members if m.status != discord.Status.offline])
        total_users = guild.member_count
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)





        """
        embed=discord.Embed(
            title=f'Information about {str(guild)}',
            description=f'{DESCRIPTION}\n{created_at}',
            color=discord.Color.purple()
        )
        
        
        embed.add_field(name="**Main Info**",value=f"\
        Name: {str(guild)}\n\
        ID: {guild.id}\n\
        OWner: <@{OWNER_ID}>\n\
        Region: {REGION}\n\
        Verification level (from 1 to 5): {VERIFICATION_LEVEL}\n\
        Created on : {BIRTH}\n\
        Created : Ago\n\
        ")
        """

        def _size(num: int):
                for unit in ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB"]:
                    if abs(num) < 1024.0:
                        return "{0:.1f}{1}".format(num, unit)
                    num /= 1024.0
                return "{0:.1f}{1}".format(num, "YB")

        def _bitsize(num: int):
            for unit in ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB"]:
                if abs(num) < 1000.0:
                    return "{0:.1f}{1}".format(num, unit)
                num /= 1000.0
            return "{0:.1f}{1}".format(num, "YB")
        """
        shard_info = (
            ("\nShard ID: **{shard_id}/{shard_count}**").format(
                shard_id=0 + 1, #shard_id=guild.shard_id + 1,
                shard_count=ctx.bot.shard_count,
            )
            if ctx.bot.shard_count is None
            else ""
        )
        """
        # Logic from: https://github.com/TrustyJAID/Trusty-cogs/blob/master/serverstats/serverstats.py#L159
        online_stats = {
            ("Humans: "): lambda x: not x.bot,
            (" •<:bot_tag:596576775555776522>Bots: "): lambda x: x.bot,
            "\n<:status_online:596576749790429200> ONLINE": lambda x: x.status is discord.Status.online,
            "\n<:status_idle:596576773488115722> IDLE": lambda x: x.status is discord.Status.idle,
            "<:status_dnd:596576774364856321> DNB": lambda x: x.status is discord.Status.do_not_disturb,
            "\n<:status_offline:596576752013279242> OFFLINE \N{VARIATION SELECTOR-16}": lambda x: (
                x.status is discord.Status.offline
            ),
            "<:status_streaming:596576747294818305> STREAMING": lambda x: any(
                a.type is discord.ActivityType.streaming for a in x.activities
            ),
            "\n\N{MOBILE PHONE} ON MOBILE": lambda x: x.is_on_mobile(),
        }
        member_msg = ("Users online: **{online}/{total_users}**\n").format(
            online=online, total_users=total_users
        )
        count = 1
        for emoji, value in online_stats.items():
            try:
                num = len([m for m in guild.members if value(m)])
            except Exception as error:
                print(error)
                continue
            else:
                member_msg += f"{emoji} {utils.bold(num)} " + (
                    "\n" if count % 2 == 0 else ""
                )
            count += 1

        vc_regions = {
            "vip-us-east": ("__VIP__ US East ") + "\U0001F1FA\U0001F1F8",
            "vip-us-west": ("__VIP__ US West ") + "\U0001F1FA\U0001F1F8",
            "vip-amsterdam": ("__VIP__ Amsterdam ") + "\U0001F1F3\U0001F1F1",
            "eu-west": ("EU West ") + "\U0001F1EA\U0001F1FA",
            "eu-central": ("EU Central ") + "\U0001F1EA\U0001F1FA",
            "europe": ("Europe ") + "\U0001F1EA\U0001F1FA",
            "london": ("London ") + "\U0001F1EC\U0001F1E7",
            "frankfurt": ("Frankfurt ") + "\U0001F1E9\U0001F1EA",
            "amsterdam": ("Amsterdam ") + "\U0001F1F3\U0001F1F1",
            "us-west": ("US West ") + "\U0001F1FA\U0001F1F8",
            "us-east": ("US East ") + "\U0001F1FA\U0001F1F8",
            "us-south": ("US South ") + "\U0001F1FA\U0001F1F8",
            "us-central": ("US Central ") + "\U0001F1FA\U0001F1F8",
            "singapore": ("Singapore ") + "\U0001F1F8\U0001F1EC",
            "sydney": ("Sydney ") + "\U0001F1E6\U0001F1FA",
            "brazil": ("Brazil ") + "\U0001F1E7\U0001F1F7",
            "hongkong": ("Hong Kong ") + "\U0001F1ED\U0001F1F0",
            "russia": ("Russia ") + "\U0001F1F7\U0001F1FA",
            "japan": ("Japan ") + "\U0001F1EF\U0001F1F5",
            "southafrica": ("South Africa ") + "\U0001F1FF\U0001F1E6",
            "india": ("India ") + "\U0001F1EE\U0001F1F3",
            "dubai": ("Dubai ") + "\U0001F1E6\U0001F1EA",
            "south-korea": ("South Korea ") + "\U0001f1f0\U0001f1f7",
        }
        verif = {
            "none": ("0 - None"),
            "low": ("1 - Low"),
            "medium": ("2 - Medium"),
            "high": ("3 - High"),
            "extreme": ("4 - Extreme"),
        }

        features = {
            "PARTNERED": ("Partnered"),
            "VERIFIED": ("Verified"),
            "DISCOVERABLE": ("Server Discovery"),
            "FEATURABLE": ("Featurable"),
            "COMMUNITY": ("Community"),
            "PUBLIC_DISABLED": ("Public disabled"),
            "INVITE_SPLASH": ("Splash Invite"),
            "VIP_REGIONS": ("VIP Voice Servers"),
            "VANITY_URL": ("Vanity URL"),
            "MORE_EMOJI": ("More Emojis"),
            "COMMERCE": ("Commerce"),
            "NEWS": ("News Channels"),
            "ANIMATED_ICON": ("Animated Icon"),
            "BANNER": ("Banner Image"),
            "MEMBER_LIST_DISABLED": ("Member list disabled"),
        }
        guild_features_list = [
            f"\N{WHITE HEAVY CHECK MARK} {name}"
            for feature, name in features.items()
            if feature in guild.features
        ]

        joined_on = (
            "{bot_name} joined this server on {bot_join}. {since_join} days passed since that wonderful moment!"
        ).format(
            bot_name=ctx.bot.user.name,
            bot_join=guild.me.joined_at.strftime("%d %b %Y %H:%M:%S"),
            since_join=(ctx.message.created_at - guild.me.joined_at).days,
        )

        data = discord.Embed(
            description=(f"{guild.description}\n\n" if guild.description else "") + created_at,
            colour=discord.Color.blue(),
        )
        data.set_author(
            name=guild.name,
            icon_url="https://cdn.discordapp.com/emojis/457879292152381443.png"
            if "VERIFIED" in guild.features
            else "https://cdn.discordapp.com/emojis/508929941610430464.png"
            if "PARTNERED" in guild.features
            else discord.Embed.Empty,
        )
        if guild.icon_url:
            data.set_thumbnail(url=guild.icon_url)
        data.add_field(name=("Members:"), value=member_msg)
        data.add_field(
            name=("Channels:"),
            value=(
                "\N{SPEECH BALLOON} Text: {text}\n"
                "\N{SPEAKER WITH THREE SOUND WAVES} Voice: {voice}"
            ).format(text=utils.bold(text_channels), voice=utils.bold(voice_channels)),
        )
        data.add_field(
            name=("Utility:"),
            value=(
                "Owner: {owner}\nVoice region: {region}\nVerif. level: {verif}\nServer ID: {id}"
            ).format(
                owner=utils.bold(str(guild.owner)),
                region=f"**{vc_regions.get(str(guild.region)) or str(guild.region)}**",
                verif=utils.bold(verif[str(guild.verification_level)]),
                id=utils.bold(str(guild.id))
            ),
            inline=False,
        )
        data.add_field(
            name=("Misc:"),
            value=(
                "AFK channel: {afk_chan}\nAFK timeout: {afk_timeout}\nCustom emojis: {emoji_count}\nRoles: {role_count}"
            ).format(
                afk_chan=utils.bold(str(guild.afk_channel))
                if guild.afk_channel
                else utils.bold(("Not set")),
                afk_timeout=utils.bold(utils.humanize_timedelta(seconds=guild.afk_timeout)),
                emoji_count=utils.bold(len(guild.emojis)),
                role_count=utils.bold(len(guild.roles)),
            ),
            inline=False,
        )
        if guild_features_list:
            data.add_field(name=("Server features:"), value="\n".join(guild_features_list))
        if guild.premium_tier != 0:
            nitro_boost = (
                "Tier {boostlevel} with {nitroboosters} boosters\n"
                "File size limit: {filelimit}\n"
                "Emoji limit: {emojis_limit}\n"
                "VCs max bitrate: {bitrate}"
            ).format(
                boostlevel=utils.bold(str(guild.premium_tier)),
                nitroboosters=utils.bold(guild.premium_subscription_count),
                filelimit=utils.bold(_size(guild.filesize_limit)),
                emojis_limit=utils.bold(str(guild.emoji_limit)),
                bitrate=utils.bold(_bitsize(guild.bitrate_limit)),
            )
            data.add_field(name=("Nitro Boost:"), value=nitro_boost)
        if guild.splash:
            data.set_image(url=guild.splash_url_as(format="png"))
        data.set_footer(text=joined_on)


        await ctx.send(embed=data)
    

def setup(bot):
    bot.add_cog(Info(bot))