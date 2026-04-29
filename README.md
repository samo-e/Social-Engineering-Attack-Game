# 🛡 Social Engineering Awareness Simulator

A terminal-based Python game that teaches you how to spot and respond to real-world social engineering attacks — phishing emails, phone scams, fake websites, and physical intrusion tactics.

---

## 🎯 What Is Social Engineering?

Social engineering is the #1 attack vector in cybersecurity. Instead of hacking systems, attackers hack **people** — using urgency, authority, and trust to trick you into revealing information or taking harmful actions. This simulator puts you in realistic scenarios and tests your instincts.

---

## 🗂 Features

- **8 realistic scenarios** across 4 attack categories:
  - ✉ Email (Phishing / BEC fraud)
  - ☎ Phone (Vishing)
  - 🌐 Web (Spoofed sites / Scareware)
  - 🏢 Physical (Tailgating / USB drops)
- **Difficulty selector** — Beginner, Intermediate, or Mixed
- **Hint system** — ask for a hint at any time (costs 5 points)
- **Detailed explanations** — learn *why* each answer is right or wrong
- **Red flags panel** — every scenario reveals what to watch for
- **Final report** — grade, score bar, per-category breakdown
- **About screen** — covers the psychology behind social engineering attacks
- **Colourful terminal UI** — no dependencies, pure Python

---

## 🚀 Getting Started

### Requirements

- Python **3.7 or higher**
- No external packages required — uses the Python standard library only

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/Social-Engineering-Attack-Game.git
cd Social-Engineering-Attack-Game

# Run the game
python main.py
```

---

## 🎮 How to Play

1. Run `python main.py`
2. Choose **Start Simulation** from the main menu
3. Select a difficulty level
4. Read each scenario carefully and choose the best response
5. Type `h` at any prompt to get a hint (−5 points)
6. Review your final report and red flags after each round

### Scoring

| Outcome | Points |
|---|---|
| ✅ Correct (no hint) | 10 |
| 💡 Correct (with hint) | 5 |
| ❌ Incorrect | 0 |

---

## 📁 Project Structure

```
Social-Engineering-Attack-Game/
├── main.py           # Entry point — menus and navigation
├── game.py           # Game engine, display helpers, report generator
├── scenarios.json    # All scenario data (easily extendable)
└── README.md
```

---

## ➕ Adding New Scenarios

Open `scenarios.json` and add a new entry to the `"scenarios"` array following this structure:

```json
{
  "id": 9,
  "category": "Email",
  "difficulty": "beginner",
  "title": "Your Scenario Title",
  "description": "The situation the user is presented with.",
  "question": "What do you do?",
  "choices": [
    "Option A",
    "Option B",
    "Option C (correct)",
    "Option D"
  ],
  "correct": 2,
  "hint": "A nudge in the right direction.",
  "explanation": {
    "correct": "Why this answer is right.",
    "wrong": [
      "Why option A is wrong.",
      "Why option B is wrong.",
      "Why option D is wrong."
    ]
  },
  "red_flags": [
    "Red flag 1",
    "Red flag 2"
  ]
}
```

> **Note:** `"correct"` is the **zero-based index** of the correct choice.  
> `"wrong"` explanations should match the order of incorrect choices.

---

## 📚 What You'll Learn

- How to identify phishing and lookalike domains
- Why urgency and authority are manipulation tools
- How to verify requests through a second channel
- What vishing (voice phishing) looks like in practice
- How physical attacks like tailgating and USB drops work
- The psychology behind social engineering (authority, fear, scarcity)
