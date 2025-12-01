# WNBA Teams Information

A Python desktop application for viewing WNBA team rosters with detailed player information and statistics. The app fetches live data from official WNBA team websites and displays it in an easy-to-use graphical interface.

**this app is a work-in-progress and will be improved**

## Features

- **15 WNBA Teams**: Browse rosters for all current teams plus 2026 expansion teams (Golden State Valkyries, Portland Fire, Toronto Tempo)
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

### Running the Application

Simply run the GUI application:

```bash
python roster_gui.py
```

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
├── roster_gui.py          # GUI application (Tkinter)
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
- Indiana Fever
- Las Vegas Aces
- Los Angeles Sparks
- Minnesota Lynx
- New York Liberty
- Phoenix Mercury
- Seattle Storm
- Washington Mystics

**Expansion Teams (2026):**
- Golden State Valkyries
- Portland Fire
- Toronto Tempo

## Dependencies

- **requests**: HTTP requests for web scraping
- **beautifulsoup4**: HTML parsing
- **Pillow**: Image processing and display

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

## License

This project is for educational purposes. All WNBA team and player data is property of the WNBA.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Created by Lior

## Acknowledgments

- Data sourced from official WNBA team websites
- Built with Python and Tkinter
