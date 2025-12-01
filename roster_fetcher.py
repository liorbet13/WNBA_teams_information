"""
WNBA Team Roster Fetcher - Business Logic
Fetches team roster data from wnba.com and saves locally
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed


class WNBARosterFetcher:
    """Handles fetching and saving WNBA team roster data"""
    
    # All 15 WNBA teams (13 current + 2 expansion teams for 2026)
    TEAMS = {
        'Atlanta Dream': 'dream',
        'Chicago Sky': 'sky',
        'Connecticut Sun': 'sun',
        'Dallas Wings': 'wings',
        'Golden State Valkyries': 'valkyries',
        'Indiana Fever': 'fever',
        'Las Vegas Aces': 'aces',
        'Los Angeles Sparks': 'sparks',
        'Minnesota Lynx': 'lynx',
        'New York Liberty': 'liberty',
        'Phoenix Mercury': 'mercury',
        'Seattle Storm': 'storm',
        'Washington Mystics': 'mystics',
        'Portland Fire': 'portland',  # 2026 expansion
        'Toronto Tempo': 'toronto'     # 2026 expansion
    }
    
    # Team IDs for stats.wnba.com API
    TEAM_STATS_IDS = {
        'Atlanta Dream': '1611661329',
        'Chicago Sky': '1611661330',
        'Connecticut Sun': '1611661313',
        'Dallas Wings': '1611661314',
        'Golden State Valkyries': '1612709921',
        'Indiana Fever': '1611661325',
        'Las Vegas Aces': '1611661319',
        'Los Angeles Sparks': '1611661320',
        'Minnesota Lynx': '1611661324',
        'New York Liberty': '1611661315',
        'Phoenix Mercury': '1611661317',
        'Seattle Storm': '1611661321',
        'Washington Mystics': '1611661322',
        'Portland Fire': '',  # 2026 expansion - no ID yet
        'Toronto Tempo': ''     # 2026 expansion - no ID yet
    }
    
    def __init__(self, data_dir='team_rosters'):
        """
        Initialize the roster fetcher
        
        Args:
            data_dir (str): Directory to save roster data files
        """
        self.data_dir = data_dir
        self.base_url = 'https://www.wnba.com'
        
        # Create data directory if it doesn't exist
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def get_all_teams(self):
        """
        Get list of all team names
        
        Returns:
            list: Sorted list of team names
        """
        return sorted(self.TEAMS.keys())
    
    def fetch_team_roster(self, team_name):
        """
        Fetch roster data for a specific team from wnba.com
        
        Args:
            team_name (str): Name of the team
            
        Returns:
            dict: Roster data including team info and players
        """
        if team_name not in self.TEAMS:
            raise ValueError(f"Team '{team_name}' not found")
        
        team_slug = self.TEAMS[team_name]
        
        # Handle expansion teams (no data available yet for 2026 teams)
        if team_name in ['Portland Fire', 'Toronto Tempo']:
            return {
                'team_name': team_name,
                'team_slug': team_slug,
                'status': 'expansion_2026',
                'players': [],
                'fetched_at': datetime.now().isoformat(),
                'message': f'{team_name} is an expansion team joining in 2026. Roster data not yet available.'
            }
        
        # Construct roster URL (teams use subdomain format: [team].wnba.com)
        roster_url = f'https://{team_slug}.wnba.com/roster/'
        
        try:
            # Fetch the roster page
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(roster_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse the HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract player data (basic stats already included from roster page)
            players = self._parse_roster_page(soup)
            
            roster_data = {
                'team_name': team_name,
                'team_slug': team_slug,
                'status': 'active',
                'players': players,
                'fetched_at': datetime.now().isoformat(),
                'source_url': roster_url
            }
            
            return roster_data
            
        except requests.RequestException as e:
            return {
                'team_name': team_name,
                'team_slug': team_slug,
                'status': 'error',
                'players': [],
                'fetched_at': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def _parse_roster_page(self, soup):
        """
        Parse roster information from BeautifulSoup object
        
        Args:
            soup: BeautifulSoup object of roster page
            
        Returns:
            list: List of player dictionaries
        """
        players = []
        
        # Find all links that go to player pages
        player_links = soup.find_all('a', href=lambda x: x and '/player/' in x)
        
        for link in player_links:
            try:
                # Extract player ID from href
                href = link.get('href', '')
                player_id = href.split('/player/')[-1] if '/player/' in href else ''
                
                if not player_id:
                    continue
                
                # Extract basic info from roster page
                number = ''
                name = ''
                position = ''
                ppg = ''
                rpg = ''
                apg = ''
                
                # Extract number from number div
                number_div = link.find('div', class_=lambda x: x and 'number' in str(x))
                if number_div:
                    number_text = number_div.get_text(strip=True)
                    number = number_text.replace('#', '')
                
                # Extract name from h3
                name_elem = link.find('h3')
                if name_elem:
                    name = name_elem.get_text(strip=True)
                
                # Extract position
                position_elem = link.find('p', class_=lambda x: x and 'subtitle' in str(x))
                if position_elem:
                    position = position_elem.get_text(strip=True)
                
                # Extract stats from dl (definition list)
                dl_stats = link.find('dl')
                if dl_stats:
                    dts = dl_stats.find_all('dt')
                    dds = dl_stats.find_all('dd')
                    
                    for dt, dd in zip(dts, dds):
                        label = dt.get_text(strip=True)
                        value = dd.get_text(strip=True)
                        
                        if label == 'PPG':
                            ppg = value
                        elif label == 'RPG':
                            rpg = value
                        elif label == 'APG':
                            apg = value
                
                if name:  # Only add if we found a name
                    # Construct image URL
                    image_url = f'https://cdn.wnba.com/headshots/wnba/latest/260x190/{player_id}.png' if player_id else ''
                    
                    # Store basic info only - details fetched on demand
                    players.append({
                        'id': player_id,
                        'number': number,
                        'name': name,
                        'position': position,
                        'height': '',
                        'weight': '',
                        'ppg': ppg,
                        'rpg': rpg,
                        'apg': apg,
                        'fgp': '',
                        '3pp': '',
                        'ftp': '',
                        'bpg': '',
                        'spg': '',
                        'tpg': '',
                        'mpg': '',
                        'college': '',
                        'experience': '',
                        'birth_date': '',
                        'birth_place': '',
                        'image_url': image_url,
                        'details_fetched': False
                    })
            except Exception as e:
                print(f"Error parsing player: {e}")
                continue
        
        return players
    
    def fetch_team_stats_from_api(self, team_name):
        """
        Placeholder for team stats fetching - stats are now fetched per-player on demand
        Advanced stats are scraped from individual player pages in fetch_single_player_details
        
        Args:
            team_name (str): Name of the team
            
        Returns:
            dict: Empty dict (stats fetched per-player now)
        """
        # Advanced stats are now fetched per-player on demand from player pages
        # This avoids the complexity of Selenium and AJAX-heavy stats pages
        return {}
    
    def fetch_single_player_details(self, player_id):
        """
        Fetch detailed information for a single player by ID
        
        Args:
            player_id (str): Player ID
            
        Returns:
            dict: Player details (height, weight, college, experience, birth date, advanced stats)
        """
        details = {
            'height': '', 'weight': '', 'college': '', 'experience': '', 
            'birth_date': '', 'birth_place': '',
            'fgp': '', '3pp': '', 'ftp': '', 'bpg': '', 'spg': '', 
            'tpg': '', 'mpg': ''
        }
        
        if not player_id:
            return details
        
        try:
            player_url = f"https://www.wnba.com/player/{player_id}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            player_response = requests.get(player_url, headers=headers, timeout=5)
            player_response.raise_for_status()
            player_soup = BeautifulSoup(player_response.content, 'html.parser')
            
            # Find the bio dl element with player details
            bio_dl = player_soup.find('dl', class_=lambda x: x and 'PlayerProfileInfoSecondary' in str(x))
            if bio_dl:
                dts = bio_dl.find_all('dt')
                dds = bio_dl.find_all('dd')
                
                for dt, dd in zip(dts, dds):
                    label = dt.get_text(strip=True)
                    value = dd.get_text(strip=True)
                    
                    if label == 'Height':
                        details['height'] = value
                    elif label == 'Weight':
                        details['weight'] = value
                    elif label == 'College/Country':
                        details['college'] = value.split('/')[0].strip()
                    elif label == 'EXP':
                        details['experience'] = value.strip()
                    elif label == 'Birthdate':
                        details['birth_date'] = value.strip()
                    elif label == 'Birthplace':
                        details['birth_place'] = value.strip()
            
            # Find advanced stats from career stats table or latest season
            # Look for stats table with class containing 'Stats'
            stats_tables = player_soup.find_all('table')
            for table in stats_tables:
                # Try to find the header row
                thead = table.find('thead')
                tbody = table.find('tbody')
                
                if thead and tbody:
                    headers = [th.get_text(strip=True) for th in thead.find_all('th')]
                    rows = tbody.find_all('tr')
                    
                    if rows:
                        # Get the most recent season (first row) or career stats
                        latest_row = rows[0]
                        cells = latest_row.find_all('td')
                        
                        if len(cells) >= len(headers):
                            for i, header in enumerate(headers):
                                if i < len(cells):
                                    value = cells[i].get_text(strip=True)
                                    
                                    if header == 'FG%':
                                        details['fgp'] = value
                                    elif header == '3P%':
                                        details['3pp'] = value
                                    elif header == 'FT%':
                                        details['ftp'] = value
                                    elif header == 'BPG':
                                        details['bpg'] = value
                                    elif header == 'SPG':
                                        details['spg'] = value
                                    elif header == 'TPG' or header == 'TO':
                                        details['tpg'] = value
                                    elif header == 'MPG' or header == 'MIN':
                                        details['mpg'] = value
                        break  # Use first valid stats table
                        
        except Exception as e:
            print(f"Could not fetch details for player {player_id}: {e}")
        
        return details
    
    def _fetch_player_details(self, player):
        """
        Fetch detailed information for a single player
        
        Args:
            player (dict): Player dictionary to update with details
            
        Returns:
            dict: Updated player dictionary
        """
        player_id = player.get('id', '')
        if not player_id:
            return player
        
        details = self.fetch_single_player_details(player_id)
        player.update(details)
        player['details_fetched'] = True
        
        return player
    
    def _fetch_player_details_parallel(self, players):
        """
        Fetch detailed information for all players in parallel using threading
        
        Args:
            players (list): List of player dictionaries to update
        """
        # Use ThreadPoolExecutor to fetch player details concurrently
        # Max 8 workers to be respectful to the server
        with ThreadPoolExecutor(max_workers=8) as executor:
            # Submit all player detail fetches
            future_to_player = {executor.submit(self._fetch_player_details, player): player 
                               for player in players}
            
            # Wait for all to complete
            for future in as_completed(future_to_player):
                try:
                    future.result()  # This updates the player dict in place
                except Exception as e:
                    print(f"Error fetching player details: {e}")
    
    def _extract_player_info(self, element):
        """
        Extract player information from a player card element
        
        Args:
            element: BeautifulSoup element containing player data
            
        Returns:
            dict: Player information
        """
        try:
            # This will need to be adjusted based on actual HTML structure
            name_elem = element.find('h3') or element.find('div', class_='name')
            number_elem = element.find('span', class_='number') or element.find('div', class_='number')
            position_elem = element.find('span', class_='position') or element.find('div', class_='position')
            
            player = {
                'name': name_elem.text.strip() if name_elem else 'Unknown',
                'number': number_elem.text.strip() if number_elem else '',
                'position': position_elem.text.strip() if position_elem else '',
            }
            
            return player
        except:
            return None
    
    def save_roster(self, roster_data):
        """
        Save roster data to a JSON file
        
        Args:
            roster_data (dict): Roster data to save
            
        Returns:
            str: Path to saved file
        """
        team_slug = roster_data['team_slug']
        filename = f"{team_slug}_roster.json"
        filepath = os.path.join(self.data_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(roster_data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def load_roster(self, team_name):
        """
        Load saved roster data from file
        
        Args:
            team_name (str): Name of the team
            
        Returns:
            dict: Roster data or None if file does not exist
        """
        if team_name not in self.TEAMS:
            return None
        
        team_slug = self.TEAMS[team_name]
        filename = f"{team_slug}_roster.json"
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None
    
    def get_all_saved_rosters(self):
        """
        Get list of all teams with saved roster data
        
        Returns:
            list: List of team names with saved data
        """
        saved_teams = []
        for team_name, team_slug in self.TEAMS.items():
            filename = f"{team_slug}_roster.json"
            filepath = os.path.join(self.data_dir, filename)
            if os.path.exists(filepath):
                saved_teams.append(team_name)
        
        return sorted(saved_teams)
