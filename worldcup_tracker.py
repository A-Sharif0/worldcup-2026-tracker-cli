#!/usr/bin/env python3
"""
FIFA World Cup 2026 Tracker (Standard Library Edition)
=====================================================
NO external packages needed! Uses only built-in Python modules.
Works on any Windows/Mac/Linux machine with Python 3.7+ installed.


"""

import urllib.request
import urllib.error
import json
import sys
import os
from datetime import datetime
from time import sleep

# ── Configuration ──────────────────────────────────────────────────
API_BASE = "https://worldcup26.ir"
ENDPOINTS = {
    "games":    "/get/games",
    "teams":    "/get/teams",
    "groups":   "/get/groups",
    "stadiums": "/get/stadiums",
    "health":   "/health",
}

# ANSI colours for terminal output (Windows 10+ supports these in PowerShell)
class Colors:
    HEADER    = "\033[95m"
    BLUE      = "\033[94m"
    CYAN      = "\033[96m"
    GREEN     = "\033[92m"
    YELLOW    = "\033[93m"
    RED       = "\033[91m"
    BOLD      = "\033[1m"
    UNDERLINE = "\033[4m"
    END       = "\033[0m"

# ── Helpers ────────────────────────────────────────────────────────
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print(f"""
{Colors.CYAN}{Colors.BOLD}
   ██████╗ ██╗   ██╗███████╗    ██╗    ██╗ ██████╗ ██████╗ ██╗     ██████╗ 
  ██╔═══██╗██║   ██║██╔════╝    ██║    ██║██╔═══██╗██╔══██╗██║     ██╔══██╗
  ██║   ██║██║   ██║█████╗      ██║ █╗ ██║██║   ██║██████╔╝██║     ██║  ██║
  ██║▄▄ ██║██║   ██║██╔══╝      ██║███╗██║██║   ██║██╔══██╗██║     ██║  ██║
  ╚██████╔╝╚██████╔╝██║         ╚███╔███╔╝╚██████╔╝██║  ██║███████╗██████╔╝
   ╚══▀▀═╝  ╚═════╝ ╚═╝          ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═════╝ 
{Colors.END}
  {Colors.YELLOW}🏆 FIFA World Cup 2026 — United States, Mexico & Canada{Colors.END}
  {Colors.GREEN}📡 API: worldcup26.ir  |  48 Teams  |  104 Matches  |  12 Groups{Colors.END}
  {Colors.CYAN}✅ Standard Library Edition — No pip install needed!{Colors.END}
""")

def api_get(endpoint):
    """Make a GET request using only urllib (built-in). Returns dict or None."""
    url = f"{API_BASE}{endpoint}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "WorldCupTracker/1.0"})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = response.read().decode("utf-8")
            return json.loads(data)
    except urllib.error.HTTPError as e:
        print(f"{Colors.RED}⚠ HTTP Error {e.code}: {e.reason}{Colors.END}")
        return None
    except urllib.error.URLError as e:
        print(f"{Colors.RED}⚠ Connection Error: {e.reason}{Colors.END}")
        return None
    except Exception as e:
        print(f"{Colors.RED}⚠ API Error ({endpoint}): {e}{Colors.END}")
        return None

def check_api():
    """Check if the API is reachable."""
    data = api_get(ENDPOINTS["health"])
    if data and data.get("status") == "healthy":
        print(f"{Colors.GREEN}✓ API is online (v{data.get('version','?')}){Colors.END}")
        return True
    # Fallback: try teams endpoint
    data = api_get(ENDPOINTS["teams"])
    if data and "teams" in data:
        print(f"{Colors.GREEN}✓ API is reachable (teams endpoint OK){Colors.END}")
        return True
    print(f"{Colors.RED}✗ API appears offline. Some features may be limited.{Colors.END}")
    return False

def parse_date(date_str):
    """Parse API date format 'MM/DD/YYYY HH:MM' into a datetime object."""
    try:
        return datetime.strptime(date_str, "%m/%d/%Y %H:%M")
    except ValueError:
        return None

def format_scorers(scorers_str):
    """Format the JSON-like scorers string into readable text."""
    if not scorers_str or scorers_str == "null":
        return ""
    try:
        scorers_str = scorers_str.strip("{}")
        items = [s.strip('"') for s in scorers_str.split('","')]
        return ", ".join(items)
    except Exception:
        return scorers_str

