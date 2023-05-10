import discord
from discord.ext import commands,tasks
from discord import app_commands
import aiohttp
import os
from dotenv import load_dotenv
import asyncio
from googletrans import Translator
from langcodes import *
import json

class Client(commands.Bot):
    def __init__(self):
        self.prefixes = {}
        self.rules = {}
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True

        super().__init__(command_prefix = "e!",help_command = None, intents = intents,activity = discord.Game("Translating for r/Place!"))
        
    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        self._BotBase__cogs  = commands.core._CaseInsensitiveDict()
        await self.load_extension("jishaku")
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
        await self.tree.set_translator(Bot_Translator())
        
    async def on_ready(self):
        print('Bot is online, and cogs are loaded.')

class Bot_Translator(app_commands.Translator):
    def __init__(self):
        self.cache = None

    def blocking_io(self,string,dest):
        print(f"Translating '{string}' to '{dest}'")
        return Translator().translate(string,dest = dest)

    async def load(self):
        with open("translations.json","r") as readfile:
            self.cache = json.load(readfile)
    async def unload(self):
        pass
    async def translate(self,string,locale,context):
        dest = Language.get(str(locale)).language.lower() if str(locale).lower() != "zh-cn" and str(locale).lower() != "zh-tw" else str(locale).lower()

        if dest in ['en','zh-cn','zh-tw','ja']:
            cache = self.cache.get(string.message,{}).get(dest)
            if cache:
                print(f"Using Cached Version for {string.message} in {dest}")
                return cache
            
            translatordata = await asyncio.gather(
                asyncio.to_thread(self.blocking_io,string.message,dest),
                asyncio.sleep(3))
            
            if string.message in self.cache:
                self.cache[string.message][dest] = translatordata[0].text 
            else:
                self.cache[string.message] = {dest:translatordata[0].text}
            
            with open("translations.json","w") as outfile:
                json.dump(self.cache,outfile)

            return translatordata[0].text or None
        else:
            return None


client = Client()

load_dotenv()
client.run(os.getenv('BOT_TOKEN'))