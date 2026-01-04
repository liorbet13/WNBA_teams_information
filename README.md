# WNBA Teams Information

A Python application for viewing WNBA team rosters with comprehensive player statistics. Available as both a desktop GUI (Tkinter) and modern web application (Streamlit), the app fetches live data from official WNBA sources and displays detailed player information with 30+ statistical categories.

**This app is a work-in-progress and will continue to be improved**

## Motivation

The official WNBA website, while comprehensive, presents a significant usability challenge for fans and analysts trying to access player statistics. Navigating to a specific player's stats requires clicking through **multiple webpages**, making quick comparisons and stat lookups frustratingly time-consuming.

This application solves that problem by providing:
- **Single-page access** to all player information - no endless clicking through menus
- **One simple filter** - just select the team you want to view
- **Instant stats** - comprehensive player data loads in seconds, not minutes
- **User-friendly interface** - clean, organized presentation of 30+ statistical categories
- **Quick comparisons** - view entire team rosters side-by-side with all key stats

Whether you're a casual fan checking your favorite player's performance, a fantasy basketball enthusiast comparing options, or an analyst gathering data, this app streamlines what should be a simple task into an actually simple experience.

*Note: All data is sourced directly from the official WNBA website and stats API, ensuring accuracy and up-to-date information.*

## Requirements

- Python 3.8 or higher
- Internet connection (for fetching live data)
- Windows, macOS, or Linux

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/liorbet13/WNBA_teams_information.git
   cd WNBA_teams_information
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**:
   - Windows (PowerShell):
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   - Windows (Command Prompt):
     ```cmd
     .venv\Scripts\activate.bat
     ```
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Desktop Application (Tkinter)

Simply run the GUI application:

```bash
python roster_gui.py
```

### Running the Web Application (Streamlit)

For a modern web-based interface that runs in your browser:

```bash
streamlit run roster_webapp.py
```

This will automatically open your browser to `http://localhost:8501` with the web app.

### Using the Application

#### Web Application (Streamlit) - Recommended

1. **Select a Team**: Click any team button from the main team selection grid (displayed in 5 columns with team logos)
2. **View Team Information**: 
   - Team logo and name at the top
   - 2025 season statistics prominently displayed:
     - "Big 3" stats (PPG, RPG, APG) in large orange numbers
     - Additional team stats (W-L, shooting %, defense, rebounds) with tooltips
3. **Browse Roster**: View all players with their numbers, positions, and key stats (PPG, RPG, APG)
4. **Sort Players**: Use the dropdown to sort by Number, Name, Position, PPG, RPG, or APG
5. **View Player Details**: Click on any player name to see:
   - Player photo and bio (height, weight, college, experience, birth date, draft info)
   - Comprehensive statistics organized by category (30+ stats)
6. **Fetch All Details**: Click "Fetch All Player Details" in the sidebar to load stats for all players at once
7. **Download Roster**: Click "Download Roster (JSON)" in the sidebar to export team data
8. **Navigate Back**: Use "← Back to Roster" or "← Back to Main Page" buttons to navigate
9. **Stats Guide**: Click "Basketball Stats Guide" in the sidebar for definitions of all statistics

#### Desktop Application (Tkinter)

1. **Select a Team**: Choose a team from the dropdown menu
2. **Fetch Roster**: Click "Fetch Roster from Web" to load the team's current roster
3. **View Team Stats**: See team logo, season statistics (PPG, RPG, APG), and complete team performance metrics
4. **View Basic Info**: See player photos, numbers, positions, and key stats
5. **View Player Details**: Click on any player name to expand and view comprehensive bio (height, weight, college, experience, draft info) and statistics
6. **Fetch All Details**: Click "Fetch All Player Details" to load comprehensive stats for all players at once
7. **Download Roster**: Click "Download Roster Data" to export the data to a JSON file
8. **Stats Guide**: Click "Stats Guide" to view a comprehensive basketball statistics dictionary
9. **Show All Stats**: For any player, click "Show All Stats" to see all 30+ statistical categories organized by type

### Interactive Tooltips (Web App Only)

When viewing player stats in the web app, hover over the (?) icon next to any statistic to instantly see its definition. For example:
- Hover over "PPG" → "Points Per Game: Average number of points scored per game"
- Hover over "+/-" → "Plus/Minus: Point differential when player is on court"
- Hover over "FG%" → "Field Goal Percentage: Percentage of field goals made"

No need to switch views - definitions appear right where you need them!

### Downloaded Data

Roster data is downloaded as JSON files with the naming format: `{team_slug}_roster.json`
- Example: `fever_roster.json` for Indiana Fever
- Contains complete player information including all 30+ stat categories
- Can be opened in any text editor or JSON viewer

