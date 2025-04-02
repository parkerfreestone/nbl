import json
import discord
from discord.ext import commands
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "data.json")
ID_PATH = os.path.join(BASE_DIR, "data", "team_ids.txt")

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL = os.getenv("GAMES_CHANNEL")


def main():
    intents = discord.Intents.default()
    intents.message_content = True
    version = 0.001

    bot = commands.Bot(command_prefix="~", intents=intents)

    @bot.event
    async def on_ready():
        print(f"Commissioner Avi online running version: {version}")
        await bot.tree.sync()

    @bot.hybrid_command()
    async def print_games(ctx, day):
        channel = bot.get_channel(CHANNEL)
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
                embed = discord.Embed(
                    title=f"{away_team} @ {home_team}",
                    description="",
                    colour=0x00B0F4,
                    timestamp=datetime.datetime.utcnow(),
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
                    name="End of Reg", value=f"{q4_home} - {q4_away}", inline=True
                )

                embed.set_footer(
                    text="Home Team is Left Number",
                    icon_url="https://i.imgur.com/ZLzUuH8.png",
                )

                await ctx.send(embed=embed)

    bot.run(TOKEN)


if __name__ == "__main__":
    main()