# ── Feature: Today's Matches ───────────────────────────────────────
def show_todays_matches():
    data = api_get(ENDPOINTS["games"])
    if not data:
        print(f"{Colors.RED}Could not fetch match data.{Colors.END}")
        return

    games = data.get("games", [])
    today = datetime.now().strftime("%m/%d/%Y")
    todays = [g for g in games if g.get("local_date", "").startswith(today)]

    print(f"\n{Colors.BOLD}{Colors.CYAN}📅 Matches for {datetime.now().strftime('%A, %B %d, %Y')}{Colors.END}\n")

    if not todays:
        print(f"{Colors.YELLOW}No matches scheduled for today.{Colors.END}")
        return

    for g in todays:
        home = g.get("home_team_name_en", "TBD")
        away = g.get("away_team_name_en", "TBD")
        score_h = g.get("home_score", "0")
        score_a = g.get("away_score", "0")
        time = g.get("local_date", "").split(" ")[1] if " " in g.get("local_date", "") else "TBD"
        status = g.get("time_elapsed", "notstarted")
        group = g.get("group", "")
        finished = g.get("finished", "FALSE") == "TRUE"

        status_icon = "🔴 LIVE" if status == "live" else ("✅ FT" if finished else "⏰")
        score_display = f"{Colors.BOLD}{score_h} - {score_a}{Colors.END}" if finished or status == "live" else f"{Colors.YELLOW}vs{Colors.END}"

        print(f"  {Colors.CYAN}{time}{Colors.END}  {status_icon:6}  {Colors.BOLD}{home}{Colors.END} {score_display} {Colors.BOLD}{away}{Colors.END}  ({group})")

        if finished or status == "live":
            h_scorers = format_scorers(g.get("home_scorers"))
            a_scorers = format_scorers(g.get("away_scorers"))
            if h_scorers:
                print(f"           {Colors.GREEN}⚽ {home}:{Colors.END} {h_scorers}")
            if a_scorers:
                print(f"           {Colors.GREEN}⚽ {away}:{Colors.END} {a_scorers}")
        print()

# ── Feature: Group Standings ───────────────────────────────────────
def show_standings():
    data = api_get(ENDPOINTS["groups"])
    teams_data = api_get(ENDPOINTS["teams"])
    if not data or not teams_data:
        print(f"{Colors.RED}Could not fetch standings data.{Colors.END}")
        return

    teams_map = {t["id"]: t for t in teams_data.get("teams", [])}
    groups = data.get("groups", [])

    print(f"\n{Colors.BOLD}{Colors.CYAN}📊 Group Standings{Colors.END}\n")

    for grp in groups:
        gname = grp.get("name", "?")
        print(f"{Colors.BOLD}{Colors.YELLOW}  Group {gname}{Colors.END}")
        print(f"  {'Team':<25} {'MP':>3} {'W':>3} {'D':>3} {'L':>3} {'GF':>3} {'GA':>3} {'GD':>4} {'Pts':>4}")
        print(f"  {'-'*25} {'--':>3} {'-':>3} {'-':>3} {'-':>3} {'--':>3} {'--':>3} {'---':>4} {'----':>4}")

        for idx, t in enumerate(grp.get("teams", [])):
            tid = t.get("team_id", "")
            team = teams_map.get(tid, {})
            name = team.get("name_en", f"Team {tid}")
            flag = team.get("fifa_code", "")
            mp = t.get("mp", "0")
            w = t.get("w", "0")
            d = t.get("d", "0")
            l = t.get("l", "0")
            gf = t.get("gf", "0")
            ga = t.get("ga", "0")
            gd = t.get("gd", "0")
            pts = t.get("pts", "0")

            rank = idx + 1
            color = Colors.GREEN if rank <= 2 else Colors.END
            print(f"  {color}{flag:<4} {name:<20}{Colors.END} {mp:>3} {w:>3} {d:>3} {l:>3} {gf:>3} {ga:>3} {gd:>4} {Colors.BOLD}{pts:>4}{Colors.END}")
        print()

# ── Feature: All Teams ─────────────────────────────────────────────
def show_teams():
    data = api_get(ENDPOINTS["teams"])
    if not data:
        print(f"{Colors.RED}Could not fetch team data.{Colors.END}")
        return

    teams = data.get("teams", [])
    print(f"\n{Colors.BOLD}{Colors.CYAN}👥 All {len(teams)} Qualified Teams{Colors.END}\n")

    by_group = {}
    for t in teams:
        g = t.get("groups", "?")
        by_group.setdefault(g, []).append(t)

    for g in sorted(by_group.keys()):
        print(f"{Colors.BOLD}{Colors.YELLOW}  Group {g}{Colors.END}")
        for t in by_group[g]:
            name = t.get("name_en", "Unknown")
            code = t.get("fifa_code", "")
            print(f"    {Colors.CYAN}{code:<4}{Colors.END} {name}")
        print()

