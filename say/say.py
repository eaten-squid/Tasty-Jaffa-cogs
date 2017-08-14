import discord
from discord.ext import commands
from .utils import checks
from .utils.dataIO import dataIO
from .utils.chat_formatting import pagify, box
import logging

#The Tasty Jaffa
#Requested by Freud

class say:
    def __init__(self, bot):
        self.bot = bot
        self.say_perm = dataIO.load_json("data/admin/say.json")
        
    @commands.group(name="setsay", pass_context=True, no_pm=True, invoke_without_command=True)
    async def sayset(self, ctx):
        """The 'Say' command set

add - Adds a user to have the abillity to use the say command
say - The Bot repeats what was said
remove - Removes a user to have the abillity to use the say command"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_message(ctx.message.channel, "```Please use the say command with: \n add - Adds a user to have the abillity to use the say command \n remove - Removes a user to have the abillity to use the say command```")

    @sayset.command(name="list", pass_context=True)
    @checks.is_owner()
    async def say_list(self,ctx):
        perm_name = []
        for x in self.say_perm:
            perm_name.append(discord.utils.get(self.bot.get_all_members(), id=x).name)
                    
        msg = ("+ Permited\n"
               "{}\n\n"
               "".format(", ".join(sorted(perm_name))))

        for page in pagify(msg, [" "], shorten_by=16):
            await self.bot.say(box(page.lstrip(" "), lang="diff"))
        
    @sayset.command(name="add", pass_context=True, no_pm=True)
    @checks.is_owner()
    async def say_add (self, ctx, user: discord.Member):
        """Adds a [user] to have the abillity to use the say command"""
        self.say_perm.append(user.id)
        dataIO.save_json("data/admin/say.json", self.say_perm)
        await self.bot.say("Done!")
        await self.bot.delete_message(ctx.message)

    @sayset.command(name="remove", pass_context=True, no_pm=True)
    @checks.is_owner()
    async def say_remove (self, ctx, user: discord.Member):
        """Removes a [user] to have the abillity to use the say command"""
        try:
            self.say_perm.remove(user.id)
            dataIO.save_json("data/admin/say.json", self.say_perm)
            await self.bot.say("Done!")
            await self.bot.delete_message(ctx.message)
        except:
            self.bot.send_message(ctx.message.channel, "Are you sure that {} had the permision in the 1st place?".format(user.mention))

    @commands.command(name="say", pass_context=True)
    async def bot_say(self, ctx, *, text):
        """The bot says what yuo tell it to"""
        channel = ctx.message.channel
        auth = ctx.message.author
        if '@everyone' not in ctx.message.content and '@here' not in ctx.message.content:
            say=False
            if channel.permissions_for(ctx.message.server.me).manage_messages:         
                for u_id in self.say_perm:
                    if ctx.message.author.id == u_id:
                        say=True 
                if say:
                    await self.bot.delete_message(ctx.message)
                    await self.bot.send_message(channel, text)
                else: 
                    await self.bot.say("You need to be given this command") 
            else: 
                await self.bot.say("This command requires the **Manage Messages** permission.")
        else:
            await self.bot.send_message(ctx.message.channel, "Woh! {}, please don't do that".format(ctx.message.author.mention))


def setup(bot):
    n = say(bot)
    bot.add_cog(n)
