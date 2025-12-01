from roster_fetcher import WNBARosterFetcher

fetcher = WNBARosterFetcher()
data = fetcher.fetch_team_roster('Indiana Fever')

print(f"\nFound {len(data['players'])} players for {data['team_name']}")
print("\nFirst 5 players:")
for p in data['players'][:5]:
    print(f"#{p['number']:>2} {p['name']:25} {p['position']:20} {p['height']}")