# ── Feature: Match Results ─────────────────────────────────────────
def show_results():
    data = api_get(ENDPOINTS["games"])
    if not data:
        print(f"{Colors.RED}Could not fetch match data.{Colors.END}")
        return

    games = data.get("games", [])
    finished_games = [g for g in games if g.get("finished") == "TRUE"]
    finished_games.sort(key=lambda x: parse_date(x.get("local_date", "")) or datetime.min)

    print(f"\n{Colors.BOLD}{Colors.CYAN}🏁 Match Results ({len(finished_games)} completed){Colors.END}\n")

    for g in finished_games:
        home = g.get("home_team_name_en", "TBD")
        away = g.get("away_team_name_en", "TBD")
        score_h = g.get("home_score", "0")
        score_a = g.get("away_score", "0")
        date = g.get("local_date", "TBD")
        group = g.get("group", "")
        match_type = g.get("type", "group").upper()

        print(f"  {Colors.YELLOW}{date}{Colors.END}  [{match_type}]  {Colors.BOLD}{home}{Colors.END} {Colors.GREEN}{score_h} - {score_a}{Colors.END} {Colors.BOLD}{away}{Colors.END}")

        h_scorers = format_scorers(g.get("home_scorers"))
        a_scorers = format_scorers(g.get("away_scorers"))
        if h_scorers:
            print(f"           {Colors.GREEN}⚽ {home}:{Colors.END} {h_scorers}")
        if a_scorers:
            print(f"           {Colors.GREEN}⚽ {away}:{Colors.END} {a_scorers}")
        print()

# ── Feature: Upcoming Fixtures ─────────────────────────────────────
def show_fixtures():
    data = api_get(ENDPOINTS["games"])
    if not data:
        print(f"{Colors.RED}Could not fetch match data.{Colors.END}")
        return

    games = data.get("games", [])
    upcoming = [g for g in games if g.get("finished") == "FALSE" and g.get("time_elapsed") == "notstarted"]
    upcoming.sort(key=lambda x: parse_date(x.get("local_date", "")) or datetime.max)

    print(f"\n{Colors.BOLD}{Colors.CYAN}📅 Upcoming Fixtures ({len(upcoming)} remaining){Colors.END}\n")

    for g in upcoming:
        home = g.get("home_team_name_en") or g.get("home_team_label", "TBD")
        away = g.get("away_team_name_en") or g.get("away_team_label", "TBD")
        date = g.get("local_date", "TBD")
        group = g.get("group", "")
        match_type = g.get("type", "group").upper()

        print(f"  {Colors.YELLOW}{date}{Colors.END}  [{match_type}]  {Colors.BOLD}{home}{Colors.END} {Colors.YELLOW}vs{Colors.END} {Colors.BOLD}{away}{Colors.END}")
    print()

# ── Feature: Stadiums ──────────────────────────────────────────────
def show_stadiums():
    data = api_get(ENDPOINTS["stadiums"])
    if not data:
        print(f"{Colors.RED}Could not fetch stadium data.{Colors.END}")
        return

    stadiums = data.get("stadiums", [])
    print(f"\n{Colors.BOLD}{Colors.CYAN}🏟️ Host Stadiums ({len(stadiums)} venues){Colors.END}\n")

    for s in stadiums:
        name = s.get("name_en", "Unknown")
        city = s.get("city_en", "")
        country = s.get("country_en", "")
        capacity = s.get("capacity", 0)
        region = s.get("region", "")
        print(f"  {Colors.BOLD}{name}{Colors.END}")
        print(f"    📍 {city}, {country}  |  👥 Capacity: {capacity:,}  |  🌍 {region}")
    print()

# ── Feature: Live Matches ────────────────────────────────────────
def show_live_matches():
    data = api_get(ENDPOINTS["games"])
    if not data:
        print(f"{Colors.RED}Could not fetch match data.{Colors.END}")
        return

    games = data.get("games", [])
    live = [g for g in games if g.get("time_elapsed") == "live"]

    print(f"\n{Colors.BOLD}{Colors.CYAN}🔴 Live Matches{Colors.END}\n")

    if not live:
        print(f"{Colors.YELLOW}No matches currently in progress.{Colors.END}")
        return

    for g in live:
        home = g.get("home_team_name_en", "TBD")
        away = g.get("away_team_name_en", "TBD")
        score_h = g.get("home_score", "0")
        score_a = g.get("away_score", "0")
        group = g.get("group", "")

        print(f"  {Colors.RED}{Colors.BOLD}● LIVE{Colors.END}  {Colors.BOLD}{home}{Colors.END} {Colors.GREEN}{score_h} - {score_a}{Colors.END} {Colors.BOLD}{away}{Colors.END}  ({group})")

        h_scorers = format_scorers(g.get("home_scorers"))
        a_scorers = format_scorers(g.get("away_scorers"))
        if h_scorers:
            print(f"         {Colors.GREEN}⚽ {home}:{Colors.END} {h_scorers}")
        if a_scorers:
            print(f"         {Colors.GREEN}⚽ {away}:{Colors.END} {a_scorers}")
        print()

