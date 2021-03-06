import discord
from discord.ext import commands
import aiohttp
import random
from cogs.utils import converters

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *, msg):
        "Make the bot say something."
        await ctx.send(msg.replace("@everyone", "@\u200beveryone").replace("@here", "@\u200bhere")) # NO @EVERYONE PINGS FOR YA.

    @commands.command()
    @commands.guild_only()
    async def hug(self, ctx, *, user: converters.Member = None):
        'Hug your waifu!'
        author = ctx.author
        hug = '**{} hugged {}!**'
        hugself = '**{} hugged themself**'.format(author.mention)
        choices = [
            'https://i.imgur.com/sW3RvRN.gif', 'https://i.imgur.com/gdE2w1x.gif', 'https://i.imgur.com/zpbtWVE.gif',
            'https://i.imgur.com/ZQivdm1.gif', 'https://i.imgur.com/MWZUMNX.gif', 'https://i.imgur.com/8futZnQ.gif',
            'https://i.imgur.com/viWWVub.gif', 'https://i.imgur.com/S27E05M.gif', 'https://i.imgur.com/mXGKeyN.gif',
            'https://i.imgur.com/mxaqyUu.gif', 'https://i.imgur.com/dLUetXa.gif', 'https://i.imgur.com/hM1LcZf.gif',
            'https://i.imgur.com/i1JGnI8.gif', 'https://i.imgur.com/7yDRQ4Z.gif', 'https://i.imgur.com/KddSqvV.gif',
            'https://i.imgur.com/pHTBEb3.gif', 'https://i.imgur.com/gypFtQ2.gif', 'https://i.imgur.com/p1qlw2N.gif',
            'https://i.imgur.com/OqjBUdr.gif', 'https://i.imgur.com/1l3PIDz.gif', 'https://i.imgur.com/bmmPXtL.gif',
            'https://i.imgur.com/RIrOf2i.gif', 'https://i.imgur.com/x6855CW.gif'
        ]
        image = random.choice(choices)
        if user:
            if user is author:
                embed = discord.Embed(color=0)
                embed.set_image(url=image)
                await ctx.send(content=hugself, embed=embed)
            else:
                mention = user.mention
                embed = discord.Embed(color=user.color)
                embed.set_image(url=image)
                await ctx.send(content=hug.format(author.mention, mention), embed=embed)
        else:
            embed = discord.Embed(color=0)
            embed.set_image(url=image)
            await ctx.send(content=hugself, embed=embed)

    @commands.command()
    @commands.guild_only()
    async def kiss(self, ctx, *, user: converters.Member = None):
        'Kiss your waifu!'
        author = ctx.author
        kiss = '**{} kissed {}**'
        kissself = '**{} kissed themself**'.format(author.mention)
        choices = [
            'http://i.imgur.com/0D0Mijk.gif', 'https://i.imgur.com/4VePCc4.gif', 'http://i.imgur.com/3wv088f.gif',
            'https://i.imgur.com/dG73Bmb.gif', 'https://i.imgur.com/5epo3Ls.gif', 'https://i.imgur.com/JZLaOA2.gif',
            'https://i.imgur.com/5Hx4D9n.gif', 'https://i.imgur.com/j9Gvrrd.gif', 'https://i.imgur.com/jEmrZGS.gif',
            'https://i.imgur.com/kn9awse.gif', 'https://i.imgur.com/AIJn1LF.gif', 'https://i.imgur.com/uoaOqXO.gif',
            'https://i.imgur.com/dJWlgnr.gif', 'https://i.imgur.com/G8Mbg1Z.gif', 'https://i.imgur.com/evjODur.gif',
            'https://i.imgur.com/tumv7DY.gif'
        ]
        image = random.choice(choices)
        if user:
            if user == author:
                embed = discord.Embed(color=0)
                embed.set_image(url=image)
                await ctx.send(content=kissself, embed=embed)
            else:
                mention = user.mention
                embed = discord.Embed(color=user.color)
                embed.set_image(url=image)
                await ctx.send(content=kiss.format(author.mention, mention), embed=embed)
        else:
            embed = discord.Embed(color=0)
            embed.set_image(url=image)
            await ctx.send(content=kissself, embed=embed)

    @commands.command()
    async def kekify(self, ctx, *, text):
        'Replaces `k` with `kek`.'
        result = ''
        for char in text:
            if char == 'k':
                result += 'kek'
            elif char == 'K':
                result += 'KEK'
            else:
                result += char
        if len(result) >= 2000:
            await ctx.send('Turns out the edited version has more than 2000 characters. Try again with a fewer amount of characters.')
        else:
            await ctx.send(f"{ctx.author.mention} {result}")

    @commands.command()
    @commands.guild_only()
    async def slap(self, ctx, *, user: converters.Member = None):
        'Slap your senpai/waifu!'
        author = ctx.author
        slap = '**{} got slapped by {}**'
        slapself = '**{} slapped themself**'.format(author.mention)
        choices = [
            'https://i.imgur.com/EO8udG1.gif', 'https://i.imgur.com/lMmn1wy.gif', 'https://i.imgur.com/TuSUTg5.gif',
            'https://i.imgur.com/9Ql97mO.gif', 'https://i.imgur.com/Qkv0q8n.gif', 'https://i.imgur.com/VBGqeIU.gif',
            'https://i.imgur.com/uPZwGFQ.gif', 'https://i.imgur.com/Su0X9iF.gif', 'https://i.imgur.com/eNiOIMB.gif',
            'https://i.imgur.com/gsAGyoI.gif', 'https://i.imgur.com/sF1BQg2.gif', 'https://i.imgur.com/zTiJjev.gif'
        ]
        image = random.choice(choices)
        if user:
            if user == author:
                embed = discord.Embed(color=0)
                embed.set_image(url=image)
                await ctx.send(content=slapself, embed=embed)
            else:
                mention = user.mention
                embed = discord.Embed(color=user.color)
                embed.set_image(url=image)
                await ctx.send(content=slap.format(mention, author.mention), embed=embed)
        else:
            embed = discord.Embed(color=0)
            embed.set_image(url=image)
            await ctx.send(content=slapself, embed=embed)

    # @commands.command()
    # async def anime(self, ctx):
    #     """A random anime picture."""
    #     author = ctx.author
    #     guild = ctx.guild
    #     async with aiohttp.ClientSession() as session:
    #         async with session.get("https://api.computerfreaker.cf/v1/anime") as r:
    #             original = await r.json()
    #             pic = original["url"].replace("\\", '/')
    #             if not guild:
    #                 color = discord.Color.default()
    #             else:
    #                 color = author.color
    #             embed = discord.Embed(description = "[Link]({})".format(pic), color = color)
    #             embed.set_image(url = pic)
    #             await ctx.send(content=author.mention, embed = embed)

    @commands.command(aliases=["wifey", "animegrill"])
    @commands.bot_has_permissions(embed_links=True)
    async def waifu(self, ctx : commands.Context):
        async with aiohttp.ClientSession() as cs:
            try:
                async with cs.get("https://waifu.pics/sfw/waifu") as r:
                    embed = discord.Embed(
                        description="Here's your waifu ;)",
                        color = discord.Color.random()
                    )
                    embed.set_image((await r.json())['url'])
                    embed.set_footer(text=f"Image requested by {ctx.author}")
                    await ctx.send(embed=embed)
            except discord.HTTPException as e:
                await ctx.send(e)

    @commands.command()
    async def nicememe(self, ctx):
        "Nice meme."
        await ctx.send("http://niceme.me")

    @commands.command()
    async def choose(self, ctx, *, choices: str):
        "Choose a random thing from provided choices."
        list_of_results = choices.split()
        if len(list_of_results) > 1:
            final_result = random.choice(list_of_results)
            if ctx.guild:
                embed_color = ctx.guild.me.color
            else:
                embed_color = 16753920
            em = discord.Embed(description = f"`{final_result}`", color = embed_color)
            await ctx.send(ctx.author.mention, embed = em)
        else:
            await ctx.send("Not enough choices.")

def setup(bot):
    n = Fun(bot)
    bot.add_cog(n)
