import json
import os
import discord
from discord import app_commands
from discord.ext import commands
from bot.utils.league_data import TEAM_ID_NAME_MAP
from bot.utils.schedule import get_next_game

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "team.json")
DATA_PATH = os.path.abspath(DATA_PATH)

LEAGUE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "league.json")
)
SCHEDULE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "data", "schedule.json")
)


class Team(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="team", description="Get your team's current information."
    )
    @app_commands.describe()
    async def team_cmd(self, ctx: commands.Context):
        """
        WIP
        """
        member = ctx.author
        team_id = None

        # Find their role
        for role in member.roles:
            if role.name in TEAM_ID_NAME_MAP:
                team_id = TEAM_ID_NAME_MAP[role.name]
                break

        if not team_id:
            await ctx.send(
                "You don't appear to have a team role assigned, assign one yourself or fucking ask kyle"
            )
            return

        try:
            with open(DATA_PATH, "r") as f:
                data = json.load(f)

            with open(LEAGUE_PATH, "r") as f:
                league_data = json.load(f)

            with open(SCHEDULE_PATH, "r") as f:
                schedule_data = json.load(f)

        except Exception as e:
            await ctx.send(f"Error reading data file: {e}")
            return

        team_data = next((t for t in data["teams"] if t["tid"] == team_id), None)
        if not team_data:
            await ctx.send("Team data not found. Ask Parker why lmao.")
            return

        latest_season = team_data.get("seasons", [{}])[-1]
        wins = latest_season.get("won", 0)
        losses = latest_season.get("lost", 0)
        strategy = team_data.get("strategy", "Unknown").capitalize()
        team_name = f"{team_data['region']} {team_data['name']} ({team_data['abbrev']})"

        next_game = get_next_game(team_id, schedule_data, league_data)

        embed = discord.Embed(
            title=team_name,
            description=f"🏀 Strategy: **{strategy}**",
            color=discord.Color.blue(),
        )
        embed.set_thumbnail(url=team_data.get("imgURL", ""))
        embed.add_field(name="📈 Wins", value=str(wins), inline=True)
        embed.add_field(name="📉 Losses", value=str(losses), inline=True)

        if next_game:
            is_home = next_game["homeTid"] == team_id
            opponent_tid = next_game["awayTid"] if is_home else next_game["homeTid"]

            opponent_team = next(
                (t for t in data["teams"] if t["tid"] == opponent_tid), None
            )
            opponent_name = (
                f"{opponent_team['region']} {opponent_team['name']}"
                if opponent_team
                else f"Team {opponent_tid}"
            )

            location = "Home" if is_home else "Away"
            day = next_game["day"]

            embed.add_field(
                name="📅 Next Game",
                value=f"{location} vs **{opponent_name}**\n\nMatchday {day}",
                inline=False,
            )
        else:
            embed.add_field(
                name="📅 Next Game", value="No upcoming games found.", inline=False
            )

        try:
            await member.send(embed=embed)
            await ctx.send("I just DMed you your team info!", ephemeral=True)
        except discord.Forbidden:
            await ctx.send(
                "I couldn't DM you — make sure your DMs are open!", ephemeral=True
            )
