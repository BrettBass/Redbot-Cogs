#this file manages all the games and currency for the discord server
from redbot.core import commands, Config
from redbot.core import commands, Config
import discord
import random
from typing import Optional
import asyncio
import time, datetime
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.predicates import MessagePredicate, ReactionPredicate
from .quackjack import quackjack
#from .blackjack.blackjack import *
#from .blackjack.user import *
#from .blackjack.Card import *

currency = "Blemflarck"

class wubba(commands.Cog):
    """
    wubba lubba dub dub Casino is a place for pure degeneracy
    """
    __author__ = ["Brett Bass"]
    __version__ = ["1.0.0"]

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=361823859125642)
        self.config.register_member(Blamflarcks = 10, interestCooldown = 0, banned = False, forceRegistration=True)
        self.config.register_guild(cooldown = 0, gambaChannels=[], forceRegistration=True)
        self.loop = bot.loop
        self.activeGames = {}
    
    @commands.group(alias=["wc"])
    async def wubba(self, ctx):
        pass

    @wubba.command(usage="<User>", aliases=["ban"])
    async def blacklist(self, ctx, user:discord.Member):
        """
        Blacklist a user from the wubba lubba dub dub Casino
        """
        await self.config.member(user).banned.set(True)
        await ctx.reply(f"{user.name} has been blacklisted from the wubba lubba dub dub Casino")
    
    @wubba.command(usage="<User>", aliases=["unban"])
    async def whitelist(self, ctx, user:discord.Member):
        """
        Whitelist a user from the wubba lubba dub dub Casino
        """
        await self.config.member(user).banned.set(False)
        await ctx.reply(f"{user.name} can now enter/gamble at wubba lubba dub dub Casino without being shot")
    
    @wubba.group()
    async def gambaChannels(self, ctx):
        pass

    @gambaChannels.command(usage="<text channels (space seperated)>")
    async def add(self, ctx, *channels:discord.TextChannel):
        """
        Add gamba channels
        """
        gambaChannels = await self.config.guild(ctx.guild).gambaChannels()
        channels_added = ""
        
        for channel in channels:
            gambaChannels.append(channel.name)
            channels_added += f"{channel.name} "
        
        await self.config.guild(ctx.guild).gambaChannels.set(gambaChannels)
        await ctx.reply(f"Added {channels_added} to gamba channel list")
    
    @gambaChannels.command(usage="<text channels (space seperated)>")
    async def remove(self, ctx, *channels:discord.TextChannel):
        """
        Remove gamba channels
        """
        gambaChannels = await self.config.guild(ctx.guild).gambaChannels()
        channels_removed = ""
        not_found = ""
        
        for channel in channels:
            try:
                gambaChannels.remove(channel.name)
                channels_removed += f"{channel.name} "
            except:
                not_found += f"{channel.name} "
        
        await self.config.guild(ctx.guild).gambaChannels.set(gambaChannels)
        await ctx.reply(f"Removed {channels_removed} from gamba channels")
        
        if not_found != "":
            await ctx.send(f"channel{'s' if len(not_found) > 1 else ''} {not_found} not in gamba channel")
    

    @gambaChannels.command()
    async def list(self, ctx):
        """
        Display Gamba Channels
        """
        gambaChannels = await self.config.guild(ctx.guild).gambaChannels()
        channels_list = ""
        
        for channel in gambaChannels:
            channels_list += f"{channel} "
        
        await ctx.reply(f"Gamba Channels: {channels_list}")
    
    async def invalid_chanel(self, ctx):
        if ctx.channel.name not in await self.config.guild(ctx.guild).gambaChannels():
            await ctx.message.delete()
            await ctx.send("<:cuttingdownoneggplant:893273818364276736>")
            return True
        else:
            return False
    
    def reset_check(author):
        return lambda message: (message.author == author and 
                                ( message.content.lower() == "confirm" or
                                  message.content.lower() == "cancel" ))
    
    # def reset_check(author):
    #     def innerCheck(message):
    #         if message.author != author:
    #             return False
    #         if message.content.lower() == "confirm" or message.content.lower() == "cancel":
    #             return True

    #     return innerCheck

    @wubba.command()
    async def resetAll(self, ctx):
        """
        Resets all users BlemFlarks to 10
        """
        msg = await ctx.send(f"Are you sure you want to reset ***__all__*** users {currency}s? [Confirm/Cancel]")

        try:
            response = await self.bot.wait_for('message', check=wubba.reset_check(ctx.author), timeout=60)
        except asyncio.TimeoutError:
            await msg.edit(content="Timed out")
        
        if response.content.lower() == "confirm":
            await self.config.clear_all_members()
            await self.config.guild(ctx.guild).coolDown.set(0)
            await ctx.send(f"All users {currency}s have been reset")
        else:
            await msg.edit(content="Cancelled")
            return
    
    
        
