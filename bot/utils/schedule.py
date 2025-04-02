def get_next_game(team_id, schedule_data, team_data):
    """
    Get the next game for a given team based on their games played.
    """
    # Grab the number of games played so far from the season stats
    latest_season = team_data.get("seasons", [{}])[-1]
    games_played = latest_season.get("won", 0) + latest_season.get("lost", 0)

    # Find all scheduled games for this team
    team_schedule = [
        g
        for g in schedule_data["schedule"]
        if g["homeTid"] == team_id or g["awayTid"] == team_id
    ]

    # Sort just in case
    team_schedule.sort(key=lambda g: g["day"])

    # Get the next game after games_played
    return team_schedule[games_played] if games_played < len(team_schedule) else None
