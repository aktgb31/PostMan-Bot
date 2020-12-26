import os
import yagmail
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord.ext.commands import Bot, when_mentioned_or
from discord.ext.commands import CommandNotFound, CommandOnCooldown, MissingPermissions, MissingRequiredArgument, BadArgument, MissingAnyRole
from mail_helper import Mail

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


client = commands.Bot(command_prefix=when_mentioned_or(';mail '),
                      description='A bot used to send mails')


async def send_message(ctx, message):
    await ctx.send(embed=discord.Embed(description=message))


@ client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@ client.command(name='start', help='Start writing the mail')
@ commands.has_role('Mailer')
async def input(ctx):
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

    print(mail_to)
    print(mail_cc)
    print(mail_bcc)
    print(mail_subject)
    print(mail_content)
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
    del temp_mail

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
