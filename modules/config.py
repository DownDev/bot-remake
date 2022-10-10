import nextcord
from nextcord.ext import commands
from nextcord import Interaction, ButtonStyle, Embed, TextChannel
from bot import Bot
from utils import *
from database import Database
import cooldowns

class ConfigButton(nextcord.ui.Button):
    def __init__(self, value: bool, row: int):
        self.value = value
        
        emoji = "✅" if value else CROSS
        style = ButtonStyle.green if value else ButtonStyle.red
        
        super().__init__(emoji=emoji, style=style, row=row)
        
    async def callback(self, interaction: Interaction):
        self.value = not self.value
        
        self.emoji = "✅" if self.value else CROSS
        self.style = ButtonStyle.green if self.value else ButtonStyle.red
        
        await interaction.response.edit_message(view=self.view)
        
class SaveButton(nextcord.ui.Button):
    buttons: list[ConfigButton]
        
    def __init__(self, buttons, label, row):
        super().__init__(label=label, style=ButtonStyle.blurple, row=row)
        
        self.buttons = buttons
        self.row = row
        
    async def callback(self, interaction: Interaction):
        guild = str(interaction.guild.id)
        channel = str(self.view.current)
        values = []
        for button in self.buttons:
            values.append(button.value)

        self.view.users[self.view.user_names[self.row-1]] = {"bedwars": values[0], "duels": values[1]}
        
        Database.update_one("guilds", {"_id": guild}, {"$set": {f"channels.{channel}.{self.view.user_names[self.row-1]}": {"bedwars": values[0], "duels": values[1]}}})
        
        msg = Embed(title="Succesfully saved", description=f"` > ` {self.view.names[self.view.user_names[self.row-1]]}", color=CLEANCOLOR)
        await interaction.send(embed=msg, ephemeral=True)
        
            
class SaveAllButton(nextcord.ui.Button):
    buttons: list[list[ConfigButton]]
    
    def __init__(self, buttons, label, disabled, row):
        super().__init__(label=label, style=ButtonStyle.blurple, disabled=disabled, row=row)
        
        self.buttons = buttons
        
    async def callback(self, interaction: Interaction):
        guild = str(interaction.guild.id)
        channel = str(self.view.current)
        for row, buttons in enumerate(self.buttons):
            values = []
            for button in buttons:
                values.append(button.value)

            self.view.users[self.view.user_names[row]] = {"bedwars": values[0], "duels": values[1]}
            
            Database.update_one("guilds", {"_id": guild}, {"$set": {f"channels.{channel}.{self.view.user_names[row]}": {"bedwars": values[0], "duels": values[1]}}})
            
        msg = Embed(title="Succesfully saved", description="\n".join(f"` > ` {name}" for name in self.view.names.values()), color=CLEANCOLOR)
        await interaction.send(embed=msg, ephemeral=True)

class RemoveButton(nextcord.ui.Button):
    def __init__(self, label, row):
        super().__init__(label=label, style=ButtonStyle.red, row=row)

        self.row = row
        self.session = Bot.session
        
    async def callback(self, interaction: Interaction):
        guild = str(interaction.guild.id)
        channel = str(self.view.current)
        
        result = Database.find_one("guilds", {"_id": guild})
        if not result:
            await interaction.send(embed=ErrorEmbed("Database error", "Report this if issue persists"), ephemeral=True)
            return
        
        uuid = self.view.user_names[self.row-1]
        
        channels = result["channels"]
        result["users"].remove(uuid)
        
        for k in channels:
            result["channels"][k].pop(uuid)
        
        Database.update_one("guilds", {"_id": guild}, {"$set": {"channels": result["channels"], "users": result["users"]}})
        
        users_data = self.view.users
        users_data.pop(uuid, None)
        embed, names = await gen_embed(users_data, channel, self.session)
        self.view.stop()
        await self.view.message.edit(embed=embed, view=MyView(users_data, names, channel, self.view.message))
        msg = Embed(title="Removed users", description=f"` - ` {self.view.names[uuid]}", color=CLEANCOLOR)
        await interaction.send(embed=msg, ephemeral=True)
    
