#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║       SOCIAL ENGINEERING AWARENESS SIMULATOR             ║
║       Learn to spot manipulation before it's too late    ║
╚══════════════════════════════════════════════════════════╝

Usage:
    python main.py
"""

import os
import sys

from game import (
    C, GameEngine, ReportGenerator, ScenarioLoader,
    clear, divider, pause, prompt, section_header,
)

SCENARIOS_FILE = os.path.join(os.path.dirname(__file__), "scenarios.json")

BANNER = f"""
{C.CYAN}{C.BOLD}
  ╔══════════════════════════════════════════════════════════╗
  ║    🛡   SOCIAL ENGINEERING AWARENESS SIMULATOR   🛡     ║
  ║         Learn to spot manipulation before it's           ║
  ║                 too late.                                 ║
  ╚══════════════════════════════════════════════════════════╝
{C.RESET}"""

INTRO = f"""
  {C.BOLD}What is social engineering?{C.RESET}

  {C.DIM}Social engineering is the art of manipulating people into
  revealing confidential information or taking harmful actions.
  It's the #1 attack vector in cybersecurity — and it works
  because it targets humans, not systems.{C.RESET}

  {C.BOLD}How to play:{C.RESET}

  {C.DIM}You'll be presented with realistic scenarios — emails,
  phone calls, websites, and physical situations. For each one,
  choose the best response. You can request a hint at any time,
  but hints reduce your score for that question.{C.RESET}

  {C.BOLD}Scoring:{C.RESET}
    {C.GREEN}Correct (no hint){C.RESET}   →  {C.BOLD}10 points{C.RESET}
    {C.YELLOW}Correct (with hint){C.RESET} →  {C.BOLD}5 points{C.RESET}
    {C.RED}Incorrect{C.RESET}           →  {C.BOLD}0 points{C.RESET}
"""


def show_menu() -> str:
    clear()
    print(BANNER)
    divider()
    print(INTRO)
    divider()
    print(f"""
  {C.BOLD}1.{C.RESET}  {C.GREEN}Start Simulation{C.RESET}
  {C.BOLD}2.{C.RESET}  {C.CYAN}About Social Engineering{C.RESET}
  {C.BOLD}3.{C.RESET}  {C.RED}Quit{C.RESET}
""")
    while True:
        choice = prompt("Choose an option (1/2/3):")
        if choice in ("1", "2", "3"):
            return choice
        print(C.red("  Invalid option. Enter 1, 2, or 3."))


def show_about():
    clear()
    section_header("ABOUT SOCIAL ENGINEERING")
    content = f"""
  {C.BOLD}Common Attack Types:{C.RESET}

  {C.BLUE}{C.BOLD}  ✉  Phishing{C.RESET}
  {C.DIM}  Deceptive emails that impersonate trusted sources to steal
  credentials or install malware.{C.RESET}

  {C.MAGENTA}{C.BOLD}  ☎  Vishing (Voice Phishing){C.RESET}
  {C.DIM}  Phone scams impersonating banks, IT support, or authorities
  to extract sensitive information.{C.RESET}

  {C.CYAN}{C.BOLD}  🌐  Pharming / Spoofed Sites{C.RESET}
  {C.DIM}  Fake websites that look identical to real ones, designed to
  capture your login credentials.{C.RESET}

  {C.YELLOW}{C.BOLD}  🏢  Physical Attacks{C.RESET}
  {C.DIM}  Tailgating into secure areas, USB drops, or impersonating
  delivery personnel to gain physical access.{C.RESET}

  {C.BOLD}The Psychology Behind It:{C.RESET}

  {C.DIM}  • {C.RESET}{C.BOLD}Authority{C.DIM}  — Impersonating bosses, IT, or police
  {C.RESET}  • {C.BOLD}Urgency{C.DIM}    — 'Act now or lose your account!'
  {C.RESET}  • {C.BOLD}Scarcity{C.DIM}   — 'Only you can fix this'
  {C.RESET}  • {C.BOLD}Liking{C.DIM}     — Building rapport before the ask
  {C.RESET}  • {C.BOLD}Fear{C.DIM}       — 'Your computer is infected!'{C.RESET}

  {C.BOLD}Your Best Defences:{C.RESET}

  {C.DIM}  1. Pause and verify — never act on urgency alone
  2. Use a second channel to confirm requests
  3. Trust your instincts — if it feels off, it probably is
  4. Report suspicious activity to your security team{C.RESET}
"""
    print(content)
    divider()
    pause()


def play_again() -> bool:
    print()
    ans = prompt("Play again? (y/n):").lower()
    return ans in ("y", "yes")


def main():
    if not os.path.exists(SCENARIOS_FILE):
        print(C.red(f"\n  Error: scenarios.json not found at {SCENARIOS_FILE}\n"))
        sys.exit(1)

    loader = ScenarioLoader(SCENARIOS_FILE)

    while True:
        choice = show_menu()

        if choice == "1":
            engine = GameEngine(loader)
            state  = engine.run()
            report = ReportGenerator(state)
            report.display()

            if not play_again():
                break

        elif choice == "2":
            show_about()

        elif choice == "3":
            break

    clear()
    print(f"\n  {C.CYAN}{C.BOLD}Stay vigilant. Stay secure. 🛡{C.RESET}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {C.DIM}Session interrupted. Goodbye!{C.RESET}\n")
        sys.exit(0)