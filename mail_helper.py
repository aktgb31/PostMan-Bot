import os
import yagmail
import asyncio
from dotenv import load_dotenv
import discord
from discord.ext import commands
from discord.ext.commands import Bot, when_mentioned_or
from discord.ext.commands import CommandNotFound, CommandOnCooldown, MissingPermissions, MissingRequiredArgument, BadArgument, MissingAnyRole


MAIL_ID = os.getenv("MAIL_ID")
MAIL_PASS = os.getenv("MAIL_PASS")
yagmail.register(MAIL_ID, MAIL_PASS)


class Mail(commands.Cog):
    def __init__(self, to, cc, bcc, subject, content):
        self.to = to
        self.cc = cc
        self.bcc = bcc
        self.subject = subject
        self.content = content
        self.signature = '''<br><br><table width="351" cellspacing="0" cellpadding="0" border="0"> <tr> <td style="vertical-align: top; text-align:left;color:#000000;font-size:12px;font-family:helvetica, arial;; text-align:left"> <span><span style="margin-right:5px;color:#000000;font-size:15px;font-family:helvetica, arial">Happy Coding;</span> <br><span style="margin-right:5px;color:#000000;font-size:12px;font-family:helvetica, arial">CPHUB | NITC Codechef Campus Chapter</span></span> <br><br> <table cellpadding="0" cellpadding="0" border="0"><tr><td style="padding-right:5px"><a href="https://facebook.com/cphub.nitc/" style="display: inline-block;"><img width="40" height="40" src="https://s1g.s3.amazonaws.com/23f7b48395f8c4e25e64a2c22e9ae190.png" alt="Facebook" style="border:none;"></a></td><td style="padding-right:5px"><a href="https://instagram.com/cphub.nitc/" style="display: inline-block;"><img width="40" height="40" src="https://s1g.s3.amazonaws.com/4c616177ca37bea6338e6964ca830de5.png" alt="Instagram" style="border:none;"></a></td><td style="padding-right:5px"><a href="https://discord.gg/dpHV4sm6XF" style="display: inline-block;"><img width="40" height="40" src="https://s1g.s3.amazonaws.com/ba48639bd505cee2cc8b43ecb698f903.png" alt="Discord" style="border:none;"></a></td><td style="padding-right:5px"><a href="https://cphub-nitc.github.io/chapter/index.html" style="display: inline-block;"><img width="40" height="40" src="https://s1g.s3.amazonaws.com/8ab12118c0ee1056ed787deb1a208149.png" alt="General (Enter full link)" style="border:none;"></a></td></tr></table> </td> </tr> </table> <table width="351" cellspacing="0" cellpadding="0" border="0" style="margin-top:10px"> <tr> <td style="text-align:left;color:#aaaaaa;font-size:10px;font-family:helvetica, arial;"><p>Note: This mail is sent using PostMan BOT</p></td> </tr> </table> '''

    def display(self, ctx):
        # print(self.to)
        # print(self.cc)
        # print(self.bcc)
        # print(self.subject)
        # print(self.content)
        desc = "Information regarding current mail \n"
        embed = discord.Embed(description=desc)
        embed.set_author(name=ctx.author)
        embed.add_field(name="To : ", value=self.to)
        embed.add_field(name="CC : ", value=self.cc)
        embed.add_field(name="BCC : ", value=self.bcc)
        embed.add_field(name="Subject : ", value=self.subject)
        embed.add_field(name="Content : ", value=self.content)
        return embed

    async def send_mail(self, ctx):
        yag = yagmail.SMTP(MAIL_ID)
        yag.set_logging(yagmail.logging.DEBUG, 'log.log')
        try:
            yag.send(to=self.to, cc=self.cc, bcc=self.bcc,
                     subject=self.subject, contents=self.content+self.signature)
            await ctx.send(f"{ctx.author.mention} Mail sent successfuly")
        except Exception as e:
            print(f'Something went wrong! {e}')
            await ctx.send(f"{ctx.author.mention} Something went wrong! {e}")
        yag.close()