# ── Feature: Auto-Refresh Live Mode ────────────────────────────────
def live_mode():
    print(f"\n{Colors.BOLD}{Colors.CYAN}🔴 Live Mode — Refreshing every 30s (Ctrl+C to exit){Colors.END}\n")
    try:
        while True:
            clear()
            banner()
            show_live_matches()
            print(f"{Colors.YELLOW}Last updated: {datetime.now().strftime('%H:%M:%S')}  |  Next refresh in 30s...{Colors.END}")
            sleep(30)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Live mode stopped.{Colors.END}")

# ── Feature: Search Team ───────────────────────────────────────────
def search_team():
    query = input(f"\n{Colors.CYAN}Enter team name (or part of it): {Colors.END}").strip().lower()
    if not query:
        return

    data = api_get(ENDPOINTS["teams"])
    if not data:
        return

    teams = data.get("teams", [])
    matches = [t for t in teams if query in t.get("name_en", "").lower() or query in t.get("fifa_code", "").lower()]

    if not matches:
        print(f"{Colors.RED}No teams found matching '{query}'.{Colors.END}")
        return

    print(f"\n{Colors.BOLD}{Colors.CYAN}🔍 Search Results{Colors.END}\n")
    for t in matches:
        print(f"  {Colors.BOLD}{t.get('name_en')}{Colors.END} ({t.get('fifa_code')}) — Group {t.get('groups')}")
        print(f"    Flag: {t.get('flag')}")

    games_data = api_get(ENDPOINTS["games"])
    if games_data:
        team_id = matches[0].get("id")
        team_games = [g for g in games_data.get("games", [])
                      if g.get("home_team_id") == team_id or g.get("away_team_id") == team_id]
        if team_games:
            print(f"\n  {Colors.BOLD}Matches:{Colors.END}")
            for g in sorted(team_games, key=lambda x: parse_date(x.get("local_date", "")) or datetime.min):
                home = g.get("home_team_name_en", "TBD")
                away = g.get("away_team_name_en", "TBD")
                score = f"{g.get('home_score','0')}-{g.get('away_score','0')}" if g.get("finished") == "TRUE" else "vs"
                print(f"    {g.get('local_date','TBD')}  {home} {score} {away}")
    print()

# ── Feature: Top Scorers ───────────────────────────────────────────
def show_top_scorers():
    data = api_get(ENDPOINTS["games"])
    if not data:
        print(f"{Colors.RED}Could not fetch match data.{Colors.END}")
        return

    games = data.get("games", [])
    scorers = {}

    for g in games:
        if g.get("finished") != "TRUE":
            continue
        for side in ["home_scorers", "away_scorers"]:
            s = format_scorers(g.get(side, ""))
            if not s:
                continue
            for item in s.split(", "):
                parts = item.rsplit(" ", 1)
                if len(parts) == 2:
                    name = parts[0].strip()
                    scorers[name] = scorers.get(name, 0) + 1

    print(f"\n{Colors.BOLD}{Colors.CYAN}⚽ Top Scorers{Colors.END}\n")
    if not scorers:
        print(f"{Colors.YELLOW}No goals recorded yet.{Colors.END}")
        return

    sorted_scorers = sorted(scorers.items(), key=lambda x: x[1], reverse=True)[:20]
    for i, (name, goals) in enumerate(sorted_scorers, 1):
        medal = "🥇" if i == 1 else ("🥈" if i == 2 else ("🥉" if i == 3 else "  "))
        print(f"  {medal} {i:2}. {Colors.BOLD}{name:<25}{Colors.END} {goals} goal{'s' if goals>1 else ''}")
    print()

