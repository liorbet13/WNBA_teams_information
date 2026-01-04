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

## Future Improvements

The following enhancements are planned for future releases:

1. **Team Information** - Add team statistics, achievements, and enhanced team-specific visualizations
2. **Full Game Data Integration** - Incorporate complete game-by-game statistics, schedules, and performance visualizations
3. **Enhanced Visualizations** - Add charts and graphs for stat comparisons and trends

## Features

### Core Functionality
- **15 WNBA Teams**: Browse rosters for all 13 current teams (including 2025 expansion team Golden State Valkyries) plus 2 upcoming 2026 expansion teams (Portland Fire, Toronto Tempo)
- **Quick Roster Loading**: Fast initial load with optimized data fetching (~2-3 seconds)
- **Player Photos**: High-quality headshots for all players
- **Comprehensive Statistics**: 30+ statistical categories per player from official WNBA API

### Statistical Categories
- **Basic Stats**: GP, W, L, W%, MPG, PPG, RPG, APG, SPG, BPG, TPG
- **Shooting Stats**: FGM, FGA, FG%, 3PM, 3PA, 3P%, FTM, FTA, FT%
- **Rebounding**: OREB, DREB, Total Rebounds
- **Defense**: Steals, Blocks, Blocked Attempts, Personal Fouls, Fouls Drawn
- **Advanced Metrics**: +/-, Double-Doubles, Triple-Doubles, Fantasy Points

### User Experience Features
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

### Running the Web Application (Streamlit) ⭐ NEW!

For a modern web-based interface that runs in your browser:

```bash
streamlit run roster_webapp.py
```

This will automatically open your browser to `http://localhost:8501` with the web app.

**Why use the web version?**
- ✨ Modern, responsive design
- 🚀 Smoother performance and interactions
- 📱 Works on any device with a browser
- 🎨 Better visual appeal with WNBA branding
- 🔄 Built-in progress indicators
- 📊 Enhanced data visualization

### Using the Application

1. **Select a Team**: Choose a team from the dropdown menu
2. **Fetch Roster**: Click "Fetch Roster from Web" to load the team's current roster
3. **View Basic Info**: See player photos, numbers, positions, and key stats
4. **View Player Details**: Click on any player name to expand and view comprehensive bio and statistics
5. **Fetch All Details**: Click "Fetch All Player Details" to load comprehensive stats for all players at once
6. **Download Roster**: Click "Download Roster Data" to export the data to a JSON file
7. **Stats Guide**: Click "Stats Guide" to view a comprehensive basketball statistics dictionary
8. **Show All Stats**: For any player, click "Show All Stats" to see all 30+ statistical categories organized by type

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
└── .gitignore            # Git ignore rules
```

## Technical Details

### Data Sources

- **Team Rosters & Player Stats**: Official WNBA Stats API at `https://stats.wnba.com/stats/leaguedashplayerstats`
  - Provides 67 comprehensive statistical categories per player
  - Requires `LeagueID='10'` parameter for WNBA data
  - Includes per-game averages, shooting percentages, advanced metrics
- **Player Bio Information**: Individual player pages at `https://www.wnba.com/player/{player-id}`
  - Height, weight, college, experience, birth date, birth place
- **Player Photos**: WNBA CDN at `https://cdn.wnba.com/headshots/`

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

## Bug Fixes & Performance Improvements

### Major Performance Optimization: Parallel Data Fetching

**Problem:** The original implementation suffered from extremely slow loading times, taking **40-60+ seconds** to fetch roster data for a single team. This made the app nearly unusable, as users had to wait over a minute just to see basic roster information.

**Root Cause Analysis:**
- **Sequential HTTP requests**: The original code fetched player data one-by-one in a loop, making synchronous requests to the WNBA API for each player
- **Blocking operations**: Each request blocked the next one, creating a waterfall effect where 15 players × 3-4 seconds per request = 45-60 seconds total
- **Image loading delays**: Player headshots were loaded synchronously, further blocking the UI
- **No threading**: All operations ran on the main thread, freezing the GUI during data fetching

**Solution Implemented:**

