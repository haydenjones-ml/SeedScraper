import csv
import json
import requests
import re
import os
import sys

# Config Skeleton
# Load API key from bundled JSON (works in .py and .exe)
def load_api_key():
    config_path = 'config_template.json'
    with open(config_path, 'r') as file:
        config = json.load(file)
        return config.get("startgg_api_key")


API_TOKEN = load_api_key()


query = '''
query EventSeeds($slug: String!, $page: Int!) {
  event(slug: $slug) {
    entrants(query: {page: $page, perPage: 50}) {
      nodes {
        name
        seeds {
          seedNum
        }
      }
      pageInfo {
        totalPages
      }
    }
  }
}
'''

def extract_event_slug(url):
    match = re.search(r'start\.gg\/(tournament\/[^\/]+\/event\/[^\/?#]+)', url)
    return match.group(1) if match else None


def format_filename(raw_name):
    clean_name = raw_name.strip().replace(" ", "_")
    clean_name = re.sub(r'[\\/*?:"<>|]', '', clean_name)
    return f"{clean_name}.csv"


def get_event_seeds(event_slug, top_n, csv_name=None):
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Content-Type': 'application/json'
    }

    players = []
    page = 1
    total_pages = 1

    while page <= total_pages:
        response = requests.post(
            'https://api.start.gg/gql/alpha',
            json={'query': query, 'variables': {'slug': event_slug, 'page': page}},
            headers=headers
        )

        if response.status_code != 200:
            raise Exception(f"GraphQL API Error {response.status_code}: {response.text}")

        data = response.json()
        event_data = data.get('data', {}).get('event')
        if event_data is None:
            raise Exception("Event not found. Check the event slug.")

        entrants = event_data['entrants']
        nodes = entrants['nodes']
        total_pages = entrants['pageInfo']['totalPages']

        for entrant in nodes:
            if entrant['seeds']:
                seed = entrant['seeds'][0]['seedNum']
                if seed is not None and seed <= top_n:
                    players.append({'name': entrant['name'], 'seed': seed})

        page += 1

    players_sorted = sorted(players, key=lambda x: x['seed'])

    # Save to CSV IF a filename was provided
    path = None
    if csv_name:
        filename = format_filename(csv_name)
        documents_path = os.path.join(os.path.expanduser("~"), "Documents", filename)
        with open(documents_path, "w", newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Seed #", "Player"]);
            for p in players_sorted:
                writer.writerow([p['seed'], p['name']])
        path = documents_path

    return players_sorted, path