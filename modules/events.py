import nextcord
from nextcord.ext import commands
from bot import Bot
from database import Database

class Events(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.session = Bot.session
        
    @commands.Cog.listener()
    async def on_guild_join(self, guild: nextcord.Guild):
        Database.insert_one("guilds", {"_id": str(guild.id), "users": [], "channels": {}})

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: nextcord.Guild):
        Database.delete_one("guilds", {"_id": str(guild.id)})
        
def setup(bot: Bot):
    bot.add_cog(Events(bot))