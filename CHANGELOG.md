# Changelog & Implementation Details

This document tracks all enhancements, bug fixes, and technical implementation details for the WNBA Teams Information project.

## Recent Enhancements (January 2026)

### Schedule UI Improvements & Next Game Feature (January 24, 2026)

**Enhancement - Schedule Navigation & Upcoming Game Display**

Improved schedule viewing experience and added next game display to team stats.

#### View Schedule Button Repositioned (Web App)
- **Previous Location**: Bottom of roster page (below player table)
- **New Location**: Sidebar, positioned under team name and above "Download Roster (JSON)"
- **Benefit**: More accessible, consistent with sidebar navigation pattern
- **Conditional Display**: Button hides when viewing schedule (replaced by "Back to Roster" button)

#### Schedule Navigation Enhancement
- **Web App**: Added "Back to Roster" button in sidebar when viewing schedule
  - Uses same pattern as player details view
  - Button replaces "View Team Schedule" when schedule is active
  - Smooth navigation between roster and schedule views
- **Desktop App**: Schedule view already had "Back to Roster" in sidebar (no change needed)

#### Next Game Display
- **New Method**: `fetch_next_game()` in `roster_fetcher.py`
  - Fetches the next upcoming game for a team from WNBA API
  - Compares game datetime with current time to find next game
  - Returns single game dictionary or None if no upcoming games
- **Display Location**: Prominent info box above team stats section
  - Web App: Blue info box with game details
  - Desktop App: Light blue frame with game details
- **Format**: "Next Game: vs/@ [Opponent] - [Date] at [Time]"
  - Example: "Next Game: @ Portland Fire - Saturday May 09, 2026 at 09:00 PM ET"
- **Expansion Team Support**: Works for all teams including 2026 expansion teams (Portland Fire, Toronto Tempo)
  - Displays next game even when roster/stats not available
  - Web App: Shows next game before expansion team warning
  - Desktop App: Changed expansion handling to show next game instead of just returning to team selection

#### UI Polish
- **Removed Emoji**: Removed calendar emoji (📅) from "View Team Schedule" button for cleaner appearance
- **Home/Away Format**: Changed from emojis (🏠/✈️) to text ("Home vs"/"Away @") in schedule display
  - More professional appearance
  - Better accessibility (screen readers)
  - Consistent with "Next Game" format

#### Technical Implementation
- **Time Comparison**: Uses `datetime.now(timezone.utc)` to find upcoming games
- **Error Handling**: Try-except blocks prevent display issues if fetch fails
- **Session State** (Web App): Tracks schedule view with `show_schedule` flag
- **View Mode** (Desktop App): Tracks schedule with existing `view_mode` state variable

### Team Schedule API Fix (January 24, 2026)

**Bug Fix - Schedule Data Source & Time Display**

Fixed schedule fetching to use official WNBA API instead of web scraping, resolving the issue where schedules were not displaying. Also fixed time display bug where all games showed 12:00 AM ET.

#### Issue Identified
- **Original Implementation**: Used BeautifulSoup to scrape WNBA.com schedule page
- **Problem**: WNBA schedule page is JavaScript-rendered (Next.js/React), so HTML scraping returned no data
- **Symptoms**: `fetch_team_schedule()` returned empty list (0 games) for all teams

#### Solution Implemented
- **API Discovery**: Found official WNBA schedule API at `https://cdn.wnba.com/static/json/staticData/scheduleLeagueV2.json`
- **Data Structure**: JSON endpoint returns complete 2026 season schedule (331 games across 112 dates)
- **Team Matching**: Uses team city + name comparison instead of abbreviations for reliability
- **Date Formatting**: Converts ISO 8601 timestamps to human-readable format (e.g., "Saturday May 09, 2026")
- **Time Conversion**: Formats game times in 12-hour format with ET timezone

