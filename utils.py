from math import floor
from nextcord import Embed, File, utils
import datetime
import random
from typing import Union
from collections import defaultdict
from range_key_dict import RangeKeyDict
from dataclasses import dataclass

from emojis import *

TOKEN = "OTY3NDM1NzgyODMyOTMwODQ2.G_NVWL.BaeRhFv-T9huRl3QIPtYp64CTZew99XiixBqYk"

NVIP = "<:nvip1:975329835092164668><:nvip2:975329836300132362><:nvip3:975329837373882368> "
VIP = "<:vip1:975329848048361472><:vip2:975329849126301696><:vip3:975329850233589781> "
NMVP = "<:nmvp1:975329831392796672><:nmvp2:975329832550404096><:nmvp3:975329833926144030> "
MVP = "<:mvp1:975329827563384862><:mvp2:975329828607774761><:mvp3:975329830134513675>"
BMVP = "<:bmvp:975329294056325160><:bmvp2:975329294974853132>"
GMVP = "<:gmvp:975329337383464991><:gmvp2:975329338826322011>"
OWNER = "<:owner1:975329838497935410><:owner2:975329839450038294><:owner3:975329840691572756><:owner4:975329841937260564> "
ADMIN = "<:admin1:975329087746887690><:admin2:975329088883556384><:admin3:975329291472613376><:admin4:975329292848365639> "
GAMEMASTER = "<:gamemaster1:975329334665555978><:gamemaster2:975329335839965254> "
YOUTUBE = "<:yt1:975329851529633812><:yt2:975329852733403138><:yt3:975329854067179520><:yt4:975329855468077126><:yt5:975329856541818900> "
PIG = "<:pig1:975329842868404265><:pig2:975329844583858186><:pig3:975329845716344832><:pig4:975329846928486480> "
MOJANG = "<:mojang1:1011620902204624976><:mojang2:1011620917002117131><:mojang3:1011620931753488514><:mojang4:1011620946869768222><:mojang5:1011620961520463932> "
EVENTS = "<:events1:1011620609521897574><:events2:1011620644905033768><:events3:1011620666887372840><:events4:1011620855136129044><:events5:1011620873704312912> "

GRED = "<:gmvpred:975329819967512606><:gmvpred2:975329821221605466> "
BRED = "<:bmvpred:975329325706534942><:bmvpred2:975329327719792770> "
RED = "<:bmvpred2:975329327719792770> "
GORANGE = "<:gmvporange:975329813436985344><:gmvporange2:975329814259060817> "
BORANGE = "<:bmvporange:975329318324555806><:bmvporange2:975329319675101215> "
ORANGE = "<:bmvporange2:975329319675101215> "
GGREEN = "<:gmvpgreen:975329810907803669><:gmvpgreen2:975329811918618665> "
BGREEN = "<:bmvpgreen:975329315505987654><:bmvpgreen2:975329316810412072> "
GREEN = "<:bmvpgreen2:975329316810412072> "
GYELLOW = "<:gmvpyellow:975329825269100545><:gmvpyellow2:975329826414145606> "
BYELLOW = "<:bmvpyellow:975329331695984650><:bmvpyellow2:975329333302423582> "
YELLOW = "<:bmvpyellow2:975329333302423582> "
GPINK = "<:gmvppink:975329815647387668><:gmvppink2:975329816691757056> "
BPINK = "<:bmvppink:975329321092800572><:bmvppink2:975329322325909534> "
PINK = "<:bmvppink2:975329322325909534> "
GWHITE = "<:gmvpwhite:975329822735749120><:gmvpwhite2:975329823914352640> "
BWHITE = "<:bmvpwhite:975329329296867358><:bmvpwhite2:975329330471264287> "
WHITE = "<:bmvpwhite2:975329330471264287> "
GBLUE = "<:gmvpblue:975329344794800178><:gmvpblue2:975329345994383470> "
BBLUE = "<:bmvpblue:975329302457503785><:bmvpblue2:975329303837433876> "
BLUE = "<:bmvpblue2:975329303837433876> "
GDARKGREEN = "<:gmvpdarkgreen:975329350079635526><:gmvpdarkgreen2:975329351501508618> "
BDARKGREEN = "<:bmvpdarkgreen:975329307926872094><:bmvpdarkgreen2:975329309151596564> "
DARKGREEN = "<:bmvpdarkgreen2:975329309151596564> "
GDARKRED = "<:gmvpdarkred:975329481965330432><:gmvpdarkred2:975329483269750845> "
BDARKRED = "<:bmvpdarkred:975329310208569344><:bmvpdarkred2:975329311131328513> "
DARKRED = "<:bmvpdarkred2:975329311131328513> "
GAQUA = "<:gmvpaqua:975329340130738217><:gmvpaqua2:975329341397434419> "
BAQUA = "<:bmvpaqua:975329296187002881><:bmvpaqua2:975329297663406101> "
AQUA = "<:bmvpaqua2:975329297663406101> "
GPURPLE = "<:gmvppurple:975329817811644456><:gmvppurple2:975329818860204032> "
BPURPLE = "<:bmvppurple:975329323206705174><:bmvppurple2:975329324192366634> "
PURPLE = "<:bmvppurple2:975329324192366634> "
GGRAY = "<:gmvpgray:975329808739356682><:gmvpgray2:975329809804722196> "
BGRAY = "<:bmvpgray:975329312767115264><:bmvpgray2:975329314138652672> "
GRAY = "<:bmvpgray2:975329314138652672> "
GBLACK = "<:gmvpblack:975329342655705108><:gmvpblack2:975329343775576164> "
BBLACK = "<:bmvpblack:975329299680854038><:bmvpblack2:975329301291487232> "
BLACK = "<:bmvpblack2:975329301291487232> "
GDARKBLUE = "<:gmvpdarkblue:975329347445587998><:gmvpdarkblue2:975329348766810143> "
BDARKBLUE = "<:bmvpdarkblue:975329305259307059><:bmvpdarkblue2:975329306597261332> "
DARKBLUE = "<:bmvpdarkblue2:975329306597261332> "

class ErrorEmbed(Embed):
    def __init__(self, title, message):
        discord_message = "\n\n**Join support discord [here](https://discord.gg/ahgj3WVh)**" # TODO: use utils oauth gen
        super().__init__(title=title, description=message+discord_message, color=0xff0000)
        self.set_thumbnail(url="https://media.giphy.com/media/cgVgNVD6cbx899eI1D/giphy.gif")
        self.set_footer(text=f"Use /help to get help")
        self.timestamp = datetime.datetime.now()

# class ListEmbed(Embed):
#     def __init__(self, title, array):
#         super().__init__(title=title, description=, color=0x0000ff)
        
EASY_LEVELS = 4
EASY_LEVELS_XP = 7000
XP_PER_PRESTIGE = 96 * 5000 + EASY_LEVELS_XP
LEVELS_PER_PRESTIGE = 100
HIGHEST_PRESTIGE = 10
DEFAULT_EXP = {1: 500, 2: 1000, 3: 2000, 4: 3500}
def getExpForLevel(level):
    if not level: 
        return 0
    respectedLevel = getLevelRespectingPrestige(level)
    return DEFAULT_EXP.get(respectedLevel, 5000)

def getLevelRespectingPrestige(level):
    if level > HIGHEST_PRESTIGE * LEVELS_PER_PRESTIGE:
        return level - HIGHEST_PRESTIGE * LEVELS_PER_PRESTIGE
    else:
        return level % LEVELS_PER_PRESTIGE
def getLevelForExp(exp):
    prestiges = floor(exp / XP_PER_PRESTIGE)
    level = prestiges * LEVELS_PER_PRESTIGE
    expWithoutPrestiges = exp - (prestiges * XP_PER_PRESTIGE)
    for i in range(1, EASY_LEVELS + 1):
        expForEasyLevel = getExpForLevel(i)
        if expWithoutPrestiges < expForEasyLevel:
            break
        level += 1
        expWithoutPrestiges -= expForEasyLevel
    return level + expWithoutPrestiges / 5000















def calc_ratio(k: int, d: int) -> int | float:
    if d == 0:
        return k
    else:  
        return round(k / d, 2)

async def get_uuid(uuid, session):
    async with session.get(f"https://api.ashcon.app/mojang/v2/user/{uuid}") as api:
        if api.status == 200:
            result = await api.json()
            uuid = result["uuid"].replace("-", "")
            displayname = result["username"]
            return uuid, utils.escape_markdown(displayname)
    return None, None

async def ifexists(uuid, session, full_check=True):
    async with session.get(f"https://api.hypixel.net/player?key=85c47906-73f1-4a25-8717-f9af3e177e18&uuid={uuid}") as api:
        api = await api.json()
        if "success" in api and "player" in api:
            if api["success"] and api["player"]:
                if not full_check:
                    return api
                if "stats" in api["player"] and "achievements" in api["player"]:
                    if "Bedwars" in api["player"]["stats"]:
                        return api
    return False

# class Bedwars():
#     stats: dict
    
#     def __init__(self, stats):
#         self.stats = stats

        
#     def __dict__(self):
#         return self.stats

