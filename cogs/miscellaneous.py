import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands import locale_str as _T, Choice

from typing import Literal

class Miscellaneous(commands.Cog):
    """
        Miscellaneous Commands
    """
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Miscellaneous Category Loaded")

    @app_commands.command(name = _T("about"), description = _T("Information about the bot, in english only."))
    async def about(self,interaction:discord.Interaction):
        embed = discord.Embed(title = "Ena Bot",description = "A translator bot designed for TheGenshinPlace for use in r/Place 2023.\nCreated and maintained by ChuGames#0001")
        embed.add_field(name = "Command List",value = "`/translate <text> [destination]`\n\n`<text>` The text to be translated.\n`[destination]` The destination language. If not specified, local client language is used.",inline = False)
        embed.add_field(name = "Supported Languages",value = "**Client Command Information:** `en`,`zh-cn`,`zh-tw`,`ja`\n**Optional Destination Languages:** `en`,`zh-cn`,`zh-tw`,`ja`,`ko`,`es`\n\nAll local client languages are supported to be translated to, and the bot is able to translate from most common languages.",inline = False)
        embed.add_field(name = "Libraries Used",value = "discord.py (https://github.com/Rapptz/discord.py)\npy-googletrans (https://github.com/ssut/py-googletrans)\nlanguagecodes (https://github.com/alephdata/languagecodes)",inline = False)
        embed.add_field(name = "Developer Information",value = "This bot is part of the Paradise Bot Team, which includes `Serenity Bot#0271` and `Oasis Bot#8212`, and is coded by `ChuGames#0001`. Any questions can be directed to the support server at [support server](https://discord.com/invite/9pmGDc8pqQ).")
        embed.set_footer(icon_url = self.client.user.avatar.url, text = self.client.user.name)
        await interaction.response.send_message(embed = embed)
    
    @app_commands.command(name = _T("ping"),description = _T("Check the ping of the bot."))
    async def ping(self,interaction:discord.Interaction):
        apiping = round(self.client.latency*1000)
        embed = discord.Embed(title = "Pong 🏓",description = f"API Ping: `{apiping}ms`",color = discord.Color.random())
        embed.set_footer(text = "Note: This message can be misleading.")
        await interaction.response.send_message(embed = embed)
        message = await interaction.original_response()
        latency = interaction.created_at - message.created_at
        embed = discord.Embed(title = "Pong 🏓",description = f"API Ping: `{apiping}ms`\nMessage Latency: `{latency.microseconds*0.001}ms`",color = discord.Color.random())
        embed.set_footer(text = "Note: This message can be misleading.")
        await interaction.edit_original_response(embed = embed)

async def setup(client):
    await client.add_cog(Miscellaneous(client))