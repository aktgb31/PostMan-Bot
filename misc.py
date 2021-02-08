import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import Bot, when_mentioned_or
from discord.ext.commands import CommandNotFound, CommandOnCooldown, MissingPermissions, MissingRequiredArgument, BadArgument, MissingAnyRole
from mail_helper import Mail

dest = ["ICPC_CORNER", "CPHUB"]

servers = {"ICPC_CORNER": 781093099601788954, "CPHUB": 744491356562653296}

channels = {"ICPC_CORNER": 781094812022865941, "CPHUB": 754069393142710422}


async def announce(Bot, ctx, subject: str, content: str):
    message = discord.Embed(
        title=subject, description="@everyone "+content, color=0x28A745)
    message.set_author(name=ctx.author.name)
    try:
        for d in dest:
            channel = Bot.get_channel(channels[d])
            await channel.send(embed=message)
        await ctx.send(f"{ctx.author.mention} Announced successfuly")
    except Exception as e:
        print(f'Something went wrong! {e}')
        await ctx.send(f"{ctx.author.mention} Something went wrong! {e}")
