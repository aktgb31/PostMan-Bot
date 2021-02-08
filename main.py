import os
import yagmail
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord.ext.commands import Bot, when_mentioned_or
from discord.ext.commands import CommandNotFound, CommandOnCooldown, MissingPermissions, MissingRequiredArgument, BadArgument, MissingAnyRole
from mail_helper import Mail
from misc import announce

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


client = commands.Bot(command_prefix=commands.when_mentioned_or(';mail '),
                      description='A bot used to send mails')

game = discord.Game("Shahraaz ORZ")
client.remove_command('help')


async def send_message(ctx, message):
    await ctx.send(embed=discord.Embed(description=message))


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
@ client.command(brief='Start writing a fresh mail')
@ commands.has_role('Mailer')
async def start(ctx, arg):

    try:
        await send_message(ctx, f"{ctx.author.mention}, Enter the reciever's mail adress")
        message = await client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author)
        mail_to = str(message.content).split(' ')
    except asyncio.TimeoutError:
        await ctx.send(f"You took too long to type{ctx.author.mention}")
        return

    try:
        await send_message(ctx, f"{ctx.author.mention}, Enter the CC reciever's adress and 'none' if empty")
        message = await client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author)
        mail_cc = []
        if str(message.content) != 'none':
            mail_cc = str(message.content).split(' ')
    except asyncio.TimeoutError:
        await ctx.send(f"You took too long to type{ctx.author.mention}")
        return

    try:
        await send_message(ctx, f"{ctx.author.mention}, Enter the BCC reciever's adress and 'none' if empty")
        message = await client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author)
        mail_bcc = []
        if str(message.content) != 'none':
            mail_bcc = str(message.content).split(' ')
    except asyncio.TimeoutError:
        await ctx.send(f"You took too long to type{ctx.author.mention}")
        return

    mail_subject = ""
    mail_content = ""

    if(arg.lower() == 'mirror'):
        try:
            await send_message(ctx, f"{ctx.author.mention}, Enter Mirror number")
            message = await client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author)
            MIRROR_NUMER = str(message.content)
        except asyncio.TimeoutError:
            await ctx.send(f"You took too long to type{ctx.author.mention}")
            return

        try:
            await send_message(ctx, f"{ctx.author.mention}, Enter Link")
            message = await client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author)
            MIRROR_LINK = str(message.content)
        except asyncio.TimeoutError:
            await ctx.send(f"You took too long to type{ctx.author.mention}")
            return

        try:
            await send_message(ctx, f"{ctx.author.mention}, Enter Date")
            message = await client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author)
            MIRROR_DATE = str(message.content)
        except asyncio.TimeoutError:
            await ctx.send(f"You took too long to type{ctx.author.mention}")
            return

        try:
            await send_message(ctx, f"{ctx.author.mention}, Enter Time")
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

    elif(arg.lower() == 'bc'):
        try:
            await send_message(ctx, f"{ctx.author.mention}, Enter CONTEST number")
            message = await client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author)
            CONTEST_NUMER = str(message.content)
        except asyncio.TimeoutError:
            await ctx.send(f"You took too long to type{ctx.author.mention}")
            return

        try:
            await send_message(ctx, f"{ctx.author.mention}, Enter Link")
            message = await client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author)
            CONTEST_LINK = str(message.content)
        except asyncio.TimeoutError:
            await ctx.send(f"You took too long to type{ctx.author.mention}")
            return

        try:
            await send_message(ctx, f"{ctx.author.mention}, Enter Date")
            message = await client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author)
            CONTEST_DATE = str(message.contentv)
        except asyncio.TimeoutError:
            await ctx.send(f"You took too long to type{ctx.author.mention}")
            return

        try:
            await send_message(ctx, f"{ctx.author.mention}, Enter Time")
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

    else:
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

    temp_mail = Mail(mail_to, mail_cc, mail_bcc,
                     mail_subject, mail_content)
    await ctx.send(embed=temp_mail.display(ctx))

    try:
        await send_message(ctx, f"{ctx.author.mention}, Enter 'DISCARD' to discard the mail or 'CONFIRM' to send it ")
        message = await client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author)
        confirm = str(message.content)
        if confirm == 'DISCARD':
            await send_message(ctx, f"{ctx.author.mention} Mail Discarded")
        if confirm == 'CONFIRM':
            await temp_mail.send_mail(ctx)
    except asyncio.TimeoutError:
        await ctx.send(f"You took too long to type{ctx.author.mention}")
        return

    try:
        await send_message(ctx, f"{ctx.author.mention}, Do you want to announce it in Announcements (yes/no) ? ")
        message = await client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author)
        confirm = str(message.content)
        if confirm.lower() == 'no':
            await send_message(ctx, f"{ctx.author.mention} Not Announced")
        if confirm.lower() == 'yes':
            await announce(client, ctx, mail_subject, mail_content)
    except asyncio.TimeoutError:
        await ctx.send(f"Not announced {ctx.author.mention}")
        return
    del temp_mail

# Announce Something


@client.command(brief='Send in Announcements')  # Announce Something
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

    await announce(client, ctx, subject, content)


# help command
@client.command()
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed()
    embed.set_author(name='Help')
    embed.add_field(name=';mail', value="Bot prefix")
    embed.add_field(name='ping', value="Ping the bot")
    embed.add_field(name='start', value="Start writing fresh new mail")
    embed.add_field(name='start mirror',
                    value="Start writing mail for ICPC mirror")
    embed.add_field(name='start bc',
                    value="Start writing mail for Beginner Contest")

    await ctx.send(author, embed=embed)

# Error handling stuff


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

    else:
        print(f"{ctx.author.id} {ctx.guild.id} {ctx.message.content}")
        print(error)
        await ctx.send(error)


if not TOKEN:
    print('Bot token not found!')
else:
    client.run(TOKEN)
