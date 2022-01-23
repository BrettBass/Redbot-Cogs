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

class WubbaLubbaDubDub(commands.Cog):
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
    
    @commands.group(alias=["wubba"])
    async def wubbalubbadub(self, ctx):
        pass

    