#     def get_mode(self, mode):
#         return {k: v for k, v in self.stats.items() if k.startswith(mode)}
    
    
#     @staticmethod
#     def get_bar(exp, star = None):
#         level = getLevelForExp(exp)
#         percent = (level - int(level)) * 100
#         SIZE = 100 / 13
#         amount = int(percent // SIZE)
#         until_pres = int(level + 1) % 100
#         if until_pres > 4:
#             n = 5000
#         elif until_pres == 1:
#             n = 500
#         elif until_pres == 2:
#             n = 1000
#         elif until_pres == 3:
#             n = 2000
#         elif until_pres == 4:
#             n = 3500
#         else:
#             n = 5000
#         curr_exp = int(percent / 100 * n)
#         if int(level + 1) % 100 == 0:
#             new_level = Bedwars.prestige_name(int(level + 1))
#         else:
#             new_level = f"Level {int(level + 1)}"
#         if not star:
#             return f'**Level {int(level)}**⠀⠀⠀⠀⠀⠀⠀⠀⠀**{new_level}**\n[{BWEXP_FILLED * amount + BWEXP_MISSING * (13 - amount)}]\n⠀⠀⠀⠀⠀⠀⠀**{curr_exp:,}**/**{n:,}** (**{curr_exp / n * 100:.1f}%**)\n'
#         else:
#             return f'**Level {star - 1}**⠀⠀⠀⠀⠀⠀⠀⠀⠀**{Bedwars.prestige_name(star)}**\n[{BWEXP_FILLED * 13}]\n**LEVEL UP!** You are now **{Bedwars.prestige_name(star)}**\n'

        
# class Duels():
#     stats: dict
    
#     def __init__(self, stats):
#         self.stats = stats
        
#         self.wins_title = RangeKeyDict({
#         (0, 50): (None, 50, 0),
#         (50, 60): ('Rookie', 60, 50),
#         (60, 70): ('Rookie II', 70, 60),      
#         (70, 80): ('Rookie III', 80, 70),     
#         (80, 90): ('Rookie IV', 90, 80),      
#         (90, 100): ('Rookie V', 100, 90),     
#         (100, 130): ('Iron', 130, 100),       
#         (130, 160): ('Iron II', 160, 130),    
#         (160, 190): ('Iron III', 190, 160),   
#         (190, 220): ('Iron IV', 220, 190),    
#         (220, 250): ('Iron V', 250, 220),     
#         (250, 300): ('Gold', 300, 250),       
#         (300, 350): ('Gold II', 350, 300),    
#         (350, 400): ('Gold III', 400, 350),   
#         (400, 450): ('Gold IV', 450, 400),    
#         (450, 500): ('Gold V', 500, 450),     
#         (500, 600): ('Diamond', 600, 500),    
#         (600, 700): ('Diamond II', 700, 600), 
#         (700, 800): ('Diamond III', 800, 700),
#         (800, 900): ('Diamond IV', 900, 800), 
#         (900, 1000): ('Diamond V', 1000, 900),
#         (1000, 1200): ('Master', 1200, 1000),
#         (1200, 1400): ('Master II', 1400, 1200),
#         (1400, 1600): ('Master III', 1600, 1400),
#         (1600, 1800): ('Master IV', 1800, 1600),
#         (1800, 2000): ('Master V', 2000, 1800),
#         (2000, 2600): ('Legend', 2600, 2000),
#         (2600, 3200): ('Legend II', 3200, 2600),
#         (3200, 3800): ('Legend III', 3800, 3200),
#         (3800, 4400): ('Legend IV', 4400, 3800),
#         (4400, 5000): ('Legend V', 5000, 4400),
#         (5000, 6000): ('Grandmaster', 6000, 5000),
#         (6000, 7000): ('Grandmaster II', 7000, 6000),
#         (7000, 8000): ('Grandmaster III', 8000, 7000),
#         (8000, 9000): ('Grandmaster IV', 9000, 8000),
#         (9000, 10000): ('Grandmaster V', 10000, 9000),
#         (10000, 13000): ('Godlike', 13000, 10000),
#         (13000, 16000): ('Godlike II', 16000, 13000),
#         (16000, 19000): ('Godlike III', 19000, 16000),
#         (19000, 22000): ('Godlike IV', 22000, 19000),
#         (22000, 25000): ('Godlike V', 25000, 22000),
#         (25000, 30000): ('Celestial', 30000, 25000),
#         (30000, 35000): ('Celestial II', 35000, 30000),
#         (35000, 40000): ('Celestial III', 40000, 35000),
#         (40000, 45000): ('Celestial IV', 45000, 40000),
#         (45000, 50000): ('Celestial V', 50000, 45000),
#         (50000, 60000): ('Divine', 60000, 50000),
#         (60000, 70000): ('Divine II', 70000, 60000),
#         (70000, 80000): ('Divine III', 80000, 70000),
#         (80000, 90000): ('Divine IV', 90000, 80000),
#         (90000, 100000): ('Divine V', 100000, 90000),
#         (100000, 10000000): ('Ascended', 10000000, 100000),
#         })
   
#     def get_bar(self, wins):
#         wins_next = self.wins_title[wins][1]
#         starter = self.wins_title[wins][2]
#         title = self.wins_title[wins][0]
#         title_next = titles[titles.index(title) + 1]

