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
    
    @commands.group(autohelp=False, invoke_without_command=True, aliases=[currency[0]])
    async def blemflark(self, ctx):
        """
        BlemFlarks
        """
        if await self.loop.create_task(wubba.invalid_chanel(self, ctx)) or self.config.memeber(ctx.author).banned(): return

        cooldown_target = await self.config.guild(ctx.guild).cooldown_target()
        time_remaining = round(cooldown_target - time.time())

        if time_remaining > 0:
            await ctx.reply(f"Time remaining: {datetime.timedelta(seconds=time_remaining)}")
            return
        
        cooldown_target = (random.randint(1800, 3600) + time.time())
        time_remaining = round(cooldown_target - time.time())
        await self.config.guild(ctx.guild).cooldown_target.set(cooldown_target)

        await ctx.reply(file=discord.File("/home/redbot/.local/share/Red-DiscordBot/data/default/cogs/CogManager/cogs/gamba/nancy-kerrigan.gif"))
        user_currency_counter = await self.config.member(ctx.author).blemflarks()
        user_currency_counter += 5
        await self.config.member(ctx.author).blemflarks.set(user_currency_counter)

        self.loop.create_task(wubba.blemflarks(self, ctx, ctx.author))

    async def paybot(self, ctx, amount: int):
        bot_member = ctx.guild.get_member(self.bot.user.id)
        bot_blemflarks = await self.config.member(bot_member).blemflarks()
        await self.config.member(bot_member).blemflarks.set(bot_blemflarks + amount)
    
    @commands.command(currency + 's', usage="<optional: user> <optional: server ID>")
    async def blemflarks(self, ctx, user: Optional[discord.Member]):
        """
        Find out how many BlemFlarks you or someone else has
        """
        if ( await self.config.member(ctx.author).banned() or 
             await self.loop.create_task(wubba.invalid_chanel(self, ctx)) ): return
            
        if ctx.guild is None:
            await ctx.reply("Unavailable in DM's")
            return
        
        if user is None: user = ctx.author
        elif user is int: user = await self.bot.fetch_user(user)

        colors = [0xb00b69, 0xff0303, 0xffe70a, 0xc2ff0a, 0x0aff1f, 0x0affeb, 0x0a47ff, 0x7141b5, 0xff00f2]
        selectedColor = random.choice(colors)
        embed = discord.Embed(description=f"{user.name}'s BlemFlarks:", colour=selectedColor)

        user_currency_counter = await self.config.member(user).blemflarks()

        if user_currency_counter == 0:
            await ctx.reply(f"{user.name}, you're broke as shit dawg")
            return
        if user_currency_counter < 0:
            await ctx.reply(f"{user.name}, you fucking owe money dawg")
            return
        
        embed.add_field(name=currency + 's', value=user_currency_counter)
        await ctx.reply(embed=embed)

    @blemflark.command(aliases=["lb"])
    async def leaderboard(self, ctx):
        pass
        
    @blemflark.command()
    async def gringotts(self, ctx):
        """
        Get your daily interest by using Gringotts™ Bank
        """
        if ( await self.config.member(ctx.author).banned() or 
             await self.loop.create_task(wubba.invalid_chanel(self, ctx)) ): return
        
        interest_cooldown_target = await self.config.member(ctx.author).interest_cooldown_target()
        time_remaining = round(interest_cooldown_target - time.time())
        user_blemflarks = await self.config.member(ctx.author).blemflarks()
        

        if time_remaining > 0:
            await ctx.reply(f"Time remaining: {datetime.timedelta(seconds=time_remaining)}")
            return
        
        interest_cooldown_tarkget = (86400 + time.time())
        await self.config.member(ctx.author).interest_cooldown_target.set(interest_cooldown_tarkget)

        rate = random.randint(5,10)
        interest = int(user_blemflarks * rate / 100)
        user_blemflarks += interest if interest > 0 else 1

        await self.config.member(ctx.author).blemflarks.set(user_blemflarks)
        await ctx.reply(f"""You have received {interest} {currency} {'s' if interest > 1 else ''} from Gringotts™ Bank. Today's interest rate was {rate}%. 
                        Thank you for trusting Gringotts™ Bank.""")

    @wubba.command(usage="<User> <BlemFlark Amount>")
    async def setBlemFlarks(self, ctx, user: discord.Member, amount: int):
        """
        owner command to manually change blemflark amount
        """
        if ctx.guild is None:
            await ctx.send("Unavailable in DM's")
            return
        
        await self.config.memeber(user).blemflarks.set(amount)
        await ctx.reply("done.")

    @blemflark.command(usage="<User> <Amount>", aliases=['p', "transfer", "spreadit"], autohelp=False)
    async def pay(self, ctx, recipient: discord.Member, amount: int):
        """
        Pay a user with some of your hard earned blemflarks
        """
        try:
            if self.game_session_active[ctx.author.id]:
                await ctx.reply("Not during game bitch.")
                return

            if self.game_session_active[recipient.id]:
                await ctx.reply("He's in a game bitch.")
                return
        
        except:
            pass
        
        if await self.config.member(ctx.author).banned() or await self.loop.create_task(wubba.invalid_chanel(self, ctx)): return

        if recipient is int:
            recipient = await self.bot.fetch_user(recipient)
        
        user_blemflark_counter = await self.config.member(ctx.author).blemflarks()
        recipient_blemflark_counter = await self.config.member(recipient).blemflarks()

        if recipient.id == ctx.author.id:
            await ctx.reply("You can't pay yourself dingus.")
            return
        
        if amount <= 0:
            await ctx.reply("Amount must be greater than 0.")
            return
        
        if amount > user_blemflark_counter:
            await ctx.reply(f"You don't have enough {currency}s chief.")
            return
        
        self.game_session_active[ctx.author.id] = True

        warning_msg = await ctx.reply(f"""Are you sure you want to send {amount} {currency}{'s' if amount > 1 else ''} to {recipient.name}?
                                     {'9% tax will be deducted from this transaction.' if amount > 50 else ''}""")

        pred = ReactionPredicate.yes_or_no(warning_msg, ctx.author)
        start_adding_reactions(warning_msg, ReactionPredicate.YES_OR_NO_EMOJIS)

        try:
            await self.bot.wait_for('reaction_add', check=pred, timeout=30)
        except asyncio.TimeoutError:
            await warning_msg.edit(content="Transaction timed out.") 
            await warning_msg.clear_reactions()
            self.game_session_active[ctx.author.id] = False
            return

        if not  pred.result:
            await warning_msg.edit(content="Transaction cancelled.")
            self.game_session_active[ctx.author.id] = False
            return

        user_blemflark_counter -= amount
        tax = 0.09 if amount > 50 else 0 
        amount -= int(amount * tax)
        
        recipient_blemflark_counter += amount

        await self.config.memeber(ctx.author).blemflarks.set(user_blemflark_counter)
        await self.config.memeber(recipient).blemflarks.set(recipient_blemflark_counter)
        await ctx.reply(f"paid {recipient.name} {amount} {currency}{'s' if amount > 1 else ''}.")
        self.game_session_active[ctx.author.id] = False

