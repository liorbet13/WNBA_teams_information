"""
WNBA Team Roster Viewer - Web App Version
A Streamlit-based web interface for viewing WNBA team rosters
Run with: streamlit run roster_webapp.py
"""

import streamlit as st
from roster_fetcher import WNBARosterFetcher
import requests
from PIL import Image
from io import BytesIO
import time


# Page configuration
st.set_page_config(
    page_title="WNBA Team Roster Viewer",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for WNBA branding
st.markdown("""
    <style>
    .main {
        background-color: #F5F5F5;
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
    st.markdown("---")
    
    # Back button
    if st.button("← Back to Roster", use_container_width=False):
        st.session_state.selected_player_id = None
        st.rerun()
    
    # Player header
    st.title(f"#{player.get('number', '--')} {player.get('name', 'Unknown')}")
    st.subheader(player.get('position', 'Position Unknown'))
    
    # Fetch details if not already fetched
    if not player.get('details_fetched', False):
        with st.spinner('Loading player details...'):
            details = st.session_state.fetcher.fetch_single_player_details(player.get('id', ''))
            player.update(details)
            player['details_fetched'] = True
            
            # Update in current roster
            if st.session_state.current_roster:
                for p in st.session_state.current_roster.get('players', []):
                    if p.get('id') == player.get('id'):
                        p.update(details)
                        p['details_fetched'] = True
                        break
                # Save updated roster
                st.session_state.fetcher.save_roster(st.session_state.current_roster)
    
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
                st.markdown("### 📷")
        else:
            st.markdown("### 📷")
        
        # Bio Information
        st.markdown("### 📋 Bio Information")
        bio_data = [
            ('Height', player.get('height', '--')),
            ('Weight', player.get('weight', '--')),
            ('College', player.get('college', '--')),
            ('Experience', player.get('experience', '--')),
            ('Birth Date', player.get('birth_date', '--')),
            ('Birth Place', player.get('birth_place', '--')),
        ]
        
        for label, value in bio_data:
            st.write(f"**{label}:** {value}")
    
    with col_right:
        # Season Statistics
        st.markdown("### 📈 Season Statistics (2025)")
        
        # Main stats
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        with metric_col1:
            st.metric("PPG", player.get('ppg', '--'))
        with metric_col2:
            st.metric("RPG", player.get('rpg', '--'))
        with metric_col3:
            st.metric("APG", player.get('apg', '--'))
        
        st.markdown("### 🎯 Shooting Percentages")
        
        # Shooting percentages
        shoot_col1, shoot_col2, shoot_col3 = st.columns(3)
        with shoot_col1:
            st.metric("FG%", player.get('fgp', '--'))
        with shoot_col2:
            st.metric("3P%", player.get('3pp', '--'))
        with shoot_col3:
            st.metric("FT%", player.get('ftp', '--'))
        
        st.markdown("### 📊 Other Stats")
        
        # Other stats
        other_col1, other_col2, other_col3, other_col4 = st.columns(4)
        with other_col1:
            st.metric("SPG", player.get('spg', '--'))
        with other_col2:
            st.metric("BPG", player.get('bpg', '--'))
        with other_col3:
            st.metric("TPG", player.get('tpg', '--'))
        with other_col4:
            st.metric("MPG", player.get('mpg', '--'))
# Header
# Try to load WNBA logo from local file
logo_col, title_col = st.columns([1, 4])

with logo_col:
    try:
        logo_img = Image.open("WNBA_logo.svg.webp")
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
    st.header("⚙️ Team Selection")
    
    # Team dropdown
    teams = st.session_state.fetcher.get_all_teams()
    selected_team = st.selectbox(
        "Choose a WNBA Team:",
        teams,
        index=teams.index("Indiana Fever") if "Indiana Fever" in teams else 0
    )
    
    st.caption("*Portland Fire and Toronto Tempo are 2026 expansion teams")
    
    st.markdown("---")
    
    # Action buttons
    if st.button("🔄 Fetch Roster from Web", use_container_width=True):
        with st.spinner(f'Fetching roster for {selected_team}...'):
            progress_bar = st.progress(0)
            
            progress_bar.progress(20)
            roster_data = st.session_state.fetcher.fetch_team_roster(selected_team)
            
            progress_bar.progress(60)
            st.session_state.fetcher.save_roster(roster_data)
            
            progress_bar.progress(80)
            st.session_state.current_roster = roster_data
            
            progress_bar.progress(100)
            time.sleep(0.5)
            progress_bar.empty()
            
        st.success(f"✅ Roster loaded for {selected_team}!")
        st.rerun()
    
    if st.button("💾 Load Saved Roster", use_container_width=True):
        roster_data = st.session_state.fetcher.load_roster(selected_team)
        if roster_data:
            st.session_state.current_roster = roster_data
            st.success(f"✅ Loaded saved roster for {selected_team}!")
            st.rerun()
        else:
            st.warning("⚠️ No saved data found. Try fetching from web first.")
    
    if st.button("🔄 Fetch All Player Details", use_container_width=True):
        if st.session_state.current_roster:
            players = st.session_state.current_roster.get('players', [])
            to_fetch = [p for p in players if not p.get('details_fetched', False)]
            
            if to_fetch:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for idx, player in enumerate(to_fetch):
                    status_text.text(f"Fetching {idx+1}/{len(to_fetch)}: {player.get('name', 'Unknown')}")
                    progress_bar.progress((idx + 1) / len(to_fetch))
                    
                    details = st.session_state.fetcher.fetch_single_player_details(player.get('id', ''))
                    player.update(details)
                    player['details_fetched'] = True
                
                st.session_state.fetcher.save_roster(st.session_state.current_roster)
                
                progress_bar.empty()
                status_text.empty()
                st.success(f"✅ Fetched details for {len(to_fetch)} players!")
                st.rerun()
            else:
                st.info("ℹ️ All player details already loaded!")
        else:
            st.warning("⚠️ Please load a roster first!")
    
    if st.button("🗑️ Clear Display", use_container_width=True):
        st.session_state.current_roster = None
        st.session_state.expanded_players.clear()
        st.rerun()
    
    st.markdown("---")
    
    # Saved rosters info
    saved_teams = st.session_state.fetcher.get_all_saved_rosters()
    st.info(f"💾 Saved rosters: {len(saved_teams)} teams")

# Main content area
if st.session_state.current_roster:
    roster_data = st.session_state.current_roster
    
    # Check if a player is selected
    if st.session_state.selected_player_id:
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
        # Team header
        st.header(f"{roster_data['team_name']}")
        
        # Status check
        if roster_data['status'] == 'expansion_2026':
            st.warning(f"⚠️ {roster_data.get('message', 'Expansion team - roster not yet available')}")
        elif roster_data['status'] == 'error':
            st.error(f"❌ Error: {roster_data.get('error', 'Unknown error occurred')}")
        else:
            # Display roster info
            players = roster_data.get('players', [])
            fetched_time = roster_data.get('fetched_at', '')[:19].replace('T', ' ')
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Players", len(players))
            with col2:
                st.metric("Last Updated", fetched_time)
            with col3:
                details_loaded = sum(1 for p in players if p.get('details_fetched', False))
                st.metric("Details Loaded", f"{details_loaded}/{len(players)}")
            
            st.markdown("---")
            
            # Display players
            if players:
                st.subheader("📋 Team Roster")
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
            else:
                st.info("ℹ️ No players found in roster")

else:
    # Welcome screen
    st.info("👈 Select a team from the sidebar and click 'Fetch Roster from Web' to get started!")
    
    # Show some stats
    st.subheader("📊 Quick Stats")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total WNBA Teams", len(st.session_state.fetcher.get_all_teams()))
    
    with col2:
        saved_count = len(st.session_state.fetcher.get_all_saved_rosters())
        st.metric("Saved Rosters", saved_count)
    
    # Instructions
    st.markdown("---")
    st.markdown("""
    ### 📖 How to Use
    
    1. **Select a team** from the dropdown in the sidebar
    2. **Fetch roster** from the web or load a saved one
    3. **Click on player cards** to expand and view detailed statistics
    4. **Use "Fetch All Details"** to load bio and advanced stats for all players at once
    
    ### ✨ Features
    
    - 🏀 Browse all 15 WNBA teams (including 2026 expansion)
    - 📸 High-quality player photos
    - 📊 Comprehensive statistics (PPG, RPG, APG, FG%, 3P%, etc.)
    - 💾 Save and load roster data
    - 🔄 Real-time data from official WNBA websites
    """)

# Footer
st.markdown("---")
st.caption("Data sourced from official WNBA team websites • Built with Streamlit")
