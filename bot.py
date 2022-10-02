import nextcord
from nextcord.ext import commands, tasks
from nextcord import Embed, Intents
import asyncio
from asyncratelimiter import AsyncRateLimiter
import datetime
from utils import track, StatsList, TOKEN
import os
import aiohttp
from emojis import *
from database import Database

async def fetch(uuid, session):
    limiter = AsyncRateLimiter(max_rate=120, interval=60) # 320
    async with limiter:
        async with session.get(f"https://api.hypixel.net/player?key=85c47906-73f1-4a25-8717-f9af3e177e18&uuid={uuid}") as api: # add random
            api = await api.json()
            return await track(api, uuid)

class Bot(commands.Bot):
    main: dict[str, StatsList]
    send: dict[str, dict[str, Embed | None]]
    session = aiohttp.ClientSession()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.main = {}
        self.send = {}
        
        Database.initialize()
        
        for file in os.listdir("modules"):
            if file.endswith(".py"):
                self.load_extension(f"modules.{file[:-3]}")
    
    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        
        if not self.main:
            uuids = Database.distinct("guilds", "users")
            for uuid in uuids:
                self.main[uuid] = await fetch(uuid, self.session)

intents = Intents.default()
bot = Bot(intents=intents)

@tasks.loop(seconds=1)
async def genmsg(bot: Bot):
    if bot.main:
        uuids = Database.distinct("guilds", "users")
        WAIT_TIME = 600 / len(uuids)
        config = Database.list_documents("guilds", ["channels"], False)
        for uuid in uuids:
            bot.send[uuid] = {"bedwars": None, "duels": None}
            await asyncio.sleep(WAIT_TIME)
            stats = await fetch(uuid, bot.session)
            if stats:
                if uuid not in bot.main.keys():
                    print(uuid)
                    bot.main[uuid] = await fetch(uuid, bot.session)
                    
                name = stats.displayname
                rank = stats.rank
                bedwars = stats.bedwars
                duels = stats.duels
                
                if bedwars != bot.main[uuid].bedwars:
                    modes = ["Overall ", "Solo ", "Doubles ", "3v3v3v3 ", "4v4v4v4 ", "4v4 ", "Rush Doubles ", "Rush 4v4v4v4 ", "Ultimate Doubles ", "Ultimate 4v4v4v4 ", "Voidless Doubles ", "Voidless 4v4v4v4 ", "Swappage Doubles ", "Swappage 4v4v4v4 ", "Armed Doubles ", "Armed 4v4v4v4 ", "Lucky Blocks Doubles ", "Lucky Blocks 4v4v4v4 ", "Castle "]
                    
                    strings = {"General": ""}
                    strings.update({mode: "" for mode in modes})
                    
                    not_matching = {k: v for k, v in bedwars.stats.items() if bot.main[uuid].bedwars.stats[k] != v}
                    
                    did_won = stats.wins_losses(not_matching)
                    if did_won:
                        description = f'**Modes played**: `{", ".join({" ".join(item.split()[:-1]) for item in did_won})}`\n\n'
                        
                        level_up = not_matching.pop("Stars", None)
                        description += bedwars.get_bar(bedwars.stats["Bedwars Experience"], level_up)
                        description += f"\n**Resources collected**:\n"
                        
                        collected = ["Iron Collected", "Gold Collected", "Diamonds Collected", "Emeralds Collected"]
                        emojis = [IRON, GOLD, DIAMOND, EMERALD]
                        for stat, emoji in zip(collected, emojis):
                            current = not_matching.pop(stat, 0)
                            if current:
                                before = bot.main[uuid].bedwars.stats[stat]
                                description += f"{emoji} {current-before} "
                            else:
                                description += f"{emoji} 0 "
                                
                        sort = stats.sort_modes(not_matching, modes)
                        for mode, dct in sort.items():
                            count = dct.copy()
                            for stat, value in dct.items():
                                before = bot.main[uuid].bedwars.stats[stat]
                                emote = REPLYCONTINUE if len(count) > 1 else REPLY
                                if mode == "General":
                                    strings["General"] += f"{emote}**{stat}** earned: **{value-before:+,}**\n"
                                else:
                                    strings[mode] += f"{emote}{stats.get_emoji(stat, before, value, modes[1:])} **{before:,}** ➡️ **{value:,}** (**{round(value-before, 2):+,}**)\n"
                                count.pop(stat)
                            
                        star = bedwars.stats["Stars"]
                        color, icon = bedwars.level(star)

                        embed=Embed(title=nextcord.utils.escape_markdown(rank+name)+" ["+str(star)+icon+"]", description=description, color=color)
                        for mode, string in strings.items():
                            if string:
                                embed.add_field(name=mode, value=string, inline=False)
                        embed.set_thumbnail(url=f"https://mc-heads.net/avatar/{uuid}")
                        embed.set_footer(text="Tracking Bot | Beta 3")
                        embed.timestamp = datetime.datetime.now()
                        bot.send[uuid]["bedwars"] = embed
                        bot.main[uuid].bedwars.stats = bedwars.stats
                        
                if duels != bot.main[uuid].duels:
                    modes = ["Overall ", "UHC Overall ", "UHC Duel ", "UHC Doubles ", "UHC Teams ", "UHC Deathmatch ", "Bridge Overall ", "Bridge Duel ", "Bridge Doubles ", "Bridge 3v3 ", "Bridge Teams ", "Bridge 2v2v2v2 ", "Bridge 3v3v3v3 ", "Bridge CTF Threes ", "Sumo Duel ", "Classic Duel ", "SkyWars Overall ", "SkyWars Duel ", "SkyWars Doubles ", "Parkour Duel ", "Boxing Duel ", "Bow Duel ", "NoDebuff Duel ", "Combo Duel ", "OP Overall ", "OP Duel ", "OP Doubles ", "MegaWalls Overall ", "MegaWalls Duel ", "MegaWalls Doubles ", "Blitz Duel ", "Bow Spleef Duel "]
                    
                    strings = {"General": ""}
                    strings.update({mode: "" for mode in modes})
                    
                    not_matching = {k: v for k, v in duels.stats.items() if bot.main[uuid].duels.stats[k] != v}
                    
                    did_won = stats.wins_losses(not_matching)
                    if did_won:
                        description = f'**Modes played**: `{", ".join({" ".join(item.split()[:-1]) for item in did_won})}`\n\n'
                        wins = duels.stats["Overall Wins"]
                        description += duels.get_bar(wins)
                        sort = stats.sort_modes(not_matching, modes)
                        for mode, dct in sort.items():
                            count = dct.copy()
                            for stat, value in dct.items():
                                before = bot.main[uuid].duels.stats[stat]
                                emote = REPLYCONTINUE if len(count) > 1 else REPLY
                                if mode == "General":
                                    if stat == "Blocks Placed":
                                        strings["General"] += f"{emote}**Blocks Placed**: **{value-before:,}**\n"
                                    else:
                                        strings["General"] += f"{emote}**{stat}** earned: **{value-before:+,}**\n"
                                else:
                                    strings[mode] += f"{emote}{stats.get_emoji(stat, before, value, modes[1:])} **{before:,}** ➡️ **{value:,}** (**{round(value-before, 2):+,}**)\n"
                                count.pop(stat)
                                
                        color = duels.wins_color[wins // 2]
                        title = duels.wins_title[wins // 2][0]
                        
                        embed=Embed(title=f"{nextcord.utils.escape_markdown(rank+name)} {title}", description=description, color=color)
                        for mode, string in strings.items():
                            if string:
                                embed.add_field(name=mode, value=string, inline=False)
                        embed.set_thumbnail(url=f"https://mc-heads.net/avatar/{uuid}")
                        embed.set_footer(text="Tracking Bot | Beta 3")
                        embed.timestamp = datetime.datetime.now()
                        bot.send[uuid]["duels"] = embed
                        bot.main[uuid].duels.stats = duels.stats
                        
        for item in config:
            for channel_id, user_dict in item["channels"].items():
                channel = bot.get_channel(int(channel_id)) or await bot.fetch_channel(int(channel_id))
                for uuid, states in user_dict.items():
                    for name, value in states.items():
                        if value:
                            embed = bot.send[uuid][name]
                            if embed:
                                await channel.send(embed=embed)
        bot.send = {}

@genmsg.before_loop
async def _before():
    await bot.wait_until_ready()
# @cycle.before_loop
# async def __before():
#     await bot.wait_until_ready()
# cycle.start(bot)
genmsg.start(bot)
bot.run(TOKEN)