1. **Parallel HTTP Requests with ThreadPoolExecutor**
   - Introduced `concurrent.futures.ThreadPoolExecutor` with 8 concurrent workers
   - Implemented `_fetch_player_details_parallel()` method to fetch multiple players simultaneously
   - Changed from sequential to parallel execution: instead of 15 × 3 seconds = 45s, now ~max(3 seconds) = 3-5s
   
2. **Asynchronous Image Loading**
   - Player headshots now load in separate daemon threads using Python's `threading` module
   - Images appear progressively as they download, instead of blocking the entire roster display
   - Implemented `load_and_display_image()` method with thread-safe GUI updates using `root.after()`
   - Added image caching to prevent re-downloading images during the session

3. **On-Demand Detail Fetching**
   - Basic roster info (name, number, position, basic stats) loads immediately (~2-3 seconds)
   - Advanced player details (bio, advanced stats) only fetch when user clicks on a player
   - "Fetch All Details" button available for users who want to bulk-load all information
   - This two-tier approach ensures fast initial load while still providing access to comprehensive data

**Performance Impact:**
- **Initial roster load**: Reduced from 40-60+ seconds to **2-3 seconds** (~95% improvement)
- **Full team details**: Reduced from 60+ seconds to **8-12 seconds** with parallel fetching
- **UI responsiveness**: App remains responsive during all operations thanks to background threading
- **Perceived performance**: Images appear progressively, providing visual feedback that data is loading

**Technical Implementation Details:**
```python
# roster_fetcher.py - Parallel player detail fetching
with ThreadPoolExecutor(max_workers=8) as executor:
    future_to_player = {executor.submit(self._fetch_player_details, player): player 
                       for player in players}
    for future in as_completed(future_to_player):
        future.result()  # Updates player dict in place

# roster_gui.py - Asynchronous image loading
threading.Thread(target=self.load_and_display_image, 
               args=(image_url, player_id, photo_label), 
               daemon=True).start()
```

This optimization transformed the app from a frustratingly slow proof-of-concept to a responsive, production-ready application that provides a smooth user experience comparable to modern web applications.

### Progress Bar Implementation (Desktop GUI)

**Problem:** Users had no visual feedback during data fetching operations, making it unclear whether the app was working or frozen, especially during the initial roster load or bulk detail fetching.

**Solution Implemented:**
- **Custom Canvas-based progress bar**: Created a visible orange progress bar (200px × 20px) in the status bar using Tkinter Canvas
- **Real-time progress updates**: Progress bar shows percentage completion (0-100%) during all fetch operations
- **Three progress tracking modes**:
  1. Team roster fetch: 0% → 20% → 60% → 80% → 100%
  2. Individual player details: 0% → 30% → 70% → 100%
  3. Bulk details fetch: Real-time counter (e.g., "5/12 players")
- **Minimum display time**: Progress stays at 100% for 1.5 seconds before resetting, ensuring visibility even for fast operations
- **Background threading**: All fetch operations run in daemon threads to keep the GUI responsive

**Performance Impact:**
- Improved user experience with clear visual feedback
- Reduced perceived wait time by showing progress
- Window minimum size set to 950x700 to ensure progress bar always visible

### Web Application Implementation (Streamlit)

**Problem:** Tkinter GUI was functional but faced limitations:
- Slow rendering when displaying many players with photos and metrics
- Each player card created 15+ widgets, causing 180-225 total widgets for a full roster
- Photo loading blocked the UI
- Not modern or mobile-friendly

**Solution Implemented:**

