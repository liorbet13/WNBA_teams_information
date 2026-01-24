"""
WNBA Team Roster Viewer - Web App Version
A Streamlit-based web interface for viewing WNBA team rosters
Run with: streamlit run roster_webapp.py
"""

import streamlit as st
from roster_fetcher import WNBARosterFetcher
from stats_guide import STATS_GUIDE, STATS_TIP, STAT_DEFINITIONS
import requests
import base64
from PIL import Image
from io import BytesIO
import time
import json
import os


# Team logo mapping (PNG files)
TEAM_LOGOS = {
    'Atlanta Dream': 'logos/Atlanta_Dream.png',
    'Chicago Sky': 'logos/Chicago_Sky.png',
    'Connecticut Sun': 'logos/Conneticut_Sun.png',
    'Dallas Wings': 'logos/Dallas_Wings.png',
    'Golden State Valkyries': 'logos/GS_Valkyries.png',
    'Indiana Fever': 'logos/Indiana_Fever.png',
    'Las Vegas Aces': 'logos/LV_Aces.png',
    'Los Angeles Sparks': 'logos/LA_Sparks.png',
    'Minnesota Lynx': 'logos/Minnesota_Lynx.png',
    'New York Liberty': 'logos/NY_Liberty.png',
    'Phoenix Mercury': 'logos/Phoenix_Mercury.png',
    'Portland Fire': 'logos/Portland_Fire_logo.png',
    'Seattle Storm': 'logos/Seattle_Storm.png',
    'Toronto Tempo': 'logos/Toronto_Tempo_logo.png',
    'Washington Mystics': 'logos/Washington_Mystics.png'
}


