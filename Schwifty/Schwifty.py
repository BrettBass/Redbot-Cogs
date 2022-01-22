from redbot.core import commands
import discord
import asyncio
import youtube_dl
from typing import Optional
import urllib.request
import re
import time
import json
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.predicates import MessagePredicate, ReactionPredicate

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
	'format': 'bestaudio/best',
	'outtmpl': '%(title)s.%(ext)s',
	'restrictfilenames': True,
	'noplaylist': True,
	'nocheckcertificate': True,
	'ignoreerrors': True,
	'logtostderr': False,
	'quiet': True,
	'no_warnings': True,
	'default_search': 'auto',
	'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
	'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
	def __init__(self, source, *, data, volume=0.5):
		super().__init__(source, volume)

		self.data = data
		self.title = data.get('title')
		self.url = data.get('url')

	@classmethod
	async def from_url(cls, url, *, loop=None, stream=True):
		loop = loop or asyncio.get_event_loop()
		data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

		if 'entries' in data:
			# take first item from a playlist
			data = data['entries'][0]

		filename = data['url'] if stream else ytdl.prepare_filename(data)
		return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Schwifty(commands.Cog):    

	def __init__(self, bot):
		self.bot = bot
		self.loop = bot.loop

		self.youtube_base_url = "https://youtube.com/"
		self.youtube_shorthand_url = "https://youtu.be"
		self.youtube_search_url = "results?search_query="
		self.youtube_video_url = "watch?v="
		
		self.name_queue = {}
		self.link_queue = {}

	@commands.group()
	async def Schwifty(self, ctx):
		pass

	@Schwifty.command()
	async def join(self, ctx, voice_channel: Optional[discord.VoiceChannel]):
		"""
		Join a voice channel
		"""
		if voice_channel is None:
			try:
				voice_channel = ctx.author.voice.channel
			except:
				await ctx.reply("Please join a voice channel first.")
				return False
		if ctx.guild.voice_client is not None:
			await ctx.guild.voice_client.move_to(voice_channel)
		else:
			await voice_channel.connect()
		
	async def parse_titles(self, search_string):
		search_string = search_string.replace(" ", "%20")

		html = urllib.request.urlopen(f"{self.youtube_base_url}{self.youtube_search_url}{search_string}")
		video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
		return f"{self.youtube_base_url}{self.youtube_video_url}{video_ids[0]}"

	async def get_title(self, link):
		params = {"format": "json", "url": link}
		url = f"{self.youtube_base_url}oembed"
		query_string = urllib.parse.urlencode(params)
		url = url + "?" + query_string
		with urllib.request.urlopen(url) as response:
			response_text = response.read()
			data = json.loads(response_text.decode())
			return data["title"]

	def filter_input(self, target_videos):
		bad_chars = "{}[]+()^&$*<>\"'"
		for char in bad_chars:
			target_videos = target_videos.replace(char,"")
		
		if len(target_videos) == 0:
			return None
		target_videos = target_videos.split(", ")
		for item in target_videos:
			if item == " ":
				target_videos = target_videos.remove(item)
			elif "http" in item and self.youtube_base_url not in item:
				target_videos = target_videos.remove(item)
		return target_videos
	
	@Schwifty.command(name="play")
	async def parse_arguments(self, ctx, *, target_videos:Optional[str]):
		"""
		Play audio by title or youtube link. comma seperate multiple entries.
		You can queue next songs with this command as well.
		"""
		if target_videos is None:
			if ctx.guild.voice_client is not None:
				if ctx.guild.voice_client.is_paused():
					ctx.guild.voice_client.resume()
					return
			else:
				await ctx.reply(f"Please provide the name of the song or a youtube link\nYou can input multiple songs seperated by a comma")
				return
		async with ctx.typing():
			if ctx.guild.id not in self.link_queue:
				self.link_queue[ctx.guild.id] = []
			if ctx.guild.id not in self.name_queue:
				self.name_queue[ctx.guild.id] = []
			target_videos = Schwifty.filter_input(self, target_videos)
		if target_videos is None:
			await ctx.reply("Invalid input")
			return

		for target_video in target_videos:
			if self.youtube_base_url not in target_video:
				link = await self.loop.create_task(Schwifty.parse_titles(self, target_video))
				title = await self.loop.create_task(Schwifty.get_title(self, link))
				self.link_queue[ctx.guild.id].append(link)
				self.name_queue[ctx.guild.id].append(title)
			elif self.youtube_base_url in target_video:
				title = await self.loop.create_task(Schwifty.get_title(self, target_video))
				self.link_queue[ctx.guild.id].append(target_video)
				self.name_queue[ctx.guild.id].append(title)

		if ctx.guild.voice_client is None:
			await self.loop.create_task(Schwifty.join(self, ctx, None))
			if ctx.guild.voice_client is None:
				return
		if len(self.link_queue[ctx.guild.id]) > 1:
			self.loop.create_task(Schwifty.playlist(self,ctx))
		if not ctx.guild.voice_client.is_playing():
			self.loop.create_task(Schwifty.player(self, ctx))
			
	@Schwifty.command()
	async def skip(self, ctx):
		"""
		Skip current song
		"""
		ctx.guild.voice_client.stop()

	async def player(self, ctx):
		await ctx.send(f"Now playing: `{self.name_queue[ctx.guild.id][0]}`")
		ctx.guild.voice_client.play(await YTDLSource.from_url(self.link_queue[ctx.guild.id][0]))

		try:
			while ctx.guild.voice_client.is_playing() or ctx.guild.voice_client.is_paused():
				await asyncio.sleep(.1)
		except AttributeError:
			pass
		Schwifty.iterate_queue(self, ctx)
		try:
			if len(self.link_queue[ctx.guild.id]) == 0:
				await ctx.send("Playlist finished. 👋")
				self.loop.create_task(Schwifty.stop(self, ctx))
		except TypeError:
			await ctx.send("Playlist finished. 👋")
			self.loop.create_task(Schwifty.stop(self, ctx))
		else:
			self.loop.create_task(Schwifty.player(self, ctx))


	@Schwifty.command()
	async def pause(self, ctx):
		"""
		Pause ongoing audio
		"""

		if ctx.guild.voice_client is None:
			await ctx.reply("I'm not playing anything right now")
			return
		if not ctx.guild.voice_client.is_playing():
			await ctx.reply("I'm not playing anything right now.")
			return
		ctx.guild.voice_client.pause()
		await ctx.message.add_reaction("⏸️")

	@Schwifty.command()
	async def resume(self, ctx):
		"""
		Resume paused audio
		"""
		if ctx.guild.voice_client is None:
			await ctx.reply("I'm not playing anything right now.")
			return
		if ctx.guild.voice_client.is_paused():
			ctx.guild.voice_client.resume()
			await ctx.message.add_reaction("▶️")

	@Schwifty.command(aliases=["leave"])
	async def stop(self, ctx):
		"""
		Stop, leave, and clear queue.
		"""
		if ctx.guild.voice_client is None:
			await ctx.reply("I'm not playing anything right now.")
			return
		await self.loop.create_task(Schwifty.clear_queue(self, ctx))
		await ctx.guild.voice_client.disconnect()
		try:
			ctx.guild.voice_client.stop()
		except AttributeError:
			pass
		await ctx.message.add_reaction("👋")
		
	@Schwifty.command(aliases=["queue", "list"])
	async def playlist(self, ctx):
		"""
		Show playlist.
		"""
		
		if ctx.guild.id not in self.link_queue or len(self.link_queue[ctx.guild.id]) == 0:
			await ctx.reply("Playlist is empty.")
			return
		color = 0xb00b69
		embed = discord.Embed(description="Playlist:", colour=color)
		embed.set_thumbnail(url="https://cdn.betterttv.net/emote/5f1abd75fe85fb4472d132b4/2x.gif")
		embed.set_footer(text="Use Schwifty play to add a new song to the playlist")
		index = 1
		for item in self.name_queue[ctx.guild.id]:
			embed.add_field(name = index, value=item, inline=False)
			index += 1
		await ctx.send(embed=embed)

	@Schwifty.command(name="clear")
	async def user_clear(self,ctx):
		"""
		Clear the playlist
		"""
		await ctx.reply(await self.loop.create_task(Schwifty.clear_queue(self, ctx)))

	async def clear_queue(self, ctx):
		try:
			self.name_queue.pop(ctx.guild.id)
			self.link_queue.pop(ctx.guild.id)
		except KeyError:
			return("Playlist is already empty.")
		return("Playlist cleared.")
		ctx.guild.voice_client.stop()

	@Schwifty.command()
	async def remove(self, ctx, *, song_to_remove):
		"""
		Remove song from queue by number, name, or link.
		For a range use a dash
		"""
		if ctx.guild.id not in self.link_queue:
			await ctx.reply("There is nothing queued")
			return

		if self.youtube_base_url in song_to_remove:
			song_to_remove = await self.loop.create_task(Schwifty.get_title(self, song_to_remove))

		if song_to_remove == "1":
			self.loop.create_task(Schwifty.skip(self,ctx))
			return
		if "-" in song_to_remove:
			if song_to_remove[0].isnumeric() and song_to_remove[2].isnumeric():
				start_range = int(song_to_remove[0]) - 1
				end_range = int(song_to_remove[2])
			try:
				del self.name_queue[ctx.guild.id][start_range:end_range]
				del self.link_queue[ctx.guild.id][start_range:end_range]
				await ctx.reply(f"Removed songs {start_range + 1}-{end_range}")
				return
			except IndexError:
				await ctx.send("Invalid range")
				return
		if song_to_remove.isnumeric():
			song_to_remove = int(song_to_remove)
			try:
				deleted = self.name_queue[ctx.guild.id][song_to_remove - 1]
				del self.link_queue[ctx.guild.id][song_to_remove - 1]
				del self.name_queue[ctx.guild.id][song_to_remove - 1]
				await ctx.reply(f"Removed `{deleted}` from playlist")
			except IndexError:
				await ctx.reply(f"song #{song_to_remove - 1} not found!")
				return
		else:
			index = None
			for item in self.name_queue[ctx.guild.id]:
				if song_to_remove.lower() in item.lower():
					index = self.name_queue[ctx.guild.id].index(item)
					resolved_name = item
			if index is None:
				await ctx.reply(f"Could not find `{song_to_remove}`")
			else:	
				del self.link_queue[ctx.guild.id][index]
				del self.name_queue[ctx.guild.id][index]
				await ctx.reply(f"`{resolved_name}` removed from playlist")
	
	def iterate_queue(self, ctx):
		try:
			del self.link_queue[ctx.guild.id][0]
			del self.name_queue[ctx.guild.id][0]
			return False
		except IndexError:
			self.link_queue[ctx.guild.id].pop()
			self.name_queue[ctx.guild.id].pop()
			return True
		except KeyError:
			return True