## Features

### Core Functionality
- **15 WNBA Teams**: Browse rosters for all 13 current teams (including 2025 expansion team Golden State Valkyries) plus 2 upcoming 2026 expansion teams (Portland Fire, Toronto Tempo)
- **Team Logos**: Professional team logos displayed next to each team name on roster pages
- **Team Season Statistics**: View comprehensive 2025 season stats for each team including PPG, RPG, APG, Win-Loss record, shooting percentages, and more
- **Quick Roster Loading**: Fast initial load with optimized data fetching (~2-3 seconds)
- **Player Photos**: High-quality headshots for all players
- **Comprehensive Statistics**: 30+ statistical categories per player from official WNBA API
- **Enhanced Bio Information**: Player details including height, weight, college, experience, birth date, and draft information

### Statistical Categories
- **Basic Stats**: GP, W, L, W%, MPG, PPG, RPG, APG, SPG, BPG, TPG
- **Shooting Stats**: FGM, FGA, FG%, 3PM, 3PA, 3P%, FTM, FTA, FT%
- **Rebounding**: OREB, DREB, Total Rebounds
- **Defense**: Steals, Blocks, Blocked Attempts, Personal Fouls, Fouls Drawn
- **Advanced Metrics**: +/-, Double-Doubles, Triple-Doubles, Fantasy Points

### User Experience Features
- **Team Statistics Display**: Each team page prominently shows the "Big 3" stats (PPG, RPG, APG) in large orange numbers, followed by additional team stats (W-L record, shooting percentages, steals, blocks, turnovers, etc.) with interactive tooltips
- **Team Logos**: Professional SVG/PNG team logos displayed alongside team names for visual identification
- **Interactive Tooltips (Web App)**: Hover over any stat to see its definition instantly - no need to switch to the guide
- **Basketball Stats Guide**: Built-in dictionary explaining all basketball statistics with definitions and descriptions
- **On-Demand Details**: Player bio and advanced stats fetched only when needed for optimal performance
- **Bulk Fetch**: "Fetch All Details" button to load all player information at once
- **Download Rosters**: Export team rosters to JSON files for offline analysis
- **Show All Stats**: Deep dive view displaying all 30+ comprehensive stat categories organized by category

### Web Application (Streamlit) Exclusive Features
- Modern, responsive design with WNBA branding
- Built-in progress indicators and smooth interactions
- Mobile-friendly interface
- Image caching for faster repeat visits
- Enhanced data visualization

## Future Improvements

The following enhancements are planned for future releases:

1. **Team Information** - Add team statistics, achievements, and enhanced team-specific visualizations
2. **Full Game Data Integration** - Incorporate complete game-by-game statistics, schedules, and performance visualizations
3. **Enhanced Visualizations** - Add charts and graphs for stat comparisons and trends

## Project Structure

```
WNBA_teams_information/
├── roster_gui.py          # Desktop GUI application (Tkinter)
├── roster_webapp.py       # Web application (Streamlit)
├── roster_fetcher.py      # Business logic for fetching roster data
├── stats_guide.py         # Basketball statistics definitions and guide
├── test_roster.py         # Unit tests
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── logos/                # Team and WNBA logos (SVG/PNG)
│   ├── WNBA_logo.svg.webp
│   ├── Atlanta_Dream.svg
│   ├── Chicago_Sky.svg
│   └── ... (15 team logos)
└── .gitignore            # Git ignore rules
```

## Technical Details

### Data Sources

- **Team Season Statistics**: Official WNBA Stats API at `https://stats.wnba.com/stats/leaguedashteamstats`
  - Provides comprehensive team-level statistics (W-L record, PPG, RPG, APG, shooting percentages, etc.)
  - Updated for current 2025 season
- **Team Rosters & Player Stats**: Official WNBA Stats API at `https://stats.wnba.com/stats/leaguedashplayerstats`
  - Provides 67 comprehensive statistical categories per player
  - Requires `LeagueID='10'` parameter for WNBA data
  - Includes per-game averages, shooting percentages, advanced metrics
- **Player Bio Information**: Individual player pages at `https://www.wnba.com/player/{player-id}`
  - Height, weight, college, experience, birth date, draft information
  - Scrapes multiple `<dl>` tags for bio data (updated structure as of 2025)
- **Player Photos**: WNBA CDN at `https://cdn.wnba.com/headshots/`
- **Team Logos**: Local `logos/` directory with SVG and PNG files for all 15 teams

### API Integration

The application uses the official WNBA Stats API to fetch comprehensive player statistics:

