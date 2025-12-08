"""
Basketball Statistics Guide
Contains definitions and descriptions for all basketball statistics used in the application.
"""

STATS_GUIDE = {
    "Basic Statistics": [
        ("GP", "Games Played", "Total number of games the player has participated in"),
        ("W", "Wins", "Number of games won when player was on the roster"),
        ("L", "Losses", "Number of games lost when player was on the roster"),
        ("MIN/MPG", "Minutes Per Game", "Average number of minutes played per game"),
        ("PTS/PPG", "Points Per Game", "Average number of points scored per game"),
        ("REB/RPG", "Rebounds Per Game", "Average number of rebounds per game"),
        ("AST/APG", "Assists Per Game", "Average number of assists per game"),
        ("STL/SPG", "Steals Per Game", "Average number of steals per game"),
        ("BLK/BPG", "Blocks Per Game", "Average number of blocked shots per game"),
        ("TOV/TPG", "Turnovers Per Game", "Average number of turnovers per game"),
        ("PF", "Personal Fouls", "Total number of fouls committed"),
        ("PFD", "Personal Fouls Drawn", "Fouls committed by opponents on this player"),
        ("BLKA", "Blocked Attempts", "Times this player's shot was blocked"),
    ],
    "Shooting Statistics": [
        ("FGM", "Field Goals Made", "Successful shots from the field (2-pointers + 3-pointers)"),
        ("FGA", "Field Goals Attempted", "Total shots attempted from the field"),
        ("FG%", "Field Goal Percentage", "Percentage of field goals made (FGM / FGA)"),
        ("3PM", "Three-Pointers Made", "Successful 3-point shots"),
        ("3PA", "Three-Pointers Attempted", "Total 3-point shots attempted"),
        ("3P%", "Three-Point Percentage", "Percentage of 3-pointers made (3PM / 3PA)"),
        ("FTM", "Free Throws Made", "Successful free throw shots"),
        ("FTA", "Free Throws Attempted", "Total free throws attempted"),
        ("FT%", "Free Throw Percentage", "Percentage of free throws made (FTM / FTA)"),
    ],
    "Rebounding Statistics": [
        ("OREB", "Offensive Rebounds", "Rebounds on offensive end (after own team's miss)"),
        ("DREB", "Defensive Rebounds", "Rebounds on defensive end (after opponent's miss)"),
        ("REB", "Total Rebounds", "Total rebounds (OREB + DREB)"),
    ],
    "Advanced Metrics": [
        ("+/-", "Plus/Minus", "Point differential when player is on court"),
        ("DD2", "Double-Doubles", "Games with double digits in 2 categories"),
        ("TD3", "Triple-Doubles", "Games with double digits in 3 categories"),
        ("W%", "Win Percentage", "Percentage of games won"),
        ("Fantasy Pts", "Fantasy Points", "Points for fantasy basketball leagues"),
    ],
}

STATS_TIP = "Higher percentages (FG%, 3P%, FT%) and per-game averages (PPG, RPG, APG) generally indicate better performance."

# Create a lookup dictionary for quick access to stat definitions
STAT_DEFINITIONS = {}
for category, stats_list in STATS_GUIDE.items():
    for abbr, name, description in stats_list:
        # Add multiple keys for different variations
        STAT_DEFINITIONS[abbr.upper()] = f"{name}: {description}"
        STAT_DEFINITIONS[abbr.lower()] = f"{name}: {description}"
        # Handle special cases
        if '/' in abbr:
            for part in abbr.split('/'):
                STAT_DEFINITIONS[part.upper()] = f"{name}: {description}"
                STAT_DEFINITIONS[part.lower()] = f"{name}: {description}"

# Add common stat key mappings
STAT_DEFINITIONS.update({
    'ppg': 'Points Per Game: Average number of points scored per game',
    'rpg': 'Rebounds Per Game: Average number of rebounds per game',
    'apg': 'Assists Per Game: Average number of assists per game',
    'spg': 'Steals Per Game: Average number of steals per game',
    'bpg': 'Blocks Per Game: Average number of blocked shots per game',
    'mpg': 'Minutes Per Game: Average number of minutes played per game',
    'tpg': 'Turnovers Per Game: Average number of turnovers per game',
    'fgm': 'Field Goals Made: Successful shots from the field',
    'fga': 'Field Goals Attempted: Total shots attempted from the field',
    'fgp': 'Field Goal Percentage: Percentage of field goals made',
    'fg_pct': 'Field Goal Percentage: Percentage of field goals made',
    '3pm': 'Three-Pointers Made: Successful 3-point shots',
    '3pa': 'Three-Pointers Attempted: Total 3-point shots attempted',
    '3pp': 'Three-Point Percentage: Percentage of 3-pointers made',
    'fg3_pct': 'Three-Point Percentage: Percentage of 3-pointers made',
    'ftm': 'Free Throws Made: Successful free throw shots',
    'fta': 'Free Throws Attempted: Total free throws attempted',
    'ftp': 'Free Throw Percentage: Percentage of free throws made',
    'ft_pct': 'Free Throw Percentage: Percentage of free throws made',
    'oreb': 'Offensive Rebounds: Rebounds on offensive end',
    'dreb': 'Defensive Rebounds: Rebounds on defensive end',
    'reb': 'Total Rebounds: Offensive + Defensive rebounds',
    'ast': 'Assists: Passes that lead directly to a score',
    'stl': 'Steals: Times player takes ball from opponent',
    'blk': 'Blocks: Times player blocks opponent shot',
    'tov': 'Turnovers: Times player loses possession',
    'pf': 'Personal Fouls: Total fouls committed',
    'pfd': 'Personal Fouls Drawn: Fouls committed by opponents on this player',
    'blka': 'Blocked Attempts: Times this player\'s shot was blocked',
    'plus_minus': 'Plus/Minus: Point differential when player is on court',
    'dd2': 'Double-Doubles: Games with double digits in 2 categories',
    'td3': 'Triple-Doubles: Games with double digits in 3 categories',
    'w_pct': 'Win Percentage: Percentage of games won',
    'fantasy_pts': 'Fantasy Points: Points for fantasy basketball leagues',
    'nba_fantasy_pts': 'NBA Fantasy Points: Points using NBA fantasy scoring',
    'wnba_fantasy_pts': 'WNBA Fantasy Points: Points using WNBA fantasy scoring',
    'gp': 'Games Played: Total number of games participated in',
    'w': 'Wins: Number of games won',
    'l': 'Losses: Number of games lost',
})