#         percent = (wins - starter) / (wins_next - starter) * 100
#         SIZE = 100 / 13
#         amount = int(percent // SIZE)
#         return f"**{title_next}** unlocked in **{wins_next - wins:,}** more wins!\n({DEXP * amount + BWEXP_MISSING * (13 - amount)})\n⠀⠀⠀⠀⠀⠀⠀⠀**{wins:,}**/**{wins_next:,}** (**{round(percent, 1)}%**)\n"


    
@dataclass
class Bedwars:
    stats: dict
    
    prestige_names = {100: 'Iron Prestige', 200: 'Gold Prestige', 300: 'Diamond Prestige', 400: 'Emerald Prestige', 500: 'Sapphire Prestige', 600: 'Ruby Prestige', 700: 'Crystal Prestige', 800: 'Opal Prestige', 900: 'Amethyst Prestige', 1000: 'Rainbow Prestige', 1100: 'Iron Prime Prestige', 1200: 'Gold Prime Prestige', 1300: 'Diamond Prime Prestige', 1400: 'Emerald Prime Prestige', 1500: 'Sapphire Prime Prestige', 1600: 'Ruby Prime Prestige', 1700: 'Crystal Prime Prestige', 1800: 'Opal Prime Prestige', 1900: 'Amethyst Prime Prestige', 2000: 'Mirror Prestige', 2100: 'Light Prestige', 2200: 'Dawn Prestige', 2300: 'Dusk Prestige', 2400: 'Air Prestige', 2500: 'Wind Prestige', 2600: 'Nebula Prestige', 2700: 'Thunder Prestige', 2800: 'Earth Prestige', 2900: 'Water Prestige', 3000: 'Fire Prestige'}
    
    star_color = RangeKeyDict({
    (0, 100): 0xaaaaaa,
    (100, 200): 0xffffff,
    (200, 300): 0xffaa00,
    (300, 400): 0x55ffff,
    (400, 500): 0xaa00,
    (500, 600): 0xaaaa,
    (600, 700): 0xaa0000,
    (700, 800): 0xff55ff,
    (800, 900): 0x5555ff,
    (900, 1000): 0xaa00aa,
    (1000, 1100): 0xfc035e,
    (1100, 1200): 0xffffff,
    (1200, 1300): 0xffaa00,
    (1300, 1400): 0x55ffff,
    (1400, 1500): 0xaa00,
    (1500, 1600): 0xaaaa,
    (1600, 1700): 0xaa0000,
    (1700, 1800): 0xff55ff,
    (1800, 1900): 0x5555ff,
    (1900, 2000): 0xaa00aa,
    (2000, 2100): 0xaaaaaa,
    (2100, 2200): 0xffff55,
    (2200, 2300): 0xffaa00,
    (2300, 2400): 0xaa00aa,
    (2400, 2500): 0x55ffff,
    (2500, 2600): 0x55ff55,
    (2600, 2700): 0xff5555,
    (2700, 2800): 0xffff55,
    (2800, 2900): 0xaa00,
    (2900, 3000): 0xaaaa,
    (3000, 10000): 0xffaa00
})

    star_icon = RangeKeyDict({
        (0, 1100): "✫",
        (1100, 2100): "✪",
        (2100, 10000): "⚝"
    })
    
    def __ne__(self, other):
        return self.stats != other.stats
    
    @staticmethod
    def prestige_name(star):
        return Bedwars.prestige_names.get(star, f"Level {star}")
    
    @staticmethod
    def level(star: int):
        icon = Bedwars.star_icon[star]
        color = Bedwars.star_color[star]
        return color, icon
    
    @staticmethod
    def get_bar(exp, star = None):
        level = getLevelForExp(exp)
        percent = (level - int(level)) * 100
        SIZE = 100 / 13
        amount = int(percent // SIZE)
        until_pres = int(level + 1) % 100
        if until_pres > 4:
            n = 5000
        elif until_pres == 1:
            n = 500
        elif until_pres == 2:
            n = 1000
        elif until_pres == 3:
            n = 2000
        elif until_pres == 4:
            n = 3500
        else:
            n = 5000
        curr_exp = int(percent / 100 * n)
        new_level = Bedwars.prestige_name(level + 1)
        if not star:
            return f'**Level {int(level)}**⠀⠀⠀⠀⠀⠀⠀⠀⠀**{new_level}**\n[{BWEXP_FILLED * amount + BWEXP_MISSING * (13 - amount)}]\n⠀⠀⠀⠀⠀⠀⠀**{curr_exp:,}**/**{n:,}** (**{curr_exp / n * 100:.1f}%**)\n'
        else:
            return f'**Level {star - 1}**⠀⠀⠀⠀⠀⠀⠀⠀⠀**{Bedwars.prestige_name(star)}**\n[{BWEXP_FILLED * 13}]\n**LEVEL UP!** You are now **{Bedwars.prestige_name(star)}**\n'
@dataclass
class Duels:
    stats: dict
    
    titles = [None, 'Rookie', 'Rookie II', 'Rookie III', 'Rookie IV', 'Rookie V', 'Iron', 'Iron II', 'Iron III', 'Iron IV', 'Iron V', 'Gold', 'Gold II', 'Gold III', 'Gold IV', 'Gold V', 'Diamond', 'Diamond II', 'Diamond III', 'Diamond IV', 'Diamond V', 'Master', 'Master II', 'Master III', 'Master IV', 'Master V', 'Legend', 'Legend II', 'Legend III', 'Legend IV', 'Legend V', 'Grandmaster', 'Grandmaster II', 'Grandmaster III', 'Grandmaster IV', 'Grandmaster V', 'Godlike', 'Godlike II', 'Godlike III', 'Godlike IV', 'Godlike V', 'Celestial', 'Celestial II', 'Celestial III', 'Celestial IV', 'Celestial V', 'Divine', 'Divine II', 'Divine III', 'Divine IV', 'Divine V', 'Ascended']
    
    wins_title = RangeKeyDict({
        (0, 50): (None, 50, 0),
        (50, 60): ('Rookie', 60, 50),
        (60, 70): ('Rookie II', 70, 60),      
        (70, 80): ('Rookie III', 80, 70),     
        (80, 90): ('Rookie IV', 90, 80),      
        (90, 100): ('Rookie V', 100, 90),     
        (100, 130): ('Iron', 130, 100),       
        (130, 160): ('Iron II', 160, 130),    
        (160, 190): ('Iron III', 190, 160),   
        (190, 220): ('Iron IV', 220, 190),    
        (220, 250): ('Iron V', 250, 220),     
        (250, 300): ('Gold', 300, 250),       
        (300, 350): ('Gold II', 350, 300),    
        (350, 400): ('Gold III', 400, 350),   
        (400, 450): ('Gold IV', 450, 400),    
        (450, 500): ('Gold V', 500, 450),     
        (500, 600): ('Diamond', 600, 500),    
        (600, 700): ('Diamond II', 700, 600), 
        (700, 800): ('Diamond III', 800, 700),
        (800, 900): ('Diamond IV', 900, 800), 
        (900, 1000): ('Diamond V', 1000, 900),
        (1000, 1200): ('Master', 1200, 1000),
        (1200, 1400): ('Master II', 1400, 1200),
        (1400, 1600): ('Master III', 1600, 1400),
        (1600, 1800): ('Master IV', 1800, 1600),
        (1800, 2000): ('Master V', 2000, 1800),
        (2000, 2600): ('Legend', 2600, 2000),
        (2600, 3200): ('Legend II', 3200, 2600),
        (3200, 3800): ('Legend III', 3800, 3200),
        (3800, 4400): ('Legend IV', 4400, 3800),
        (4400, 5000): ('Legend V', 5000, 4400),
        (5000, 6000): ('Grandmaster', 6000, 5000),
        (6000, 7000): ('Grandmaster II', 7000, 6000),
        (7000, 8000): ('Grandmaster III', 8000, 7000),
        (8000, 9000): ('Grandmaster IV', 9000, 8000),
        (9000, 10000): ('Grandmaster V', 10000, 9000),
        (10000, 13000): ('Godlike', 13000, 10000),
        (13000, 16000): ('Godlike II', 16000, 13000),
        (16000, 19000): ('Godlike III', 19000, 16000),
        (19000, 22000): ('Godlike IV', 22000, 19000),
        (22000, 25000): ('Godlike V', 25000, 22000),
        (25000, 30000): ('Celestial', 30000, 25000),
        (30000, 35000): ('Celestial II', 35000, 30000),
        (35000, 40000): ('Celestial III', 40000, 35000),
        (40000, 45000): ('Celestial IV', 45000, 40000),
        (45000, 50000): ('Celestial V', 50000, 45000),
        (50000, 60000): ('Divine', 60000, 50000),
        (60000, 70000): ('Divine II', 70000, 60000),
        (70000, 80000): ('Divine III', 80000, 70000),
        (80000, 90000): ('Divine IV', 90000, 80000),
        (90000, 100000): ('Divine V', 100000, 90000),
        (100000, 10000000): ('Ascended', 10000000, 100000),
        })
    
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
    
    def __ne__(self, other):
        return self.stats != other.stats
    
    @staticmethod
    def get_bar(wins):
        title, wins_next, starter = Duels.wins_title[wins]
        title_next = Duels.titles[Duels.titles.index(title) + 1]

        percent = (wins - starter) / (wins_next - starter) * 100
        SIZE = 100 / 13
        amount = int(percent // SIZE)
        return f"**{title_next}** unlocked in **{wins_next - wins:,}** more wins!\n({DEXP * amount + BWEXP_MISSING * (13 - amount)})\n⠀⠀⠀⠀⠀⠀⠀⠀**{wins:,}**/**{wins_next:,}** (**{round(percent, 1)}%**)\n"
@dataclass
class StatsList:
    bedwars: Bedwars
    duels: Duels
    displayname: str
    rank: str
    
    def __bool__(self):
        return bool(self.bedwars and self.duels)
    
    @staticmethod
    def sort_modes(data: dict, modes: list[str]) -> dict:
        result = defaultdict(dict)
        for key, value in data.items():
            starters = [mode for mode in modes if key.startswith(mode)]
            result[starters[0] if starters else 'General'].update({key: value})
        return result
    
    @staticmethod
    def wins_losses(data):
        return [k for k in data.keys() if not "Overall " in k and (k.endswith("Wins") or k.endswith("Losses"))]
    
    @staticmethod
    def get_emoji(stat, before, after, modes):
        if "Los" in stat or "Death" in stat:
            emoji = "🔻"
        elif before < after:
            emoji = "<:small_green_triangle_up:977158469973061682>"
        else:
            emoji = "🔻"
        for mode in modes[::-1]:
            stat = stat.replace(mode, "")
        stat = stat.replace("Overall ", "")
        return f'**{stat}** {emoji}:'

    
    
    
    
    
    
    
    
    

async def track(data: dict, uuid: str) -> StatsList | None:
    mapping = {
        "Bedwars": {
            "Experience": "Bedwars Experience",
            "wins_bedwars": "Overall Wins",
            "eight_one_wins_bedwars": "Solo Wins",
            "eight_two_wins_bedwars": "Doubles Wins",
            "four_three_wins_bedwars": "3v3v3v3 Wins",
            "four_four_wins_bedwars": "4v4v4v4 Wins",
            "two_four_wins_bedwars": "4v4 Wins",
            "eight_two_rush_wins_bedwars": "Rush Doubles Wins",
            "four_four_rush_wins_bedwars": "Rush 4v4v4v4 Wins",
            "eight_two_ultimate_wins_bedwars": "Ultimate Doubles Wins",
            "four_four_ultimate_wins_bedwars": "Ultimate 4v4v4v4 Wins",
            "eight_two_voidless_wins_bedwars": "Voidless Doubles Wins",
            "four_four_voidless_wins_bedwars": "Voidless 4v4v4v4 Wins",
            "eight_two_swap_wins_bedwars": "Swappage Doubles Wins",
            "four_four_swap_wins_bedwars": "Swappage 4v4v4v4 Wins",
            "eight_two_armed_wins_bedwars": "Armed Doubles Wins",
            "four_four_armed_wins_bedwars": "Armed 4v4v4v4 Wins",
            "eight_two_lucky_wins_bedwars": "Lucky Blocks Doubles Wins",
            "four_four_lucky_wins_bedwars": "Lucky Blocks 4v4v4v4 Wins",
            "castle_wins_bedwars": "Castle Wins",
            "losses_bedwars": "Overall Losses",
            "eight_one_losses_bedwars": "Solo Losses",
            "eight_two_losses_bedwars": "Doubles Losses",
            "four_three_losses_bedwars": "3v3v3v3 Losses",
            "four_four_losses_bedwars": "4v4v4v4 Losses",
            "two_four_losses_bedwars": "4v4 Losses",
            "eight_two_rush_losses_bedwars": "Rush Doubles Losses",
            "four_four_rush_losses_bedwars": "Rush 4v4v4v4 Losses",
            "eight_two_ultimate_losses_bedwars": "Ultimate Doubles Losses",
            "four_four_ultimate_losses_bedwars": "Ultimate 4v4v4v4 Losses",
            "eight_two_voidless_losses_bedwars": "Voidless Doubles Losses",
            "four_four_voidless_losses_bedwars": "Voidless 4v4v4v4 Losses",
            "eight_two_swap_losses_bedwars": "Swappage Doubles Losses",
            "four_four_swap_losses_bedwars": "Swappage 4v4v4v4 Losses",
            "eight_two_armed_losses_bedwars": "Armed Doubles Losses",
            "four_four_armed_losses_bedwars": "Armed 4v4v4v4 Losses",
            "eight_two_lucky_losses_bedwars": "Lucky Blocks Doubles Losses",
            "four_four_lucky_losses_bedwars": "Lucky Blocks 4v4v4v4 Losses",
            "castle_losses_bedwars": "Castle Losses",
            "final_kills_bedwars": "Overall F. Kills",
            "eight_one_final_kills_bedwars": "Solo F. Kills",
            "eight_two_final_kills_bedwars": "Doubles F. Kills",
            "four_three_final_kills_bedwars": "3v3v3v3 F. Kills",
            "four_four_final_kills_bedwars": "4v4v4v4 F. Kills",
            "two_four_final_kills_bedwars": "4v4 F. Kills",
            "eight_two_rush_final_kills_bedwars": "Rush Doubles F. Kills",
            "four_four_rush_final_kills_bedwars": "Rush 4v4v4v4 F. Kills",
            "eight_two_ultimate_final_kills_bedwars": "Ultimate Doubles F. Kills",
            "four_four_ultimate_final_kills_bedwars": "Ultimate 4v4v4v4 F. Kills",
            "eight_two_voidless_final_kills_bedwars": "Voidless Doubles F. Kills",
            "four_four_voidless_final_kills_bedwars": "Voidless 4v4v4v4 F. Kills",
            "eight_two_swap_final_kills_bedwars": "Swappage Doubles F. Kills",
            "four_four_swap_final_kills_bedwars": "Swappage 4v4v4v4 F. Kills",
            "eight_two_armed_final_kills_bedwars": "Armed Doubles F. Kills",
            "four_four_armed_final_kills_bedwars": "Armed 4v4v4v4 F. Kills",
            "eight_two_lucky_final_kills_bedwars": "Lucky Blocks Doubles F. Kills",
            "four_four_lucky_final_kills_bedwars": "Lucky Blocks 4v4v4v4 F. Kills",
            "castle_final_kills_bedwars": "Castle F. Kills",
            "final_deaths_bedwars": "Overall F. Deaths",
            "eight_one_final_deaths_bedwars": "Solo F. Deaths",
            "eight_two_final_deaths_bedwars": "Doubles F. Deaths",
            "four_three_final_deaths_bedwars": "3v3v3v3 F. Deaths",
            "four_four_final_deaths_bedwars": "4v4v4v4 F. Deaths",
            "two_four_final_deaths_bedwars": "4v4 F. Deaths",
            "eight_two_rush_final_deaths_bedwars": "Rush Doubles F. Deaths",
            "four_four_rush_final_deaths_bedwars": "Rush 4v4v4v4 F. Deaths",
            "eight_two_ultimate_final_deaths_bedwars": "Ultimate Doubles F. Deaths",
            "four_four_ultimate_final_deaths_bedwars": "Ultimate 4v4v4v4 F. Deaths",
            "eight_two_voidless_final_deaths_bedwars": "Voidless Doubles F. Deaths",
            "four_four_voidless_final_deaths_bedwars": "Voidless 4v4v4v4 F. Deaths",
            "eight_two_swap_final_deaths_bedwars": "Swappage Doubles F. Deaths",
            "four_four_swap_final_deaths_bedwars": "Swappage 4v4v4v4 F. Deaths",
            "eight_two_armed_final_deaths_bedwars": "Armed Doubles F. Deaths",
            "four_four_armed_final_deaths_bedwars": "Armed 4v4v4v4 F. Deaths",
            "eight_two_lucky_final_deaths_bedwars": "Lucky Blocks Doubles F. Deaths",
            "four_four_lucky_final_deaths_bedwars": "Lucky Blocks 4v4v4v4 F. Deaths",
            "castle_final_deaths_bedwars": "Castle F. Deaths",
            "beds_broken_bedwars": "Overall B. Broken",
            "eight_one_beds_broken_bedwars": "Solo B. Broken",
            "eight_two_beds_broken_bedwars": "Doubles B. Broken",
            "four_three_beds_broken_bedwars": "3v3v3v3 B. Broken",
            "four_four_beds_broken_bedwars": "4v4v4v4 B. Broken",
            "two_four_beds_broken_bedwars": "4v4 B. Broken",
            "eight_two_rush_beds_broken_bedwars": "Rush Doubles B. Broken",
            "four_four_rush_beds_broken_bedwars": "Rush 4v4v4v4 B. Broken",
            "eight_two_ultimate_beds_broken_bedwars": "Ultimate Doubles B. Broken",
            "four_four_ultimate_beds_broken_bedwars": "Ultimate 4v4v4v4 B. Broken",
            "eight_two_voidless_beds_broken_bedwars": "Voidless Doubles B. Broken",
            "four_four_voidless_beds_broken_bedwars": "Voidless 4v4v4v4 B. Broken",
            "eight_two_swap_beds_broken_bedwars": "Swappage Doubles B. Broken",
            "four_four_swap_beds_broken_bedwars": "Swappage 4v4v4v4 B. Broken",
            "eight_two_armed_beds_broken_bedwars": "Armed Doubles B. Broken",
            "four_four_armed_beds_broken_bedwars": "Armed 4v4v4v4 B. Broken",
            "eight_two_lucky_beds_broken_bedwars": "Lucky Blocks Doubles B. Broken",
            "four_four_lucky_beds_broken_bedwars": "Lucky Blocks 4v4v4v4 B. Broken",
            "castle_beds_broken_bedwars": "Castle B. Broken",
            "beds_lost_bedwars": "Overall B. Lost",
            "eight_one_beds_lost_bedwars": "Solo B. Lost",
            "eight_two_beds_lost_bedwars": "Doubles B. Lost",
            "four_three_beds_lost_bedwars": "3v3v3v3 B. Lost",
            "four_four_beds_lost_bedwars": "4v4v4v4 B. Lost",
            "two_four_beds_lost_bedwars": "4v4 B. Lost",
            "eight_two_rush_beds_lost_bedwars": "Rush Doubles B. Lost",
            "four_four_rush_beds_lost_bedwars": "Rush 4v4v4v4 B. Lost",
            "eight_two_ultimate_beds_lost_bedwars": "Ultimate Doubles B. Lost",
            "four_four_ultimate_beds_lost_bedwars": "Ultimate 4v4v4v4 B. Lost",
            "eight_two_voidless_beds_lost_bedwars": "Voidless Doubles B. Lost",
            "four_four_voidless_beds_lost_bedwars": "Voidless 4v4v4v4 B. Lost",
            "eight_two_swap_beds_lost_bedwars": "Swappage Doubles B. Lost",
            "four_four_swap_beds_lost_bedwars": "Swappage 4v4v4v4 B. Lost",
            "eight_two_armed_beds_lost_bedwars": "Armed Doubles B. Lost",
            "four_four_armed_beds_lost_bedwars": "Armed 4v4v4v4 B. Lost",
            "eight_two_lucky_beds_lost_bedwars": "Lucky Blocks Doubles B. Lost",
            "four_four_lucky_beds_lost_bedwars": "Lucky Blocks 4v4v4v4 B. Lost",
            "castle_beds_lost_bedwars": "Castle B. Lost",
            "coins": "Coins"
        },
        "Duels": {
            "coins": "Coins",
            "duels_chests": "Loot Chests",
            
            "wins": "Overall Wins",
            "kills": "Overall Kills",
            "losses": "Overall Losses",
            "deaths": "Overall Deaths",
            "blocks_placed": "Blocks Placed",
            
            
            "uhc_duel_wins": "UHC Duel Wins",
            "uhc_duel_kills": "UHC Duel Kills",
            "uhc_duel_losses": "UHC Duel Losses",
            "uhc_duel_deaths": "UHC Duel Deaths",
            
            "uhc_doubles_wins": "UHC Doubles Wins",
            "uhc_doubles_kills": "UHC Doubles Kills",
            "uhc_doubles_losses": "UHC Doubles Losses",
            "uhc_doubles_deaths": "UHC Doubles Deaths",
            
            "uhc_four_wins": "UHC Teams Wins",
            "uhc_four_kills": "UHC Teams Kills",
            "uhc_four_losses": "UHC Teams Losses",
            "uhc_four_deaths": "UHC Teams Deaths",
            
            "uhc_meetup_wins": "UHC Deathmatch Wins",
            "uhc_meetup_kills": "UHC Deathmatch Kills",
            "uhc_meetup_losses": "UHC Deathmatch Losses",
            "uhc_meetup_deaths": "UHC Deathmatch Deaths",
            
            "bridge_duel_wins": "Bridge Duel Wins",
            "bridge_duel_bridge_kills": "Bridge Duel Kills",
            "bridge_duel_losses": "Bridge Duel Losses",
            "bridge_duel_bridge_deaths": "Bridge Duel Deaths",
            "bridge_duel_goals": "Bridge Duel Goals",
            
            "bridge_doubles_wins": "Bridge Doubles Wins",
            "bridge_doubles_bridge_kills": "Bridge Doubles Kills",
            "bridge_doubles_losses": "Bridge Doubles Losses",
            "bridge_doubles_bridge_deaths": "Bridge Doubles Deaths",
            "bridge_doubles_goals": "Bridge Doubles Goals",
            
            "bridge_threes_wins": "Bridge 3v3 Wins",
            "bridge_threes_bridge_kills": "Bridge 3v3 Kills",
            "bridge_threes_losses": "Bridge 3v3 Losses",
            "bridge_threes_bridge_deaths": "Bridge 3v3 Deaths",
            "bridge_threes_goals": "Bridge 3v3 Goals",
            
            "bridge_four_wins": "Bridge Teams Wins",
            "bridge_four_bridge_kills": "Bridge Teams Kills",
            "bridge_four_losses": "Bridge Teams Losses",
            "bridge_four_bridge_deaths": "Bridge Teams Deaths",
            "bridge_four_goals": "Bridge Teams Goals",
            
            "bridge_2v2v2v2_wins": "Bridge 2v2v2v2 Wins",
            "bridge_2v2v2v2_bridge_kills": "Bridge 2v2v2v2 Kills",
            "bridge_2v2v2v2_losses": "Bridge 2v2v2v2 Losses",
            "bridge_2v2v2v2_bridge_deaths": "Bridge 2v2v2v2 Deaths",
            "bridge_2v2v2v2_goals": "Bridge 2v2v2v2 Goals",
            
            "bridge_3v3v3v3_wins": "Bridge 3v3v3v3 Wins",
            "bridge_3v3v3v3_bridge_kills": "Bridge 3v3v3v3 Kills",
            "bridge_3v3v3v3_losses": "Bridge 3v3v3v3 Losses",
            "bridge_3v3v3v3_bridge_deaths": "Bridge 3v3v3v3 Deaths",
            "bridge_3v3v3v3_goals": "Bridge 3v3v3v3 Goals",
            
            "capture_threes_wins": "Bridge CTF Threes Wins",
            "capture_threes_bridge_kills": "Bridge CTF Threes Kills",
            "capture_threes_losses": "Bridge CTF Threes Losses",
            "capture_threes_bridge_deaths": "Bridge CTF Threes Deaths",
            "capture_threes_captures": "Bridge CTF Threes Captures",

            "sumo_duel_wins": "Sumo Duel Wins",
            "sumo_duel_kills": "Sumo Duel Kills",
            "sumo_duel_losses": "Sumo Duel Losses",
            "sumo_duel_deaths": "Sumo Duel Deaths",

            "classic_duel_wins": "Classic Duel Wins",
            "classic_duel_kills": "Classic Duel Kills",
            "classic_duel_losses": "Classic Duel Losses",
            "classic_duel_deaths": "Classic Duel Deaths",
            
            "sw_duel_wins": "SkyWars Duel Wins",
            "sw_duel_kills": "SkyWars Duel Kills",
            "sw_duel_losses": "SkyWars Duel Losses",
            "sw_duel_deaths": "SkyWars Duel Deaths",
            
            "sw_doubles_wins": "SkyWars Doubles Wins",
            "sw_doubles_kills": "SkyWars Doubles Kills",
            "sw_doubles_losses": "SkyWars Doubles Losses",
            "sw_doubles_deaths": "SkyWars Doubles Deaths",
            
            "parkour_eight_wins": "Parkour Duel Wins",
            "parkour_eight_losses": "Parkour Duel Losses",
            "parkour_eight_deaths": "Parkour Duel Deaths",
            
            "boxing_duel_wins": "Boxing Duel Wins",
            "boxing_duel_kills": "Boxing Duel Kills",
            "boxing_duel_losses": "Boxing Duel Losses",
            "boxing_duel_deaths": "Boxing Duel Deaths",
            
            "bow_duel_wins": "Bow Duel Wins",
            "bow_duel_kills": "Bow Duel Kills",
            "bow_duel_losses": "Bow Duel Losses",
            "bow_duel_deaths": "Bow Duel Deaths",
            
            "potion_duel_wins": "NoDebuff Duel Wins",
            "potion_duel_kills": "NoDebuff Duel Kills",
            "potion_duel_losses": "NoDebuff Duel Losses",
            "potion_duel_deaths": "NoDebuff Duel Deaths",
            
            "combo_duel_wins": "Combo Duel Wins",
            "combo_duel_kills": "Combo Duel Kills",
            "combo_duel_losses": "Combo Duel Losses",
            "combo_duel_deaths": "Combo Duel Deaths",
            
            "op_duel_wins": "OP Duel Wins",
            "op_duel_kills": "OP Duel Kills",
            "op_duel_losses": "OP Duel Losses",
            "op_duel_deaths": "OP Duel Deaths",
            
            "op_doubles_wins": "OP Doubles Wins",
            "op_doubles_kills": "OP Doubles Kills",
            "op_doubles_losses": "OP Doubles Losses",
            "op_doubles_deaths": "OP Doubles Deaths",
            
            "mw_duel_wins": "MegaWalls Duel Wins",
            "mw_duel_kills": "MegaWalls Duel Kills",
            "mw_duel_losses": "MegaWalls Duel Losses",
            "mw_duel_deaths": "MegaWalls Duel Deaths",
            
            "mw_doubles_wins": "MegaWalls Doubles Wins",
            "mw_doubles_kills": "MegaWalls Doubles Kills",
            "mw_doubles_losses": "MegaWalls Doubles Losses",
            "mw_doubles_deaths": "MegaWalls Doubles Deaths",
            
            "blitz_duel_wins": "Blitz Duel Wins",
            "blitz_duel_kills": "Blitz Duel Kills",
            "blitz_duel_losses": "Blitz Duel Losses",
            "blitz_duel_deaths": "Blitz Duel Deaths",
            
            "bowspleef_duel_wins": "Bow Spleef Duel Wins",
            "bowspleef_duel_kills": "Bow Spleef Duel Kills",
            "bowspleef_duel_losses": "Bow Spleef Duel Losses",
            "bowspleef_duel_deaths": "Bow Spleef Duel Deaths",
        }
    }
    ratios = {
        "Bedwars": {
            "Overall FKDR": ("Overall F. Kills", "Overall F. Deaths"),
            "Solo FKDR": ("Solo F. Kills", "Solo F. Deaths"),
            "Doubles FKDR": ("Doubles F. Kills", "Doubles F. Deaths"),
            "3v3v3v3 FKDR": ("3v3v3v3 F. Kills", "3v3v3v3 F. Deaths"),
            "4v4v4v4 FKDR": ("4v4v4v4 F. Kills", "4v4v4v4 F. Deaths"),
            "Rush Doubles FKDR": ("Rush Doubles F. Kills", "Rush Doubles F. Deaths"),
            "Rush 4v4v4v4 FKDR": ("Rush 4v4v4v4 F. Kills", "Rush 4v4v4v4 F. Deaths"),
            "Ultimate Doubles FKDR": ("Ultimate Doubles F. Kills", "Ultimate Doubles F. Deaths"),
            "Ultimate 4v4v4v4 FKDR": ("Ultimate 4v4v4v4 F. Kills", "Ultimate 4v4v4v4 F. Deaths"),
            "Voidless Doubles FKDR": ("Voidless Doubles F. Kills", "Voidless Doubles F. Deaths"),
            "Voidless 4v4v4v4 FKDR": ("Voidless 4v4v4v4 F. Kills", "Voidless 4v4v4v4 F. Deaths"),
            "Swappage Doubles FKDR": ("Swappage Doubles F. Kills", "Swappage Doubles F. Deaths"),
            "Swappage 4v4v4v4 FKDR": ("Swappage 4v4v4v4 F. Kills", "Swappage 4v4v4v4 F. Deaths"),
            "Armed Doubles FKDR": ("Armed Doubles F. Kills", "Armed Doubles F. Deaths"),
            "Armed 4v4v4v4 FKDR": ("Armed 4v4v4v4 F. Kills", "Armed 4v4v4v4 F. Deaths"),
            "Lucky Blocks Doubles FKDR": ("Lucky Blocks Doubles F. Kills", "Lucky Blocks Doubles F. Deaths"),
            "Lucky Blocks 4v4v4v4 FKDR": ("Lucky Blocks 4v4v4v4 F. Kills", "Lucky Blocks 4v4v4v4 F. Deaths"),
            "Castle FKDR": ("Castle F. Kills", "Castle F. Deaths"),
            
            "Overall WLR": ("Overall Wins", "Overall Losses"),
            "Solo WLR": ("Solo Wins", "Solo Losses"),
            "Doubles WLR": ("Doubles Wins", "Doubles Losses"),
            "3v3v3v3 WLR": ("3v3v3v3 Wins", "3v3v3v3 Losses"),
            "4v4v4v4 WLR": ("4v4v4v4 Wins", "4v4v4v4 Losses"),
            "Rush Doubles WLR": ("Rush Doubles Wins", "Rush Doubles Losses"),
            "Rush 4v4v4v4 WLR": ("Rush 4v4v4v4 Wins", "Rush 4v4v4v4 Losses"),
            "Ultimate Doubles WLR": ("Ultimate Doubles Wins", "Ultimate Doubles Losses"),
            "Ultimate 4v4v4v4 WLR": ("Ultimate 4v4v4v4 Wins", "Ultimate 4v4v4v4 Losses"),
            "Voidless Doubles WLR": ("Voidless Doubles Wins", "Voidless Doubles Losses"),
            "Voidless 4v4v4v4 WLR": ("Voidless 4v4v4v4 Wins", "Voidless 4v4v4v4 Losses"),
            "Swappage Doubles WLR": ("Swappage Doubles Wins", "Swappage Doubles Losses"),
            "Swappage 4v4v4v4 WLR": ("Swappage 4v4v4v4 Wins", "Swappage 4v4v4v4 Losses"),
            "Armed Doubles WLR": ("Armed Doubles Wins", "Armed Doubles Losses"),
            "Armed 4v4v4v4 WLR": ("Armed 4v4v4v4 Wins", "Armed 4v4v4v4 Losses"),
            "Lucky Blocks Doubles WLR": ("Lucky Blocks Doubles Wins", "Lucky Blocks Doubles Losses"),
            "Lucky Blocks 4v4v4v4 WLR": ("Lucky Blocks 4v4v4v4 Wins", "Lucky Blocks 4v4v4v4 Losses"),
            "Castle WLR": ("Castle Wins", "Castle Losses"),
            
            "Overall BBLR": ("Overall B. Broken", "Overall B. Lost"),
            "Solo BBLR": ("Solo B. Broken", "Solo B. Lost"),
            "Doubles BBLR": ("Doubles B. Broken", "Doubles B. Lost"),
            "3v3v3v3 BBLR": ("3v3v3v3 B. Broken", "3v3v3v3 B. Lost"),
            "4v4v4v4 BBLR": ("4v4v4v4 B. Broken", "4v4v4v4 B. Lost"),
            "Rush Doubles BBLR": ("Rush Doubles B. Broken", "Rush Doubles B. Lost"),
            "Rush 4v4v4v4 BBLR": ("Rush 4v4v4v4 B. Broken", "Rush 4v4v4v4 B. Lost"),
            "Ultimate Doubles BBLR": ("Ultimate Doubles B. Broken", "Ultimate Doubles B. Lost"),
            "Ultimate 4v4v4v4 BBLR": ("Ultimate 4v4v4v4 B. Broken", "Ultimate 4v4v4v4 B. Lost"),
            "Voidless Doubles BBLR": ("Voidless Doubles B. Broken", "Voidless Doubles B. Lost"),
            "Voidless 4v4v4v4 BBLR": ("Voidless 4v4v4v4 B. Broken", "Voidless 4v4v4v4 B. Lost"),
            "Swappage Doubles BBLR": ("Swappage Doubles B. Broken", "Swappage Doubles B. Lost"),
            "Swappage 4v4v4v4 BBLR": ("Swappage 4v4v4v4 B. Broken", "Swappage 4v4v4v4 B. Lost"),
            "Armed Doubles BBLR": ("Armed Doubles B. Broken", "Armed Doubles B. Lost"),
            "Armed 4v4v4v4 BBLR": ("Armed 4v4v4v4 B. Broken", "Armed 4v4v4v4 B. Lost"),
            "Lucky Blocks Doubles BBLR": ("Lucky Blocks Doubles B. Broken", "Lucky Blocks Doubles B. Lost"),
            "Lucky Blocks 4v4v4v4 BBLR": ("Lucky Blocks 4v4v4v4 B. Broken", "Lucky Blocks 4v4v4v4 B. Lost"),
            "Castle BBLR": ("Castle B. Broken", "Castle B. Lost")
        },
        "Duels": {
            "UHC Duel WLR": ("UHC Duel Wins", "UHC Duel Losses"),
            "UHC Doubles WLR": ("UHC Doubles Wins", "UHC Doubles Losses"),
            "UHC Teams WLR": ("UHC Teams Wins", "UHC Teams Losses"), 
            "UHC Deathmatch WLR": ("UHC Deathmatch Wins", "UHC Deathmatch Losses"),
            "Bridge Duel WLR": ("Bridge Duel Wins", "Bridge Duel Losses"),
            "Bridge Doubles WLR": ("Bridge Doubles Wins", "Bridge Doubles Losses"),
            "Bridge 3v3 WLR": ("Bridge 3v3 Wins", "Bridge 3v3 Losses"),
            "Bridge Teams WLR": ("Bridge Teams Wins", "Bridge Teams Losses"),
            "Bridge 2v2v2v2 WLR": ("Bridge 2v2v2v2 Wins", "Bridge 2v2v2v2 Losses"),
            "Bridge 3v3v3v3 WLR": ("Bridge 3v3v3v3 Wins", "Bridge 3v3v3v3 Losses"),
            "Bridge CTF Threes WLR": ("Bridge CTF Threes Wins", "Bridge CTF Threes Losses"),
            "Sumo Duel WLR": ("Sumo Duel Wins", "Sumo Duel Losses"), 
            "Classic Duel WLR": ("Classic Duel Wins", "Classic Duel Losses"),
            "SkyWars Duel WLR": ("SkyWars Duel Wins", "SkyWars Duel Losses"),
            "SkyWars Doubles WLR": ("SkyWars Doubles Wins", "SkyWars Doubles Losses"),
            "Boxing Duel WLR": ("Boxing Duel Wins", "Boxing Duel Losses"),
            "Bow Duel WLR": ("Bow Duel Wins", "Bow Duel Losses"),    
            "NoDebuff Duel WLR": ("NoDebuff Duel Wins", "NoDebuff Duel Losses"),
            "Combo Duel WLR": ("Combo Duel Wins", "Combo Duel Losses"),
            "OP Duel WLR": ("OP Duel Wins", "OP Duel Losses"),       
            "OP Doubles WLR": ("OP Doubles Wins", "OP Doubles Losses"),
            "MegaWalls Duel WLR": ("MegaWalls Duel Wins", "MegaWalls Duel Losses"),
            "MegaWalls Doubles WLR": ("MegaWalls Doubles Wins", "MegaWalls Doubles Losses"),
            "Blitz Duel WLR": ("Blitz Duel Wins", "Blitz Duel Losses"),
            "Bow Spleef Duel WLR": ("Bow Spleef Duel Wins", "Bow Spleef Duel Losses"),
            
            "UHC Overall WLR": ("UHC Overall Wins", "UHC Overall Losses"),
            "Bridge Overall WLR": ("Bridge Overall Wins", "Bridge Overall Losses"),
            "SkyWars Overall WLR": ("SkyWars Overall Wins", "SkyWars Overall Losses"),
            "OP Overall WLR": ("OP Overall Wins", "OP Overall Losses"),
            "MegaWalls Overall WLR": ("MegaWalls Overall Wins", "MegaWalls Overall Losses"),
            
            "UHC Duel KDR": ("UHC Duel Kills", "UHC Duel Deaths"),
            "UHC Doubles KDR": ("UHC Doubles Kills", "UHC Doubles Deaths"),
            "UHC Teams KDR": ("UHC Teams Kills", "UHC Teams Deaths"),
            "UHC Deathmatch KDR": ("UHC Deathmatch Kills", "UHC Deathmatch Deaths"),
            "Bridge Duel KDR": ("Bridge Duel Kills", "Bridge Duel Deaths"),
            "Bridge Doubles KDR": ("Bridge Doubles Kills", "Bridge Doubles Deaths"),
            "Bridge 3v3 KDR": ("Bridge 3v3 Kills", "Bridge 3v3 Deaths"),
            "Bridge Teams KDR": ("Bridge Teams Kills", "Bridge Teams Deaths"),
            "Bridge 2v2v2v2 KDR": ("Bridge 2v2v2v2 Kills", "Bridge 2v2v2v2 Deaths"),
            "Bridge 3v3v3v3 KDR": ("Bridge 3v3v3v3 Kills", "Bridge 3v3v3v3 Deaths"),
            "Bridge CTF Threes KDR": ("Bridge CTF Threes Kills", "Bridge CTF Threes Deaths"),
            "Sumo Duel KDR": ("Sumo Duel Kills", "Sumo Duel Deaths"),
            "Classic Duel KDR": ("Classic Duel Kills", "Classic Duel Deaths"),
            "SkyWars Duel KDR": ("SkyWars Duel Kills", "SkyWars Duel Deaths"),
            "SkyWars Doubles KDR": ("SkyWars Doubles Kills", "SkyWars Doubles Deaths"),
            "Boxing Duel KDR": ("Boxing Duel Kills", "Boxing Duel Deaths"),
            "Bow Duel KDR": ("Bow Duel Kills", "Bow Duel Deaths"),   
            "NoDebuff Duel KDR": ("NoDebuff Duel Kills", "NoDebuff Duel Deaths"),
            "Combo Duel KDR": ("Combo Duel Kills", "Combo Duel Deaths"),
            "OP Duel KDR": ("OP Duel Kills", "OP Duel Deaths"),      
            "OP Doubles KDR": ("OP Doubles Kills", "OP Doubles Deaths"),
            "MegaWalls Duel KDR": ("MegaWalls Duel Kills", "MegaWalls Duel Deaths"),
            "MegaWalls Doubles KDR": ("MegaWalls Doubles Kills", "MegaWalls Doubles Deaths"),
            "Blitz Duel KDR": ("Blitz Duel Kills", "Blitz Duel Deaths"),
            "Bow Spleef Duel KDR": ("Bow Spleef Duel Kills", "Bow Spleef Duel Deaths"),
            
            "UHC Overall KDR": ("UHC Overall Kills", "UHC Overall Deaths"),
            "Bridge Overall KDR": ("Bridge Overall Kills", "Bridge Overall Deaths"),
            "SkyWars Overall KDR": ("SkyWars Overall Kills", "SkyWars Overall Deaths"),
            "OP Overall KDR": ("OP Overall Kills", "OP Overall Deaths"),
            "MegaWalls Overall KDR": ("MegaWalls Overall Kills", "MegaWalls Overall Deaths")
        }
    }
    if "success" in data and "player" in data:
        if data["success"] and data["player"]:
            if "stats" in data["player"] and "achievements" in data["player"]:
                if "Bedwars" in data["player"]["stats"] and "Duels" in data["player"]["stats"]:
                    stats = {}
                    for key, mode in mapping.items():
                        stats[key] = {}
                        for source, target in mode.items():
                            stats[key][target] = data["player"]["stats"][key].get(source, 0)
                            
                        if key == "Bedwars":
                            boxes = data["player"]["stats"]["Bedwars"].get("bedwars_boxes", 0)
                            christmas = data["player"]["stats"]["Bedwars"].get("bedwars_christmas_boxes", 0)
                            haloween = data["player"]["stats"]["Bedwars"].get("bedwars_halloween_boxes", 0)
                            easter = data["player"]["stats"]["Bedwars"].get("bedwars_easter_boxes", 0)
                            lunar = data["player"]["stats"]["Bedwars"].get("bedwars_lunar_boxes", 0)
                            golden = data["player"]["stats"]["Bedwars"].get("bedwars_golden_boxes", 0)
                            loot_chests_all = boxes + christmas + haloween + easter + lunar + golden
                            
                            modes = ['', 'eight_two_rush_', 'four_four_rush_', 'eight_two_ultimate_', 'four_four_ultimate_', 'eight_two_voidless_', 'four_four_voidless_', 'eight_two_swap_', 'four_four_swap_', 'eight_two_armed_', 'four_four_armed_', 'eight_two_lucky_', 'four_four_lucky_', 'castle_']
                            iron_collected = sum([data["player"]["stats"]["Bedwars"].get(f"{mode}iron_resources_collected_bedwars", 0) for mode in modes])
                            gold_collected = sum([data["player"]["stats"]["Bedwars"].get(f"{mode}gold_resources_collected_bedwars", 0) for mode in modes])
                            diamonds_collected = sum([data["player"]["stats"]["Bedwars"].get(f"{mode}diamond_resources_collected_bedwars", 0) for mode in modes])
                            emeralds_collected = sum([data["player"]["stats"]["Bedwars"].get(f"{mode}emerald_resources_collected_bedwars", 0) for mode in modes])
                            
                            stats["Bedwars"].update({
                                "Stars": data["player"]["achievements"].get("bedwars_level", 0), 
                                "Loot Chests": loot_chests_all,
                                "Iron Collected": iron_collected,
                                "Gold Collected": gold_collected,
                                "Diamonds Collected": diamonds_collected,
                                "Emeralds Collected": emeralds_collected
                                })
                            
                        elif key == "Duels":
                            uhc_wins = sum((stats["Duels"]["UHC Duel Wins"], stats["Duels"]["UHC Doubles Wins"], stats["Duels"]["UHC Teams Wins"], stats["Duels"]["UHC Deathmatch Wins"]))
                            uhc_kills = sum((stats["Duels"]["UHC Duel Kills"], stats["Duels"]["UHC Doubles Kills"], stats["Duels"]["UHC Teams Kills"], stats["Duels"]["UHC Deathmatch Kills"]))
                            uhc_losses = sum((stats["Duels"]["UHC Duel Losses"], stats["Duels"]["UHC Doubles Losses"], stats["Duels"]["UHC Teams Losses"], stats["Duels"]["UHC Deathmatch Losses"]))
                            uhc_deaths = sum((stats["Duels"]["UHC Duel Deaths"], stats["Duels"]["UHC Doubles Deaths"], stats["Duels"]["UHC Teams Deaths"], stats["Duels"]["UHC Deathmatch Deaths"]))
                            
                            bridge_wins = sum((stats["Duels"]["Bridge Duel Wins"], stats["Duels"]["Bridge Doubles Wins"], stats["Duels"]["Bridge 3v3 Wins"], stats["Duels"]["Bridge Teams Wins"], stats["Duels"]["Bridge 2v2v2v2 Wins"], stats["Duels"]["Bridge 3v3v3v3 Wins"], stats["Duels"]["Bridge CTF Threes Wins"]))
                            bridge_kills = sum((stats["Duels"]["Bridge Duel Kills"], stats["Duels"]["Bridge Doubles Kills"], stats["Duels"]["Bridge 3v3 Kills"], stats["Duels"]["Bridge Teams Kills"], stats["Duels"]["Bridge 2v2v2v2 Kills"], stats["Duels"]["Bridge 3v3v3v3 Kills"], stats["Duels"]["Bridge CTF Threes Kills"]))
                            bridge_losses = sum((stats["Duels"]["Bridge Duel Losses"], stats["Duels"]["Bridge Doubles Losses"], stats["Duels"]["Bridge 3v3 Losses"], stats["Duels"]["Bridge Teams Losses"], stats["Duels"]["Bridge 2v2v2v2 Losses"], stats["Duels"]["Bridge 3v3v3v3 Losses"], stats["Duels"]["Bridge CTF Threes Losses"]))
                            bridge_deaths = sum((stats["Duels"]["Bridge Duel Deaths"], stats["Duels"]["Bridge Doubles Deaths"], stats["Duels"]["Bridge 3v3 Deaths"], stats["Duels"]["Bridge Teams Deaths"], stats["Duels"]["Bridge 2v2v2v2 Deaths"], stats["Duels"]["Bridge 3v3v3v3 Deaths"], stats["Duels"]["Bridge CTF Threes Deaths"]))
                            
                            sw_wins = sum((stats["Duels"]["SkyWars Duel Wins"], stats["Duels"]["SkyWars Doubles Wins"]))
                            sw_kills = sum((stats["Duels"]["SkyWars Duel Kills"], stats["Duels"]["SkyWars Doubles Kills"]))
                            sw_losses = sum((stats["Duels"]["SkyWars Duel Losses"], stats["Duels"]["SkyWars Doubles Losses"]))
                            sw_deaths = sum((stats["Duels"]["SkyWars Duel Deaths"], stats["Duels"]["SkyWars Doubles Deaths"]))
                            
                            op_wins = sum((stats["Duels"]["OP Duel Wins"], stats["Duels"]["OP Doubles Wins"]))
                            op_kills = sum((stats["Duels"]["OP Duel Kills"], stats["Duels"]["OP Doubles Kills"]))  
                            op_losses = sum((stats["Duels"]["OP Duel Losses"], stats["Duels"]["OP Doubles Losses"]))
                            op_deaths = sum((stats["Duels"]["OP Duel Deaths"], stats["Duels"]["OP Doubles Deaths"]))
                            
                            mw_wins = sum((stats["Duels"]["MegaWalls Duel Wins"], stats["Duels"]["MegaWalls Doubles Wins"]))
                            mw_kills = sum((stats["Duels"]["MegaWalls Duel Kills"], stats["Duels"]["MegaWalls Doubles Kills"]))
                            mw_losses = sum((stats["Duels"]["MegaWalls Duel Losses"], stats["Duels"]["MegaWalls Doubles Losses"]))
                            mw_deaths = sum((stats["Duels"]["MegaWalls Duel Deaths"], stats["Duels"]["MegaWalls Doubles Deaths"]))
                            
                            stats["Duels"].update({
                                "UHC Overall Wins": uhc_wins, 
                                "UHC Overall Kills": uhc_kills, 
                                "UHC Overall Losses": uhc_losses, 
                                "UHC Overall Deaths": uhc_deaths,
                                
                                "Bridge Overall Wins": bridge_wins, 
                                "Bridge Overall Kills": bridge_kills, 
                                "Bridge Overall Losses": bridge_losses, 
                                "Bridge Overall Deaths": bridge_deaths,
                                
                                "SkyWars Overall Wins": sw_wins, 
                                "SkyWars Overall Kills": sw_kills, 
                                "SkyWars Overall Losses": sw_losses, 
                                "SkyWars Overall Deaths": sw_deaths,
                                
                                "OP Overall Wins": op_wins, 
                                "OP Overall Kills": op_kills, 
                                "OP Overall Losses": op_losses, 
                                "OP Overall Deaths": op_deaths,
                                
                                "MegaWalls Overall Wins": mw_wins, 
                                "MegaWalls Overall Kills": mw_kills, 
                                "MegaWalls Overall Losses": mw_losses, 
                                "MegaWalls Overall Deaths": mw_deaths,
                                })
                            
                    for key, mode in ratios.items():
                        for stat, (dividend, divisor) in mode.items():
                            stats[key][stat] = calc_ratio(stats[key][dividend], stats[key][divisor])
                            
                    
                    rank = get_rank(data)
                    displayname = data["player"]["displayname"]
   
                    return StatsList(Bedwars(stats["Bedwars"]), Duels(stats["Duels"]), displayname, rank)
                else:
                    print(f"Not success 4: ({uuid})")
            else:
                print(f"Not success 3: ({uuid})")
        else:
            print(f"Not success 2: ({uuid})")
    else:
        print(f"Not success 1: ({uuid})")
    return None

_rank = {
    "§c[OWNER]": OWNER,
    "§d[PIG§b+++§d]": PIG,
    "§6[MOJANG]": MOJANG,
    "§6[EVENTS]": EVENTS,
    "YOUTUBER": YOUTUBE,
    "ADMIN": ADMIN,
    "GAME_MASTER": GAMEMASTER,
    "MVP": NMVP,
    "VIP_PLUS": VIP,
    "VIP": NVIP
}

_b_plus = {
    "RED": BRED,
    "ORANGE": BORANGE,
    "GREEN": BGREEN,
    "YELLOW": BYELLOW,
    "LIGHT_PURPLE": BPINK,
    "WHITE": BWHITE,
    "BLUE": BBLUE,
    "DARK_GREEN": BDARKGREEN,
    "DARK_RED": BDARKRED,
    "DARK_AQUA": BAQUA,
    "DARK_PURPLE": BPURPLE,
    "DARK_GRAY": BGRAY,
    "BLACK": BBLACK,
    "DARK_BLUE": BDARKBLUE
}

_g_plus = {
    "RED": GRED,
    "ORANGE": GORANGE,
    "GREEN": GGREEN,
    "YELLOW": GYELLOW,
    "LIGHT_PURPLE": GPINK,
    "WHITE": GWHITE,
    "BLUE": GBLUE,
    "DARK_GREEN": GDARKGREEN,
    "DARK_RED": GDARKRED,
    "DARK_AQUA": GAQUA,
    "DARK_PURPLE": GPURPLE,
    "DARK_GRAY": GGRAY,
    "BLACK": GBLACK,
    "DARK_BLUE": GDARKBLUE
}

_plus = {
    "RED": RED,
    "ORANGE": ORANGE,
    "GREEN": GREEN,
    "YELLOW": YELLOW,
    "LIGHT_PURPLE": PINK,
    "WHITE": WHITE,
    "BLUE": BLUE,
    "DARK_GREEN": DARKGREEN,
    "DARK_RED": DARKRED,
    "DARK_AQUA": AQUA,
    "DARK_PURPLE": PURPLE,
    "DARK_GRAY": GRAY,
    "BLACK": BLACK,
    "DARK_BLUE": DARKBLUE
}

def get_rank(data):
    player = data.get("player", None)
    if not player:
        return
    custom_prefix = player.get("prefix", None)
    if custom_prefix:
        return _rank.get(custom_prefix, custom_prefix)
    
    rank = player.get("rank", None)
    if rank:
        return _rank.get(rank, rank)
    rankPlusColor = player.get("rankPlusColor", None)
    monthlyPackageRank = player.get("monthlyPackageRank", None)
    if monthlyPackageRank != "NONE" and monthlyPackageRank:
        monthlyRankColor = player.get("monthlyRankColor", None)
        
        if monthlyRankColor == "AQUA":
            plus = _b_plus.get(rankPlusColor, BRED)
            return BMVP+plus
            
        plus = _g_plus.get(rankPlusColor, GRED)
        return GMVP+plus
    
    newPackageRank = player.get("newPackageRank", None)
    if newPackageRank == "MVP_PLUS":
        plus = _plus.get(rankPlusColor, RED)
        return MVP+plus
        
    return _rank.get(newPackageRank, "")
        
async def get_stats(data: dict, mode: str) -> dict[str, int | float] | list[dict[str, int] | list[int]] | list[int] | None:
    if "success" in data and "player" in data:
        if data["success"] and data["player"]:
            if "stats" in data["player"] and "achievements" in data["player"]:
                if "Bedwars" in data["player"]["stats"]:
                    bw_level = data["player"]["achievements"].get("bedwars_level", 0)
                    bw_exp = data["player"]["stats"]["Bedwars"].get("Experience", 0)
                    bw_final_kills = data["player"]["stats"]["Bedwars"].get(mode+"final_kills_bedwars", 0)
                    bw_final_deaths = data["player"]["stats"]["Bedwars"].get(mode+"final_deaths_bedwars", 0)        
                    bw_wins = data["player"]["stats"]["Bedwars"].get(mode+"wins_bedwars", 0)
                    bw_losses = data["player"]["stats"]["Bedwars"].get(mode+"losses_bedwars", 0)
                    bw_beds_broken = data["player"]["stats"]["Bedwars"].get(mode+"beds_broken_bedwars", 0)
                    bw_beds_lost = data["player"]["stats"]["Bedwars"].get(mode+"beds_lost_bedwars", 0)
                    bw_kills = data["player"]["stats"]["Bedwars"].get(mode+"kills_bedwars", 0)
                    bw_deaths = data["player"]["stats"]["Bedwars"].get(mode+"deaths_bedwars", 0)
                    bw_games = data["player"]["stats"]["Bedwars"].get(mode+"games_played_bedwars", 1)
                    coins = data["player"]["stats"]["Bedwars"].get("coins", 0)
                    boxes = data["player"]["stats"]["Bedwars"].get("bedwars_boxes", 0)
                    christmas = data["player"]["stats"]["Bedwars"].get("bedwars_christmas_boxes", 0)
                    haloween = data["player"]["stats"]["Bedwars"].get("bedwars_halloween_boxes", 0)
                    easter = data["player"]["stats"]["Bedwars"].get("bedwars_easter_boxes", 0)
                    lunar = data["player"]["stats"]["Bedwars"].get("bedwars_lunar_boxes", 0)
                    golden = data["player"]["stats"]["Bedwars"].get("bedwars_golden_boxes", 0)
                    solo_wins = data["player"]["stats"]["Bedwars"].get("eight_one_wins_bedwars", 0)
                    doubles_wins = data["player"]["stats"]["Bedwars"].get("eight_two_wins_bedwars", 0)
                    threes_wins = data["player"]["stats"]["Bedwars"].get("four_three_wins_bedwars", 0)
                    fours_wins = data["player"]["stats"]["Bedwars"].get("four_four_wins_bedwars", 0)
                    fives_wins = data["player"]["stats"]["Bedwars"].get("two_four_wins_bedwars", 0)
                    solo_final_kills = data["player"]["stats"]["Bedwars"].get("eight_one_final_kills_bedwars", 0)   
                    doubles_final_kills = data["player"]["stats"]["Bedwars"].get("eight_two_final_kills_bedwars", 0)
                    threes_final_kills = data["player"]["stats"]["Bedwars"].get("four_three_final_kills_bedwars", 0)
                    fours_final_kills = data["player"]["stats"]["Bedwars"].get("four_four_final_kills_bedwars", 0)  
                    fives_final_kills = data["player"]["stats"]["Bedwars"].get("two_four_final_kills_bedwars", 0)   
                    solo_beds_broken = data["player"]["stats"]["Bedwars"].get("eight_one_beds_broken_bedwars", 0)
                    doubles_beds_broken = data["player"]["stats"]["Bedwars"].get("eight_two_beds_broken_bedwars", 0)
                    threes_beds_broken = data["player"]["stats"]["Bedwars"].get("four_three_beds_broken_bedwars", 0)
                    fours_beds_broken = data["player"]["stats"]["Bedwars"].get("four_four_beds_broken_bedwars", 0)
                    fives_beds_broken = data["player"]["stats"]["Bedwars"].get("two_four_beds_broken_bedwars", 0)
                    solo_kills = data["player"]["stats"]["Bedwars"].get("eight_one_kills_bedwars", 0)
                    doubles_kills = data["player"]["stats"]["Bedwars"].get("eight_two_kills_bedwars", 0)
                    threes_kills = data["player"]["stats"]["Bedwars"].get("four_three_kills_bedwars", 0)
                    fours_kills = data["player"]["stats"]["Bedwars"].get("four_four_kills_bedwars", 0)
                    fives_kills = data["player"]["stats"]["Bedwars"].get("two_four_kills_bedwars", 0)
                    winstreak = data["player"]["stats"]["Bedwars"].get("winstreak", 0)
                    solo_winstreak = data["player"]["stats"]["Bedwars"].get("eight_one_winstreak", 0)
                    doubles_winstreak = data["player"]["stats"]["Bedwars"].get("eight_two_winstreak", 0)
                    threes_winstreak = data["player"]["stats"]["Bedwars"].get("four_three_winstreak", 0)
                    fours_winstreak = data["player"]["stats"]["Bedwars"].get("four_four_winstreak", 0)
                    fives_winstreak = data["player"]["stats"]["Bedwars"].get("two_four_winstreak", 0)
                    loot_chests_all = boxes + christmas + haloween + easter + lunar + golden
                    bw_wlr = calc_ratio(bw_wins, bw_losses)
                    bw_fkdr = calc_ratio(bw_final_kills, bw_final_deaths)
                    bw_kdr = calc_ratio(bw_kills, bw_deaths)
                    bw_bblr = calc_ratio(bw_beds_broken, bw_beds_lost)

                    return {"Stars": bw_level, "Bedwars Experience": bw_exp, "Wins": bw_wins, "Losses": bw_losses, "Final Kills": bw_final_kills,"Final Deaths": bw_final_deaths, "Kills": bw_kills, "Games": bw_games, 
                    "Deaths": bw_deaths, "Beds Broken": bw_beds_broken, "Beds Lost": bw_beds_lost, "WLR": bw_wlr, "FKDR": bw_fkdr, "KDR": bw_kdr, "BBLR": bw_bblr, "Coins": coins, "Loot Chests": loot_chests_all}, \
                    [{"Solo": solo_wins, "Doubles": doubles_wins, "Threes": threes_wins, "Fours":  fours_wins, "4v4": fives_wins}, [solo_final_kills, doubles_final_kills, threes_final_kills, fours_final_kills, fives_final_kills], 
                    [solo_beds_broken, doubles_beds_broken, threes_beds_broken, fours_beds_broken, fives_beds_broken], [solo_kills, doubles_kills, threes_kills, fours_kills, fives_kills]], \
                    [winstreak, solo_winstreak, doubles_winstreak, threes_winstreak, fours_winstreak, fives_winstreak]
    return None, None, None