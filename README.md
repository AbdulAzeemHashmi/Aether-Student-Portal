# AETHER: Zenith Academic OS 🌌

> A premium, glassmorphism-powered Learning OS for the modern scholar.

![Platform](https://img.shields.io/badge/Platform-Flask%20%2B%20MongoDB-6366f1?style=for-the-badge&logo=flask&logoColor=white)
![Frontend](https://img.shields.io/badge/Frontend-Vanilla%20HTML%2FCSS%2FJS-ec4899?style=for-the-badge&logo=html5&logoColor=white)
![Database](https://img.shields.io/badge/Database-MongoDB%20Atlas-10b981?style=for-the-badge&logo=mongodb&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-a855f7?style=for-the-badge)

---

## What is AETHER?

AETHER is a full-stack academic management platform built with a high-fidelity "Zenith Glass" design language. It gives university students a unified, visually immersive workspace to track their GPA trajectory, map course prerequisites, visualize their academic timeline, and manage their identity profile, all backed by a persistent cloud database.

Think of it as a mission control center for your degree.

---

## Screenshots

| Login | Animus Hub | Nexus Map |
|---|---|---|
| Glassmorphic auth card with 3D parallax | Central dashboard with stat grid | Interactive prerequisite skill tree |

| Chronicle | Intelligence Report | Neural Identity |
|---|---|---|
| Animated semester timeline | AI-driven GPA and health analysis | Profile sync with photo upload |

---

## Feature Breakdown

### Animus Hub
The central command dashboard. Displays at-a-glance stats including current GPA, credit hours completed, health scores, and quick-launch tiles to all other modules.

### Nexus Map
An interactive skill-tree graph that visualizes the prerequisite topology of your entire degree. Courses are nodes; prerequisites are directed edges. Unlock progression as you advance.

### Academic Chronicle
A scroll-triggered, alternating timeline of all 8 semesters. Completed semesters display locked GPA and course data; future semesters appear as "quantum possibilities." Powered by IntersectionObserver for cinematic entrance animations.

### Intelligence Report
An AI-driven analysis panel that evaluates your GPA trend, academic health score, and flags gatekeeper courses that may affect your graduation trajectory.

### Neural Identity
A persistent profile page where students synchronize their name, roll number, email, password, and profile photo across all devices via MongoDB Atlas.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3, Flask 3.0, Flask-CORS |
| Database | MongoDB Atlas (cloud), pymongo 4.7 |
| Frontend | Vanilla HTML5, CSS3, JavaScript (ES6+) |
| Fonts | Outfit, Space Grotesk, Inter (Google Fonts) |
| Extras | python-pptx (report export), CSS backdrop-filter glassmorphism |

---

## Getting Started

### Prerequisites
- Python 3.9 or higher
- pip
- An active internet connection (for MongoDB Atlas and Google Fonts)
- A free [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) account (or use the provided URI)

### 1. Clone the Repository

```bash
git clone https://github.com/AbdulAzeemHashmi/aether-academic-os.git
cd aether-academic-os
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the Database

Open `app.py` and locate the `MONGO_URI` variable near the top. Replace it with your own MongoDB Atlas connection string if you want your own isolated database:

```python
MONGO_URI = "mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority"
```

The app auto-seeds course data and creates indexes on the first run. No manual database setup is required.

### 4. Launch the Server

```bash
python app.py
```

You will see:

```
Checking Database Integrity...
Database Ready.
 * Running on http://0.0.0.0:3000
```

### 5. Open the Platform

| Device | URL |
|---|---|
| PC / Laptop | `http://localhost:3000` |
| Mobile (same WiFi) | `http://<your-pc-local-ip>:3000` |

Create an account via **Join AETHER**, then sign in. Roll number format: `24I-2013`.

---

## Project Structure

```
aether-academic-os/
├── app.py              # Flask backend, REST API, MongoDB logic
├── requirements.txt    # Python dependencies
├── login.html          # Authentication entry point
├── signup.html         # New user registration
├── hub.html            # Animus Hub dashboard
├── nexus.html          # Nexus Map skill tree
├── chronicle.html      # Academic Chronicle timeline
├── analysis.html       # Intelligence Report
├── profile.html        # Neural Identity profile editor
└── README.md
```

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/login` | Authenticate a user by roll number and password |
| POST | `/api/register` | Register a new student account |
| POST | `/api/update-user` | Update profile fields including roll number cascade |
| GET | `/api/get-profile/<roll>` | Retrieve stored profile data for a roll number |
| POST | `/api/get-profile` | Save profile data blob for a roll number |

All endpoints return JSON with a `success` boolean and a `message` on failure.

---

## Roll Number Format

AETHER enforces the following format for roll numbers at registration:

```
Pattern:  \d{2}[A-Z]-\d{4}
Example:  24I-2013
```

---

## Design Philosophy

AETHER is built around the "Zenith Glass" design principle:

- **Dark-first aesthetics** with a near-black `#030303` base
- **Glassmorphism** via `backdrop-filter: blur()` and translucent card surfaces
- **Ambient lighting** through large, blurred gradient blobs that react to mouse parallax
- **3D depth** using CSS `transform-style: preserve-3d` and `perspective`
- **Scroll choreography** powered by IntersectionObserver for cinematic page reveals
- **Typographic hierarchy** with Outfit (display), Space Grotesk (UI), and Inter (body)

---

## Contributing

Contributions are welcome. To propose a change:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "feat: describe your change"`
4. Push to your fork: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please keep the design language consistent with the existing Zenith Glass aesthetic.

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.

---

<div align="center">
  <strong>Built with precision by Abdul Azeem Hashmi</strong><br/>
  <em>Zenith Glass Design Principles | AETHER Protocol</em>
</div>
