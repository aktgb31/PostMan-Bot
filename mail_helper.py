import os
import yagmail
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord.ext.commands import Bot, when_mentioned_or
from discord.ext.commands import CommandNotFound, CommandOnCooldown, MissingPermissions, MissingRequiredArgument, BadArgument, MissingAnyRole
from misc import announce
import traceback

MAIL_ID = os.getenv("MAIL_ID")
MAIL_PASS = os.getenv("MAIL_PASS")
yagmail.register(MAIL_ID, MAIL_PASS)


async def send_message(ctx, message):
    await ctx.send(embed=discord.Embed(description=message))


async def send_mail(temp, ctx):
    yag = yagmail.SMTP(MAIL_ID)
    try:
        yag.send(to=temp.to, cc=temp.cc, bcc=temp.bcc,
                 subject=temp.subject, contents=temp.content+temp.signature)
        await ctx.send(f"{ctx.author.mention} Mail sent successfuly")
        yag.close()
        return True

    except Exception as e:
        print(f'Something went wrong! {e}')
        await ctx.send(f"{ctx.author.mention} Something went wrong! {e}")
        yag.close()
        return False


class Mail(commands.Cog):

    to = []
    cc = []
    bcc = []
    subject = ""
    content = ""
    signature = '''<br><br><table width="351" cellspacing="0" cellpadding="0" border="0"> <tr> <td style="vertical-align: top; text-align:left;color:#000000;font-size:12px;font-family:helvetica, arial;; text-align:left"> <span><span style="margin-right:5px;color:#000000;font-size:15px;font-family:helvetica, arial">Happy Coding;</span> <br><span style="margin-right:5px;color:#000000;font-size:12px;font-family:helvetica, arial">CPHUB | NITC Codechef Campus Chapter</span></span> <br><br> <table cellpadding="0" cellpadding="0" border="0"><tr><td style="padding-right:5px"><a href="https://facebook.com/cphub.nitc/" style="display: inline-block;"><img width="40" height="40" src="https://s1g.s3.amazonaws.com/23f7b48395f8c4e25e64a2c22e9ae190.png" alt="Facebook" style="border:none;"></a></td><td style="padding-right:5px"><a href="https://instagram.com/cphub.nitc/" style="display: inline-block;"><img width="40" height="40" src="https://s1g.s3.amazonaws.com/4c616177ca37bea6338e6964ca830de5.png" alt="Instagram" style="border:none;"></a></td><td style="padding-right:5px"><a href="https://discord.gg/dpHV4sm6XF" style="display: inline-block;"><img width="40" height="40" src="https://s1g.s3.amazonaws.com/ba48639bd505cee2cc8b43ecb698f903.png" alt="Discord" style="border:none;"></a></td><td style="padding-right:5px"><a href="https://cphub-nitc.github.io/chapter/index.html" style="display: inline-block;"><img width="40" height="40" src="https://s1g.s3.amazonaws.com/8ab12118c0ee1056ed787deb1a208149.png" alt="General (Enter full link)" style="border:none;"></a></td></tr></table> </td> </tr> </table> <table width="351" cellspacing="0" cellpadding="0" border="0" style="margin-top:10px"> <tr> <td style="text-align:left;color:#aaaaaa;font-size:10px;font-family:helvetica, arial;"><p>Note: This mail is sent using PostMan BOT</p></td> </tr> </table> '''

    async def mail_to(self, client, ctx):
        try:
            await send_message(ctx, f"{ctx.author.mention}, Enter the reciever's mail adress")
            message = await client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author)
            self.to = str(message.content).split(' ')
            return True
        except asyncio.TimeoutError:
            await ctx.send(f"You took too long to type{ctx.author.mention}")
            return False

    async def mail_cc(self, client, ctx):
        try:
            await send_message(ctx, f"{ctx.author.mention}, Enter the CC reciever's adress and 'none' if empty")
            message = await client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author)
            if str(message.content) != 'none':
                self.cc = str(message.content).split(' ')
            return True
        except asyncio.TimeoutError:
            await ctx.send(f"You took too long to type{ctx.author.mention}")
            return False

    async def mail_bcc(self, client, ctx):
        try:
            await send_message(ctx, f"{ctx.author.mention}, Enter the BCC reciever's adress and 'none' if empty")
            message = await client.wait_for('message', timeout=30, check=lambda message: message.author == ctx.author)
            if str(message.content) != 'none':
                self.bcc = str(message.content).split(' ')
            return True
        except asyncio.TimeoutError:
            await ctx.send(f"You took too long to type{ctx.author.mention}")
            return False

    async def sub_content(self, mail_sub, mail_content):
        self.subject = mail_sub
        self.content = mail_content

    async def display(self, ctx):
        desc = "**Information regarding current mail** \n\n"
        desc += "**To **: "+" ".join(self.to)
        desc += "\n**CC **: "+" ".join(self.cc)
        desc += "\n**BCC **: "+" ".join(self.bcc)
        desc += "\n**Subject **: "+self.subject
        desc += "\n**Content **: "+self.content
        embed = discord.Embed(description=desc)
        await ctx.send(embed=embed)

    async def send(self, client, ctx):
        try:
            embed = discord.Embed(
                description=f"{ctx.author.mention} React with ✅ to send mail and ❌ to not")
            message = await ctx.send(embed=embed)
            await message.add_reaction("✅")
            await message.add_reaction("❌")
            reaction, user = await client.wait_for('reaction_add', timeout=30, check=lambda reaction, user: reaction.emoji in ["✅", "❌"] and user == ctx.author)
            if(reaction.emoji == "✅"):
                if await send_mail(self, ctx) == False:
                    return
                try:
                    embed = discord.Embed(
                        description=f"{ctx.author.mention} React with ✅ to announce and ❌ to not")
                    message = await ctx.send(embed=embed)
                    await message.add_reaction("✅")
                    await message.add_reaction("❌")
                    reaction, user = await client.wait_for('reaction_add', timeout=30, check=lambda reaction, user: reaction.emoji in ["✅", "❌"] and user == ctx.author)
                    if(reaction.emoji == "✅"):
                        await announce(client, ctx, self.subject, self.content)
                    else:
                        await send_message(ctx, f"{ctx.author.mention} Not Announced")
                except asyncio.TimeoutError:
                    await ctx.send(f"You took too long to react{ctx.author.mention}")
                    return
            else:
                await send_message(ctx, f"{ctx.author.mention} Mail Discarded")
                return
        except asyncio.TimeoutError:
            await ctx.send(f"You took too long to react{ctx.author.mention}")
            return
