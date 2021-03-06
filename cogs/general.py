import discord
from discord.ext import commands
import datetime
import psutil
import os
import time
import random
import re
import aiohttp
import json
from cogs.utils import converters

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ball = [
            "As I see it, yes.", "It is certain.", "It is decidedly so.",
            "Most likely.", "Outlook good.", "Signs point to yes.",
            "Without a doubt.", "Yes.", "Yes – definitely.", "You may rely on it.",
            "Reply hazy, try again.", "Ask again later.",
            "Better not tell you now.", "Cannot predict now.",
            "Concentrate and ask again.", "Don't count on it.", "My reply is no.",
            "My sources say no.", "Outlook not so good.", "Very doubtful."
        ]

    @commands.command(aliases=['yt'])
    async def youtube(self, ctx, *, search_terms):
        "Find YouTube video with specified title."
        try:
            query = {'search_query': search_terms}
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://www.youtube.com/results?", params=query) as req:
                    content = await req.read()
                    search_result = re.findall(r'href=\"\/watch\?v=(.{11})', content.decode())
            await ctx.send(f"http://www.youtube.com/watch?v={search_result[0]}")
        except IndexError:
            await ctx.send("No video was found.")

    @commands.command(aliases=['sinfo'])
    @commands.guild_only()
    async def serverinfo(self, ctx):
        "Get current server info."
        guild = ctx.guild
        levels = {
            "None - No criteria set.": discord.VerificationLevel.none,
            "Low - Member must have a verified email on their Discord account.": discord.VerificationLevel.low,
            "Medium - Member must have a verified email and be registered on Discord for more than five minutes.": discord.VerificationLevel.medium,
            "High - Member must have a verified email, be registered on Discord for more than five minutes, and be a member of the guild itself for more than ten minutes.": discord.VerificationLevel.table_flip,
            "Extreme - Member must have a verified phone on their Discord account.": discord.VerificationLevel.double_table_flip
        }
        filters = {
            "Disabled - The guild does not have the content filter enabled.": discord.ContentFilter.disabled,
            "No Role - The guild has the content filter enabled for members without a role.": discord.ContentFilter.no_role,
            "All Members - The guild has the content filter enabled for every member.": discord.ContentFilter.all_members
        }
        regions = {
            "US West": discord.VoiceRegion.us_west,
            "US East": discord.VoiceRegion.us_east,
            "US South": discord.VoiceRegion.us_south,
            "US Central": discord.VoiceRegion.us_central,
            "London": discord.VoiceRegion.london,
            "Sydney": discord.VoiceRegion.sydney,
            "Amsterdam": discord.VoiceRegion.amsterdam,
            "Frankfurt": discord.VoiceRegion.frankfurt,
            "Brazil": discord.VoiceRegion.brazil,
            "Hong Kong": discord.VoiceRegion.hongkong,
            "Russia": discord.VoiceRegion.russia,
            "VIP US East": discord.VoiceRegion.vip_us_east,
            "VIP US West": discord.VoiceRegion.vip_us_west,
            "VIP Amsterdam": discord.VoiceRegion.vip_amsterdam,
            "Singapore": discord.VoiceRegion.singapore,
            "EU Central": discord.VoiceRegion.eu_central,
            "EU West": discord.VoiceRegion.eu_west
        }
        for name, reg in regions.items():
            if reg is guild.region:
                server_region = name
        verif_lvl = 'None'
        for text, dvl in levels.items():
            if dvl is guild.verification_level:
                verif_lvl = text
        for response, filt in filters.items():
            if filt is guild.explicit_content_filter:
                content_fiter = response
        feats = ''
        if guild.features != []:
            for feature in guild.features:
                feats += feature + '\n'
        else:
            feats = 'None'
        if guild.emojis:
            emotes_list = ', '.join([f'`{emoji.name}` - <:{emoji.name}:{emoji.id}>' for emoji in guild.emojis[0:10]])
        else:
            emotes_list = "None"
        if len(guild.roles) > 1:
            roles_list = ', '.join([f'`{role}`' for role in guild.roles[::-1] if role.name != '@everyone'])
        else:
            roles_list = "None"
        embed = discord.Embed(title='Server info', color = guild.me.color)
        embed.set_author(name=f'{guild.name} - {guild.id}')
        embed.set_thumbnail(url=guild.icon_url_as(format='png'))
        embed.add_field(name='Owner', value=guild.owner)
        embed.add_field(name='Owner ID', value=guild.owner.id)
        embed.add_field(name='Members', value=guild.member_count)
        embed.add_field(name='Text Channels', value=len(guild.text_channels))
        embed.add_field(name='Voice Channels', value=len(guild.voice_channels))
        embed.add_field(name='Created at', value=guild.created_at.strftime('%d.%m.%Y %H:%M'))
        embed.add_field(name='Categories', value=len(guild.categories))
        embed.add_field(name='Region', value=server_region)
        embed.add_field(name=f'Roles ({len(guild.roles)})', value=roles_list)
        embed.add_field(name=f'Features ({len(guild.features)})', value=feats)
        embed.add_field(name='Verification Level', value=verif_lvl)
        embed.add_field(name='Content Filter', value=content_fiter)
        embed.add_field(name=f'Emojis ({len(guild.emojis)})', value=emotes_list)
        await ctx.send(embed=embed)

    @commands.command()
    async def contact(self, ctx, *, msg):
        "Contact the bot owner through the bot."
        owner = self.bot.owner
        embed = discord.Embed(title=f'Sent by {ctx.author} ({ctx.author.id})', description = msg)
        try:
            await owner.send('`contact` command used.', embed = embed)
        except discord.Forbidden:
            await ctx.send(f"Bot owner ({owner}) disabled DMs from non-friends.")

    @commands.command(aliases=['8ball'])
    async def eightball(self, ctx, *, question):
        "Ask 8ball a question."
        result = random.choice(self.ball)
        if ctx.guild:
            embed_color = ctx.guild.me.color
        else:
            embed_color = 16753920
        em = discord.Embed(description=question, title='🎱 8ball', color=embed_color)
        em.add_field(name='Answer', value=result)
        await ctx.send(ctx.author.mention, embed=em)

    @commands.command(aliases=['pong'])
    async def ping(self, ctx):
        "Bot's connection to Discord."
        t1 = time.perf_counter()
        await ctx.channel.trigger_typing()
        t2 = time.perf_counter()
        thedata = f'🏓 **Pong.**\nTime: {round((t2 - t1) * 1000)}ms'
        if ctx.guild:
            embed_color = ctx.guild.me.color
        else:
            embed_color = discord.Color.default()
        data = discord.Embed(description=thedata, color=embed_color)
        await ctx.send(embed=data)

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, *, user: converters.User = None):
        "User's avatar."
        author = ctx.author
        user = user or author
        embed = discord.Embed(color=ctx.guild.me.color if ctx.guild else 16753920)
        embed.set_author(name=user)
        avatar_url = str(user.avatar_url)
        embed.set_image(url=avatar_url.replace('.webp', '.png').replace('size=1024', 'size=2048'))
        await ctx.send(embed=embed)

    @commands.command()
    async def roles(self, ctx, *, user: converters.Member = None):
        "Check the user's roles. Provide no arguments to check your roles."
        user = user or ctx.author
        desc = '\n'.join([r.name for r in user.roles if r.name != '@everyone'])
        if not desc:
            await ctx.send(f'{user} has no roles!')
        else:
            embed = discord.Embed(
                title=f"{user} roles",
                description=desc,
                colour=user.color)
            await ctx.send(ctx.author.mention, embed=embed)

    @commands.command()
    async def invite(self, ctx):
        "A link that lets you invite this bot your server."
        await ctx.send(f'{ctx.author.mention} **OAuth2 link to invite {self.bot.user.name} bot to your server:** <https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&permissions=469887047&scope=bot>')

    @commands.command(aliases=['roleperms', 'role_permissions', 'rolepermissions']) # WHY SO MANY ALIASES
    @commands.guild_only()
    async def role_perms(self, ctx, * , role: converters.Role):
        "Get role permissions."
        s = []
        for perm, value in role.permissions:
            perm_name = perm.replace('_', ' ').replace('Tts', 'TTS')
            if not value:
                s.append(f'-{perm_name.title()}: ❌')
            else:
                s.append(f'+{perm_name.title()}: ✅')
        output = '\n'.join(s)
        await ctx.send(f'```diff\n{output}\n```')

    def get_bot_uptime(self):
        # Courtesy of Danny
        now = datetime.datetime.utcnow()
        delta = now - self.bot.uptime
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)

        if days:
            fmt = f'{days} days, {hours} hours, {minutes} minutes, and {seconds} seconds'
        else:
            fmt = f'{hours} hours, {minutes} minutes, and {seconds} seconds'

        return fmt

    @commands.command()
    async def stats(self, ctx):
        "Bot uptime and stuff."
        channels = 0
        members = 0
        for guild in self.bot.guilds:
            channels += len(guild.text_channels) + len(guild.voice_channels)
        members = len(self.bot.users)
        owner = self.bot.owner
        author = ctx.author
        uptime_time = self.get_bot_uptime()
        if self.bot.user.id == 458607948755763200:
            support_stuff = f'[Support server](https://discord.gg/f5nDpp6)\n[Patreon](https://www.patreon.com/shivaco)\n[Vote for {self.bot.user.name} on discordbots.org](https://discordbots.org/bot/{self.bot.user.id}/vote)'
        else:
            support_stuff = '[Support server](https://discord.gg/f5nDpp6)\n[Patreon](https://www.patreon.com/shivaco)'
        servers = len(self.bot.guilds)
        process = psutil.Process(os.getpid())
        mem = round(process.memory_info()[0] / float(2 ** 20), 2)
        if ctx.guild:
            embed_color = ctx.guild.me.color
        else:
            embed_color = 16753920
        embed = discord.Embed(description = f'**Uptime:** {uptime_time}\n**Memory**: {mem} MB', color = embed_color)
        embed.set_author(
            name = 'Source Code',
            url = 'https://github.com/shivaco/Mari-bot',
            icon_url = self.bot.user.avatar_url)
        embed.add_field(name='Owner', value=owner)
        embed.add_field(name='Bot ID', value=self.bot.user.id)
        embed.add_field(name='Servers', value=servers)
        embed.add_field(name='Channels', value=channels)
        embed.add_field(name='Users', value=members)
        embed.add_field(name='Additional Info', value=support_stuff)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(General(bot))
