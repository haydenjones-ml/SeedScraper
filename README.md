# SeedScraper

A powerful Python-based tool to scrape top seeds from any tournament on Start.gg—export results straight to CSV and tailor quantity and scope.

## 🚀 What It Does

-   Given a tournament with public seeding data, **SeedScraper** will retrieve the **top N seeds** (where _N_ is whatever number you need).   
-   Optionally **exports the scraped seed list to CSV**, ready for analysis, reporting, or archiving.
-   Fully configurable: choose **tournament**, **number of top seeds**, and output destination (to CSV, optional).

## How to use (.exe version)
The .exe version of the project is the most simple to use and has a "plug-n-play" approach to easily get and export seeding data!
To use the exe:
- Download the ZIP file under the green "<> CODE" dropdown (CODE -> Download ZIP)
- Extract the folder to wherever you want
- Open the folder titled "EXE In Here" and run the executable
- If you get a prompt saying "Windows is Protecting Your PC", this is normal for programs like this! Click accept.
- Follow the instructions in the application, and get your data!

## How to use (.py version)
Utilizing the program by running its python files has several benefits such as less bloat from build files + exe, ability to use your own API key for the backend, and (via the new API key) avoiding rate limiting on the main application.
To run the program using the .py files:
- Make sure that you have both [Python 3.13](https://www.python.org/downloads/) and [requests](https://pypi.org/project/requests/) downloaded. Requests can be installed with `pip install requests` in your command line.
- Download and extract the folder
- Get your start.gg API key following [these instructions](https://developer.start.gg/docs/authentication/) and replace the temporary text stored in "config_template.json" with it.
- Run the `gui.py` program, and use the application like normal! Note: You can only have 1 instance running at a time. If you cannot get your program to open, be sure to close all other instances.

## Link Formatting Examples
I know that "start.gg event link" can feel a bit arbitrary, so this section is just to make sure you know exactly what your links should look like when you paste them into the top field. The 1-sentence explanation would be to, on any page within a tournament on start.gg, take the link up name of the event `/event/event-name-is-here`. For clarity, here are a couple different examples of start.gg event links, with only the **highlighted portion** being what you would post in the top field:
- **https://www.start.gg/tournament/combo-breaker-2025/event/granblue-fantasy-versus-rising**
- **https://www.start.gg/tournament/evo-2024/event/granblue-fantasy-versus-rising** /brackets?filter=%7B%22phaseId%22%3A1707247%2C%22perPage%22%3A16%7D
- **https://www.start.gg/tournament/evo-2025/event/fatal-fury-city-of-the-wolves** /entrant/20355431

Just follow this format with your links and you will be able to use this program with no hiccups. Happy scraping!