class RemoveAllButton(nextcord.ui.Button):
    def __init__(self, label, disabled, row):
        super().__init__(label=label, style=ButtonStyle.red, disabled=disabled, row=row)
        
        self.session = Bot.session
        
    async def callback(self, interaction: Interaction):
        guild = str(interaction.guild.id)
        channel = str(self.view.current)

        result = Database.find_one("guilds", {"_id": guild})
        if not result:
            await interaction.send(embed=ErrorEmbed("Database error", "Report this if issue persists"), ephemeral=True)
            return
        
        channels = result["channels"]
        for k in channels:
            result["channels"][k] = {}
        
        Database.update_one("guilds", {"_id": guild}, {"$set": {"channels": result["channels"], "users": []}})
        
        users_data = {}

        embed, names = await gen_embed(users_data, channel, self.session)
        self.view.stop()
        await self.view.message.edit(embed=embed, view=MyView(users_data, names, channel, self.view.message))
        msg = Embed(title="Removed users", description="\n".join(f"` - ` {name}" for name in self.view.names.values()), color=CLEANCOLOR)
        await interaction.send(embed=msg, ephemeral=True)
    

class AddingModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("Add player")
        
        self.player = nextcord.ui.TextInput(
            label="Player nickname",
            placeholder="Enter a player's name...",
            required=True,
            max_length=16,
        )
        self.add_item(self.player)
        
    async def callback(self, interaction: Interaction):
        self.stop()

class AddUser(nextcord.ui.Button):
    def __init__(self, label, disabled, row):
        super().__init__(label=label, style=ButtonStyle.green, disabled=disabled, row=row)
        
        
    async def callback(self, interaction: Interaction):
        modal = AddingModal()
        await interaction.response.send_modal(modal)
        await modal.wait()

        session = Bot.session
        
        name = modal.player.value.strip()

        uuid, _ = await get_uuid(name, session)

        if not uuid:
            await interaction.send(embed=ErrorEmbed("Invalid player", f"Player named **`{name}`** does not exist!"), ephemeral=True)
            return
        
        data = await ifexists(uuid, session, full_check=False)
        if not data:
            await interaction.send(embed=ErrorEmbed("Invalid player", f"Player named **`{name}`** never has played on Hypixel!"), ephemeral=True)
            return
        
        guild = str(interaction.guild.id)
        channel = str(self.view.current)
        
        result = Database.find_one("guilds", {"_id": guild})
        if not result:
            await interaction.send(embed=ErrorEmbed("Database error", "Report this if issue persists"), ephemeral=True)
            return
        
        users = result.get("users", [])
        if uuid in users:
            await interaction.send(embed=ErrorEmbed("Player already registered", "..."), ephemeral=True) # TODO: add error message
            return
        
        result["users"].append(uuid)
        
        channels = result["channels"]
        for k in channels:
            result["channels"][k][uuid] = {"bedwars": False, "duels": False}
        
        users_data = self.view.users
        users_data[uuid] = {"bedwars": False, "duels": False}

        embed, names = await gen_embed(users_data, channel, session)
        if not all([embed, names]):
            await interaction.send(embed=ErrorEmbed("Invalid player", f"Player named **`{name}`** never has played on Hypixel!"), ephemeral=True)
            return
        
        Bot.main.update({uuid: await track(data, uuid)})
        Database.update_one("guilds", {"_id": guild}, {"$set": {"channels": result["channels"], "users": result["users"]}})
        self.view.stop()
        await self.view.message.edit(embed=embed, view=MyView(users_data, names, channel, self.view.message))
        msg = Embed(title="Added users", description=f"` + ` {list(names.values())[-1]}", color=CLEANCOLOR)
        await interaction.send(embed=msg, ephemeral=True)

