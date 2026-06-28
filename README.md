# ⚽ World Cup Tracker 2026

> A beautiful command-line application for tracking every match, live score, group table, fixture, and tournament statistic for the FIFA World Cup 2026.
<br>
<img width="844" height="650" alt="Screenshot 2026-06-28 051857" src="https://github.com/user-attachments/assets/1123c986-e15b-4a2c-911d-001771609270" />
<img width="820" height="839" alt="Screenshot 2026-06-28 052053" src="https://github.com/user-attachments/assets/3a0f2995-9677-492c-b5ef-db1e8bc3fee7" />
<img width="855" height="987" alt="Screenshot 2026-06-28 052018" src="https://github.com/user-attachments/assets/fba30379-6b94-4193-bddc-f93313f5ed6b" />
<img width="838" height="943" alt="Screenshot 2026-06-28 051928" src="https://github.com/user-attachments/assets/71d07888-8e43-4f21-9024-5e422bbc661b" />


---

![Python](https://img.shields.io/badge/Python-3.7+-blue?style=for-the-badge\&logo=python\&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![API](https://img.shields.io/badge/API-worldcup26.ir-orange?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=for-the-badge)

---

## 📖 Table of Contents

* [Features](#-features)
* [Installation](#-installation)
* [Menu](#-menu)
* [API](#-api)
* [Tournament Overview](#-tournament-overview)
* [Repository Structure](#-repository-structure)
* [System Requirements](#-system-requirements)
* [Contributing](#-contributing)
* [License](#-license)

---

## ⚽ Features

* 📅 Today's Matches
* 🔴 Live Matches
* 🔄 Live Mode (Auto Refresh)
* 📊 Group Standings
* 🌍 All 48 Qualified Teams
* ✅ Match Results
* 📆 Upcoming Fixtures
* 🏟 Host Stadiums
* 🥇 Top Scorers
* 🔍 Search Teams
* 📄 Match Details

---

## 🚀 Installation

### Clone the repository

```bash
git clone https://github.com/a-sharif0/worldcup-2026-tracker-cli.git
cd worldcup-2026-tracker-cli
```

Or download the ZIP directly from GitHub.

### Check Python

Linux / macOS

```bash
python3 --version
```

Windows

```powershell
python --version
```

Download Python if necessary:

https://www.python.org/downloads/

---

## ▶ Running the Application

Linux / macOS

```bash
python3 worldcup_tracker.py
```

Windows

```powershell
python worldcup_tracker.py
```

or

```powershell
py worldcup_tracker.py
```

No virtual environment.

No pip.

No dependencies.

Only Python.

---

## 📋 Menu

```text
Main Menu

1. Today's Matches
2. Group Standings
3. All Teams
4. Match Results
5. Upcoming Fixtures
6. Host Stadiums
7. Live Matches
8. Live Mode
9. Top Scorers
10. Search Team
11. Match Details
0. Exit
```

---

## 🌍 API

Powered by the free **worldcup26.ir** REST API.

| Feature        | Value |
| -------------- | ----- |
| Authentication | None  |
| Matches        | 104   |
| Teams          | 48    |
| Groups         | 12    |
| Stadiums       | 16    |

### Endpoints

```text
GET /get/games
GET /get/groups
GET /get/teams
GET /get/stadiums
GET /health
```

---

## 🏆 Tournament Overview

* **Tournament:** FIFA World Cup 2026
* **Dates:** 11 June – 19 July 2026
* **Host Nations:** 🇺🇸 United States 🇲🇽 Mexico 🇨🇦 Canada
* **Teams:** 48
* **Matches:** 104
* **Groups:** 12
* **Defending Champions:** Argentina

---

## 📁 Repository Structure

```text
worldcup-2026-tracker-cli/
├── worldcup_tracker.py
├── README.md
├── LICENSE
└── .gitignore
```

---

## 💻 System Requirements

| Requirement | Minimum         |
| ----------- | --------------- |
| Python      | 3.7+            |
| RAM         | 50 MB           |
| Disk Space  | 1 MB            |
| Internet    | Required        |
| Terminal    | Unicode Support |

---

## 💡 Notes

* Built entirely with the Python Standard Library.
* Cross-platform support.
* ANSI colour support.
* Live Mode refreshes every 30 seconds.
* Press **Ctrl + C** to exit Live Mode.

---

## 🤝 Contributing

Contributions are welcome.

```bash
git checkout -b feature/my-feature
git commit -m "Add awesome feature"
git push origin feature/my-feature
```

Then open a Pull Request.

---

## 📄 License

This project is licensed under the MIT License.

---

## ❤️ Acknowledgements

* worldcup26.ir API
* FIFA World Cup 2026
* Every football fan who loves the terminal

---

<div align="center">

### ⭐ If you enjoy this project, consider giving it a star!

Made with ❤️ for the beautiful game.

</div>
