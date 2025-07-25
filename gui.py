import tkinter as tk
from tkinter import messagebox
from seed_scraper import extract_event_slug, get_event_seeds


def on_submit():
    url = url_entry.get().strip()
    seeds_raw = seeds_entry.get().strip()
    csv_raw = filename_entry.get().strip()

    if not url or not seeds_raw:
        messagebox.showerror("Input Error", "Event URL and seed count are required.")
        return

    # Validate URL
    slug = extract_event_slug(url)
    if not slug:
        messagebox.showerror("URL Error", "Invalid start.gg event URL.")
        return

    # Validate seed count
    if not seeds_raw.isdigit():
        messagebox.showerror("Input Error", "Top seeds must be a number.")
        return
    seeds = int(seeds_raw)
    if seeds <= 0 or seeds > 1000:
        messagebox.showerror("Input Error", "Top seeds must be between 1 and 1000.")
        return

    try:
        players, path = get_event_seeds(slug, seeds, csv_raw or None)
        output = "\n".join([f"Seed {p['seed']}: {p['name']}" for p in players])
        messagebox.showinfo("Top Seeds", output)
        if path:
            messagebox.showinfo("CSV Saved", f"File saved to:\n{path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("Start.gg Seed Scraper")

# URL Field
tk.Label(root, text="Start.gg Event Link:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
url_entry = tk.Entry(root, width=60)
url_entry.grid(row=0, column=1, padx=10)

# "Top Seeds to Display"
tk.Label(root, text="Top Seeds to Display:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
seeds_entry = tk.Entry(root, width=10)
seeds_entry.grid(row=1, column=1, sticky="w", padx=10)

# CSV Filename
tk.Label(root, text="CSV Filename (no extension, leave empty for no export):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
filename_entry = tk.Entry(root, width=30)
filename_entry.grid(row=2, column=1, sticky="w", padx=10)

# Submit Button
submit_btn = tk.Button(root, text="Submit", command=on_submit)
submit_btn.grid(row=3, column=0, columnspan=2, pady=15)

root.mainloop()