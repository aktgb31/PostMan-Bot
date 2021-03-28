import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import Bot, when_mentioned_or
from discord.ext.commands import CommandNotFound, CommandOnCooldown, MissingPermissions, MissingRequiredArgument, BadArgument, MissingAnyRole

SERVERS = {"1": "ICPC_CORNER_GENERAL",
           "2": "ICPC_CORNER_EVENT", "3": "CPHUB"}
CHANNELS = {"ICPC_CORNER_GENERAL": 781094812022865941, "ICPC_CORNER_EVENT": 789411627190583326,
            "CPHUB": 754069393142710422}


async def send_message(ctx, message):
    await ctx.send(embed=discord.Embed(description=message))


async def announce(Bot, ctx, subject: str, content: str):
    mess = discord.Embed(description=content, color=0x28A745)
    mess.set_author(name=subject)
    mess.set_footer(text="-CP Hub, Nitc")
    await ctx.send(embed=mess)

    try:
        desc = f"{ctx.author.mention} \n\n**List of Announcement Channels Set** \n\n"
        for id in SERVERS:
            desc += f"{id} : {SERVERS[id]}\n"
        desc += "\n**Enter space separated indexes of channels to send announcement**\n"

        embed = discord.Embed(description=desc)
        await ctx.send(embed=embed)
        message = await Bot.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author)
        message = str(message.content).split(' ')

        channels = []
        for id in message:
            if id not in SERVERS:
                raise Exception('Invalid Values')
            channel = Bot.get_channel(CHANNELS[SERVERS[id]])
            channels.append(channel)

        for channel in channels:
            await channel.send(embed=mess)

    except Exception as e:
        print(f'Something went wrong! {e}')
        await ctx.send(f"{ctx.author.mention} Something went wrong! {e}")
        return

    await ctx.send(f"{ctx.author.mention} Announced successfuly.")
