import discord


def get_intents():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True
    intents.members = True
    return intents


def get_version():
    return "0.0.1"
