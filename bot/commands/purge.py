from discord import app_commands
from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure


class Purge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="purge")
    @has_permissions(administrator=True)
    async def purge(self, ctx: commands.Context, amount: int):
        if amount > 50:
            amount = 50
        await ctx.channel.purge(limit=amount + 1)

    @purge.error
    async def purge_error(self, ctx: commands.Context, error):
        if isinstance(error, CheckFailure):
            msg = "You do not have permission to run this command. Kil your self :D"
            await ctx.send(msg)