class MyView(nextcord.ui.View):
    message: nextcord.PartialInteractionMessage | nextcord.WebhookMessage
    
    def __init__(self, users: dict[str, dict[str, bool]], names: dict[str, str], current: str, message = None):
        super().__init__(timeout=20)

        if message:
            self.message = message
        self.names = names
        self.current = current
        self.users = users
        self.user_names = list(users.keys())
        
        modes = ("<:bedwars:1017540243563495476>", "<:duels:1017540258931429458>")

        self.add_item(nextcord.ui.Button(label="\u200b", style=ButtonStyle.gray))
        
        for mode in modes:
            self.add_item(nextcord.ui.Button(emoji=mode, style=ButtonStyle.blurple))
        
        self.add_item(nextcord.ui.Button(label="⠀⠀⠀⠀⠀", style=ButtonStyle.gray))
        
        self.add_item(nextcord.ui.Button(label="⠀⠀⠀⠀           ⠀", style=ButtonStyle.gray))
        
        all_buttons = []
        
        for i, user in enumerate(users.values(), 1):
            self.add_item(nextcord.ui.Button(emoji=NUMBERS.get(i, i), style=ButtonStyle.blurple, row=i))
            
            buttons = []
            
            for value in user.values():
                config = ConfigButton(value=value, row=i)
                buttons.append(config)
                self.add_item(config)
                
            self.add_item(SaveButton(buttons=buttons, label="⠀Save⠀", row=i))
            
            self.add_item(RemoveButton(label="     Remove     ", row=i))
            
            all_buttons.append(buttons)
        
        last = len(users) + 1
        
        if last >= 4:
            self.add_item(AddUser("Add", disabled=True, row=last))
        else:
            self.add_item(AddUser("Add", disabled=False, row=last))
        
        self.add_item(nextcord.ui.Button(label="\u200b", style=ButtonStyle.gray, row=last))
        self.add_item(nextcord.ui.Button(label="\u200b", style=ButtonStyle.gray, row=last))
        
        if last <= 1:
            self.add_item(SaveAllButton(buttons=all_buttons, label="Save all ", disabled=True, row=last))
            self.add_item(RemoveAllButton(label="Remove all", disabled=True, row=last))
        else:
            self.add_item(SaveAllButton(buttons=all_buttons, label="Save all ", disabled=False, row=last))
            self.add_item(RemoveAllButton(label="Remove all", disabled=False, row=last))
            
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        try:
            await self.message.edit(view=self)
        except Exception as e:
            print(e)
        # try:
        #     await self.message.edit(view=None)
        # except Exception as e:
        #     print(e)

async def gen_embed(users_data, channel_id, session):
    description = f"**Managing**: <#{channel_id}>\n**Users**:\n"
    names = {}
    for i, uuid in enumerate(users_data, 1):
        uuid, displayname = await get_uuid(uuid, session)
        data = await ifexists(uuid, session, full_check=False)
        if not data:
            return None, None
        
        rank = get_rank(data)
        names[uuid] = rank+displayname
        
        description += f"{NUMBERS.get(i, i)} {rank}{displayname}\n"

    return Embed(title=f"{len(users_data)} Users registered", description=description, color=CLEANCOLOR), names

