from discord import app_commands
from discord.ext import commands


class Team(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="team", description="😎 Get your team information")
    @app_commands.describe()
    async def team_cmd(self, ctx: commands.Context):
        """
        Currently returns nothing but fucking a basketball.
        """
        await ctx.send("🏀")
