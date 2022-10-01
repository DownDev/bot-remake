import nextcord
from nextcord.ext import commands, tasks
import asyncio
import aiosqlite
from asyncratelimiter import AsyncRateLimiter
import datetime
from utils import *
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

intents = nextcord.Intents.default()
bot = Bot(intents=intents)

@tasks.loop(seconds=1)
async def genmsg(bot: Bot):
    if bot.main:
        print(bot.main)
        uuids = Database.distinct("guilds", "users")
        # uuids = ["6500f9522334438080e6e5f39c73c774"]
        WAIT_TIME = 30 / len(uuids)
        config = Database.list_documents("guilds", ["channels"], False)
        # config = [{"_id":"1003962871471947836","channels":{"1005223562535256124":{"6500f9522334438080e6e5f39c73c774":{"bedwars":True,"duels":True}},"1003986268809601045":{"6500f9522334438080e6e5f39c73c774":{"bedwars":False,"duels":False}},"1010612927532896436":{"6500f9522334438080e6e5f39c73c774":{"bedwars":False,"duels":False}},"1005224381867372674":{"6500f9522334438080e6e5f39c73c774":{"bedwars":False,"duels":True}}},"users":["6500f9522334438080e6e5f39c73c774"]}]
        for uuid in uuids:
            bot.send[uuid] = {"bedwars": None, "duels": None}
            stats = await fetch(uuid, bot.session)
            if stats:
                if uuid not in bot.main.keys():
                    print(uuid)
                    bot.main[uuid] = await fetch(uuid, bot.session)
                    
                name = stats.displayname
                rank = stats.rank
                
                
                if stats.bedwars.stats != bot.main[uuid].bedwars.stats:
                    if stats.bedwars.stats["Bedwars Experience"] == bot.main[uuid].bedwars.stats["Bedwars Experience"]:
                        stats = await fetch(uuid, bot.session)
                        
                        
                    modes = ["Overall ", "Solo ", "Doubles ", "3v3v3v3 ", "4v4v4v4 ", "4v4 ", "Rush Doubles ", "Rush 4v4v4v4 ", "Ultimate Doubles ", "Ultimate 4v4v4v4 ", "Voidless Doubles ", "Voidless 4v4v4v4 ", "Swappage Doubles ", "Swappage 4v4v4v4 ", "Armed Doubles ", "Armed 4v4v4v4 ", "Lucky Blocks Doubles ", "Lucky Blocks 4v4v4v4 ", "Castle "]
                    
                    strings = {"General": ""}
                    
                    strings.update({mode: "" for mode in modes})
                    
                    not_matching = {k: v for k, v in stats.bedwars.stats.items() if bot.main[uuid].bedwars.stats[k] != v}
                    
                    did_won = stats.wins_losses(not_matching)
                    if did_won:
                        description = ""
                        for item in did_won:
                            *mode, status = item.split()
                            description += f'**Game {"Won** 📈" if status == "Wins" else "Lost** 📉"}\nMode played: `{" ".join(mode)}`\n\n'
                        
                        
                        temp_str = ""
                        
                        collected = ["Iron Collected", "Gold Collected", "Diamonds Collected", "Emeralds Collected"]
                        emojis = [IRON, GOLD, DIAMOND, EMERALD]
                        
                        for stat, emoji in zip(collected, emojis):
                            current = not_matching.pop(stat, 0)
                            if current:
                                before = bot.main[uuid].bedwars.stats[stat]
                                temp_str += f"{emoji} {current-before} "
                            else:
                                temp_str += f"{emoji} 0 "
                        
                        level_up = not_matching.pop("Stars", None)
                        
                        sort = stats.sort_modes(not_matching, modes)
                        
                        for mode, dct in sort.items():
                            count = dct.copy()
                            for stat, value in dct.items():
                                before = bot.main[uuid].bedwars.stats[stat]
                                if len(count) > 1:
                                    emote = REPLYCONTINUE
                                else:
                                    emote = REPLY
                                if mode == "General":
                                    strings["General"] += f"{emote}**{stat}** earned: **{value-before:+,}**\n"
                                else:
                                    strings[mode] += f"{emote}{get_emoji(stat, before, value, modes[1:])} **{before:,}** ➡️ **{value:,}** (**{round(value-before, 2):+,}**)\n"
                                count.pop(stat)

                        
                        description += stats.bedwars.get_bar(stats.bedwars.stats["Bedwars Experience"], level_up)
                        
                        

                        description += f"\n**Resources collected**:\n{temp_str}"
                        
                            
                        star = stats.bedwars.stats["Stars"]
                            
                        color, icon = level(star)

                        embed=nextcord.Embed(title=nextcord.utils.escape_markdown(rank+name)+" ["+str(star)+icon+"]", description=description, color=color) 

                        for mode, string in strings.items():
                            if string:
                                embed.add_field(name=mode, value=string, inline=False)
                            
                        embed.set_thumbnail(url=f"https://mc-heads.net/avatar/{uuid}")
                        embed.set_footer(text="Tracking Bot | Beta 3")
                        embed.timestamp = datetime.datetime.now()
                        bot.send[uuid]["bedwars"] = embed
                        bot.main[uuid].bedwars.stats = stats.bedwars.stats
                    
                    
                if stats.duels.stats != bot.main[uuid].duels.stats:
                    if stats.duels.stats["Overall Wins"] == bot.main[uuid].duels.stats["Overall Wins"] and stats.duels.stats["Overall Losses"] == bot.main[uuid].duels.stats["Overall Losses"]:
                        stats = await fetch(uuid, bot.session)
                    
                    
                    modes = ["Overall ", "UHC Overall ", "UHC Duel ", "UHC Doubles ", "UHC Teams ", "UHC Deathmatch ", "Bridge Overall ", "Bridge Duel ", "Bridge Doubles ", "Bridge 3v3 ", "Bridge Teams ", "Bridge 2v2v2v2 ", "Bridge 3v3v3v3 ", "Bridge CTF Threes ", "Sumo Duel ", "Classic Duel ", "SkyWars Overall ", "SkyWars Duel ", "SkyWars Doubles ", "Parkour Duel ", "Boxing Duel ", "Bow Duel ", "NoDebuff Duel ", "Combo Duel ", "OP Overall ", "OP Duel ", "OP Doubles ", "MegaWalls Overall ", "MegaWalls Duel ", "MegaWalls Doubles ", "Blitz Duel ", "Bow Spleef Duel "]
                    
                    strings = {"General": ""}
                    
                    strings.update({mode: "" for mode in modes})
                    
                    
                    not_matching = {k: v for k, v in stats.duels.stats.items() if bot.main[uuid].duels.stats[k] != v}
                    
                    did_won = stats.wins_losses(not_matching)
                    if did_won:
                    
                        wins_save = 0
                        description = ""
                        
                        for item in stats.wins_losses(not_matching):
                            *mode, status = item.split()
                            description += f'**Duel {"Won** 📈" if status == "Wins" else "Lost** 📉"}\nMode played: `{" ".join(mode)}`\n\n'
                            
                            wins = stats.duels.stats[f'{" ".join(mode)} Wins']

                            if mode[0] in ["UHC", "Bridge", "SkyWars", "OP", "MegaWalls"]:
                                wins = stats.duels.stats[f'{mode[0]} Overall Wins']
                            
                            wins_save = wins
                            
                            description += stats.duels.get_bar(wins)
                        
                        
                        sort = stats.sort_modes(not_matching, modes)
                        
                        
                        for mode, dct in sort.items():
                            count = dct.copy()
                            for stat, value in dct.items():
                                before = bot.main[uuid].duels.stats[stat]
                                if len(count) > 1:
                                    emote = REPLYCONTINUE
                                else:
                                    emote = REPLY
                                if mode == "General":
                                    if stat == "Blocks Placed":
                                        strings["General"] += f"{emote}**Blocks Placed**: **{value-before:,}**\n"
                                    else:
                                        strings["General"] += f"{emote}**{stat}** earned: **{value-before:+,}**\n"
                                else:
                                    strings[mode] += f"{emote}{get_emoji(stat, before, value, modes[1:])} **{before:,}** ➡️ **{value:,}** (**{round(value-before, 2):+,}**)\n"
                                count.pop(stat)
                        
                        
                        wins_color = RangeKeyDict({
                        (0, 100): 0x535252,
                        (100, 250): 0xe7e7e7,
                        (250, 500): 0xe79a00,
                        (500, 1000): 0x009696,
                        (1000, 2000): 0x00a201,
                        (2000, 5000): 0x970000,
                        (5000, 10000): 0xf4f553,
                        (10000, 22000): 0x9a009a,
                        (22000, 50000): 0x55ffff,
                        (50000, 100000): 0xfe55fe,
                        (100000, 10000000): 0xff5555,
                    })

                        color = wins_color[wins_save]
                        title = stats.duels.wins_title[wins_save][0]
                        
                        embed=nextcord.Embed(title=f"{nextcord.utils.escape_markdown(rank+name)} {title}", description=description, color=color) 

                        for mode, string in strings.items():
                            if string:
                                embed.add_field(name=mode, value=string, inline=False)
                            
                        embed.set_thumbnail(url=f"https://mc-heads.net/avatar/{uuid}")
                        embed.set_footer(text="Tracking Bot | Beta 3")
                        embed.timestamp = datetime.datetime.now()
                        bot.send[uuid]["duels"] = embed
                        bot.main[uuid].duels.stats = stats.duels.stats
            
            await asyncio.sleep(WAIT_TIME)
            
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