"""
WNBA Team Roster Viewer - Modern GUI (matching webapp interface)
Allows users to select teams visually and fetch/view roster data
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font as tkfont
from roster_fetcher import WNBARosterFetcher
from stats_guide import STATS_GUIDE, STATS_TIP, STAT_DEFINITIONS
import json
from PIL import Image, ImageTk
import requests
from io import BytesIO
import threading
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


class ModernRosterGUI:
    """Modern GUI for viewing WNBA team rosters (matches webapp interface)"""
    
    def __init__(self, root):
        """Initialize the modern GUI"""
        self.root = root
        self.root.title("WNBA Team Roster Viewer")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Colors matching webapp
        self.bg_color = "#F5F5F5"
        self.wnba_orange = "#FE5000"
        self.wnba_red = "#C8102E"
        self.wnba_blue = "#006BB6"
        self.wnba_black = "#000000"
        self.wnba_white = "#FFFFFF"
        
        self.root.configure(bg=self.bg_color)
        
        # Initialize fetcher
        self.fetcher = WNBARosterFetcher()
        
        # State
        self.current_roster = None
        self.selected_player_id = None
        self.image_cache = {}
        self.team_logo_cache = {}
        self.sort_by = tk.StringVar(value="Number")
        self.view_mode = 'team_selection'  # 'team_selection', 'roster', 'schedule', 'player'
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main UI"""
        # Header
        self.create_header()
        
        # Main content area (will switch between team selection and roster view)
        self.content_frame = tk.Frame(self.root, bg=self.bg_color)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Show team selection by default
        self.show_team_selection()
        
    def create_header(self):
        """Create the header with title and WNBA logo"""
        header = tk.Frame(self.root, bg=self.wnba_black, height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Container for logo and title
        header_container = tk.Frame(header, bg=self.wnba_black)
        header_container.pack(expand=True)
        
        # WNBA logo
        logo_path = 'logos/WNBA_logo.png'
        if os.path.exists(logo_path):
            try:
                img = Image.open(logo_path)
                img.thumbnail((60, 60), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.wnba_header_logo = photo  # Keep reference
                
                logo_label = tk.Label(
                    header_container,
                    image=photo,
                    bg=self.wnba_black
                )
                logo_label.pack(side=tk.LEFT, padx=(0, 15))
            except:
                pass
        
        title = tk.Label(
            header_container,
            text="TEAM ROSTER VIEWER",
            font=("Arial", 24, "bold"),
            bg=self.wnba_black,
            fg=self.wnba_white
        )
        title.pack(side=tk.LEFT)
        
    def show_team_selection(self):
        """Show visual team selection screen with logo grid"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Reset state
        self.current_roster = None
        self.selected_player_id = None
        
        # Title
        title = tk.Label(
            self.content_frame,
            text="Select a Team",
            font=("Arial", 20, "bold"),
            bg=self.bg_color,
            fg=self.wnba_black
        )
        title.pack(pady=(0, 5))
        
        caption = tk.Label(
            self.content_frame,
            text="*Portland Fire and Toronto Tempo are 2026 expansion teams",
            font=("Arial", 9, "italic"),
            bg=self.bg_color,
            fg="#666666"
        )
        caption.pack(pady=(0, 20))
        
        # Scrollable frame for team grid
        canvas = tk.Canvas(self.content_frame, bg=self.bg_color, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg=self.bg_color)
        
        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Get teams
        teams = self.fetcher.get_all_teams()
        current_teams = [t for t in teams if t not in ['Portland Fire', 'Toronto Tempo']]
        expansion_teams = [t for t in teams if t in ['Portland Fire', 'Toronto Tempo']]
        
        # Current teams section
        current_label = tk.Label(
            scrollable,
            text="Current Teams (2025)",
            font=("Arial", 16, "bold"),
            bg=self.bg_color,
            fg=self.wnba_black
        )
        current_label.pack(pady=(10, 15))
        
        # Create grid for current teams (5 columns)
        current_grid = tk.Frame(scrollable, bg=self.bg_color)
        current_grid.pack(fill=tk.X, padx=50, pady=10)
        
        for i, team in enumerate(current_teams):
            row = i // 5
            col = i % 5
            self.create_team_button(current_grid, team, row, col)
        
        # Expansion teams section
        expansion_label = tk.Label(
            scrollable,
            text="2026 Expansion Teams",
            font=("Arial", 16, "bold"),
            bg=self.bg_color,
            fg=self.wnba_black
        )
        expansion_label.pack(pady=(30, 15))
        
        expansion_grid = tk.Frame(scrollable, bg=self.bg_color)
        expansion_grid.pack(fill=tk.X, padx=50, pady=10)
        
        for i, team in enumerate(expansion_teams):
            self.create_team_button(expansion_grid, team, 0, i)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind mousewheel
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        
    def create_team_button(self, parent, team_name, row, col):
        """Create a team button with logo"""
        frame = tk.Frame(parent, bg=self.wnba_white, relief=tk.RAISED, borderwidth=2)
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        parent.grid_columnconfigure(col, weight=1, uniform="team")
        
        # Logo container
        logo_frame = tk.Frame(frame, bg=self.wnba_white, height=120)
        logo_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        logo_frame.pack_propagate(False)
        
        logo_label = tk.Label(logo_frame, bg=self.wnba_white)
        logo_label.pack(expand=True)
        
        # Load logo
        logo_path = TEAM_LOGOS.get(team_name)
        if logo_path and os.path.exists(logo_path) and logo_path.endswith('.png'):
            try:
                img = Image.open(logo_path)
                img.thumbnail((100, 100), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.team_logo_cache[team_name] = photo
                logo_label.config(image=photo)
            except Exception as e:
                # Use team abbreviation as fallback
                logo_label.config(text=team_name.split()[0], font=("Arial", 14, "bold"), fg=self.wnba_orange)
        else:
            # For SVG files or missing logos, show team abbreviation
            logo_label.config(text=team_name.split()[0], font=("Arial", 14, "bold"), fg=self.wnba_orange)
        
        # Team button
        btn = tk.Button(
            frame,
            text=team_name,
            command=lambda t=team_name: self.load_team_roster(t),
            bg=self.wnba_orange,
            fg=self.wnba_white,
            font=("Arial", 10, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        btn.pack(fill=tk.X, padx=10, pady=(5, 10))
        
    def load_team_roster(self, team_name):
        """Load and display team roster"""
        # Show loading
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        loading = tk.Label(
            self.content_frame,
            text=f"Loading {team_name}...",
            font=("Arial", 16),
            bg=self.bg_color
        )
        loading.pack(expand=True)
        self.root.update()
        
        def fetch_in_background():
            try:
                roster_data = self.fetcher.fetch_team_roster(team_name)
                
                # Fetch team season statistics
                team_stats = self.fetcher.fetch_team_season_stats(team_name)
                if team_stats:
                    roster_data['team_stats'] = team_stats
                
                self.current_roster = roster_data
                self.root.after(0, lambda: self.show_roster_view(roster_data))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to load roster:\n{str(e)}"))
                self.root.after(0, self.show_team_selection)
        
        threading.Thread(target=fetch_in_background, daemon=True).start()
    
    def show_roster_view(self, roster_data):
        """Display the roster view"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Set view mode
        self.view_mode = 'roster'
        
        # Sidebar and main area
        sidebar = tk.Frame(self.content_frame, bg=self.wnba_white, width=250)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        sidebar.pack_propagate(False)
        
        main_area = tk.Frame(self.content_frame, bg=self.bg_color)
        main_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Sidebar content
        self.create_sidebar(sidebar)
        
        # Main area content
        # Check for expansion teams - show message but still display the view
        if roster_data.get('status') == 'expansion_2026':
            # Show expansion team message in main area
            expansion_frame = tk.Frame(main_area, bg=self.wnba_white)
            expansion_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
            
            tk.Label(
                expansion_frame,
                text=roster_data.get('message', 'Expansion team - roster not yet available'),
                font=("Arial", 12),
                bg=self.wnba_white,
                fg="#856404",
                wraplength=600
            ).pack(pady=20)
            
            # Still show next game if available
            try:
                team_name = roster_data.get('team_name', '')
                next_game = self.fetcher.fetch_next_game(team_name)
                if next_game:
                    next_game_frame = tk.Frame(expansion_frame, bg="#E8F4F8", relief=tk.RAISED, borderwidth=1)
                    next_game_frame.pack(fill=tk.X, padx=15, pady=15)
                    
                    tk.Label(
                        next_game_frame,
                        text=f"Next Game: {next_game['home_away']} {next_game['opponent']} - {next_game['date']} at {next_game['time']}",
                        font=("Arial", 12, "bold"),
                        bg="#E8F4F8",
                        fg=self.wnba_blue,
                        wraplength=600,
                        justify="left"
                    ).pack(padx=15, pady=15)
            except:
                pass
            return
        
        if self.selected_player_id:
            self.view_mode = 'player'
            self.show_player_details(main_area)
        else:
            self.show_roster_list(main_area)
    
    def create_sidebar(self, sidebar):
        """Create sidebar with navigation and actions"""
        # Back button
        back_btn = tk.Button(
            sidebar,
            text="← Back to Main Page",
            command=self.show_team_selection,
            bg=self.wnba_orange,
            fg=self.wnba_white,
            font=("Arial", 10, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            padx=15,
            pady=10
        )
        back_btn.pack(fill=tk.X, padx=10, pady=(10, 5))
        
        # If viewing player details or schedule, add back to roster button
        if self.selected_player_id or self.view_mode == 'schedule':
            back_roster_btn = tk.Button(
                sidebar,
                text="← Back to Roster",
                command=lambda: self.set_selected_player(None) if self.selected_player_id else self.show_roster_view(self.current_roster),
                bg=self.wnba_blue,
                fg=self.wnba_white,
                font=("Arial", 10, "bold"),
                cursor="hand2",
                relief=tk.FLAT,
                padx=15,
                pady=10
            )
            back_roster_btn.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Frame(sidebar, bg=self.wnba_white, height=20).pack()
        
        # View Schedule button (only show when viewing roster, not player details or schedule)
        if self.view_mode == 'roster' and not self.selected_player_id:
            schedule_btn = tk.Button(
                sidebar,
                text="View Team Schedule",
                command=self.show_schedule_view,
                bg=self.wnba_orange,
                fg=self.wnba_white,
                font=("Arial", 10, "bold"),
                cursor="hand2",
                relief=tk.FLAT,
                wraplength=200,
                padx=15,
                pady=10
            )
            schedule_btn.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Frame(sidebar, bg=self.wnba_white, height=10).pack()
        
        # Fetch all details button
        fetch_all_btn = tk.Button(
            sidebar,
            text="Fetch All Player Details",
            command=self.fetch_all_player_details,
            bg=self.wnba_blue,
            fg=self.wnba_white,
            font=("Arial", 10, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            wraplength=200,
            padx=15,
            pady=10
        )
        fetch_all_btn.pack(fill=tk.X, padx=10, pady=5)
        
        # Download roster button
        download_btn = tk.Button(
            sidebar,
            text="Download Roster (JSON)",
            command=self.download_roster,
            bg=self.wnba_black,
            fg=self.wnba_white,
            font=("Arial", 10, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            wraplength=200,
            padx=15,
            pady=10
        )
        download_btn.pack(fill=tk.X, padx=10, pady=5)
        
        # Stats guide button
        guide_btn = tk.Button(
            sidebar,
            text="Basketball Stats Guide",
            command=self.show_stats_guide,
            bg=self.wnba_blue,
            fg=self.wnba_white,
            font=("Arial", 10),
            cursor="hand2",
            relief=tk.FLAT,
            wraplength=200,
            padx=15,
            pady=10
        )
        guide_btn.pack(fill=tk.X, padx=10, pady=5)
        
    def show_roster_list(self, main_area):
        """Show the roster list with team stats"""
        # Team header
        header_frame = tk.Frame(main_area, bg=self.bg_color)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        team_name = self.current_roster.get('team_name', '')
        
        # Team name with logo
        title_frame = tk.Frame(header_frame, bg=self.bg_color)
        title_frame.pack()
        
        # Load and display team logo
        logo_path = TEAM_LOGOS.get(team_name)
        logo_label = tk.Label(title_frame, bg=self.bg_color)
        logo_label.pack(side=tk.LEFT, padx=(0, 15))
        
        if logo_path and os.path.exists(logo_path) and logo_path.endswith('.png'):
            try:
                img = Image.open(logo_path)
                img.thumbnail((80, 80), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                # Store reference to prevent garbage collection
                if not hasattr(self, 'current_team_logo'):
                    self.current_team_logo = None
                self.current_team_logo = photo
                logo_label.config(image=photo)
            except Exception as e:
                # Use team abbreviation as fallback
                logo_label.config(text=team_name.split()[0], font=("Arial", 18, "bold"), fg=self.wnba_orange)
        else:
            # For SVG files or missing logos, show team abbreviation
            logo_label.config(text=team_name.split()[0], font=("Arial", 18, "bold"), fg=self.wnba_orange)
        
        team_title = tk.Label(
            title_frame,
            text=team_name,
            font=("Arial", 24, "bold"),
            bg=self.bg_color,
            fg=self.wnba_black
        )
        team_title.pack(side=tk.LEFT)
        
        # Team statistics
        team_stats = self.current_roster.get('team_stats')
        if team_stats:
            self.display_team_stats(main_area, team_stats)
        
        # Roster section
        roster_frame = tk.Frame(main_area, bg=self.bg_color)
        roster_frame.pack(fill=tk.BOTH, expand=True)
        
        # Roster title and sort
        controls_frame = tk.Frame(roster_frame, bg=self.bg_color)
        controls_frame.pack(fill=tk.X, pady=(10, 10))
        
        roster_label = tk.Label(
            controls_frame,
            text="Team Roster",
            font=("Arial", 16, "bold"),
            bg=self.bg_color,
            fg=self.wnba_black
        )
        roster_label.pack(side=tk.LEFT)
        
        # Sort dropdown
        sort_frame = tk.Frame(controls_frame, bg=self.bg_color)
        sort_frame.pack(side=tk.RIGHT)
        
        tk.Label(
            sort_frame,
            text="Sort by:",
            font=("Arial", 10),
            bg=self.bg_color
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        sort_combo = ttk.Combobox(
            sort_frame,
            textvariable=self.sort_by,
            values=["Number", "Name", "Position", "PPG", "RPG", "APG"],
            state='readonly',
            width=12
        )
        sort_combo.pack(side=tk.LEFT)
        sort_combo.bind('<<ComboboxSelected>>', lambda e: self.show_roster_view(self.current_roster))
        
        caption = tk.Label(
            roster_frame,
            text="Click on a player's name to view full details",
            font=("Arial", 9, "italic"),
            bg=self.bg_color,
            fg="#666666"
        )
        caption.pack(pady=(0, 10))
        
        # Player table
        self.create_player_table(roster_frame)
        
    def display_team_stats(self, parent, team_stats):
        """Display team statistics"""
        stats_frame = tk.Frame(parent, bg=self.wnba_white, relief=tk.RAISED, borderwidth=1)
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Next game info
        try:
            team_name = self.current_roster.get('team_name', '')
            next_game = self.fetcher.fetch_next_game(team_name)
            if next_game:
                next_game_frame = tk.Frame(stats_frame, bg="#E8F4F8", relief=tk.RAISED, borderwidth=1)
                next_game_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
                
                tk.Label(
                    next_game_frame,
                    text=f"Next Game: {next_game['home_away']} {next_game['opponent']} - {next_game['date']} at {next_game['time']}",
                    font=("Arial", 10, "bold"),
                    bg="#E8F4F8",
                    fg=self.wnba_blue,
                    wraplength=800,
                    justify="left"
                ).pack(padx=10, pady=10)
        except Exception as e:
            pass  # Silently skip if next game fetch fails
        
        # Big 3 stats
        big3_frame = tk.Frame(stats_frame, bg=self.wnba_white)
        big3_frame.pack(fill=tk.X, pady=15)
        
        big3_stats = [
            ("PPG", f"{team_stats.get('ppg', 0):.1f}", "Points Per Game"),
            ("RPG", f"{team_stats.get('rpg', 0):.1f}", "Rebounds Per Game"),
            ("APG", f"{team_stats.get('apg', 0):.1f}", "Assists Per Game")
        ]
        
        for stat_abbr, value, tooltip in big3_stats:
            col = tk.Frame(big3_frame, bg=self.wnba_white)
            col.pack(side=tk.LEFT, expand=True, padx=20)
            
            tk.Label(
                col,
                text=stat_abbr,
                font=("Arial", 12, "bold"),
                bg=self.wnba_white,
                fg="#666666"
            ).pack()
            
            tk.Label(
                col,
                text=value,
                font=("Arial", 28, "bold"),
                bg=self.wnba_white,
                fg=self.wnba_orange
            ).pack()
        
        # Additional stats
        tk.Frame(stats_frame, bg="#DDDDDD", height=1).pack(fill=tk.X, padx=20)
        
        additional_frame = tk.Frame(stats_frame, bg=self.wnba_white)
        additional_frame.pack(fill=tk.X, pady=15, padx=20)
        
        additional_stats = [
            ("W-L", f"{team_stats.get('w', 0)}-{team_stats.get('l', 0)}"),
            ("FG%", f"{team_stats.get('fgp', 0):.1%}"),
            ("3P%", f"{team_stats.get('3pp', 0):.1%}"),
            ("FT%", f"{team_stats.get('ftp', 0):.1%}"),
            ("SPG", f"{team_stats.get('spg', 0):.1f}"),
            ("BPG", f"{team_stats.get('bpg', 0):.1f}"),
            ("TPG", f"{team_stats.get('tpg', 0):.1f}"),
            ("OREB", f"{team_stats.get('oreb', 0):.1f}"),
            ("DREB", f"{team_stats.get('dreb', 0):.1f}"),
        ]
        
        for i, (label, value) in enumerate(additional_stats):
            col = tk.Frame(additional_frame, bg=self.wnba_white)
            col.grid(row=i//3, column=i%3, padx=15, pady=5, sticky="w")
            
            tk.Label(
                col,
                text=f"{label}:",
                font=("Arial", 10, "bold"),
                bg=self.wnba_white
            ).pack(side=tk.LEFT)
            
            tk.Label(
                col,
                text=value,
                font=("Arial", 10),
                bg=self.wnba_white,
                fg=self.wnba_blue
            ).pack(side=tk.LEFT, padx=5)
        
    def create_player_table(self, parent):
        """Create scrollable player table"""
        # Canvas for scrolling
        canvas = tk.Canvas(parent, bg=self.wnba_white, highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg=self.wnba_white)
        
        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Header row
        header = tk.Frame(scrollable, bg=self.wnba_orange, height=40)
        header.pack(fill=tk.X, pady=(0, 1))
        
        headers = [("#", 50), ("Player Name", 250), ("Position", 100), ("PPG", 80), ("RPG", 80), ("APG", 80)]
        for text, width in headers:
            tk.Label(
                header,
                text=text,
                bg=self.wnba_orange,
                fg=self.wnba_white,
                font=("Arial", 10, "bold"),
                width=width//8
            ).pack(side=tk.LEFT, padx=5)
        
        # Sort players
        players = self.current_roster.get('players', [])
        players = self.sort_players(players)
        
        # Player rows
        for idx, player in enumerate(players):
            bg = "#F5F5F5" if idx % 2 == 0 else self.wnba_white
            self.create_player_row(scrollable, player, bg)
        
        # Footer info
        footer = tk.Frame(scrollable, bg=self.wnba_white)
        footer.pack(fill=tk.X, pady=20)
        
        fetched_time = self.current_roster.get('fetched_at', '')[:19].replace('T', ' ')
        details_loaded = sum(1 for p in players if p.get('details_fetched', False))
        
        info_frame = tk.Frame(footer, bg=self.wnba_white)
        info_frame.pack()
        
        metrics = [
            ("Total Players", len(players)),
            ("Last Updated", fetched_time),
            ("Details Loaded", f"{details_loaded}/{len(players)}")
        ]
        
        for label, value in metrics:
            col = tk.Frame(info_frame, bg=self.wnba_white)
            col.pack(side=tk.LEFT, padx=20)
            
            tk.Label(
                col,
                text=label,
                font=("Arial", 9, "bold"),
                bg=self.wnba_white,
                fg="#666666"
            ).pack()
            
            tk.Label(
                col,
                text=str(value),
                font=("Arial", 12, "bold"),
                bg=self.wnba_white,
                fg=self.wnba_blue
            ).pack()
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    
    def sort_players(self, players):
        """Sort players based on selected criterion"""
        sort_by = self.sort_by.get()
        
        sort_map = {
            "Number": lambda p: int(p.get('number', '0') or '0'),
            "Name": lambda p: p.get('name', ''),
            "Position": lambda p: p.get('position', ''),
            "PPG": lambda p: float(p.get('ppg', '0') or '0'),
            "RPG": lambda p: float(p.get('rpg', '0') or '0'),
            "APG": lambda p: float(p.get('apg', '0') or '0'),
        }
        
        return sorted(players, key=sort_map.get(sort_by, sort_map["Number"]))
    
    def create_player_row(self, parent, player, bg):
        """Create a clickable player row"""
        row = tk.Frame(parent, bg=bg, cursor="hand2")
        row.pack(fill=tk.X, pady=1)
        
        # Number
        tk.Label(
            row,
            text=f"#{player.get('number', '--')}",
            bg=bg,
            font=("Arial", 10, "bold"),
            width=50//8
        ).pack(side=tk.LEFT, padx=5)
        
        # Name (clickable button)
        name_btn = tk.Button(
            row,
            text=player.get('name', 'Unknown'),
            bg=bg,
            fg=self.wnba_blue,
            font=("Arial", 10, "bold", "underline"),
            relief=tk.FLAT,
            cursor="hand2",
            anchor="w",
            width=250//8,
            command=lambda: self.set_selected_player(player.get('id'))
        )
        name_btn.pack(side=tk.LEFT, padx=5)
        
        # Position
        tk.Label(
            row,
            text=player.get('position', '--'),
            bg=bg,
            font=("Arial", 10),
            width=100//8
        ).pack(side=tk.LEFT, padx=5)
        
        # Stats
        for stat in ['ppg', 'rpg', 'apg']:
            value = player.get(stat, '--')
            tk.Label(
                row,
                text=value if value else '--',
                bg=bg,
                font=("Arial", 10),
                width=80//8
            ).pack(side=tk.LEFT, padx=5)
    
    def set_selected_player(self, player_id):
        """Set selected player and refresh view"""
        self.selected_player_id = player_id
        self.show_roster_view(self.current_roster)
    
    def show_player_details(self, main_area):
        """Show detailed player view"""
        # Find player
        player = None
        for p in self.current_roster.get('players', []):
            if p.get('id') == self.selected_player_id:
                player = p
                break
        
        if not player:
            self.set_selected_player(None)
            return
        
        # Fetch details if needed
        if not player.get('details_fetched', False):
            loading = tk.Label(
                main_area,
                text=f"Loading details for {player.get('name')}...",
                font=("Arial", 16),
                bg=self.bg_color
            )
            loading.pack(expand=True)
            self.root.update()
            
            def fetch_details():
                team_name = self.current_roster.get('team_name', '')
                api_stats_dict = self.fetcher.fetch_team_stats_from_api(team_name)
                api_stats = api_stats_dict.get(player.get('name', ''), None)
                details = self.fetcher.fetch_single_player_details(
                    player.get('id', ''),
                    player.get('name', ''),
                    api_stats
                )
                player.update(details)
                player['details_fetched'] = True
                
                self.root.after(0, lambda: self.show_roster_view(self.current_roster))
            
            threading.Thread(target=fetch_details, daemon=True).start()
            return
        
        # Player header
        header_frame = tk.Frame(main_area, bg=self.bg_color)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            header_frame,
            text=f"#{player.get('number', '--')} {player.get('name', 'Unknown')}",
            font=("Arial", 24, "bold"),
            bg=self.bg_color,
            fg=self.wnba_black
        ).pack()
        
        tk.Label(
            header_frame,
            text=player.get('position', 'Position Unknown'),
            font=("Arial", 14),
            bg=self.bg_color,
            fg="#666666"
        ).pack()
        
        # Content area with scroll
        canvas = tk.Canvas(main_area, bg=self.bg_color, highlightthickness=0)
        scrollbar = tk.Scrollbar(main_area, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg=self.bg_color)
        
        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Two column layout
        content_frame = tk.Frame(scrollable, bg=self.bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        left_col = tk.Frame(content_frame, bg=self.bg_color)
        left_col.grid(row=0, column=0, sticky="nw", padx=(0, 20))
        
        right_col = tk.Frame(content_frame, bg=self.bg_color)
        right_col.grid(row=0, column=1, sticky="new")
        
        # Left column - Photo and Bio
        # Player photo
        photo_frame = tk.Frame(left_col, bg=self.wnba_white, relief=tk.RAISED, borderwidth=1)
        photo_frame.pack(pady=(0, 20))
        
        photo_label = tk.Label(photo_frame, bg=self.wnba_white, width=200, height=200)
        photo_label.pack(padx=10, pady=10)
        
        image_url = player.get('image_url', '')
        if image_url:
            try:
                response = requests.get(image_url, timeout=3)
                if response.status_code == 200:
                    img = Image.open(BytesIO(response.content))
                    img.thumbnail((180, 180), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    self.image_cache[player.get('id')] = photo
                    photo_label.config(image=photo, width=180, height=180)
                else:
                    photo_label.config(text="[No Photo]", font=("Arial", 14))
            except:
                photo_label.config(text="[No Photo]", font=("Arial", 14))
        else:
            photo_label.config(text="[No Photo]", font=("Arial", 14))
        
        # Bio information
        bio_frame = tk.Frame(left_col, bg=self.wnba_white, relief=tk.RAISED, borderwidth=1)
        bio_frame.pack(fill=tk.X)
        
        tk.Label(
            bio_frame,
            text="Bio Information",
            font=("Arial", 14, "bold"),
            bg=self.wnba_white,
            fg=self.wnba_orange
        ).pack(pady=(10, 10))
        
        bio_data = [
            ('Height', player.get('height', '--')),
            ('Weight', player.get('weight', '--')),
            ('College', player.get('college', '--')),
            ('Experience', player.get('experience', '--')),
            ('Birth Date', player.get('birth_date', '--')),
            ('Draft', player.get('draft', '--')),
        ]
        
        for label, value in bio_data:
            row_frame = tk.Frame(bio_frame, bg=self.wnba_white)
            row_frame.pack(fill=tk.X, padx=15, pady=3)
            
            tk.Label(
                row_frame,
                text=f"{label}:",
                font=("Arial", 10, "bold"),
                bg=self.wnba_white,
                width=12,
                anchor="e"
            ).pack(side=tk.LEFT)
            
            tk.Label(
                row_frame,
                text=value,
                font=("Arial", 10),
                bg=self.wnba_white,
                anchor="w"
            ).pack(side=tk.LEFT, padx=10)
        
        tk.Frame(bio_frame, height=10).pack()
        
        # Right column - Statistics
        stats_container = tk.Frame(right_col, bg=self.wnba_white, relief=tk.RAISED, borderwidth=1)
        stats_container.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            stats_container,
            text="Season Statistics (2025)",
            font=("Arial", 14, "bold"),
            bg=self.wnba_white,
            fg=self.wnba_orange
        ).pack(pady=(10, 15))
        
        # Main metrics
        metrics_frame = tk.Frame(stats_container, bg=self.wnba_white)
        metrics_frame.pack(fill=tk.X, padx=20, pady=10)
        
        main_stats = [
            ("PPG", player.get('ppg', '--'), "Points Per Game"),
            ("RPG", player.get('rpg', '--'), "Rebounds Per Game"),
            ("APG", player.get('apg', '--'), "Assists Per Game")
        ]
        
        for stat, value, tooltip in main_stats:
            col = tk.Frame(metrics_frame, bg=self.wnba_white)
            col.pack(side=tk.LEFT, expand=True, padx=10)
            
            tk.Label(
                col,
                text=stat,
                font=("Arial", 10, "bold"),
                bg=self.wnba_white,
                fg="#666666"
            ).pack()
            
            tk.Label(
                col,
                text=value if value else '--',
                font=("Arial", 20, "bold"),
                bg=self.wnba_white,
                fg=self.wnba_orange
            ).pack()
        
        # Shooting percentages
        tk.Label(
            stats_container,
            text="Shooting Percentages",
            font=("Arial", 12, "bold"),
            bg=self.wnba_white,
            fg=self.wnba_black
        ).pack(pady=(15, 10))
        
        shooting_frame = tk.Frame(stats_container, bg=self.wnba_white)
        shooting_frame.pack(fill=tk.X, padx=20, pady=10)
        
        shooting_stats = [
            ("FG%", player.get('fgp', '--')),
            ("3P%", player.get('3pp', '--')),
            ("FT%", player.get('ftp', '--'))
        ]
        
        for stat, value in shooting_stats:
            col = tk.Frame(shooting_frame, bg=self.wnba_white)
            col.pack(side=tk.LEFT, expand=True, padx=10)
            
            tk.Label(
                col,
                text=stat,
                font=("Arial", 10, "bold"),
                bg=self.wnba_white,
                fg="#666666"
            ).pack()
            
            tk.Label(
                col,
                text=value if value else '--',
                font=("Arial", 16, "bold"),
                bg=self.wnba_white,
                fg=self.wnba_blue
            ).pack()
        
        # Other stats grid
        tk.Label(
            stats_container,
            text="Additional Statistics",
            font=("Arial", 12, "bold"),
            bg=self.wnba_white,
            fg=self.wnba_black
        ).pack(pady=(15, 10))
        
        other_stats_frame = tk.Frame(stats_container, bg=self.wnba_white)
        other_stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        other_stats = [
            ('GP', 'gp'), ('MPG', 'mpg'), ('SPG', 'spg'),
            ('BPG', 'bpg'), ('TPG', 'tpg'), ('+/-', 'plus_minus'),
            ('OREB', 'oreb'), ('DREB', 'dreb'), ('PF', 'pf')
        ]
        
        for i, (label, key) in enumerate(other_stats):
            row = i // 3
            col = i % 3
            
            stat_frame = tk.Frame(other_stats_frame, bg=self.wnba_white)
            stat_frame.grid(row=row, column=col, padx=15, pady=5, sticky="w")
            
            tk.Label(
                stat_frame,
                text=f"{label}:",
                font=("Arial", 10, "bold"),
                bg=self.wnba_white,
                width=6,
                anchor="e"
            ).pack(side=tk.LEFT)
            
            value = player.get(key, '--')
            tk.Label(
                stat_frame,
                text=value if value else '--',
                font=("Arial", 10),
                bg=self.wnba_white,
                fg=self.wnba_blue,
                width=8,
                anchor="w"
            ).pack(side=tk.LEFT, padx=5)
        
        tk.Frame(stats_container, height=20).pack()
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    
    def show_schedule_view(self):
        """Display the team schedule"""
        if not self.current_roster:
            return
        
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Set view mode
        self.view_mode = 'schedule'
        
        # Sidebar and main area
        sidebar = tk.Frame(self.content_frame, bg=self.wnba_white, width=250)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        sidebar.pack_propagate(False)
        
        main_area = tk.Frame(self.content_frame, bg=self.bg_color)
        main_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Sidebar content
        self.create_sidebar(sidebar)
        
        # Team header
        team_name = self.current_roster.get('team_name', '')
        
        header_frame = tk.Frame(main_area, bg=self.bg_color)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Team name with logo
        title_frame = tk.Frame(header_frame, bg=self.bg_color)
        title_frame.pack()
        
        # Load and display team logo
        logo_path = TEAM_LOGOS.get(team_name)
        logo_label = tk.Label(title_frame, bg=self.bg_color)
        logo_label.pack(side=tk.LEFT, padx=(0, 15))
        
        if logo_path and os.path.exists(logo_path) and logo_path.endswith('.png'):
            try:
                img = Image.open(logo_path)
                img.thumbnail((80, 80), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                if not hasattr(self, 'schedule_team_logo'):
                    self.schedule_team_logo = None
                self.schedule_team_logo = photo
                logo_label.config(image=photo)
            except:
                logo_label.config(text=team_name.split()[0], font=("Arial", 18, "bold"), fg=self.wnba_orange)
        else:
            logo_label.config(text=team_name.split()[0], font=("Arial", 18, "bold"), fg=self.wnba_orange)
        
        team_title = tk.Label(
            title_frame,
            text=f"{team_name} - 2026 Schedule",
            font=("Arial", 24, "bold"),
            bg=self.bg_color,
            fg=self.wnba_black
        )
        team_title.pack(side=tk.LEFT)
        
        # Fetch schedule
        games = self.fetcher.fetch_team_schedule(team_name)
        
        if games:
            # Info label
            info_label = tk.Label(
                main_area,
                text=f"{len(games)} games scheduled for the 2026 season",
                font=("Arial", 12, "bold"),
                bg=self.bg_color,
                fg=self.wnba_blue
            )
            info_label.pack(pady=10)
            
            # Create scrollable frame for games
            canvas = tk.Canvas(main_area, bg=self.wnba_white, highlightthickness=0)
            scrollbar = tk.Scrollbar(main_area, orient="vertical", command=canvas.yview)
            scrollable = tk.Frame(canvas, bg=self.wnba_white)
            
            scrollable.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Display games
            for idx, game in enumerate(games):
                bg = "#F5F5F5" if idx % 2 == 0 else self.wnba_white
                
                game_frame = tk.Frame(scrollable, bg=bg, pady=10, padx=15)
                game_frame.pack(fill=tk.X)
                
                # Date
                date_label = tk.Label(
                    game_frame,
                    text=game['date'],
                    font=("Arial", 11, "bold"),
                    bg=bg,
                    fg=self.wnba_black,
                    width=25,
                    anchor="w"
                )
                date_label.pack(side=tk.LEFT, padx=5)
                
                # Home/Away indicator and opponent
                if game['home_away'] == 'vs':
                    matchup_text = f"Home vs {game['opponent']}"
                else:
                    matchup_text = f"Away @ {game['opponent']}"
                
                matchup_label = tk.Label(
                    game_frame,
                    text=matchup_text,
                    font=("Arial", 11, "bold"),
                    bg=bg,
                    fg=self.wnba_blue,
                    width=20,
                    anchor="w"
                )
                matchup_label.pack(side=tk.LEFT, padx=10)
                
                # Time
                time_label = tk.Label(
                    game_frame,
                    text=game['time'],
                    font=("Arial", 10, "italic"),
                    bg=bg,
                    fg="#666666",
                    width=12,
                    anchor="w"
                )
                time_label.pack(side=tk.LEFT, padx=5)
                
                # Game type
                type_label = tk.Label(
                    game_frame,
                    text=game['game_type'],
                    font=("Arial", 10, "italic"),
                    bg=bg,
                    fg="#999999"
                )
                type_label.pack(side=tk.LEFT, padx=5)
                
                # Divider
                if idx < len(games) - 1:
                    tk.Frame(scrollable, bg="#DDDDDD", height=1).pack(fill=tk.X, padx=15)
            
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
            
            canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        else:
            tk.Label(
                main_area,
                text="Schedule not available yet for this team",
                font=("Arial", 14),
                bg=self.bg_color,
                fg="#666666"
            ).pack(pady=50)
    
    def fetch_all_player_details(self):
        """Fetch details for all players"""
        if not self.current_roster:
            return
        
        players = self.current_roster.get('players', [])
        to_fetch = [p for p in players if not p.get('details_fetched', False)]
        
        if not to_fetch:
            messagebox.showinfo("Complete", "All player details already loaded!")
            return
        
        result = messagebox.askyesno(
            "Fetch All Details",
            f"Fetch comprehensive stats for {len(to_fetch)} players?\n\nThis may take a moment."
        )
        
        if not result:
            return
        
        # Show progress window
        progress_win = tk.Toplevel(self.root)
        progress_win.title("Loading Player Details")
        progress_win.geometry("400x100")
        progress_win.transient(self.root)
        progress_win.grab_set()
        
        tk.Label(
            progress_win,
            text="Fetching player details...",
            font=("Arial", 12)
        ).pack(pady=20)
        
        progress_bar = ttk.Progressbar(progress_win, length=300, mode='determinate')
        progress_bar.pack(pady=10)
        
        def fetch_all():
            team_name = self.current_roster.get('team_name', '')
            self.fetcher.fetch_all_player_details(to_fetch, team_name)
            
            for player in to_fetch:
                player['details_fetched'] = True
            
            self.root.after(0, progress_win.destroy)
            self.root.after(0, lambda: self.show_roster_view(self.current_roster))
            self.root.after(0, lambda: messagebox.showinfo("Complete", f"Loaded details for {len(to_fetch)} players!"))
        
        threading.Thread(target=fetch_all, daemon=True).start()
    
    def download_roster(self):
        """Download current roster as JSON"""
        if not self.current_roster:
            messagebox.showwarning("No Roster", "Please load a roster first.")
            return
        
        team_slug = self.current_roster.get('team_slug', 'roster')
        default_filename = f"{team_slug}_roster.json"
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=default_filename
        )
        
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(self.current_roster, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Success", f"Roster saved to:\n{filepath}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save:\n{str(e)}")
    
    def show_stats_guide(self):
        """Show statistics guide window"""
        guide_win = tk.Toplevel(self.root)
        guide_win.title("Basketball Statistics Guide")
        guide_win.geometry("900x700")
        
        # Header
        header = tk.Frame(guide_win, bg=self.wnba_orange, height=60)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="Basketball Statistics Guide",
            font=("Arial", 16, "bold"),
            bg=self.wnba_orange,
            fg=self.wnba_white
        ).pack(expand=True)
        
        # Scrollable content
        canvas = tk.Canvas(guide_win, bg=self.wnba_white)
        scrollbar = tk.Scrollbar(guide_win, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg=self.wnba_white)
        
        scrollable.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Display stats guide
        for category, stats_list in STATS_GUIDE.items():
            category_frame = tk.LabelFrame(
                scrollable,
                text=category,
                font=("Arial", 12, "bold"),
                bg=self.wnba_white,
                fg=self.wnba_orange,
                padx=15,
                pady=10
            )
            category_frame.pack(fill=tk.X, padx=20, pady=10)
            
            for abbr, name, description in stats_list:
                stat_row = tk.Frame(category_frame, bg=self.wnba_white)
                stat_row.pack(fill=tk.X, pady=3)
                
                tk.Label(
                    stat_row,
                    text=abbr,
                    font=("Arial", 9, "bold"),
                    bg=self.wnba_white,
                    fg=self.wnba_orange,
                    width=10,
                    anchor="w"
                ).pack(side=tk.LEFT)
                
                tk.Label(
                    stat_row,
                    text=name,
                    font=("Arial", 9, "bold"),
                    bg=self.wnba_white,
                    width=25,
                    anchor="w"
                ).pack(side=tk.LEFT)
                
                tk.Label(
                    stat_row,
                    text=description,
                    font=("Arial", 9),
                    bg=self.wnba_white,
                    wraplength=400,
                    anchor="w"
                ).pack(side=tk.LEFT, padx=10)
        
        # Tip
        tip_frame = tk.Frame(scrollable, bg="#E8F4F8", relief=tk.RIDGE, borderwidth=2)
        tip_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(
            tip_frame,
            text="Tip:",
            font=("Arial", 10, "bold"),
            bg="#E8F4F8",
            fg=self.wnba_orange
        ).pack(anchor="w", padx=10, pady=(10, 5))
        
        tk.Label(
            tip_frame,
            text=STATS_TIP,
            font=("Arial", 9),
            bg="#E8F4F8",
            wraplength=800,
            justify="left"
        ).pack(anchor="w", padx=10, pady=(0, 10))
        
        # Close button
        tk.Button(
            scrollable,
            text="Close",
            command=guide_win.destroy,
            bg=self.wnba_orange,
            fg=self.wnba_white,
            font=("Arial", 10, "bold"),
            padx=30,
            pady=10,
            cursor="hand2",
            relief=tk.FLAT
        ).pack(pady=20)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        guide_win.protocol("WM_DELETE_WINDOW", lambda: [canvas.unbind_all("<MouseWheel>"), guide_win.destroy()])


def main():
    """Main entry point"""
    root = tk.Tk()
    app = ModernRosterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
