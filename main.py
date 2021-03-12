import os
import yagmail
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord.ext.commands import Bot, when_mentioned_or
from discord.ext.commands import CommandNotFound, CommandOnCooldown, MissingPermissions, MissingRequiredArgument, BadArgument, MissingAnyRole, CheckFailure
from mail_helper import Mail
from misc import announce

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CPHUB = 744491356562653296
MAILER = 'Mailer'

client = commands.Bot(command_prefix=commands.when_mentioned_or(';mail '),
                      description='A bot used to send mails')

game = discord.Game("Listening to CPHUB Mails")


async def send_message(ctx, message):
    await ctx.send(embed=discord.Embed(description=message))


def check_if_it_is_us(ctx):
    return ctx.guild.id == CPHUB


@ client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    print('Logged in as '+client.user.name+' (ID:'+str(client.user.id) +
          ') | Connected to '+str(len(client.guilds))+' servers')
    print('--------')
    await client.change_presence(status=discord.Status.online, activity=game)


@client.command(brief='Measure delays')  # ping command
async def ping(ctx):
    await ctx.send(':ping_pong: Pong! ~' + str(round(client.latency * 1000, 2)) + " ms")


# Start sending the mail
@ client.command(brief='Start writing a fresh mail',)
@ commands.check(check_if_it_is_us)
@ commands.has_role(MAILER)
async def start(ctx):

    temp_mail = Mail()
    if await temp_mail.mail_to(client, ctx) == False:
        return

    if await temp_mail.mail_cc(client, ctx) == False:
        return

    if await temp_mail.mail_bcc(client, ctx) == False:
        return

    try:
        await send_message(ctx, f"{ctx.author.mention}, Enter the Subject")
        message = await client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author)
        mail_subject = str(message.content)
    except asyncio.TimeoutError:
        await ctx.send(f"You took too long to type{ctx.author.mention}")
        return

    try:
        await send_message(ctx, f"{ctx.author.mention}, Enter the Content")
        message = await client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author)
        mail_content = str(message.content)
    except asyncio.TimeoutError:
        await ctx.send(f"You took too long to type{ctx.author.mention}")
        return

    await temp_mail.sub_content(mail_subject, mail_content)
    if await temp_mail.footer(client, ctx) == False:
        return
    await temp_mail.display(ctx)
    await temp_mail.send(client, ctx)
    del temp_mail


@ client.command(brief='Write mail for Mirror')
@ commands.check(check_if_it_is_us)
@ commands.has_role(MAILER)
async def mirror(ctx):
    temp_mail = Mail()
    if await temp_mail.mail_to(client, ctx) == False:
        return

    if await temp_mail.mail_cc(client, ctx) == False:
        return

    if await temp_mail.mail_bcc(client, ctx) == False:
        return

    try:
        await send_message(ctx, f"{ctx.author.mention}, Enter Mirror number")
        message = await client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author)
        MIRROR_NUMER = str(message.content)
    except asyncio.TimeoutError:
        await ctx.send(f"You took too long to type{ctx.author.mention}")
        return
    try:
        await send_message(ctx, f"{ctx.author.mention}, Enter Contest Link")
        message = await client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author)
        MIRROR_LINK = str(message.content)
    except asyncio.TimeoutError:
        await ctx.send(f"You took too long to type{ctx.author.mention}")
        return
    try:
        await send_message(ctx, f"{ctx.author.mention}, Enter Contest Date")
        message = await client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author)
        MIRROR_DATE = str(message.content)
    except asyncio.TimeoutError:
        await ctx.send(f"You took too long to type{ctx.author.mention}")
        return
    try:
        await send_message(ctx, f"{ctx.author.mention}, Enter Contest Time")
        message = await client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author)
        MIRROR_TIME = str(message.content)
    except asyncio.TimeoutError:
        await ctx.send(f"You took too long to type{ctx.author.mention}")
        return
    mail_subject = "Invitation to NITC ICPC Mirror #"+MIRROR_NUMER
    mail_content = '''Greetings,

    We are glad to invite you to take part in NITC ICPC Mirror #'''+MIRROR_NUMER+'''This contest will be held on Virtual Judge. You will be given 8-12 previous ICPC Regionals problems and 5 hours to solve them. You guys can participate in a team of 3 members wherein you can discuss the strategy, logic, code, etc and submit your solutions.
    
    Contest link: ''' + MIRROR_LINK + '''
    Date: '''+MIRROR_DATE+'''
    Start time: '''+MIRROR_TIME + ''' (IST)
    Contest Duration: 5:00 hours
    
    Editorials will be sent to your mail after the contest.
    All The Best.'''

    await temp_mail.sub_content(mail_subject, mail_content)
    if await temp_mail.footer(client, ctx) == False:
        return
    await temp_mail.display(ctx)
    await temp_mail.send(client, ctx)