1. **Complete Streamlit Web Application** (`roster_webapp.py`)
   - Modern, responsive web interface accessible via browser
   - Built-in progress indicators and state management
   - Professional design with WNBA branding (orange #FE5000, black, white color scheme)

2. **Lazy Loading Architecture**
   - **Stage 1 (Roster List)**: Instant display of simple table with player names, numbers, positions, and basic stats
   - **Stage 2 (Detail View)**: Full player profile loads only when user clicks a player's name
   - Reduced initial render from 180-225 widgets to just 12-15 simple rows

3. **Performance Optimizations**
   - **Image caching**: Photos stored in session state, loaded once per session
   - **Progressive disclosure**: Details fetched on-demand only for clicked players
   - **Reduced timeout**: Image requests timeout after 3 seconds instead of 5
   - **Smart sorting**: Client-side sorting by any stat without re-fetching
   - **Aspect ratio preservation**: All images (logo and player photos) maintain proper proportions

**Performance Impact:**
- **Initial roster load**: Reduced from 10-15 seconds to **< 1 second** (instant)
- **Player detail view**: 2-3 seconds when clicking a player (only loads when needed)
- **Smoother interactions**: No lag when scrolling or clicking
- **Better UX**: Clean table view → detailed player profile workflow

**Technical Implementation:**
```python
# Lazy loading: Simple row display (instant)
def display_player_row(player, index):
    cols = st.columns([1, 3, 2, 2, 2, 2])
    # Just text - no images, metrics, or expanders
    
# Full details only when clicked
if st.session_state.selected_player_id:
    display_player_details(selected_player)  # Loads everything
```

**Web vs Desktop Comparison:**
| Feature | Desktop (Tkinter) | Web (Streamlit) |
|---------|------------------|-----------------|
| Initial roster load | 2-3 seconds | < 1 second |
| Rendering speed | Moderate | Fast |
| Photo handling | Threading required | Built-in async |
| Progress bars | Custom implementation | Built-in |
| Mobile friendly | No | Yes |
| Deployment | Local only | Can deploy to cloud |

### Stats Guide & Interactive Tooltips

**Problem:** Users unfamiliar with basketball statistics needed a reference guide to understand abbreviations and metrics.

**Solution Implemented:**

1. **Basketball Statistics Dictionary** (`stats_guide.py`)
   - Comprehensive guide with 30+ stat definitions
   - Organized into 4 categories: Basic Statistics, Shooting Statistics, Rebounding Statistics, Advanced Metrics
   - Each stat includes: abbreviation, full name, and detailed description
   - Accessible via "Stats Guide" button in both applications

2. **Interactive Tooltips (Web App)**
   - Hover-based tooltips on all stat metrics using Streamlit's built-in `help` parameter
   - `STAT_DEFINITIONS` lookup dictionary for instant access (O(1) performance)
   - Zero performance cost - definitions rendered client-side
   - Covers all 50+ statistics displayed in the application
   
3. **Desktop GUI Stats Guide Window**
   - Scrollable popup window with categorized stat definitions
   - Professional layout with WNBA branding
   - Mouse wheel scrolling support

**User Experience Impact:**
- Users can learn about stats without leaving the app
- Web app users get instant definitions on hover (no clicking required)
- Educational value for users new to basketball analytics
- Professional, self-documenting interface

**Technical Implementation:**
```python
# stats_guide.py
STAT_DEFINITIONS = {
    'ppg': 'Points Per Game: Average number of points scored per game',
    'fg_pct': 'Field Goal Percentage: Percentage of field goals made',
    # ... 50+ definitions
}

# roster_webapp.py - Tooltip usage
st.metric("PPG", player.get('ppg', '--'), help=get_stat_help('ppg'))
```

### UI/UX Improvements

**Changes Implemented:**

1. **Emoji Removal**: Removed all emojis from both applications for a clean, professional appearance
   - Changed headers from "📋 Team Roster" to "Team Roster"
   - Updated buttons, messages, and labels across 30+ locations
   - Photo placeholders changed from "📷" to "[No Photo]"
   - Indicators changed from "✓ Details" to "[Details]"

2. **Section Cleanup**: Removed redundant "Player & Team Info" section that duplicated data already shown elsewhere

3. **Stats Organization**: Reorganized "Show All Stats" feature with 6 clear categories:
   - Bio Information (6 fields)
   - Game Statistics (5 fields)
   - Scoring Statistics (10 fields)
   - Rebounding Statistics (3 fields)
   - Assists & Defense (7 fields)
   - Advanced Metrics (6 fields)

**Impact:**
- More professional, business-ready appearance
- Better information architecture
- Easier navigation through comprehensive stats
- Suitable for presentations and demonstrations

## License

This project is for educational purposes. All WNBA team and player data is property of the WNBA.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Created by Lior

## Acknowledgments

- Data sourced from official WNBA team websites
- Built with Python and Tkinter
