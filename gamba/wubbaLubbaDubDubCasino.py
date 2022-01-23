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
    