class Config(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.session = Bot.session
        
    @nextcord.slash_command(name="channel", guild_ids=GUILD_IDS)
    async def channel(self, interaction: Interaction):
        pass    
    
    @channel.subcommand(name="config", description="Manage channel")
    # @cooldowns.cooldown(1, 300, bucket=cooldowns.SlashBucket.guild) # TODO: check this cooldown
    async def _channel_config(self, interaction: Interaction, channel: nextcord.TextChannel = None):
        await interaction.response.defer()

        result = Database.find_one("guilds", {"_id": str(interaction.guild.id)})
        if not result:
            await interaction.send(embed=ErrorEmbed("Database error", "Report this if issue persists"), ephemeral=True)
            return
        
        channel = channel or interaction.channel
        current = str(channel.id)
        
        channels = result["channels"]

        users_data = channels.get(current, None)
        if users_data is None:
            await interaction.send(embed=ErrorEmbed("Channel not registered", "This channel is not added to bot's channels. Register it using </channel register:1019954199796133928>"), ephemeral=True)
            return

        embed, names = await gen_embed(users_data, current, self.session)
        view = MyView(users_data, names, current)
        view.message = await interaction.send(embed=embed, view=view)

    @channel.subcommand(name="register", description="Adds channel")
    async def _register_channel(self, interaction: Interaction, channel: TextChannel = None):
        guild = str(interaction.guild.id)
        result = Database.find_one("guilds", {"_id": guild})
        if not result:
            await interaction.send(embed=ErrorEmbed("Database error", "Report this if issue persists"), ephemeral=True)
            return
        
        channels = result["channels"]
        if len(channels) >= 6:
            await interaction.send(embed=ErrorEmbed("Maximum amount of channels", "You already registered maximum amount of channels possible, you can always remove one using </channel remove:123>"))
            return
        
        channel = channel or interaction.channel
        new = str(channel.id)
        
        if new in channels:
            await interaction.send(embed=ErrorEmbed("Channel already registered", f"{channel.mention} is already registered"), ephemeral=True)
            return
        
        users = result.get("users", [])
        
        clone = {uuid: {"bedwars": False, "duels": False} for uuid in users}
        
        result["channels"][new] = clone
        
        Database.update_one("guilds", {"_id": guild}, {"$set": {"channels": result["channels"]}})
        embed = Embed(title=f"Succesfully added", description=f"**Added**:\n` + ` {channel.mention}", color=CLEANCOLOR)
        await interaction.send(embed=embed)

    @channel.subcommand(name="unregister", description="Removes channel")
    async def _unregister_channel(self, interaction: Interaction, channel: TextChannel = None):
        guild = str(interaction.guild.id)
        result = Database.find_one("guilds", {"_id": guild})
        if not result:
            await interaction.send(embed=ErrorEmbed("Database error", "Report this if issue persists"), ephemeral=True)
            return
        
        channels = result["channels"]
        
        channel = channel or interaction.channel
        new = str(channel.id)
        
        if new not in channels:
            await interaction.send(embed=ErrorEmbed("Channel not registered", f"{channel.mention} is not registered"), ephemeral=True)
            return
        
        result["channels"].pop(new, None)
        
        Database.update_one("guilds", {"_id": guild}, {"$set": {"channels": result["channels"]}})
        embed = Embed(title=f"Succesfully removed", description=f"**Removed**:\n` - ` {channel.mention}", color=CLEANCOLOR)
        await interaction.send(embed=embed)
        
    @channel.subcommand(name="info", description="Lists all registered channels")
    async def _info_channels(self, interaction: Interaction):
        guild = str(interaction.guild.id)
        result = Database.find_one("guilds", {"_id": guild})
        if not result:
            await interaction.send(embed=ErrorEmbed("Database error", "Report this if issue persists"), ephemeral=True)
            return
        
        channels = result["channels"]
        if not channels:
            embed = Embed(title="None channels defined", description="You didnt register any channels yet. Register one using </channel register:0>")
            await interaction.send(embed=embed)
            return
        
        description = "**Users**:\n"
        
        users = result.get("users", [])
        for uuid in users:
            uuid, displayname = await get_uuid(uuid, self.session)
            data = await ifexists(uuid, self.session, full_check=False)
            rank = get_rank(data)
            description += f"` > ` {rank} {displayname}\n"
        
        description += "\n**Channels**:\n"
        
        for channel_id in channels:
            channel = self.bot.get_channel(int(channel_id)) or await self.bot.fetch_channel(int(channel_id))
            description += f"` > ` {channel.mention}\n"
        
        embed = Embed(title=f"**`{nextcord.utils.escape_markdown(interaction.guild.name)}` Information**", description=description, color=CLEANCOLOR)
        
        await interaction.send(embed=embed)

def setup(bot: Bot):
    bot.add_cog(Config(bot))