#### Updated Implementation
```python
# Old: Web scraping (didn't work - JS-rendered page)
soup = BeautifulSoup(response.text, 'html.parser')
game_links = soup.find_all('a', href=lambda x: x and '/game/' in x)

# New: API consumption (works reliably)
response = requests.get('https://cdn.wnba.com/static/json/staticData/scheduleLeagueV2.json')
data = response.json()
game_dates = data['leagueSchedule']['gameDates']
```

#### Time Display Bug Fix
- **Issue**: All game times displaying as "12:00 AM ET" regardless of actual game time
- **Root Cause**: Code was using `gameDateEst` field which only contains date (with 00:00:00 default time)
- **Solution**: Changed to use `gameDateTimeEst` field which contains full datetime with actual game time
- **Result**: Times now display correctly (e.g., "01:00 PM ET", "09:00 PM ET")
- **Code Change**: `game_datetime_str = game.get('gameDateTimeEst', '')` instead of `gameDateEst`

#### Additional Improvements
- **Arena Information**: Now includes venue name for each game
- **Game ID**: Includes unique game identifier for potential future features
- **Better Error Handling**: More robust exception handling with detailed error messages
- **Full Season Coverage**: Returns all 44 regular season games per team (2026 schedule)
- **Display Format**: Changed from emoji indicators to text ("Home vs"/"Away @") for better accessibility

