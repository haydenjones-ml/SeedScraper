import csv
import requests
import re
import os
import tkinter as tk
from tkinter import simpledialog, messagebox

API_TOKEN = '1fbf00e703d2316372e0bbb8dbafafd2'

# Query Skeleton
query = """
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
"""

def extract_event_slug(url):
    """Extract slug from a valid start.gg event URL."""
    match = re.search(r'start\.gg\/(tournament\/[^\/]+\/event\/[^\/?#]+)', url)
    return match.group(1) if match else None

def format_filename(raw_name):
    clean_name = raw_name.strip().replace(" ", "_")
    clean_name = re.sub(r'[\\/*?:"<>|]', '', clean_name)
    return f"{clean_name}.csv"

def get_event_seeds(event_slug, top_n):
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
            messagebox.showerror("API Error", f"GraphQL API returned error code {response.status_code}.\n\n{response.text}")
            return

        try:
            data = response.json()
            event_data = data['data']['event']
            if event_data is None:
                raise ValueError("Event not found. Check the event slug.")
            entrants = event_data['entrants']
            nodes = entrants['nodes']
            total_pages = entrants['pageInfo']['totalPages']
        except Exception as e:
            messagebox.showerror("Error", f"Invalid API response:\n{str(e)}\n\nRaw Response:\n{response.text}")
            return

        for entrant in nodes:
            if entrant['seeds']:
                seed = entrant['seeds'][0]['seedNum']
                if seed is not None and seed <= top_n:
                    players.append({
                        'name': entrant['name'],
                        'seed': seed
                    })

        page += 1

    players_sorted = sorted(players, key=lambda x: x['seed'])

    # Results Output
    output = "\n".join([f"Seed {p['seed']}: {p['name']}" for p in players_sorted])
    messagebox.showinfo("Top Seeds", output)

    # Ask user for filename
    csv_name = simpledialog.askstring("Save As", "Enter a name for your CSV file (no extension):")
    if not csv_name:
        messagebox.showerror("Error", "No file name provided.")
        return

    filename = format_filename(csv_name)

    # Create CSV and save path (defaults to 'Documents Folder' + user-defined doc name)
    documents_path = os.path.join(os.path.expanduser("~"), "Documents", filename)

    try:
        with open(documents_path, "w", newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Seed #", "Player"])
            for player in players_sorted:
                writer.writerow([player['seed'], player['name']])
        messagebox.showinfo("Export Complete", f"Top seeds saved to Documents as '{filename}'")
    except Exception as e:
        messagebox.showerror("File Error", f"Could not save file:\n{str(e)}")

# GUI SETUP GOES HERE; currently just 3 different windows but will change.
root = tk.Tk()
root.withdraw()

# Prompt for event URL
event_url = simpledialog.askstring("Event Link", "Paste the start.gg *event* link:")
if not event_url:
    messagebox.showerror("Input Error", "No event link provided.")
    exit()

event_slug = extract_event_slug(event_url)
if not event_slug:
    messagebox.showerror("URL Error", "Invalid event URL. It must include '/event/'.")
    exit()

# Prompt for number of top seeds
try:
    num_seeds = int(simpledialog.askstring("Top N Seeds", "Enter number of top seeds to show:"))
    if num_seeds <= 0:
        raise ValueError()
except:
    messagebox.showerror("Input Error", "Please enter a valid positive integer for top seeds.")
    exit()

get_event_seeds(event_slug, num_seeds)