# ── Feature: Match Details ───────────────────────────────────────
def match_details():
    match_id = input(f"\n{Colors.CYAN}Enter match ID (1-104): {Colors.END}").strip()
    if not match_id.isdigit():
        print(f"{Colors.RED}Invalid match ID.{Colors.END}")
        return

    data = api_get(f"/get/game/{match_id}")
    if not data or "game" not in data:
        print(f"{Colors.RED}Match not found.{Colors.END}")
        return

    g = data["game"]
    home = g.get("home_team_name_en") or g.get("home_team_label", "TBD")
    away = g.get("away_team_name_en") or g.get("away_team_label", "TBD")
    score_h = g.get("home_score", "0")
    score_a = g.get("away_score", "0")
    date = g.get("local_date", "TBD")
    group = g.get("group", "")
    status = g.get("time_elapsed", "notstarted")
    finished = g.get("finished", "FALSE") == "TRUE"
    match_type = g.get("type", "group").upper()

    print(f"\n{Colors.BOLD}{Colors.CYAN}⚽ Match #{match_id} Details{Colors.END}\n")
    print(f"  {Colors.BOLD}{home}{Colors.END} {Colors.GREEN}{score_h} - {score_a}{Colors.END} {Colors.BOLD}{away}{Colors.END}")
    print(f"  📅 {date}  |  🏷️ {match_type}  |  📊 {group}")
    print(f"  Status: {Colors.GREEN if finished else Colors.YELLOW}{status.upper()}{Colors.END}")

    h_scorers = format_scorers(g.get("home_scorers"))
    a_scorers = format_scorers(g.get("away_scorers"))
    if h_scorers:
        print(f"\n  {Colors.GREEN}⚽ {home} Scorers:{Colors.END}")
        for s in h_scorers.split(", "):
            print(f"    • {s}")
    if a_scorers:
        print(f"\n  {Colors.GREEN}⚽ {away} Scorers:{Colors.END}")
        for s in a_scorers.split(", "):
            print(f"    • {s}")
    print()

# ── Main Menu ──────────────────────────────────────────────────────
def print_menu():
    print(f"""
{Colors.BOLD}{Colors.YELLOW}  Main Menu{Colors.END}
  {Colors.CYAN}1.{Colors.END} 📅 Today's Matches
  {Colors.CYAN}2.{Colors.END} 📊 Group Standings
  {Colors.CYAN}3.{Colors.END} 👥 All Teams
  {Colors.CYAN}4.{Colors.END} 🏁 Match Results
  {Colors.CYAN}5.{Colors.END} 📅 Upcoming Fixtures
  {Colors.CYAN}6.{Colors.END} 🏟️ Host Stadiums
  {Colors.CYAN}7.{Colors.END} 🔴 Live Matches
  {Colors.CYAN}8.{Colors.END} 🔴 Live Mode (auto-refresh)
  {Colors.CYAN}9.{Colors.END} ⚽ Top Scorers
  {Colors.CYAN}10.{Colors.END} 🔍 Search Team
  {Colors.CYAN}11.{Colors.END} 📋 Match Details (by ID)
  {Colors.CYAN}0.{Colors.END} ❌ Exit
""")

def main():
    clear()
    banner()

    print(f"{Colors.YELLOW}Checking API connection...{Colors.END}")
    api_ok = check_api()

    if not api_ok:
        print(f"\n{Colors.YELLOW}⚠ The API is currently unavailable or the tournament hasn't started yet.\n"
              f"   Tournament begins: June 11, 2026.\n"
              f"   You can still browse cached data if available.{Colors.END}\n")

    while True:
        print_menu()
        choice = input(f"{Colors.BOLD}Select an option: {Colors.END}").strip()

        if choice == "1":
            clear(); banner(); show_todays_matches()
        elif choice == "2":
            clear(); banner(); show_standings()
        elif choice == "3":
            clear(); banner(); show_teams()
        elif choice == "4":
            clear(); banner(); show_results()
        elif choice == "5":
            clear(); banner(); show_fixtures()
        elif choice == "6":
            clear(); banner(); show_stadiums()
        elif choice == "7":
            clear(); banner(); show_live_matches()
        elif choice == "8":
            clear(); banner(); live_mode()
        elif choice == "9":
            clear(); banner(); show_top_scorers()
        elif choice == "10":
            clear(); banner(); search_team()
        elif choice == "11":
            clear(); banner(); match_details()
        elif choice == "0":
            print(f"\n{Colors.GREEN}Goodbye! Enjoy the World Cup! ⚽🏆{Colors.END}\n")
            sys.exit(0)
        else:
            print(f"{Colors.RED}Invalid option. Please try again.{Colors.END}")

        input(f"\n{Colors.YELLOW}Press Enter to return to menu...{Colors.END}")
        clear()
        banner()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.GREEN}\nGoodbye! Enjoy the World Cup! ⚽🏆{Colors.END}")
        sys.exit(0)