```python
# API endpoint
https://stats.wnba.com/stats/leaguedashplayerstats

# Required parameters
LeagueID='10'              # WNBA league identifier
Season='2025'              # Current season
SeasonType='Regular Season'
PerMode='PerGame'          # Per-game averages

# Required headers
User-Agent: Mozilla/5.0...
Referer: https://stats.wnba.com
```

### Statistical Categories (67 Total)

The API provides comprehensive statistics including:
- **Player identification**: PLAYER_ID, PLAYER_NAME, NICKNAME, TEAM_ABBREVIATION, AGE
- **Game statistics**: GP (games played), W (wins), L (losses), W_PCT, MIN (minutes)
- **Scoring**: PTS, FGM, FGA, FG_PCT, FG3M, FG3A, FG3_PCT, FTM, FTA, FT_PCT
- **Rebounds**: OREB, DREB, REB
- **Other stats**: AST, TOV, STL, BLK, BLKA, PF, PFD
- **Advanced metrics**: PLUS_MINUS, DD2 (double-doubles), TD3 (triple-doubles), NBA_FANTASY_PTS, WNBA_FANTASY_PTS

Note: 30 ranking fields (ending in `_RANK`) are filtered out for cleaner display.

### Performance Optimizations

- **Official API Integration**: Direct access to WNBA Stats API provides all 67 stat categories in a single request per team
- **Parallel HTTP Requests**: Uses ThreadPoolExecutor with 8 concurrent workers for fetching player bio information
- **Parallel Image Loading**: Downloads multiple player photos simultaneously
- **On-Demand Details**: Bio information fetched only when user clicks a player
- **Image Caching**: Downloaded images cached in memory during the session (web app)
- **Lazy Loading (Web App)**: Simple roster table loads instantly, full details load on-demand
- **Interactive Tooltips (Web App)**: Stat definitions available on hover with zero performance cost (client-side rendering, O(1) dictionary lookup)

### Teams Supported

**Current Teams (2025 Season):**
- Atlanta Dream
- Chicago Sky
- Connecticut Sun
- Dallas Wings
- Golden State Valkyries 
- Indiana Fever
- Las Vegas Aces
- Los Angeles Sparks
- Minnesota Lynx
- New York Liberty
- Phoenix Mercury
- Seattle Storm
- Washington Mystics

**Upcoming Expansion Teams (2026):**
- Portland Fire
- Toronto Tempo

## Dependencies

- **requests**: HTTP requests for web scraping
- **beautifulsoup4**: HTML parsing
- **Pillow**: Image processing and display
- **streamlit**: Web application framework (for roster_webapp.py)

## Development

### Running Tests

```bash
python test_roster.py
```

### Code Structure

- `WNBARosterFetcher` class: Handles all data fetching and parsing logic
- `WNBARosterGUI` class: Manages the Tkinter GUI and user interactions
- Modular design separates business logic from presentation

## Troubleshooting

**Issue**: "No module named 'requests'" or similar import errors  
**Solution**: Make sure you've activated the virtual environment and installed dependencies

**Issue**: Roster not loading or showing errors  
**Solution**: Check your internet connection. WNBA websites may occasionally be down for maintenance

**Issue**: Player photos not displaying  
**Solution**: Photos load asynchronously. Wait a few seconds. Some players may not have photos available

**Issue**: Advanced stats showing "--"  
**Solution**: Click "Fetch All Player Details" to load comprehensive stats from the WNBA API. Bio information is fetched from individual player pages when you click on a player.

**Issue**: Stats Guide button not visible (Web App)  
**Solution**: The "Stats Guide" button is located in the sidebar below the "Clear Display" button. Scroll down in the sidebar if needed.

**Issue**: Tooltips not showing (Web App)  
**Solution**: Hover over the (?) icon next to any stat metric. If tooltips aren't appearing, ensure you're using a modern browser (Chrome, Firefox, Edge, Safari).

## Changelog

For detailed information about recent updates, bug fixes, and implementation details, see [CHANGELOG.md](CHANGELOG.md).

**Recent highlights:**
- Visual team selection with logo grid (January 2026)
- Team season statistics integration
- Enhanced player statistics with 37+ fields
- Improved navigation and UI polish
- Official WNBA Stats API integration for comprehensive player data
- Basketball Stats Guide with interactive tooltips

## License

This project is for educational purposes. All WNBA team and player data is property of the WNBA.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Created by Lior Batat

## Acknowledgments

- This project was created as part of a [basic Python programming course](https://github.com/Code-Maven/wis-python-course-2025-10/) at WSOS (Weizmann School of Science)
- Data sourced from official WNBA team websites
- Built with Python and Tkinter
