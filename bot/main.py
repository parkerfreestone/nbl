import json
import datetime
import os
import importlib
import discord
from discord.ext import commands
from dotenv import load_dotenv
from bot.utils.conf import get_intents, get_version

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")


class NBLBot(commands.Bot):
    def __init__(self, intents: discord.Intents, bot_version):
        super().__init__(command_prefix="~", intents=intents)
        self.bot_version = bot_version

    def setup_hook(self):
        return self.load_all_cogs()

    async def load_all_cogs(self):
        for filename in os.listdir("./bot/commands"):
            if filename.endswith(".py") and not filename.startswith("_"):
                module = f"bot.commands.{filename[:-3]}"
                mod = importlib.import_module(module)

                cog_class = next(
                    cls
                    for cls in mod.__dict__.values()
                    if isinstance(cls, type)
                    and issubclass(cls, commands.Cog)
                    and cls is not commands.Cog
                )
                await self.add_cog(cog_class(self))

    async def on_ready(self):
        print(f"Commissioner Avi online running version: {self.bot_version}")
        await self.tree.sync()


def main():
    intents = get_intents()
    version = get_version()

    bot = NBLBot(intents, version)

    bot.run(TOKEN)


if __name__ == "__main__":
    main()
