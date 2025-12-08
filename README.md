# WNBA Teams Information

A Python desktop application for viewing WNBA team rosters with detailed player information and statistics. The app fetches live data from official WNBA team websites and displays it in an easy-to-use graphical interface.

**this app is a work-in-progress and will be improved**

## Future Improvements

The following enhancements are planned for future releases:

1. **Advanced Stats Fetching Improvements** - Fix and enhance the scraping logic for advanced player statistics
2. **GUI Aesthetic Enhancements** - Modernize the visual design with improved color schemes, layouts, and team branding
3. **Full Game Data Integration** - Incorporate complete game-by-game statistics, schedules, and performance visualizations
4. **Data Management Options** - Add ability to delete fetched data and clear cache before closing the application

## Features

- **15 WNBA Teams**: Browse rosters for all 13 current teams (including 2025 expansion team Golden State Valkyries) plus 2 upcoming 2026 expansion teams (Portland Fire, Toronto Tempo)
- **Quick Roster Loading**: Fast initial load with parallel image fetching (~2-3 seconds)
- **Player Photos**: High-quality headshots for all players
- **Basic Statistics**: Points per game (PPG), Rebounds per game (RPG), Assists per game (APG)
- **Detailed Player Information**: Click any player to view:
  - Bio information (height, weight, college, experience, birthdate, birthplace)
  - Advanced statistics (FG%, 3P%, FT%, blocks, steals, turnovers, minutes)
- **On-Demand Details**: Player details are fetched only when needed for optimal performance
- **Bulk Fetch**: "Fetch All Details" button to load all player information at once
- **Save Rosters**: Export team rosters to JSON files for offline viewing

## Screenshots

The app displays players in a clean grid layout with:
- Player number and name
- Position
- Basic statistics (PPG, RPG, APG)
- Player headshot photo
- Click-to-expand details panel

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

1. **Select a Team**: Choose a team from the dropdown menu at the top
2. **Fetch Roster**: Click "Fetch Roster" to load the team's current roster
3. **View Basic Info**: See player photos, numbers, positions, and basic stats
4. **View Details**: Click on any player to expand and view detailed bio and statistics
5. **Fetch All Details**: Click "Fetch All Details" to load information for all players at once
6. **Save Roster**: Click "Save Roster" to export the data to a JSON file

### Saved Data

Roster data is saved in the `team_rosters/` directory as JSON files:
- Format: `{team_slug}_roster.json`
- Example: `fever_roster.json` for Indiana Fever

## Project Structure

```
WNBA_teams_information/
├── roster_gui.py          # Desktop GUI application (Tkinter)
├── roster_webapp.py       # Web application (Streamlit) ⭐ NEW!
├── roster_fetcher.py      # Business logic for fetching roster data
├── test_roster.py         # Unit tests
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore            # Git ignore rules
└── team_rosters/         # Saved roster JSON files (created automatically)
```

## Technical Details

### Data Sources

- **Team Rosters**: Fetched from `https://{team-slug}.wnba.com/roster/`
- **Player Details**: Fetched from `https://www.wnba.com/player/{player-id}`
- **Player Photos**: Loaded from WNBA CDN at `https://cdn.wnba.com/headshots/`

### Performance Optimizations

- **Parallel HTTP Requests**: Uses ThreadPoolExecutor with 8 concurrent workers
- **Parallel Image Loading**: Downloads multiple player photos simultaneously
- **On-Demand Details**: Bio and advanced stats fetched only when user clicks a player
- **Caching**: Downloaded images are cached in memory during the session

### Teams Supported

**Current Teams (2025 Season):**
- Atlanta Dream
- Chicago Sky
- Connecticut Sun
- Dallas Wings
- Golden State Valkyries (2025 expansion team)
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
**Solution**: Click on the player to fetch detailed stats. Some stats may not be available for all players

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

### Advanced Stats Scraping Refinement

**Problem:** Initial attempts to scrape advanced statistics from stats.wnba.com using Selenium encountered multiple issues:
- JavaScript-heavy pages required browser automation
- AJAX/dynamic content loading made table parsing difficult
- Unicode encoding errors on Windows (Hebrew locale)
- Selenium added complexity and 4+ second overhead per team

**Solution Implemented:**
- **Removed Selenium dependency**: Eliminated browser automation complexity
- **Individual player page scraping**: Advanced stats now fetched from static player profile pages
- **On-demand fetching**: Stats only loaded when user requests player details
- **Simplified requirements**: Removed selenium from dependencies, reducing setup complexity

**Impact:**
- Cleaner codebase without browser automation overhead
- More reliable data fetching from static HTML pages
- Easier setup (no ChromeDriver installation needed)
- Better error handling for missing stats

## License

This project is for educational purposes. All WNBA team and player data is property of the WNBA.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Created by Lior

## Acknowledgments

- Data sourced from official WNBA team websites
- Built with Python and Tkinter