@ client.command(brief='Write mail for Beginner Contest')
@ commands.check(check_if_it_is_us)
@ commands.has_role(MAILER)
async def bc(ctx):

    temp_mail = Mail()
    if await temp_mail.mail_to(client, ctx) == False:
        return

    if await temp_mail.mail_cc(client, ctx) == False:
        return

    if await temp_mail.mail_bcc(client, ctx) == False:
        return

    try:
        await send_message(ctx, f"{ctx.author.mention}, Enter Contest number")
        message = await client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author)
        CONTEST_NUMER = str(message.content)
    except asyncio.TimeoutError:
        await ctx.send(f"You took too long to type{ctx.author.mention}")
        return
    try:
        await send_message(ctx, f"{ctx.author.mention}, Enter Contest Link")
        message = await client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author)
        CONTEST_LINK = str(message.content)
    except asyncio.TimeoutError:
        await ctx.send(f"You took too long to type{ctx.author.mention}")
        return
    try:
        await send_message(ctx, f"{ctx.author.mention}, Enter Contest Date")
        message = await client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author)
        CONTEST_DATE = str(message.content)
    except asyncio.TimeoutError:
        await ctx.send(f"You took too long to type{ctx.author.mention}")
        return
    try:
        await send_message(ctx, f"{ctx.author.mention}, Enter Contest Time")
        message = await client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author)
        CONTEST_TIME = str(message.content)
    except asyncio.TimeoutError:
        await ctx.send(f"You took too long to type{ctx.author.mention}")
        return
    mail_subject = "Invitation to CPHUB Beginner Contest #"+CONTEST_NUMER
    mail_content = '''Greetings,
    
    We are glad to invite you to take part in CP Hub Beginner Contest #'''+CONTEST_NUMER+'''. This contest will be held on Virtual Judge. You will be given 6-8 problems and 2 hours to solve them. You guys can participate in a team of 3 members wherein you can discuss the strategy, logic, code, etc and submit your solutions.
    
    Contest link: ''' + CONTEST_LINK + '''
    Date: '''+CONTEST_DATE+'''
    Start time: '''+CONTEST_TIME + ''' (IST)
    Contest Duration: 2 hours

    Editorials will be sent to your mail after the contest.
    All The Best.'''

    await temp_mail.sub_content(mail_subject, mail_content)
    if await temp_mail.footer(client, ctx) == False:
        return
    await temp_mail.display(ctx)
    await temp_mail.send(client, ctx)

 # Announce Something


@client.command(brief='Send Announcements')  # Announce Something
@ commands.check(check_if_it_is_us)
@ commands.has_role(MAILER)
async def ann(ctx):
    try:
        await send_message(ctx, f"{ctx.author.mention}, Enter the Subject")
        message = await client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author)
        subject = str(message.content)
    except asyncio.TimeoutError:
        await ctx.send(f"You took too long to type{ctx.author.mention}")
        return
    try:
        await send_message(ctx, f"{ctx.author.mention}, Enter the Content")
        message = await client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author)
        content = str(message.content)
    except asyncio.TimeoutError:
        await ctx.send(f"You took too long to type{ctx.author.mention}")
        return
    try:
        embed = discord.Embed(
            description=f"{ctx.author.mention} React with ✅ to announce and ❌ to not")
        message = await ctx.send(embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        reaction, user = await client.wait_for('reaction_add', timeout=30, check=lambda reaction, user: reaction.emoji in ["✅", "❌"] and user == ctx.author)
        if(reaction.emoji == "✅"):
            await announce(client, ctx, subject, content)
        if(reaction.emoji == "❌"):
            await send_message(ctx, f"{ctx.author.mention} Not Announced")

    except asyncio.TimeoutError:
        await ctx.send(f"You took too long to type{ctx.author.mention}")
        return


@ client.event
async def on_command_error(ctx: commands.Context, error: Exception):
    if isinstance(error, CommandNotFound):
        pass

    elif isinstance(error, CommandOnCooldown):
        pass

    elif isinstance(error, BadArgument) or isinstance(error, MissingRequiredArgument):
        command = ctx.command
        usage = f".{str(command)} "
        params = []
        for key, value in command.params.items():
            if key not in ['self', 'ctx']:
                params.append(f"[{key}]" if "NoneType" in str(
                    value) else f"<{key}>")
        usage += ' '.join(params)
        await ctx.send(f"Usage: **{usage}**")

    elif isinstance(error, MissingPermissions) or isinstance(error, MissingAnyRole):
        await ctx.send(f"{str(error)}")

    elif isinstance(error, CheckFailure):
        print(error)
        await ctx.send(f"{ctx.author.mention} This command can be used only in CPHUB server")

    else:
        print(f"{ctx.author.id} {ctx.guild.id} {ctx.message.content}")
        print(error)
        await ctx.send(error)


if not TOKEN:
    print('Bot token not found!')
else:
    client.run(TOKEN)