# Page configuration
st.set_page_config(
    page_title="WNBA Team Roster Viewer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for WNBA branding
st.markdown("""
    <style>
    .main {
        background-color: #F5F5F5;
    }
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0rem;
        margin-top: -3rem;
    }
    .stButton>button {
        background-color: #FE5000;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 2rem;
    }
    .stButton>button:hover {
        background-color: #C8102E;
        color: white;
    }
    .stButton>button {
        height: 50px;
        white-space: normal;
        line-height: 1.2;
    }
    h1 {
        color: #000000;
        font-weight: bold;
    }
    h2 {
        color: #FE5000;
    }
    h3 {
        color: #006BB6;
    }
    .player-card {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'fetcher' not in st.session_state:
    st.session_state.fetcher = WNBARosterFetcher()
if 'current_roster' not in st.session_state:
    st.session_state.current_roster = None
if 'selected_player_id' not in st.session_state:
    st.session_state.selected_player_id = None
if 'image_cache' not in st.session_state:
    st.session_state.image_cache = {}
if 'expanded_players' not in st.session_state:
    st.session_state.expanded_players = set()


def load_image_from_url(url, size=(100, 100)):
    """Load and resize image from URL with caching, maintaining aspect ratio"""
    # Check cache first
    if url in st.session_state.image_cache:
        return st.session_state.image_cache[url]
    
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            # Maintain aspect ratio
            img.thumbnail(size, Image.Resampling.LANCZOS)
            st.session_state.image_cache[url] = img
            return img
    except:
        pass
    return None


def get_stat_help(stat_key):
    """Get the definition/help text for a stat"""
    return STAT_DEFINITIONS.get(stat_key.lower(), '')


def display_player_row(player, index):
    """Display a simple player row - fast and lightweight"""
    # Create a clickable row
    cols = st.columns([1, 3, 2, 2, 2, 2])
    
    with cols[0]:
        st.write(f"**#{player.get('number', '--')}**")
    
    with cols[1]:
        # Make the name a button
        if st.button(
            player.get('name', 'Unknown'),
            key=f"player_{player.get('id', index)}",
            use_container_width=True
        ):
            st.session_state.selected_player_id = player.get('id')
            st.rerun()
    
    with cols[2]:
        st.write(player.get('position', '--'))
    
    with cols[3]:
        ppg = player.get('ppg', '--')
        st.write(ppg if ppg else '--')
    
    with cols[4]:
        rpg = player.get('rpg', '--')
        st.write(rpg if rpg else '--')
    
    with cols[5]:
        apg = player.get('apg', '--')
        st.write(apg if apg else '--')


def display_player_details(player):
    """Display full player details when selected"""
    
    # Back button
    if st.button("← Back to Roster", use_container_width=False):
        st.session_state.selected_player_id = None
        st.rerun()
    
    # Player header
    st.title(f"#{player.get('number', '--')} {player.get('name', 'Unknown')}")
    st.subheader(player.get('position', 'Position Unknown'))
    
    # Fetch details if not already fetched
    if not player.get('details_fetched', False):
        with st.spinner('Loading comprehensive player stats...'):
            # Get team name and fetch API stats
            team_name = st.session_state.current_roster.get('team_name', '')
            
            # Fetch API stats for the team
            api_stats_dict = st.session_state.fetcher.fetch_team_stats_from_api(team_name)
            api_stats = api_stats_dict.get(player.get('name', ''), None)
            
            # Fetch player details with API stats
            details = st.session_state.fetcher.fetch_single_player_details(
                player.get('id', ''),
                player.get('name', ''),
                api_stats
            )
            player.update(details)
            player['details_fetched'] = True
            
            # Update in current roster
            if st.session_state.current_roster:
                for p in st.session_state.current_roster.get('players', []):
                    if p.get('id') == player.get('id'):
                        p.update(details)
                        p['details_fetched'] = True
                        break
    
    # Two-column layout
    col_left, col_right = st.columns([1, 2])
    
    with col_left:
        # Player photo
        image_url = player.get('image_url', '')
        if image_url:
            img = load_image_from_url(image_url, size=(200, 200))
            if img:
                st.image(img, width=200)
            else:
                st.markdown("### [No Photo]")
        else:
            st.markdown("### [No Photo]")
        
        # Bio Information
        st.markdown("### Bio Information")
        bio_data = [
            ('Height', player.get('height', '--')),
            ('Weight', player.get('weight', '--')),
            ('College', player.get('college', '--')),
            ('Experience', player.get('experience', '--')),
            ('Birth Date', player.get('birth_date', '--')),
            ('Draft', player.get('draft', '--')),
        ]
        
        for label, value in bio_data:
            st.write(f"**{label}:** {value}")
    
    with col_right:
        # Season Statistics
        st.markdown("### Season Statistics (2025)")
        
        # Main stats with tooltips
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        with metric_col1:
            st.metric("PPG", player.get('ppg', '--'), help=get_stat_help('ppg'))
        with metric_col2:
            st.metric("RPG", player.get('rpg', '--'), help=get_stat_help('rpg'))
        with metric_col3:
            st.metric("APG", player.get('apg', '--'), help=get_stat_help('apg'))
        
        st.markdown("### Shooting Percentages")
        
        # Shooting percentages with tooltips
        shoot_col1, shoot_col2, shoot_col3 = st.columns(3)
        with shoot_col1:
            st.metric("FG%", player.get('fgp', '--'), help=get_stat_help('fgp'))
        with shoot_col2:
            st.metric("3P%", player.get('3pp', '--'), help=get_stat_help('3pp'))
        with shoot_col3:
            st.metric("FT%", player.get('ftp', '--'), help=get_stat_help('ftp'))
        
        st.markdown("### Other Stats")
        
        # Other stats with tooltips
        other_col1, other_col2, other_col3, other_col4 = st.columns(4)
        with other_col1:
            st.metric("SPG", player.get('spg', '--'), help=get_stat_help('spg'))
        with other_col2:
            st.metric("BPG", player.get('bpg', '--'), help=get_stat_help('bpg'))
        with other_col3:
            st.metric("TPG", player.get('tpg', '--'), help=get_stat_help('tpg'))
        with other_col4:
            st.metric("MPG", player.get('mpg', '--'), help=get_stat_help('mpg'))
        
        # Advanced stats preview with tooltips
        st.markdown("### Advanced Stats")
        adv_col1, adv_col2, adv_col3 = st.columns(3)
        with adv_col1:
            st.metric("Games", player.get('gp', '--'), help=get_stat_help('gp'))
        with adv_col2:
            st.metric("+/-", player.get('plus_minus', '--'), help=get_stat_help('plus_minus'))
        with adv_col3:
            st.metric("Fantasy Pts", player.get('fantasy_pts', '--'), help=get_stat_help('fantasy_pts'))
    
    # Full comprehensive stats (expandable)
    with st.expander("Show All Stats", expanded=False):
        st.markdown("### Complete Statistical Breakdown")
        
        # Exclude non-stat fields and ranking stats
        exclude_fields = {'id', 'name', 'number', 'position', 'image_url', 'details_fetched'}
        
        # Get all stats (including what's shown above)
        all_stats = {}
        for key, value in player.items():
            if key not in exclude_fields and not key.endswith('_RANK') and value:
                all_stats[key] = value
        
        if all_stats:
            # Bio Information
            st.markdown("#### Bio Information")
            bio_cols = st.columns(3)
            bio_stats = ['height', 'weight', 'college', 'experience', 'birth_date', 'draft']
            bio_labels = {'height': 'Height', 'weight': 'Weight', 'college': 'College',
                         'experience': 'Experience', 'birth_date': 'Birth Date', 'draft': 'Draft'}
            for idx, stat in enumerate(bio_stats):
                if stat in all_stats:
                    with bio_cols[idx % 3]:
                        st.metric(bio_labels[stat], all_stats[stat])
            
            # Game Statistics
            st.markdown("#### Game Statistics")
            game_cols = st.columns(4)
            game_stats_keys = ['gp', 'w', 'l', 'w_pct', 'mpg']
            game_labels = {'gp': 'Games Played', 'w': 'Wins', 'l': 'Losses', 
                          'w_pct': 'Win %', 'mpg': 'Minutes Per Game'}
            for idx, stat in enumerate(game_stats_keys):
                if stat in all_stats:
                    with game_cols[idx % 4]:
                        st.metric(game_labels.get(stat, stat.upper()), all_stats[stat], help=get_stat_help(stat))
            
            # Scoring Statistics
            st.markdown("#### Scoring Statistics")
            score_cols = st.columns(3)
            score_stats = ['ppg', 'fgm', 'fga', 'fgp', '3pm', '3pa', '3pp', 'ftm', 'fta', 'ftp']
            score_labels = {'ppg': 'Points Per Game', 'fgm': 'FG Made', 'fga': 'FG Attempted', 'fgp': 'FG %',
                           '3pm': '3P Made', '3pa': '3P Attempted', '3pp': '3P %',
                           'ftm': 'FT Made', 'fta': 'FT Attempted', 'ftp': 'FT %'}
            for idx, stat in enumerate(score_stats):
                if stat in all_stats:
                    with score_cols[idx % 3]:
                        st.metric(score_labels.get(stat, stat.upper()), all_stats[stat], help=get_stat_help(stat))
            
            # Rebounding Statistics
            st.markdown("#### Rebounding Statistics")
            reb_cols = st.columns(3)
            reb_stats = ['rpg', 'oreb', 'dreb']
            reb_labels = {'rpg': 'Rebounds Per Game', 'oreb': 'Offensive Reb', 'dreb': 'Defensive Reb'}
            for idx, stat in enumerate(reb_stats):
                if stat in all_stats:
                    with reb_cols[idx % 3]:
                        st.metric(reb_labels.get(stat, stat.upper()), all_stats[stat], help=get_stat_help(stat))
            
            # Assists & Defense
            st.markdown("#### Assists & Defense")
            def_cols = st.columns(4)
            def_stats = ['apg', 'spg', 'bpg', 'tpg', 'blka', 'pf', 'pfd']
            def_labels = {'apg': 'Assists Per Game', 'spg': 'Steals Per Game', 'bpg': 'Blocks Per Game',
                         'tpg': 'Turnovers Per Game', 'blka': 'Blocked Attempts', 
                         'pf': 'Personal Fouls', 'pfd': 'Fouls Drawn'}
            for idx, stat in enumerate(def_stats):
                if stat in all_stats:
                    with def_cols[idx % 4]:
                        st.metric(def_labels.get(stat, stat.upper()), all_stats[stat], help=get_stat_help(stat))
            
            # Advanced Metrics
            st.markdown("#### Advanced Metrics")
            adv_cols = st.columns(4)
            adv_stats = ['plus_minus', 'dd2', 'td3', 'fantasy_pts', 'nba_fantasy_pts', 'wnba_fantasy_pts']
            adv_labels = {'plus_minus': 'Plus/Minus', 'dd2': 'Double-Doubles', 'td3': 'Triple-Doubles',
                         'fantasy_pts': 'Fantasy Points', 'nba_fantasy_pts': 'NBA Fantasy Pts', 
                         'wnba_fantasy_pts': 'WNBA Fantasy Pts'}
            for idx, stat in enumerate(adv_stats):
                if stat in all_stats:
                    with adv_cols[idx % 4]:
                        st.metric(adv_labels.get(stat, stat.upper()), all_stats[stat], help=get_stat_help(stat))
        else:
            st.info("No stats available.")

# Header
# Try to load WNBA logo from local file
logo_col, title_col = st.columns([1, 4])

with logo_col:
    try:
        logo_img = Image.open("logos/WNBA_logo.png")
        # Maintain aspect ratio - resize based on height
        aspect_ratio = logo_img.width / logo_img.height
        new_height = 80
        new_width = int(new_height * aspect_ratio)
        logo_img = logo_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        st.image(logo_img, width=new_width)
    except Exception as e:
        pass  # If logo fails to load, just skip it

with title_col:
    st.title("WNBA Team Roster Viewer")

st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("Navigation")
    
    # How to Use section
    with st.expander("How to Use", expanded=False):
        st.markdown("""
        **Getting Started:**
        1. Click any team button in the main area
        2. View team stats and logo
        3. Browse player roster and stats
        4. Click player names for detailed info
        
        **Features:**
        - Team season statistics
        - Player photos and bio
        - 30+ stat categories per player
        - Interactive tooltips (hover over stats)
        - Download roster data as JSON
        """)
    
    # Stats Guide button
    if st.button("Basketball Stats Guide", use_container_width=True):
        st.session_state.show_stats_guide = True
    
    # Current team info and actions
    if st.session_state.current_roster:
        st.markdown("### Current Team")
        st.info(st.session_state.current_roster.get('team_name', 'No team selected'))
        
        # Back to Roster button (shown when viewing player details or schedule)
        if st.session_state.selected_player_id:
            if st.button("← Back to Roster", use_container_width=True, key="sidebar_back_to_roster"):
                st.session_state.selected_player_id = None
                st.rerun()
        elif st.session_state.get('show_schedule', False):
            if st.button("← Back to Roster", use_container_width=True, key="sidebar_back_from_schedule"):
                st.session_state.show_schedule = False
                st.rerun()
        
        # View Schedule button (only show when not viewing schedule)
        if not st.session_state.get('show_schedule', False):
            if st.button("View Team Schedule", use_container_width=True, type="primary"):
                st.session_state.show_schedule = True
                st.rerun()
        
        # Download button
        roster_json = json.dumps(st.session_state.current_roster, indent=2, ensure_ascii=False)
        team_slug = st.session_state.current_roster.get('team_slug', 'roster')
        
        st.download_button(
            label='Download Roster (JSON)',
            data=roster_json,
            file_name=f'{team_slug}_roster.json',
            mime='application/json',
            use_container_width=True
        )
        
        # Fetch all details button
        players = st.session_state.current_roster.get('players', [])
        to_fetch = [p for p in players if not p.get('details_fetched', False)]
        
        if to_fetch:
            if st.button(f"Fetch All Player Details ({len(to_fetch)})", use_container_width=True):
                team_name = st.session_state.current_roster.get('team_name', '')
                with st.spinner(f'Fetching details for {len(to_fetch)} players...'):
                    progress_bar = st.progress(0)
                    
                    # Get API stats for all players
                    api_stats = st.session_state.fetcher.fetch_team_stats_from_api(team_name)
                    
                    for idx, player in enumerate(to_fetch):
                        player_api_stats = api_stats.get(player['name'])
                        details = st.session_state.fetcher.fetch_single_player_details(
                            player['id'],
                            player['name'],
                            player_api_stats
                        )
                        player.update(details)
                        player['details_fetched'] = True
                        progress_bar.progress((idx + 1) / len(to_fetch))
                    
                    progress_bar.empty()
                
                st.success(f"Fetched details for {len(to_fetch)} players!")
                st.rerun()
        
        # Back to main page button
        if st.button("← Back to Main Page", use_container_width=True):
            st.session_state.current_roster = None
            st.session_state.selected_player_id = None
            st.session_state.show_schedule = False
            st.rerun()

# Main content area
if st.session_state.get('show_stats_guide', False):
    # Display Stats Guide
    st.title("Basketball Statistics Guide")
    
    if st.button("← Back to Teams"):
        st.session_state.show_stats_guide = False
        st.rerun()
    
    st.markdown("---")
    
    # Display stats from imported guide
    for category_name, stats_list in STATS_GUIDE.items():
        st.header(category_name)
        
        # Split into two columns for better layout
        col1, col2 = st.columns(2)
        mid_point = (len(stats_list) + 1) // 2
        
        with col1:
            for abbr, name, description in stats_list[:mid_point]:
                st.markdown(f"**{abbr}** - {name}  \n{description}\n")
        
        with col2:
            for abbr, name, description in stats_list[mid_point:]:
                st.markdown(f"**{abbr}** - {name}  \n{description}\n")
        
        st.markdown("---")
    
    st.info(f"**Tip:** {STATS_TIP}")

elif st.session_state.current_roster:
    roster_data = st.session_state.current_roster
    
    # Check if schedule view is requested
    if st.session_state.get('show_schedule', False):
        team_name = roster_data['team_name']
        
        # Team header with logo
        logo_col, name_col = st.columns([1, 8], gap="small")
        
        with logo_col:
            logo_path = TEAM_LOGOS.get(team_name)
            if logo_path and os.path.exists(logo_path):
                try:
                    if logo_path.endswith('.svg'):
                        st.image(logo_path, width=80)
                    else:
                        logo_img = Image.open(logo_path)
                        aspect_ratio = logo_img.width / logo_img.height
                        new_height = 80
                        new_width = int(new_height * aspect_ratio)
                        logo_img = logo_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                        st.image(logo_img, width=new_width)
                except:
                    pass
        
        with name_col:
            st.header(f"{team_name} - 2026 Schedule")
        
        st.markdown("---")
        
        # Back button
        if st.button("← Back to Roster"):
            st.session_state.show_schedule = False
            st.rerun()
        
        # Fetch schedule
        with st.spinner("Loading schedule..."):
            games = st.session_state.fetcher.fetch_team_schedule(team_name)
        
        if games:
            st.info(f"**{len(games)} games scheduled for the 2026 season**")
            
            # Display games in a nice table
            for idx, game in enumerate(games):
                # Alternate background colors
                bg_color = "#f0f2f6" if idx % 2 == 0 else "white"
                
                col1, col2, col3, col4 = st.columns([2, 2, 1, 3])
                
                with col1:
                    st.markdown(f"**{game['date']}**")
                
                with col2:
                    if game['home_away'] == 'vs':
                        st.markdown(f"**Home vs {game['opponent']}**")
                    else:
                        st.markdown(f"**Away @ {game['opponent']}**")
                
                with col3:
                    st.markdown(f"*{game['time']}*")
                
                with col4:
                    st.markdown(f"_{game['game_type']}_")
                
                if idx < len(games) - 1:
                    st.markdown("<div style='margin: 8px 0; border-bottom: 1px solid #e0e0e0;'></div>", unsafe_allow_html=True)
        else:
            st.warning("Schedule not available yet for this team")
    
    # Check if a player is selected
    elif st.session_state.selected_player_id:
        # Find the selected player
        players = roster_data.get('players', [])
        selected_player = None
        for p in players:
            if p.get('id') == st.session_state.selected_player_id:
                selected_player = p
                break
        
        if selected_player:
            display_player_details(selected_player)
        else:
            st.error("Player not found")
            st.session_state.selected_player_id = None
    else:
        # Show roster list view
        # Team header with logo
        team_name = roster_data['team_name']
        
        logo_col, name_col = st.columns([1, 8], gap="small")
        
        with logo_col:
            # Display team logo if available
            logo_path = TEAM_LOGOS.get(team_name)
            if logo_path and os.path.exists(logo_path):
                try:
                    # SVG files can be displayed directly by Streamlit
                    if logo_path.endswith('.svg'):
                        st.image(logo_path, width=80)
                    else:
                        # PNG files need to be resized with PIL
                        logo_img = Image.open(logo_path)
                        aspect_ratio = logo_img.width / logo_img.height
                        new_height = 80
                        new_width = int(new_height * aspect_ratio)
                        logo_img = logo_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                        st.image(logo_img, width=new_width)
                except:
                    pass
        
        with name_col:
            st.header(team_name)
        
        # Next game info (show for all teams, including expansion teams)
        try:
            next_game = st.session_state.fetcher.fetch_next_game(team_name)
            if next_game:
                st.info(f"**Next Game:** {next_game['home_away']} {next_game['opponent']} - {next_game['date']} at {next_game['time']}")
        except Exception as e:
            pass  # Silently skip if next game fetch fails
        
        # Status check
        if roster_data['status'] == 'expansion_2026':
            st.warning(f"{roster_data.get('message', 'Expansion team - roster not yet available')}")
        elif roster_data['status'] == 'error':
            st.error(f"Error: {roster_data.get('error', 'Unknown error occurred')}")
        else:
            # Fetch and display team stats
            with st.spinner("Loading team stats..."):
                team_stats = st.session_state.fetcher.fetch_team_season_stats(team_name)
            
            if team_stats:
                st.markdown("### 2025 Season Stats")
                
                # Big 3 stats displayed prominently with custom HTML for larger font
                big3_html = f"""
                <div style="display: flex; justify-content: space-around; margin: 20px 0;">
                    <div style="text-align: center;">
                        <div style="font-size: 14px; color: #666;">Points Per Game</div>
                        <div style="font-size: 42px; font-weight: bold; color: #FF6B35;">{team_stats['ppg']:.1f}</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 14px; color: #666;">Rebounds Per Game</div>
                        <div style="font-size: 42px; font-weight: bold; color: #FF6B35;">{team_stats['rpg']:.1f}</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 14px; color: #666;">Assists Per Game</div>
                        <div style="font-size: 42px; font-weight: bold; color: #FF6B35;">{team_stats['apg']:.1f}</div>
                    </div>
                </div>
                """
                st.markdown(big3_html, unsafe_allow_html=True)
                
                # Additional stats with tooltips (smaller font)
                st.markdown("""
                    <style>
                    [data-testid="stMetricValue"] {
                        font-size: 18px !important;
                    }
                    [data-testid="stMetricLabel"] {
                        font-size: 12px !important;
                    }
                    </style>
                """, unsafe_allow_html=True)
                
                stat_cols = st.columns(11)
                
                with stat_cols[0]:
                    st.metric("W-L", f"{team_stats['w']}-{team_stats['l']}", help="Wins-Losses")
                with stat_cols[1]:
                    st.metric("Win %", f"{team_stats['w_pct']:.3f}", help="Win Percentage")
                with stat_cols[2]:
                    st.metric("FG%", f"{team_stats['fgp']:.1%}", help=get_stat_help('fgp'))
                with stat_cols[3]:
                    st.metric("3P%", f"{team_stats['3pp']:.1%}", help=get_stat_help('3pp'))
                with stat_cols[4]:
                    st.metric("FT%", f"{team_stats['ftp']:.1%}", help=get_stat_help('ftp'))
                with stat_cols[5]:
                    st.metric("SPG", f"{team_stats['spg']:.1f}", help=get_stat_help('spg'))
                with stat_cols[6]:
                    st.metric("BPG", f"{team_stats['bpg']:.1f}", help=get_stat_help('bpg'))
                with stat_cols[7]:
                    st.metric("TPG", f"{team_stats['tpg']:.1f}", help=get_stat_help('tpg'))
                with stat_cols[8]:
                    st.metric("OREB", f"{team_stats['oreb']:.1f}", help=get_stat_help('oreb'))
                with stat_cols[9]:
                    st.metric("DREB", f"{team_stats['dreb']:.1f}", help=get_stat_help('dreb'))
                with stat_cols[10]:
                    st.metric("PF", f"{team_stats['pf']:.1f}", help=get_stat_help('pf'))
                
                st.markdown("---")
            
            # Display roster info
            players = roster_data.get('players', [])
            fetched_time = roster_data.get('fetched_at', '')[:19].replace('T', ' ')
            
            # Display players
            if players:
                st.subheader("Team Roster")
                st.caption("Click on a player's name to view full details")
                
                # Sort options
                sort_by = st.selectbox(
                    "Sort by:",
                    ["Number", "Name", "Position", "PPG", "RPG", "APG"],
                    index=0
                )
                
                # Sort players
                sort_map = {
                    "Number": lambda p: int(p.get('number', '0') or '0'),
                    "Name": lambda p: p.get('name', ''),
                    "Position": lambda p: p.get('position', ''),
                    "PPG": lambda p: float(p.get('ppg', '0') or '0'),
                    "RPG": lambda p: float(p.get('rpg', '0') or '0'),
                    "APG": lambda p: float(p.get('apg', '0') or '0'),
                }
                
                sorted_players = sorted(players, key=sort_map[sort_by])
                
                # Header row
                header_cols = st.columns([1, 3, 2, 2, 2, 2])
                with header_cols[0]:
                    st.markdown("**#**")
                with header_cols[1]:
                    st.markdown("**Player Name**")
                with header_cols[2]:
                    st.markdown("**Position**")
                with header_cols[3]:
                    st.markdown("**PPG**")
                with header_cols[4]:
                    st.markdown("**RPG**")
                with header_cols[5]:
                    st.markdown("**APG**")
                
                st.markdown("---")
                
                # Display each player row - lightning fast!
                for idx, player in enumerate(sorted_players):
                    display_player_row(player, idx)
                
                # Roster info at bottom
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Players", len(players))
                with col2:
                    st.metric("Last Updated", fetched_time)
                with col3:
                    details_loaded = sum(1 for p in players if p.get('details_fetched', False))
                    st.metric("Details Loaded", f"{details_loaded}/{len(players)}")
            else:
                st.info("No players found in roster")

else:
    # Team selection screen with buttons
    st.subheader("Select a Team")
    st.caption("*Portland Fire and Toronto Tempo are 2026 expansion teams")
    
    # Get all teams
    teams = st.session_state.fetcher.get_all_teams()
    
    # Split teams into current and expansion
    current_teams = [t for t in teams if t not in ['Portland Fire', 'Toronto Tempo']]
    expansion_teams = [t for t in teams if t in ['Portland Fire', 'Toronto Tempo']]
    
    # Display current teams in grid (5 columns)
    st.markdown("### Current Teams (2025)")
    for i in range(0, len(current_teams), 5):
        cols = st.columns(5)
        for j, col in enumerate(cols):
            if i + j < len(current_teams):
                team = current_teams[i + j]
                with col:
                    # Create button with team logo (fixed height container for alignment)
                    logo_path = TEAM_LOGOS.get(team)
                    if logo_path and os.path.exists(logo_path):
                        # Use HTML img tag in fixed-height container for proper alignment
                        mime_type = "image/png" if logo_path.endswith('.png') else "image/svg+xml"
                        st.markdown(f'''<div style="height: 120px; display: flex; align-items: center; justify-content: center;">
                            <img src="data:{mime_type};base64,{base64.b64encode(open(logo_path, 'rb').read()).decode()}" style="max-height: 100%; max-width: 100%; object-fit: contain;" />
                        </div>''', unsafe_allow_html=True)
                    else:
                        st.markdown('<div style="height: 120px;"></div>', unsafe_allow_html=True)
                    
                    if st.button(team, use_container_width=True, key=f"btn_{team}"):
                        with st.spinner(f'Loading {team}...'):
                            roster_data = st.session_state.fetcher.fetch_team_roster(team)
                            st.session_state.current_roster = roster_data
                        st.rerun()
    
    # Display expansion teams
    st.markdown("### 2026 Expansion Teams")
    cols = st.columns(5)
    for i, team in enumerate(expansion_teams):
        with cols[i]:
            logo_path = TEAM_LOGOS.get(team)
            if logo_path and os.path.exists(logo_path):
                # Use HTML img tag in fixed-height container for proper alignment
                mime_type = "image/png" if logo_path.endswith('.png') else "image/svg+xml"
                st.markdown(f'''<div style="height: 120px; display: flex; align-items: center; justify-content: center;">
                    <img src="data:{mime_type};base64,{base64.b64encode(open(logo_path, 'rb').read()).decode()}" style="max-height: 100%; max-width: 100%; object-fit: contain;" />
                </div>''', unsafe_allow_html=True)
            else:
                st.markdown('<div style="height: 120px;"></div>', unsafe_allow_html=True)
            
            if st.button(team, use_container_width=True, key=f"btn_{team}"):
                with st.spinner(f'Loading {team}...'):
                    roster_data = st.session_state.fetcher.fetch_team_roster(team)
                    st.session_state.current_roster = roster_data
                st.rerun()

# Footer
st.markdown("---")
st.caption("Data sourced from official WNBA team websites • Built with Streamlit")
