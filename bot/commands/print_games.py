from discord import app_commands
from discord.ext import commands
import os
import json
import discord
import datetime
from discord.ext.commands import has_permissions, CheckFailure
from bot.utils.league_data import TEAM_ID_NAME_MAP

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "league.json")
ID_PATH = os.path.join(BASE_DIR, "..", "data", "team_ids.txt")

CHANNEL = os.getenv("GAMES_CHANNEL")


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(names="print_games")
    @has_permissions(administrator=True)
    async def print_games(self, ctx: commands.Context, day):
        channel = self.bot.get_channel(CHANNEL)
        with open(DATA_PATH, "r") as file:
            data = json.load(file)
        matchday = int(data["games"][0]["day"])
        game_number = int(data["games"][0]["gid"]) + 1
        id_data = {}
        with open(ID_PATH, "r") as team_ids:
            for line in team_ids:
                split_line = line.split("-")
                id_data[int(split_line[0])] = split_line[1]
        temp_day = 0
        for game_number in range(len(data["games"])):
            if int(data["games"][game_number]["day"]) == int(day):
                temp_day += 1
                home_team = id_data[
                    data["games"][game_number]["teams"][0]["tid"]
                ].strip("\n")
                home_team = home_team[1:]
                away_team = id_data[
                    data["games"][game_number]["teams"][1]["tid"]
                ].strip("\n")
                away_team = away_team[1:]
                q1_home, q2_home_temp, q3_home_temp, q4_home_temp = (
                    data["games"][game_number]["teams"][0]["ptsQtrs"][0],
                    data["games"][game_number]["teams"][0]["ptsQtrs"][1],
                    data["games"][game_number]["teams"][0]["ptsQtrs"][2],
                    data["games"][game_number]["teams"][0]["ptsQtrs"][3],
                )
                q2_home = q1_home + q2_home_temp
                q3_home = q2_home + q3_home_temp
                q4_home = q3_home + q4_home_temp
                q1_away, q2_away_temp, q3_away_temp, q4_away_temp = (
                    data["games"][game_number]["teams"][1]["ptsQtrs"][0],
                    data["games"][game_number]["teams"][1]["ptsQtrs"][1],
                    data["games"][game_number]["teams"][1]["ptsQtrs"][2],
                    data["games"][game_number]["teams"][1]["ptsQtrs"][3],
                )
                q2_away = q1_away + q2_away_temp
                q3_away = q2_away + q3_away_temp
                q4_away = q3_away + q4_away_temp
                home_role_name = next(
                    (
                        k
                        for k, v in TEAM_ID_NAME_MAP.items()
                        if v == data["games"][game_number]["teams"][0]["tid"]
                    ),
                    None,
                )
                away_role_name = next(
                    (
                        k
                        for k, v in TEAM_ID_NAME_MAP.items()
                        if v == data["games"][game_number]["teams"][1]["tid"]
                    ),
                    None,
                )
                home_role = discord.utils.get(ctx.guild.roles, name=home_role_name)
                away_role = discord.utils.get(ctx.guild.roles, name=away_role_name)
                home_emoji = discord.utils.get(
                    ctx.guild.emojis, name=home_role_name.lower().replace(" ", "_")
                )
                away_emoji = discord.utils.get(
                    ctx.guild.emojis, name=away_role_name.lower().replace(" ", "_")
                )
                game_winner = id_data[data["games"][game_number]["won"]["tid"]]
                embed = discord.Embed(
                    title=f"{away_emoji} {away_team} @ {home_team} {home_emoji}",
                    description="",
                    colour=0x00B0F4,
                    timestamp=datetime.datetime.now(),
                )

                embed.set_author(
                    name=f"Matchday: {day} Game: {temp_day}", url="https://example.com"
                )

                embed.add_field(
                    name="Quarter 1", value=f"{q1_home} - {q1_away}", inline=True
                )
                embed.add_field(
                    name="Halftime", value=f"{q2_home} - {q2_away}", inline=True
                )
                embed.add_field(
                    name="Quarter 3", value=f"{q3_home} - {q3_away}", inline=True
                )
                embed.add_field(
                    name="Fulltime",
                    value=f"{home_role_name}: {q4_home} - {away_role_name}: {q4_away}",
                    inline=True,
                )
                embed.add_field(
                    name="",
                    value=f"{home_role.mention} {away_role.mention}",
                    inline=False,
                )
                embed.set_footer(
                    text=f"Home Team is Left Number / All times are in MST",
                    icon_url="https://i.imgur.com/ZLzUuH8.png",
                )
                await ctx.send(embed=embed)

    @print_games.error
    async def print_games_error(self, ctx: commands.Context, error):
        if isinstance(error, CheckFailure):
            msg = "You do not have permission to run this command. Kil your self :D"
            await ctx.send(msg)