#### Test Results
- Chicago Sky: 44 games successfully retrieved
- Includes home and away games
- Proper opponent names (full team names like "Portland Fire" instead of abbreviations)
- Accurate dates and times in ET timezone
- Game type correctly identified (Regular Season, Commissioner's Cup)

### Team Schedule Viewing Feature (January 24, 2026)

**New Feature - View Full Team Schedule**

Added comprehensive schedule viewing capability to both desktop and web applications, allowing users to see all 2026 season games for any team.

#### Schedule Integration
- **Schedule Fetching**: New `fetch_team_schedule()` method in `roster_fetcher.py`
  - Uses official WNBA CDN API (`https://cdn.wnba.com/static/json/staticData/scheduleLeagueV2.json`)
  - Parses JSON data for 2026 season (331 total games)
  - Filters games by team name matching (city + team name)
  - Extracts date, opponent, home/away status, time, arena, and game type
  - Returns structured list of game dictionaries (~44 games per team)
- **Team Matching**: Intelligent matching using full team names (e.g., "New York Liberty")
- **Game Type Detection**: Distinguishes between Regular Season, Commissioner's Cup, and Playoffs
- **Date Formatting**: Converts ISO timestamps to readable format (e.g., "Saturday May 09, 2026")

#### Web Application (Streamlit)
- **View Schedule Button**: Prominent button on roster page (📅 View Team Schedule)
- **Schedule View**: Clean table-style display with:
  - Date in bold
  - Home (🏠 vs) or Away (✈️ @) indicator with opponent
  - Game time in italics
  - Game type (Regular Season / Commissioner's Cup)
  - Alternating row colors for readability
- **Navigation**: "Back to Roster" button to return to roster view
- **Session State**: Tracks schedule view mode separately from player details

#### Desktop Application (Tkinter)
- **View Schedule Button**: Added to sidebar navigation when viewing roster
- **Schedule View**: Scrollable game list with:
  - Team logo and header
  - Game count display
  - Date, opponent, home/away, time, and game type columns
  - Alternating row backgrounds (#F5F5F5 and white)
  - Mouse wheel scrolling support
- **View Mode Tracking**: New `view_mode` state variable ('team_selection', 'roster', 'schedule', 'player')
- **Sidebar Updates**: Context-aware "Back to Roster" button appears in schedule view

#### Technical Implementation
- **API Consumption**: Uses official WNBA CDN JSON endpoint (no web scraping needed)
- **Error Handling**: Graceful fallback if schedule unavailable or API fails
- **Performance**: Efficient JSON parsing and filtering of 331 games to team-specific subset
- **Data Structure**: Each game contains date, opponent, home_away, time, game_type, arena, game_id
- **Reliability**: Direct API access more stable than web scraping JavaScript-rendered pages

#### User Experience Impact
- **Complete Season Overview**: Users can see all upcoming games at a glance
- **Home/Away Clarity**: Visual indicators make it easy to identify home vs road games
- **Commissioner's Cup Games**: Special games highlighted with distinct game type label
- **Quick Access**: Single button click from roster view
- **Consistent UX**: Same functionality and layout in both desktop and web apps

### Desktop GUI Complete Modernization (January 24, 2026)

**Major Redesign - Feature Parity with Web App**

Complete overhaul of the desktop GUI (`roster_gui.py`) to match the modern interface and functionality of the Streamlit web application. The desktop application now provides the same visual experience and features as the web version.

#### New Modern Interface
- **Visual Team Selection Grid**: Replaced dropdown menu with 5-column grid layout displaying all 15 teams
- **Team Logo Display**: PNG logos shown in team buttons (100x100) and roster header (80x80)
- **WNBA Branding**: Added WNBA logo (60x60) to main header for professional appearance
- **Modern Color Scheme**: WNBA orange (#FE5000) and red (#C8102E) throughout interface
- **Responsive Layout**: Clean, organized sections with proper spacing and visual hierarchy

#### Team Statistics Integration
- **API Integration**: Fetches real-time team season statistics from WNBA Stats API
- **"Big 3" Display**: PPG, RPG, APG shown prominently in large orange numbers (36px)
- **Comprehensive Stats Grid**: 9 additional statistics displayed in organized format
  - Win-Loss record and percentage
  - Shooting percentages (FG%, 3P%, FT%)
  - Defensive stats (SPG, BPG, TPG)
- **Visual Organization**: Stats displayed above roster table for easy comparison

#### Enhanced Roster Management
- **Sorting Functionality**: Dropdown menu to sort roster by:
  - Jersey Number
  - Player Name (alphabetical)
  - Position
  - Points Per Game (PPG)
  - Rebounds Per Game (RPG)
  - Assists Per Game (APG)
- **Interactive Table**: Clean roster display with alternating row colors
- **Player Details**: Click any player to view full statistics and bio information

#### Improved Navigation
- **Sidebar Design**: Professional navigation panel matching web app layout
- **Back Buttons**: Context-aware navigation
  - "Back to Main" - Returns to team selection
  - "Back to Roster" - Returns to roster view from player details
- **Organized Actions**: Logical button grouping (navigation, data operations, help)
- **Persistent Controls**: Navigation accessible from any screen

#### Logo System Updates
- **PNG Format**: Converted all logos from SVG to PNG for universal compatibility
- **Eliminated Dependencies**: Removed cairosvg requirement (Cairo library issues on Windows)
- **Optimized Loading**: PIL/Pillow native PNG support for faster rendering
- **Fallback System**: Text-based display if logo file unavailable
- **Updated Both Apps**: Web app also migrated to PNG logos for consistency

#### Technical Improvements
- **ModernRosterGUI Class**: Complete rewrite with improved architecture
- **State Management**: Better handling of view states and data caching
- **Error Handling**: Robust fallbacks for missing logos or API failures
- **Code Organization**: Cleaner methods with single responsibility principle
- **Performance**: Cached team data and logos for faster subsequent access

#### Files Modified
- `roster_gui.py` - Complete rewrite (1179 lines)
- `roster_webapp.py` - Updated logo paths to PNG format
- `.gitignore` - Removed PNG exclusion to allow logo commits
- `README.md` - Comprehensive documentation updates across 6 sections
- `logos/` - All 16 PNG files (15 teams + WNBA logo)

#### User Experience Impact
- **Unified Experience**: Desktop and web apps now have matching interfaces
- **Visual Appeal**: Professional appearance with team branding throughout
- **Feature Complete**: Desktop app no longer missing web app features
- **Intuitive Navigation**: Clear visual flow and navigation paths
- **Educational Value**: Team stats provide context for roster evaluation

### UI Redesign - Visual Team Selection (Web App)
- Replaced dropdown menu with visual team button grid (5 columns)
- Team logos displayed above each team button for instant recognition
- Clean, modern layout with all 15 teams visible at once
- Separate sections for current teams (2025) and expansion teams (2026)
- Clicking any team button instantly loads the roster

### Team Logos Integration
- Added professional team logos for all 15 WNBA teams in `logos/` directory
- Logos displayed on both team selection screen and roster pages
- Supports both SVG and PNG formats with proper MIME type detection
- Fixed-height containers (120px) ensure perfect button alignment across all teams
- HTML/CSS implementation with base64 encoding for reliable display

### Team Season Statistics
- Integrated WNBA Stats API team-level data
- "Big 3" stats (PPG, RPG, APG) prominently displayed in large orange numbers (42px)
- Additional team stats shown in compact format with tooltips:
  - W-L record and win percentage
  - Shooting percentages (FG%, 3P%, FT%)
  - Defensive stats (SPG, BPG, TPG)
  - Rebounding stats (OREB, DREB)
  - Personal fouls
- All team stats include interactive tooltips explaining each metric

### Enhanced Player Statistics
- Added missing stat fields to player advanced details:
  - Win Percentage (w_pct) - formatted to 3 decimal places
  - Blocked Attempts (blka)
  - Fouls Drawn (pfd)
- Draft information now included in advanced details section
- Total of 37 fields displayed across 6 organized categories

### Player Bio Information Fix
- Fixed bio scraping to handle WNBA website structure changes
- Updated to iterate through all `<dl>` tags instead of targeting specific classes
- Corrected field mapping: "Experience" label (was incorrectly looking for "EXP")
- Added Draft information field (e.g., "2018 Rnd 1 Pick 2")
- Removed non-existent Birthplace field
- Now successfully extracts: Height, Weight, College, Experience, Birth Date, Draft

### Navigation & UX Improvements
- Reorganized sidebar with collapsible "How to Use" section
- "← Back to Main Page" button replaces "Clear Display" for better clarity
- "← Back to Roster" button appears in sidebar when viewing player details
- Removed unnecessary spacing and dividers from sidebar for cleaner look
- Reduced top padding in sidebar (Navigation header positioned closer to top)
- Moved roster info metrics (Total Players, Last Updated, Details Loaded) to bottom of roster page
- Custom button styling: 50px height with text wrapping for longer team names

### Visual Polish
- Fixed horizontal line spacing issues (removed duplicate dividers)
- Consistent button heights prevent misalignment with long team names
- WNBA orange (#FE5000) buttons with red (#C8102E) hover effect
- Clean, professional spacing throughout the interface

## Previous Enhancements

### Basketball Stats Guide Integration

**Implementation:**
1. **Comprehensive Stats Dictionary**: Created `stats_guide.py` with 50+ stat definitions
   - Covers all basic stats (PPG, RPG, APG, etc.)
   - Shooting metrics (FG%, 3P%, FT%, etc.)
   - Advanced analytics (PER, +/-, fantasy points)
   - Organized by category for easy reference

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
   - Changed headers from "Team Roster" (previously with emoji) to plain text
   - Updated buttons, messages, and labels across 30+ locations
   - Photo placeholders changed to "[No Photo]"
   - Indicators changed to "[Details]"

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

## Bug Fixes & Performance Improvements

### Official WNBA Stats API Integration (Major Update)

**Problem:** 
The application was originally fetching player statistics by scraping individual player pages from wnba.com, which had several issues:
- Very slow performance (sequential requests for each player)
- Limited stat availability (only a few basic stats visible on player pages)
- No advanced metrics (fantasy points, +/-, double-doubles, etc.)
- Fragile scraping code prone to breaking when website structure changed

**Solution:**
Integrated with the official WNBA Stats API endpoint: `https://stats.wnba.com/stats/leaguedashplayerstats`

**Benefits:**
1. **Comprehensive Statistics**: Now fetching 67 statistical categories per player in a single API call
   - All basic stats (PPG, RPG, APG, FG%, 3P%, FT%, etc.)
   - Advanced metrics (PLUS_MINUS, DD2, TD3, fantasy points)
   - Detailed shooting stats (FGM, FGA, 3PM, 3PA, FTM, FTA)
   - Defensive stats (STL, BLK, BLKA, PF, PFD)
   
2. **Massive Performance Improvement**: 
   - Before: ~30-60 seconds to fetch stats for a full team (sequential web scraping)
   - After: ~2-3 seconds for all players on a team (single API call)
   - Parallel processing for bio information (height, weight, college) still uses web scraping
   
3. **Reliability**: Official API is stable and maintained by the WNBA
   - No more broken scrapers when website redesigns happen
   - Consistent data format
   - Season-based queries with proper parameters

**Technical Details:**
```python
# API Configuration
url = "https://stats.wnba.com/stats/leaguedashplayerstats"
params = {
    'LeagueID': '10',              # WNBA identifier
    'Season': '2025',              # Current season
    'SeasonType': 'Regular Season',
    'PerMode': 'PerGame',          # Per-game averages
    # ... 40+ additional parameters
}
headers = {
    'User-Agent': 'Mozilla/5.0...',
    'Referer': 'https://stats.wnba.com/'
}
```

**Impact:**
- 10-20x faster stats loading
- 10x more statistical categories available
- More reliable and maintainable codebase
- Better user experience with comprehensive player analytics

### Image Caching & Performance

**Desktop GUI (Tkinter):**
- Implemented in-memory caching for player photos
- Photos downloaded once per session and reused
- Significant reduction in network requests when switching between players

**Web App (Streamlit):**
- Leverages Streamlit's built-in caching with `@st.cache_data`
- Images cached across page reruns
- Lazy loading: images only downloaded when player details are viewed

### Parallel Processing

**Player Bio Information:**
- Uses `ThreadPoolExecutor` with 8 concurrent workers
- Fetches bio data (height, weight, college, experience) in parallel
- Reduces total fetch time from ~30 seconds (sequential) to ~5 seconds (parallel)

**Implementation:**
```python
with ThreadPoolExecutor(max_workers=8) as executor:
    future_to_player = {
        executor.submit(self._fetch_player_details_with_api, player, api_stats): player 
        for player in players
    }
    for future in as_completed(future_to_player):
        future.result()
```

## Technical Architecture

### Data Flow
1. **Team Selection** → Fetch roster from stats.wnba.com (basic info: name, number, position)
2. **Initial Display** → Show roster table with basic stats from initial load
3. **Player Click** → Fetch comprehensive stats from API + bio from player page
4. **"Fetch All Details"** → Parallel fetch for all players (API stats + bio scraping)

### API Integration Points
- **Team Season Stats**: `stats.wnba.com/stats/leaguedashteamstats`
- **Player Stats**: `stats.wnba.com/stats/leaguedashplayerstats`
- **Player Bio**: Scraping from `wnba.com/player/{player_id}`
- **Team Rosters**: Scraping from `wnba.com/stats/team/{team_slug}`

### Performance Optimizations
- Single API call per team for all player stats
- Parallel HTTP requests for bio information (8 workers)
- In-memory image caching (desktop) and Streamlit caching (web)
- On-demand detail fetching (click to load)
- Interactive tooltips with O(1) dictionary lookup (no API calls)

## Future Roadmap

### Planned Enhancements
1. **Team Information** - Add team statistics, achievements, and enhanced team-specific visualizations
2. **Full Game Data Integration** - Incorporate complete game-by-game statistics, schedules, and performance visualizations
3. **Enhanced Visualizations** - Add charts and graphs for stat comparisons and trends
4. **Data Export** - Additional export formats (CSV, Excel)
5. **Player Comparison** - Side-by-side player statistics comparison

### Under Consideration
- Historical season data
- Player career statistics across seasons
- Team-level analytics and insights
- Mobile app version
- Real-time game updates

## Performance Optimization Details

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
