"""
WNBA Team Roster Viewer - GUI
Allows users to select teams and fetch/view roster data
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from roster_fetcher import WNBARosterFetcher
from stats_guide import STATS_GUIDE, STATS_TIP
import json
from PIL import Image, ImageTk
import requests
from io import BytesIO
import threading


class RosterViewerGUI:
    """GUI for viewing and fetching WNBA team rosters"""
    
    def __init__(self, root):
        """
        Initialize the GUI
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("WNBA Team Roster Viewer")
        self.root.geometry("1000x750")
        self.root.minsize(950, 700)  # Prevent window from being too small
        
        # WNBA website colors (updated to match official site)
        self.wnba_black = "#000000"          # Main background
        self.wnba_dark_gray = "#1A1A1A"     # Secondary background
        self.wnba_orange = "#FE5000"        # WNBA primary orange
        self.wnba_white = "#FFFFFF"         # White text/backgrounds
        self.wnba_light_gray = "#F5F5F5"    # Light backgrounds
        self.wnba_red = "#C8102E"           # Accent red
        
        self.root.configure(bg=self.wnba_dark_gray)
        
        # Logo cache
        self.wnba_logo = None
        
        # Initialize the roster fetcher
        self.fetcher = WNBARosterFetcher()
        
        # Cache for player images
        self.image_cache = {}
        
        # Store current roster data
        self.current_roster_data = None
        self.expanded_player = None
        
        # Setup the UI
        self.setup_ui()
    
    def setup_ui(self):
        """Create and layout all UI elements"""
        
        # Title frame with logo
        title_frame = tk.Frame(self.root, bg=self.wnba_black, height=100)
        title_frame.pack(fill=tk.X, padx=0, pady=0)
        title_frame.pack_propagate(False)
        
        # Logo and title container
        title_container = tk.Frame(title_frame, bg=self.wnba_black)
        title_container.pack(expand=True)
        
        # Try to load WNBA logo
        logo_label = tk.Label(title_container, bg=self.wnba_black)
        logo_label.pack(side=tk.LEFT, padx=(0, 15))
        self.load_wnba_logo(logo_label)
        
        # Title text
        title_label = tk.Label(
            title_container,
            text="TEAM ROSTER VIEWER",
            font=("Arial", 28, "bold"),
            bg=self.wnba_black,
            fg=self.wnba_white
        )
        title_label.pack(side=tk.LEFT)
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg=self.wnba_dark_gray)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Team selection section
        selection_frame = tk.LabelFrame(
            content_frame,
            text="Select Team",
            font=("Arial", 12, "bold"),
            bg=self.wnba_light_gray,
            fg=self.wnba_black,
            padx=15,
            pady=15
        )
        selection_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Team dropdown
        team_label = tk.Label(
            selection_frame,
            text="Choose a WNBA Team:",
            font=("Arial", 11, "bold"),
            bg=self.wnba_light_gray,
            fg=self.wnba_black
        )
        team_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.team_var = tk.StringVar()
        self.team_combo = ttk.Combobox(
            selection_frame,
            textvariable=self.team_var,
            values=self.fetcher.get_all_teams(),
            state='readonly',
            font=("Arial", 11),
            width=30
        )
        self.team_combo.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        
        # Note about expansion teams
        note_label = tk.Label(
            selection_frame,
            text="* Portland Fire and Toronto Tempo are 2026 expansion teams",
            font=("Arial", 9, "italic"),
            bg=self.wnba_light_gray,
            fg="#666666"
        )
        note_label.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(5, 0))
        
        # Action buttons
        button_frame = tk.Frame(selection_frame, bg=self.wnba_light_gray)
        button_frame.grid(row=2, column=0, columnspan=3, pady=15)
        
        fetch_btn = tk.Button(
            button_frame,
            text="Fetch Roster from Web",
            command=self.fetch_roster,
            bg=self.wnba_orange,
            fg=self.wnba_white,
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10,
            cursor="hand2",
            relief=tk.FLAT
        )
        fetch_btn.pack(side=tk.LEFT, padx=5)
        
        download_btn = tk.Button(
            button_frame,
            text="Download Roster Data",
            command=self.download_roster,
            bg=self.wnba_black,
            fg=self.wnba_white,
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10,
            cursor="hand2",
            relief=tk.FLAT
        )
        download_btn.pack(side=tk.LEFT, padx=5)
        
        fetch_all_btn = tk.Button(
            button_frame,
            text="Fetch All Details",
            command=self.fetch_all_details,
            bg="#006BB6",
            fg=self.wnba_white,
            font=("Arial", 11, "bold"),
            padx=20,
            pady=10,
            cursor="hand2",
            relief=tk.FLAT
        )
        fetch_all_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(
            button_frame,
            text="Clear Display",
            command=self.clear_display,
            bg="#666666",
            fg=self.wnba_white,
            font=("Arial", 11),
            padx=20,
            pady=10,
            cursor="hand2",
            relief=tk.FLAT
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        guide_btn = tk.Button(
            button_frame,
            text="Stats Guide",
            command=self.show_stats_guide,
            bg="#006BB6",
            fg=self.wnba_white,
            font=("Arial", 11),
            padx=20,
            pady=10,
            cursor="hand2",
            relief=tk.FLAT
        )
        guide_btn.pack(side=tk.LEFT, padx=5)
        
        # Display area
        display_frame = tk.LabelFrame(
            content_frame,
            text="Roster Information",
            font=("Arial", 12, "bold"),
            bg=self.wnba_light_gray,
            fg=self.wnba_black,
            padx=15,
            pady=15
        )
        display_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas with scrollbar for custom roster display
        canvas_frame = tk.Frame(display_frame, bg=self.wnba_light_gray)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg='white')
        scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg='white')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind mouse wheel scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Info label for team info
        self.info_label = tk.Label(
            display_frame,
            text="Select a team and fetch roster data",
            font=("Arial", 10, "italic"),
            bg=self.wnba_light_gray,
            fg="#666666",
            wraplength=600,
            justify=tk.LEFT
        )
        self.info_label.pack(pady=(10, 0))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_frame = tk.Frame(self.root, bg=self.wnba_black)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        status_bar = tk.Label(
            status_frame,
            textvariable=self.status_var,
            bg=self.wnba_black,
            fg=self.wnba_white,
            font=("Arial", 9),
            anchor=tk.W,
            padx=10,
            pady=8
        )
        status_bar.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create a custom progress bar using Canvas for better visibility
        progress_container = tk.Frame(status_frame, bg=self.wnba_black)
        progress_container.pack(side=tk.RIGHT, padx=15, pady=5)
        
        # Label for progress percentage
        self.progress_label = tk.Label(
            progress_container,
            text="0%",
            bg=self.wnba_black,
            fg=self.wnba_white,
            font=("Arial", 9, "bold"),
            width=5
        )
        self.progress_label.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Canvas-based progress bar
        self.progress_canvas = tk.Canvas(
            progress_container,
            width=200,
            height=20,
            bg=self.wnba_dark_gray,
            highlightthickness=1,
            highlightbackground=self.wnba_white
        )
        self.progress_canvas.pack(side=tk.RIGHT)
        
        # Create the progress rectangle (initially at 0%)
        self.progress_rect = self.progress_canvas.create_rectangle(
            0, 0, 0, 20,
            fill=self.wnba_orange,
            outline=""
        )
        
        self.progress_var = tk.DoubleVar()
        self.progress_visible = True
    
    def show_progress(self):
        """Reset and show the progress bar"""
        self.progress_var.set(0)
        self.update_progress(0)
        self.root.update()
    
    def hide_progress(self):
        """Reset the progress bar to 0"""
        self.progress_var.set(0)
        self.update_progress(0)
        self.root.update()
    
    def update_progress(self, value):
        """Update the visual progress bar"""
        # Update the canvas rectangle width based on percentage
        width = int((value / 100) * 200)  # 200 is the canvas width
        self.progress_canvas.coords(self.progress_rect, 0, 0, width, 20)
        
        # Update the percentage label
        self.progress_label.config(text=f"{int(value)}%")
        self.root.update()
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def load_wnba_logo(self, label_widget):
        """
        Load WNBA logo from CDN
        
        Args:
            label_widget: Label widget to display the logo in
        """
        try:
            # Try multiple WNBA logo sources
            logo_urls = [
                'https://content.sportslogos.net/logos/45/1068/full/wnba_logo_2019_sportslogosnet-8326.png',
                'https://upload.wikimedia.org/wikipedia/en/thumb/4/4a/WNBA_logo.svg/200px-WNBA_logo.svg.png',
                'https://cdn.nba.com/logos/leagues/logo-wnba.png'
            ]
            
            for logo_url in logo_urls:
                try:
                    response = requests.get(logo_url, timeout=5)
                    if response.status_code == 200:
                        image = Image.open(BytesIO(response.content))
                        # Resize logo to fit nicely in header
                        image = image.resize((80, 80), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(image)
                        self.wnba_logo = photo
                        label_widget.config(image=photo)
                        return  # Success, exit the function
                except:
                    continue  # Try next URL
            
            # If all URLs fail, show text instead
            label_widget.config(text="WNBA", font=("Arial", 36, "bold"), 
                              fg=self.wnba_orange)
        except:
            # If everything fails, show text instead
            label_widget.config(text="WNBA", font=("Arial", 36, "bold"), 
                              fg=self.wnba_orange)
    
    def fetch_roster(self):
        """Fetch roster data from the web (quick - no detailed stats)"""
        team_name = self.team_var.get()
        
        if not team_name:
            messagebox.showwarning("No Team Selected", "Please select a team first.")
            return
        
        # Show progress bar
        self.show_progress()
        self.status_var.set(f"Fetching roster for {team_name}...")
        self.root.update()
        
        def fetch_in_background():
            try:
                # Update progress
                self.root.after(0, lambda: self.update_progress(20))
                
                # Fetch the roster (without detailed player info)
                roster_data = self.fetcher.fetch_team_roster(team_name)
                
                self.root.after(0, lambda: self.update_progress(80))
                
                # Store and display the roster
                self.current_roster_data = roster_data
                self.root.after(0, lambda: self.display_roster(roster_data))
                
                self.root.after(0, lambda: self.update_progress(100))
                self.root.after(0, lambda: self.status_var.set(f"Roster loaded! Click players for details."))
                
                # Keep progress bar at 100% for at least 1.5 seconds before resetting
                self.root.after(1500, self.hide_progress)
                
                self.root.after(0, lambda: messagebox.showinfo(
                    "Success",
                    f"Roster for {team_name} loaded!\nClick on any player to see their details."
                ))
                
            except Exception as e:
                self.root.after(0, lambda: self.status_var.set("Error occurred"))
                self.root.after(0, self.hide_progress)
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to fetch roster:\n{str(e)}"))
        
        # Run in background thread
        threading.Thread(target=fetch_in_background, daemon=True).start()
    
    def download_roster(self):
        """Download roster data to JSON file"""
        if not self.current_roster_data:
            messagebox.showwarning(
                "No Data",
                "Please fetch a roster first before downloading."
            )
            return
        
        # Get team slug for filename
        team_slug = self.current_roster_data.get('team_slug', 'roster')
        default_filename = f"{team_slug}_roster.json"
        
        # Ask user where to save
        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            initialfile=default_filename,
            title="Save Roster Data"
        )
        
        if filepath:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(self.current_roster_data, f, indent=2, ensure_ascii=False)
                
                messagebox.showinfo(
                    "Success",
                    f"Roster data saved to:\n{filepath}"
                )
                self.status_var.set(f"Downloaded roster data to {filepath}")
            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"Failed to save file:\n{str(e)}"
                )
                self.status_var.set("Download failed")
    
    def display_roster(self, roster_data):
        """
        Display roster data with player photos
        
        Args:
            roster_data (dict): Roster data to display
        """
        # Clear existing display
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Clear image cache for new roster
        self.image_cache.clear()
        
        # Update info label
        team_name = roster_data['team_name']
        status = roster_data['status']
        
        if status == 'expansion_2026':
            self.info_label.config(
                text=f"[Warning] {roster_data['message']}",
                fg='orange'
            )
            return
        elif status == 'error':
            self.info_label.config(
                text=f"ERROR: {roster_data.get('error', 'Unknown error')}",
                fg='red'
            )
            return
        
        # Update info with team details
        fetched_time = roster_data['fetched_at'][:19].replace('T', ' ')
        source = roster_data.get('source_url', 'N/A')
        player_count = len(roster_data.get('players', []))
        
        self.info_label.config(
            text=f"{team_name} • {player_count} players • Fetched: {fetched_time}",
            fg='green'
        )
        
        players = roster_data.get('players', [])
        
        if not players:
            no_data_label = tk.Label(
                self.scrollable_frame,
                text="No player data available",
                font=("Arial", 12),
                bg='white',
                fg='gray'
            )
            no_data_label.pack(pady=50)
            return
        
        # Create header row
        header_frame = tk.Frame(self.scrollable_frame, bg=self.wnba_orange, height=40)
        header_frame.pack(fill=tk.X, padx=5, pady=(5, 0))
        
        tk.Label(header_frame, text="Photo", bg=self.wnba_orange, fg='white', 
                font=('Arial', 10, 'bold'), width=6).pack(side=tk.LEFT, padx=3)
        tk.Label(header_frame, text="#", bg=self.wnba_orange, fg='white',
                font=('Arial', 10, 'bold'), width=4).pack(side=tk.LEFT, padx=3)
        tk.Label(header_frame, text="Player Name", bg=self.wnba_orange, fg='white',
                font=('Arial', 10, 'bold'), width=20, anchor='w').pack(side=tk.LEFT, padx=3)
        tk.Label(header_frame, text="Pos", bg=self.wnba_orange, fg='white',
                font=('Arial', 10, 'bold'), width=10, anchor='w').pack(side=tk.LEFT, padx=3)
        tk.Label(header_frame, text="PPG", bg=self.wnba_orange, fg='white',
                font=('Arial', 10, 'bold'), width=5).pack(side=tk.LEFT, padx=3)
        tk.Label(header_frame, text="RPG", bg=self.wnba_orange, fg='white',
                font=('Arial', 10, 'bold'), width=5).pack(side=tk.LEFT, padx=3)
        tk.Label(header_frame, text="APG", bg=self.wnba_orange, fg='white',
                font=('Arial', 10, 'bold'), width=5).pack(side=tk.LEFT, padx=3)
        tk.Label(header_frame, text="Click for Details →", bg=self.wnba_orange, fg='white',
                font=('Arial', 10, 'bold', 'italic'), width=20, anchor='w').pack(side=tk.LEFT, padx=3)
        
        # Add each player as a row with photo
        for i, player in enumerate(players):
            bg_color = '#F5F5F5' if i % 2 == 0 else 'white'
            
            # Main player frame - make it clickable
            player_frame = tk.Frame(self.scrollable_frame, bg=bg_color, height=70, cursor="hand2")
            player_frame.pack(fill=tk.X, padx=5, pady=1)
            
            # Bind click event to expand/collapse player details
            player_frame.bind("<Button-1>", lambda e, p=player: self.toggle_player_details(p))
            
            # Photo
            photo_label = tk.Label(player_frame, bg=bg_color, width=60, height=60, cursor="hand2")
            photo_label.pack(side=tk.LEFT, padx=3, pady=5)
            photo_label.bind("<Button-1>", lambda e, p=player: self.toggle_player_details(p))
            
            # Load image in background thread (no delay)
            image_url = player.get('image_url', '')
            player_id = player.get('id', '')
            if image_url and player_id:
                threading.Thread(target=self.load_and_display_image, 
                               args=(image_url, player_id, photo_label), 
                               daemon=True).start()
            else:
                photo_label.config(text='[No Photo]', font=('Arial', 9))
            
            # Number
            num_label = tk.Label(player_frame, text=player.get('number', '--'), bg=bg_color,
                    font=('Arial', 10, 'bold'), width=4, cursor="hand2")
            num_label.pack(side=tk.LEFT, padx=3)
            num_label.bind("<Button-1>", lambda e, p=player: self.toggle_player_details(p))
            
            # Name
            name_label = tk.Label(player_frame, text=player.get('name', 'Unknown'), bg=bg_color,
                    font=('Arial', 10, 'bold'), width=20, anchor='w', cursor="hand2")
            name_label.pack(side=tk.LEFT, padx=3)
            name_label.bind("<Button-1>", lambda e, p=player: self.toggle_player_details(p))
            
            # Position
            pos_label = tk.Label(player_frame, text=player.get('position', '--'), bg=bg_color,
                    font=('Arial', 9), width=10, anchor='w', cursor="hand2")
            pos_label.pack(side=tk.LEFT, padx=3)
            pos_label.bind("<Button-1>", lambda e, p=player: self.toggle_player_details(p))
            
            # PPG
            ppg = player.get('ppg', '--')
            ppg_label = tk.Label(player_frame, text=ppg, bg=bg_color,
                    font=('Arial', 9), width=5, fg='#006BB6' if ppg != '--' else 'black', cursor="hand2")
            ppg_label.pack(side=tk.LEFT, padx=3)
            ppg_label.bind("<Button-1>", lambda e, p=player: self.toggle_player_details(p))
            
            # RPG
            rpg = player.get('rpg', '--')
            rpg_label = tk.Label(player_frame, text=rpg, bg=bg_color,
                    font=('Arial', 9), width=5, fg='#006BB6' if rpg != '--' else 'black', cursor="hand2")
            rpg_label.pack(side=tk.LEFT, padx=3)
            rpg_label.bind("<Button-1>", lambda e, p=player: self.toggle_player_details(p))
            
            # APG
            apg = player.get('apg', '--')
            apg_label = tk.Label(player_frame, text=apg, bg=bg_color,
                    font=('Arial', 9), width=5, fg='#006BB6' if apg != '--' else 'black', cursor="hand2")
            apg_label.pack(side=tk.LEFT, padx=3)
            apg_label.bind("<Button-1>", lambda e, p=player: self.toggle_player_details(p))
            
            # Click indicator
            details_fetched = player.get('details_fetched', False)
            indicator_text = "[Details]" if details_fetched else "Click to load"
            indicator_label = tk.Label(player_frame, text=indicator_text, bg=bg_color,
                    font=('Arial', 9, 'italic'), width=20, anchor='w',
                    fg='green' if details_fetched else '#666666', cursor="hand2")
            indicator_label.pack(side=tk.LEFT, padx=3)
            indicator_label.bind("<Button-1>", lambda e, p=player: self.toggle_player_details(p))
    def load_and_display_image(self, image_url, player_id, label_widget):
        """
        Load player image from URL and display in label (thread-safe)
        
        Args:
            image_url (str): URL of the player's headshot
            player_id (str): Player ID for caching
            label_widget: Label widget to display the image in
        """
        # Check if already cached
        if player_id in self.image_cache:
            self.root.after(0, lambda: label_widget.config(image=self.image_cache[player_id]))
            return
        
        try:
            # Download image (in background thread)
            response = requests.get(image_url, timeout=5)
            if response.status_code == 200:
                # Open and resize image
                image = Image.open(BytesIO(response.content))
                # Resize to fit in row (60x60 pixels)
                image = image.resize((60, 60), Image.Resampling.LANCZOS)
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(image)
                # Cache it
                self.image_cache[player_id] = photo
                # Display it (schedule on main thread for thread safety)
                self.root.after(0, lambda: label_widget.config(image=photo))
        except Exception as e:
            # Show emoji if image fails to load (schedule on main thread)
            self.root.after(0, lambda: label_widget.config(text='[No Photo]', font=('Arial', 9)))
            label_widget.config(text='[No Photo]', font=('Arial', 9))
    
    def clear_display(self):
        """Clear the display"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.image_cache.clear()
        self.current_roster_data = None
        self.expanded_player = None
        self.info_label.config(text="Select a team and fetch roster data", fg="gray")
        self.status_var.set("Display cleared")
    
    def toggle_player_details(self, player):
        """
        Toggle expanded view for a player, fetching details if needed
        
        Args:
            player (dict): Player dictionary
        """
        player_id = player.get('id', '')
        player_name = player.get('name', 'Unknown')
        
        # If this player is already expanded, collapse it
        if self.expanded_player == player_id:
            self.expanded_player = None
            self.display_roster(self.current_roster_data)
            self.status_var.set(f"Collapsed details for {player_name}")
            return
        
        # Fetch details if not already fetched
        if not player.get('details_fetched', False):
            # Show progress bar
            self.show_progress()
            self.status_var.set(f"Fetching comprehensive stats for {player_name}...")
            self.root.update()
            
            # Fetch in background thread
            def fetch_and_display():
                self.root.after(0, lambda: self.update_progress(30))
                
                # Get team name and fetch API stats
                team_name = self.current_roster_data.get('team_name', '') if self.current_roster_data else ''
                api_stats_dict = self.fetcher.fetch_team_stats_from_api(team_name)
                api_stats = api_stats_dict.get(player_name, None)
                
                # Fetch details with API stats
                details = self.fetcher.fetch_single_player_details(player_id, player_name, api_stats)
                player.update(details)
                player['details_fetched'] = True
                
                self.root.after(0, lambda: self.update_progress(70))
                
                # Update the saved roster data
                if self.current_roster_data:
                    for p in self.current_roster_data.get('players', []):
                        if p.get('id') == player_id:
                            p.update(details)
                            p['details_fetched'] = True
                            break
                    # Save updated roster
                    self.fetcher.save_roster(self.current_roster_data)
                
                self.root.after(0, lambda: self.update_progress(100))
                
                # Update display on main thread
                self.root.after(0, lambda: self._show_expanded_details(player))
                self.root.after(0, lambda: self.status_var.set(f"Loaded comprehensive stats for {player_name}"))
                
                # Keep progress bar at 100% for at least 1.5 seconds before resetting
                self.root.after(1500, self.hide_progress)
            
            threading.Thread(target=fetch_and_display, daemon=True).start()
        else:
            # Details already fetched, just expand
            self._show_expanded_details(player)
            self.status_var.set(f"Showing details for {player_name}")
    
    def _show_expanded_details(self, player):
        """
        Show expanded details for a player with comprehensive stats
        
        Args:
            player (dict): Player dictionary with fetched details
        """
        self.expanded_player = player.get('id')
        self.display_roster(self.current_roster_data)
        
        # Find and highlight the expanded player row
        # Add a details panel below the player row
        players = self.current_roster_data.get('players', [])
        for i, p in enumerate(players):
            if p.get('id') == player.get('id'):
                # Insert details frame after this player
                details_frame = tk.Frame(self.scrollable_frame, bg='#E8F4F8', relief=tk.RIDGE, borderwidth=2)
                details_frame.pack(fill=tk.X, padx=20, pady=5, after=self.scrollable_frame.winfo_children()[i+1])
                
                # Title
                title_frame = tk.Frame(details_frame, bg='#E8F4F8')
                title_frame.pack(fill=tk.X, pady=(10, 5))
                
                tk.Label(title_frame, text=f"Complete Profile: {player.get('name')}", 
                        bg='#E8F4F8', font=('Arial', 12, 'bold'),
                        fg=self.wnba_orange).pack()
                
                # Create two columns: Bio and Stats
                content_frame = tk.Frame(details_frame, bg='#E8F4F8')
                content_frame.pack(pady=10, padx=20, fill=tk.BOTH)
                
                # Left column - Bio Information
                bio_frame = tk.LabelFrame(content_frame, text="Bio Information", 
                                         font=('Arial', 10, 'bold'), bg='white',
                                         fg=self.wnba_black, padx=15, pady=10)
                bio_frame.grid(row=0, column=0, sticky='nsew', padx=5)
                
                bio_data = [
                    ('Height:', player.get('height', '--')),
                    ('Weight:', player.get('weight', '--')),
                    ('College:', player.get('college', '--')),
                    ('Experience:', player.get('experience', '--')),
                    ('Birth Date:', player.get('birth_date', '--')),
                    ('Birth Place:', player.get('birth_place', '--')),
                ]
                
                for idx, (label, value) in enumerate(bio_data):
                    tk.Label(bio_frame, text=label, font=('Arial', 9, 'bold'),
                            bg='white', anchor='e').grid(row=idx, column=0, sticky='e', padx=5, pady=3)
                    tk.Label(bio_frame, text=value, font=('Arial', 9),
                            bg='white', anchor='w').grid(row=idx, column=1, sticky='w', padx=5, pady=3)
                
                # Right column - Statistics
                stats_frame = tk.LabelFrame(content_frame, text="Season Statistics", 
                                           font=('Arial', 10, 'bold'), bg='white',
                                           fg=self.wnba_black, padx=15, pady=10)
                stats_frame.grid(row=0, column=1, sticky='nsew', padx=5)
                
                # Scoring stats
                scoring_label = tk.Label(stats_frame, text="Season Averages (2025)", 
                                        font=('Arial', 9, 'bold', 'italic'),
                                        bg='white', fg='#006BB6')
                scoring_label.grid(row=0, column=0, columnspan=2, sticky='w', pady=(0, 5))
                
                row_idx = 1
                scoring_stats = [
                    ('PPG:', player.get('ppg', '--')),
                    ('RPG:', player.get('rpg', '--')),
                    ('APG:', player.get('apg', '--')),
                ]
                
                for label, value in scoring_stats:
                    tk.Label(stats_frame, text=label, font=('Arial', 9, 'bold'),
                            bg='white', anchor='e').grid(row=row_idx, column=0, sticky='e', padx=5, pady=2)
                    tk.Label(stats_frame, text=value, font=('Arial', 9),
                            bg='white', anchor='w', fg='#006BB6').grid(row=row_idx, column=1, sticky='w', padx=5, pady=2)
                    row_idx += 1
                
                # Advanced stats - always show
                other_label = tk.Label(stats_frame, text="Advanced Stats", 
                                      font=('Arial', 9, 'bold', 'italic'),
                                      bg='white', fg='#006BB6')
                other_label.grid(row=row_idx, column=0, columnspan=2, sticky='w', pady=(5, 5))
                row_idx += 1
                
                other_stats = [
                    ('FG%:', player.get('fgp', '--')),
                    ('3P%:', player.get('3pp', '--')),
                    ('FT%:', player.get('ftp', '--')),
                    ('SPG:', player.get('spg', '--')),
                    ('BPG:', player.get('bpg', '--')),
                    ('TPG:', player.get('tpg', '--')),
                    ('MPG:', player.get('mpg', '--')),
                ]
                
                for label, value in other_stats:
                    tk.Label(stats_frame, text=label, font=('Arial', 9, 'bold'),
                            bg='white', anchor='e').grid(row=row_idx, column=0, sticky='e', padx=5, pady=2)
                    tk.Label(stats_frame, text=value, font=('Arial', 9),
                            bg='white', anchor='w', fg='#006BB6' if value != '--' else 'gray').grid(row=row_idx, column=1, sticky='w', padx=5, pady=2)
                    row_idx += 1
                
                content_frame.columnconfigure(0, weight=1)
                content_frame.columnconfigure(1, weight=1)
                
                # Button frame for actions
                button_frame = tk.Frame(details_frame, bg='#E8F4F8')
                button_frame.pack(pady=(5, 15))
                
                # View all stats button
                view_all_btn = tk.Button(button_frame, text="Show All Stats", 
                                        command=lambda p=player: self.show_all_stats_window(p),
                                        bg='#006BB6', fg='white', font=('Arial', 9, 'bold'),
                                        padx=15, pady=7, cursor="hand2", relief=tk.FLAT)
                view_all_btn.pack(side=tk.LEFT, padx=5)
                
                # Close button
                close_btn = tk.Button(button_frame, text="Close Details", 
                                     command=lambda: self.toggle_player_details(player),
                                     bg=self.wnba_orange, fg='white', font=('Arial', 9, 'bold'),
                                     padx=20, pady=7, cursor="hand2", relief=tk.FLAT)
                close_btn.pack(side=tk.LEFT, padx=5)
                
                break
    
    def show_all_stats_window(self, player):
        """
        Show a popup window with all 67 stat categories
        
        Args:
            player (dict): Player dictionary with all stats
        """
        # Create new window
        stats_window = tk.Toplevel(self.root)
        stats_window.title(f"All Stats - {player.get('name', 'Unknown')}")
        stats_window.geometry("800x600")
        stats_window.configure(bg='white')
        
        # Header
        header_frame = tk.Frame(stats_window, bg=self.wnba_orange, height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, 
                text=f"Complete Statistical Breakdown - {player.get('name', 'Unknown')}", 
                bg=self.wnba_orange, fg='white',
                font=('Arial', 14, 'bold')).pack(expand=True)
        
        # Create scrollable frame
        canvas = tk.Canvas(stats_window, bg='white')
        scrollbar = tk.Scrollbar(stats_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Prepare stats - exclude non-stat fields and rankings
        exclude_fields = {'id', 'name', 'number', 'position', 'image_url', 'details_fetched'}
        
        # Categorize stats (including all available stats)
        bio_fields = {'height', 'weight', 'college', 'experience', 'birth_date', 'birth_place'}
        game_stats = {'gp', 'w', 'l', 'w_pct', 'mpg'}
        scoring_stats = {'ppg', 'fgm', 'fga', 'fgp', '3pm', '3pa', '3pp', 'ftm', 'fta', 'ftp'}
        rebound_stats = {'rpg', 'oreb', 'dreb'}
        assist_defense_stats = {'apg', 'spg', 'bpg', 'tpg', 'blka', 'pf', 'pfd'}
        advanced_stats = {'plus_minus', 'dd2', 'td3', 'fantasy_pts', 'nba_fantasy_pts', 'wnba_fantasy_pts'}
        
        y_pos = 10
        
        # Helper function to create stat section
        def create_stat_section(title, stat_keys, labels_map):
            nonlocal y_pos
            
            section_frame = tk.LabelFrame(scrollable_frame, text=title, 
                                         font=('Arial', 11, 'bold'),
                                         bg='white', fg=self.wnba_orange,
                                         padx=15, pady=10)
            section_frame.pack(fill=tk.X, padx=20, pady=10)
            
            row = 0
            col = 0
            max_cols = 3
            
            for stat_key in stat_keys:
                value = player.get(stat_key, '--')
                if value or value == 0:  # Show if has value or is 0
                    label_text = labels_map.get(stat_key, stat_key.upper())
                    
                    tk.Label(section_frame, text=f"{label_text}:", 
                            font=('Arial', 9, 'bold'),
                            bg='white', anchor='e').grid(row=row, column=col*2, 
                                                         sticky='e', padx=5, pady=3)
                    tk.Label(section_frame, text=str(value), 
                            font=('Arial', 9),
                            bg='white', fg='#006BB6', anchor='w').grid(row=row, column=col*2+1, 
                                                                       sticky='w', padx=5, pady=3)
                    
                    col += 1
                    if col >= max_cols:
                        col = 0
                        row += 1
        
        # Bio Information
        bio_labels = {
            'height': 'Height', 'weight': 'Weight', 'college': 'College',
            'experience': 'Experience', 'birth_date': 'Birth Date', 'birth_place': 'Birth Place'
        }
        create_stat_section("Bio Information", bio_fields, bio_labels)
        
        # Game Stats
        game_labels = {
            'gp': 'Games Played', 'w': 'Wins', 'l': 'Losses', 'w_pct': 'Win Percentage', 'mpg': 'Minutes Per Game'
        }
        create_stat_section("Game Statistics", game_stats, game_labels)
        
        # Scoring
        scoring_labels = {
            'ppg': 'Points Per Game', 'fgm': 'FG Made', 'fga': 'FG Attempted',
            'fgp': 'FG Percentage', '3pm': '3-Pointers Made', '3pa': '3-Pointers Attempted',
            '3pp': '3-Point Percentage', 'ftm': 'Free Throws Made', 'fta': 'Free Throws Attempted',
            'ftp': 'Free Throw Percentage'
        }
        create_stat_section("Scoring & Shooting", scoring_stats, scoring_labels)
        
        # Rebounding
        rebound_labels = {
            'rpg': 'Rebounds Per Game', 'oreb': 'Offensive Rebounds', 'dreb': 'Defensive Rebounds'
        }
        create_stat_section("Rebounding", rebound_stats, rebound_labels)
        
        # Assists & Defense
        assist_defense_labels = {
            'apg': 'Assists Per Game', 'spg': 'Steals Per Game', 'bpg': 'Blocks Per Game',
            'tpg': 'Turnovers Per Game', 'blka': 'Blocked Attempts', 'pf': 'Personal Fouls', 'pfd': 'Fouls Drawn'
        }
        create_stat_section("Assists & Defense", assist_defense_stats, assist_defense_labels)
        
        # Advanced Stats
        advanced_labels = {
            'plus_minus': 'Plus/Minus', 'dd2': 'Double-Doubles', 'td3': 'Triple-Doubles',
            'fantasy_pts': 'Fantasy Points', 'nba_fantasy_pts': 'NBA Fantasy Points', 
            'wnba_fantasy_pts': 'WNBA Fantasy Points'
        }
        create_stat_section("Advanced Metrics", advanced_stats, advanced_labels)
        
        # Any remaining stats not categorized (excluding rankings)
        all_categorized = bio_fields | game_stats | scoring_stats | rebound_stats | assist_defense_stats | advanced_stats
        remaining = {}
        for key, value in player.items():
            if key not in exclude_fields and key not in all_categorized and not key.endswith('_RANK') and value:
                remaining[key] = value
        
        if remaining:
            remaining_frame = tk.LabelFrame(scrollable_frame, text="Additional API Stats", 
                                           font=('Arial', 11, 'bold'),
                                           bg='white', fg=self.wnba_orange,
                                           padx=15, pady=10)
            remaining_frame.pack(fill=tk.X, padx=20, pady=10)
            
            row = 0
            col = 0
            for stat_key, value in remaining.items():
                tk.Label(remaining_frame, text=f"{stat_key.upper()}:", 
                        font=('Arial', 9, 'bold'),
                        bg='white', anchor='e').grid(row=row, column=col*2, 
                                                     sticky='e', padx=5, pady=3)
                tk.Label(remaining_frame, text=str(value), 
                        font=('Arial', 9),
                        bg='white', fg='#006BB6', anchor='w').grid(row=row, column=col*2+1, 
                                                                   sticky='w', padx=5, pady=3)
                
                col += 1
                if col >= 3:
                    col = 0
                    row += 1
        
        # Close button at bottom
        close_btn = tk.Button(scrollable_frame, text="Close", 
                             command=stats_window.destroy,
                             bg=self.wnba_orange, fg='white', font=('Arial', 10, 'bold'),
                             padx=30, pady=10, cursor="hand2", relief=tk.FLAT)
        close_btn.pack(pady=20)
        
        # Bind mouse wheel to scroll
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        stats_window.protocol("WM_DELETE_WINDOW", lambda: [canvas.unbind_all("<MouseWheel>"), stats_window.destroy()])
    
    def fetch_all_details(self):
        """Fetch comprehensive stats for all players using API"""
        if not self.current_roster_data:
            messagebox.showwarning("No Roster Loaded", "Please load or fetch a roster first.")
            return
        
        players = self.current_roster_data.get('players', [])
        if not players:
            return
        
        # Count how many need fetching
        to_fetch = [p for p in players if not p.get('details_fetched', False)]
        
        if not to_fetch:
            messagebox.showinfo("All Details Loaded", "All player details are already loaded!")
            return
        
        # Show progress bar
        self.show_progress()
        self.status_var.set(f"Fetching comprehensive stats for {len(to_fetch)} players...")
        self.root.update()
        
        def fetch_in_background():
            total = len(to_fetch)
            team_name = self.current_roster_data.get('team_name', '')
            
            # Update progress
            self.root.after(0, lambda: self.update_progress(20))
            self.root.after(0, lambda: self.status_var.set(f"Fetching API stats for {team_name}..."))
            
            # Use new API-based method
            self.fetcher.fetch_all_player_details(to_fetch, team_name)
            
            # Mark as fetched
            for player in to_fetch:
                player['details_fetched'] = True
            
            # Refresh display
            self.root.after(0, lambda: self.update_progress(90))
            self.root.after(0, lambda: self.display_roster(self.current_roster_data))
            self.root.after(0, lambda: self.update_progress(100))
            self.root.after(0, lambda t=total: self.status_var.set(f"Loaded comprehensive stats for all {t} players!"))
            
            # Keep progress bar at 100% for at least 1.5 seconds before resetting
            self.root.after(1500, self.hide_progress)
            
            self.root.after(0, lambda t=total: messagebox.showinfo("Success", f"Fetched details for {t} players!"))
        
        # Run in background thread
        threading.Thread(target=fetch_in_background, daemon=True).start()
    
    def show_stats_guide(self):
        """Show a window with basketball statistics guide"""
        guide_window = tk.Toplevel(self.root)
        guide_window.title("Basketball Statistics Guide")
        guide_window.geometry("900x700")
        guide_window.configure(bg='white')
        
        # Header
        header_frame = tk.Frame(guide_window, bg=self.wnba_orange, height=60)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, 
                text="Basketball Statistics Guide", 
                bg=self.wnba_orange, fg='white',
                font=('Arial', 16, 'bold')).pack(expand=True)
        
        # Create scrollable frame
        canvas = tk.Canvas(guide_window, bg='white')
        scrollbar = tk.Scrollbar(guide_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Display stats from imported guide
        for category_name, stats_list in STATS_GUIDE.items():
            # Category header
            category_frame = tk.LabelFrame(scrollable_frame, text=category_name,
                                          font=('Arial', 12, 'bold'),
                                          bg='white', fg=self.wnba_orange,
                                          padx=15, pady=10)
            category_frame.pack(fill=tk.X, padx=20, pady=10)
            
            for abbr, name, description in stats_list:
                stat_frame = tk.Frame(category_frame, bg='white')
                stat_frame.pack(fill=tk.X, pady=3)
                
                tk.Label(stat_frame, text=f"{abbr}",
                        font=('Arial', 9, 'bold'),
                        bg='white', fg=self.wnba_orange,
                        width=12, anchor='w').pack(side=tk.LEFT)
                
                tk.Label(stat_frame, text=f"{name}",
                        font=('Arial', 9, 'bold'),
                        bg='white', width=25, anchor='w').pack(side=tk.LEFT)
                
                tk.Label(stat_frame, text=description,
                        font=('Arial', 9),
                        bg='white', wraplength=400, anchor='w').pack(side=tk.LEFT, padx=10)
        
        # Tip box
        tip_frame = tk.Frame(scrollable_frame, bg='#E8F4F8', relief=tk.RIDGE, borderwidth=2)
        tip_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(tip_frame, text="Tip:",
                font=('Arial', 10, 'bold'),
                bg='#E8F4F8', fg=self.wnba_orange).pack(anchor='w', padx=10, pady=(10, 5))
        
        tk.Label(tip_frame, 
                text=STATS_TIP,
                font=('Arial', 9),
                bg='#E8F4F8', wraplength=800, justify='left').pack(anchor='w', padx=10, pady=(0, 10))
        
        # Close button
        close_btn = tk.Button(scrollable_frame, text="Close",
                             command=guide_window.destroy,
                             bg=self.wnba_orange, fg='white',
                             font=('Arial', 10, 'bold'),
                             padx=30, pady=10, cursor="hand2", relief=tk.FLAT)
        close_btn.pack(pady=20)
        
        # Bind mouse wheel
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        guide_window.protocol("WM_DELETE_WINDOW", lambda: [canvas.unbind_all("<MouseWheel>"), guide_window.destroy()])


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = RosterViewerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
