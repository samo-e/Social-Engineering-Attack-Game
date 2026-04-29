import json
import os
import random
from dataclasses import dataclass, field
from typing import Optional


# ── Colours ──────────────────────────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"

    @staticmethod
    def bold(text):      return f"{C.BOLD}{text}{C.RESET}"
    @staticmethod
    def red(text):       return f"{C.RED}{text}{C.RESET}"
    @staticmethod
    def green(text):     return f"{C.GREEN}{text}{C.RESET}"
    @staticmethod
    def yellow(text):    return f"{C.YELLOW}{text}{C.RESET}"
    @staticmethod
    def cyan(text):      return f"{C.CYAN}{text}{C.RESET}"
    @staticmethod
    def magenta(text):   return f"{C.MAGENTA}{text}{C.RESET}"
    @staticmethod
    def dim(text):       return f"{C.DIM}{text}{C.RESET}"


# ── Data classes ──────────────────────────────────────────────────────────────
@dataclass
class Result:
    scenario_id:   int
    category:      str
    difficulty:    str
    title:         str
    correct:       bool
    used_hint:     bool
    chosen_index:  int


@dataclass
class GameState:
    difficulty:    str = "all"
    results:       list = field(default_factory=list)
    hints_used:    int  = 0
    score:         int  = 0
    max_score:     int  = 0


# ── ScenarioLoader ────────────────────────────────────────────────────────────
class ScenarioLoader:
    def __init__(self, path: str):
        with open(path, "r") as f:
            data = json.load(f)
        self.all_scenarios = data["scenarios"]

    def get_scenarios(self, difficulty: str) -> list:
        if difficulty == "all":
            return list(self.all_scenarios)
        return [s for s in self.all_scenarios if s["difficulty"] == difficulty]

    def categories(self) -> list:
        return sorted(set(s["category"] for s in self.all_scenarios))


# ── Display helpers ───────────────────────────────────────────────────────────
def clear():
    os.system("cls" if os.name == "nt" else "clear")


def divider(char="─", width=60, colour=C.DIM):
    print(f"{colour}{char * width}{C.RESET}")


def section_header(text: str, colour=C.CYAN):
    divider()
    print(f"{colour}{C.BOLD}  {text}{C.RESET}")
    divider()


def prompt(text: str) -> str:
    return input(f"\n{C.BOLD}{C.YELLOW}  ▶  {text}{C.RESET} ").strip()


def pause():
    input(f"\n{C.DIM}  Press Enter to continue...{C.RESET}")


# ── Category badge ────────────────────────────────────────────────────────────
CATEGORY_COLOURS = {
    "Email":    C.BLUE,
    "Phone":    C.MAGENTA,
    "Web":      C.CYAN,
    "Physical": C.YELLOW,
}

CATEGORY_ICONS = {
    "Email":    "✉",
    "Phone":    "☎",
    "Web":      "🌐",
    "Physical": "🏢",
}

DIFFICULTY_COLOURS = {
    "beginner":     C.GREEN,
    "intermediate": C.YELLOW,
}


def category_badge(category: str) -> str:
    colour = CATEGORY_COLOURS.get(category, C.WHITE)
    icon   = CATEGORY_ICONS.get(category, "•")
    return f"{colour}{C.BOLD} {icon}  {category} {C.RESET}"


def difficulty_badge(difficulty: str) -> str:
    colour = DIFFICULTY_COLOURS.get(difficulty, C.WHITE)
    label  = difficulty.capitalize()
    return f"{colour}[{label}]{C.RESET}"


# ── Core game engine ──────────────────────────────────────────────────────────
class GameEngine:
    def __init__(self, loader: ScenarioLoader):
        self.loader = loader
        self.state  = GameState()

    # ── Difficulty selection ──────────────────────────────────────────────────
    def select_difficulty(self) -> str:
        clear()
        section_header("SELECT DIFFICULTY")
        options = {
            "1": ("beginner",     "Beginner      — 4 scenarios, obvious red flags"),
            "2": ("intermediate", "Intermediate  — 4 scenarios, subtler attacks"),
            "3": ("all",          "Mixed         — All 8 scenarios, randomised order"),
        }
        for key, (_, label) in options.items():
            col = C.GREEN if "Beginner" in label else (C.YELLOW if "Inter" in label else C.CYAN)
            print(f"\n  {C.BOLD}{key}.{C.RESET}  {col}{label}{C.RESET}")

        while True:
            choice = prompt("Choose difficulty (1/2/3):")
            if choice in options:
                diff, label = options[choice]
                self.state.difficulty = diff
                return diff
            print(C.red("  Invalid choice. Please enter 1, 2, or 3."))

    # ── Run a single scenario ─────────────────────────────────────────────────
    def run_scenario(self, scenario: dict, index: int, total: int) -> Result:
        clear()
        used_hint = False

        # Header
        print(f"\n  {C.DIM}Scenario {index} of {total}{C.RESET}  "
              f"{category_badge(scenario['category'])}  "
              f"{difficulty_badge(scenario['difficulty'])}\n")
        print(f"  {C.BOLD}{C.WHITE}{scenario['title']}{C.RESET}\n")
        divider()

        # Scenario description
        for line in scenario["description"].splitlines():
            print(f"  {C.DIM}{line}{C.RESET}")
        print()

        # Question
        print(f"\n  {C.BOLD}{C.WHITE}{scenario['question']}{C.RESET}\n")
        for i, choice in enumerate(scenario["choices"]):
            print(f"  {C.CYAN}{C.BOLD}  {i + 1}.{C.RESET}  {choice}")

        # Input loop
        valid_choices = [str(i + 1) for i in range(len(scenario["choices"]))]
        while True:
            print(f"\n  {C.DIM}(Enter a number, or 'h' for a hint){C.RESET}")
            ans = prompt("Your choice:").lower()

            if ans == "h":
                used_hint = True
                print(f"\n  {C.YELLOW}{C.BOLD}💡 Hint:{C.RESET}  "
                      f"{C.YELLOW}{scenario['hint']}{C.RESET}")
                continue

            if ans in valid_choices:
                chosen = int(ans) - 1
                break
            print(C.red("  Please enter a valid option number."))

        # Evaluate answer
        is_correct = (chosen == scenario["correct"])

        # Feedback
        print()
        divider(char="═")
        if is_correct:
            print(f"\n  {C.GREEN}{C.BOLD}✔  Correct!{C.RESET}\n")
            print(f"  {scenario['explanation']['correct']}")
        else:
            print(f"\n  {C.RED}{C.BOLD}✘  Not quite.{C.RESET}\n")
            wrong_exp = scenario["explanation"]["wrong"]
            idx = chosen if chosen < len(wrong_exp) else 0
            print(f"  {wrong_exp[idx]}")
            print(f"\n  {C.GREEN}The best answer was:{C.RESET}  "
                  f"{C.BOLD}{scenario['choices'][scenario['correct']]}{C.RESET}")

        # Red flags
        print(f"\n  {C.BOLD}{C.MAGENTA}🚩 Red Flags in this scenario:{C.RESET}")
        for flag in scenario["red_flags"]:
            print(f"     {C.MAGENTA}•{C.RESET}  {flag}")

        divider(char="═")
        pause()

        return Result(
            scenario_id  = scenario["id"],
            category     = scenario["category"],
            difficulty   = scenario["difficulty"],
            title        = scenario["title"],
            correct      = is_correct,
            used_hint    = used_hint,
            chosen_index = chosen,
        )

    # ── Run full game ─────────────────────────────────────────────────────────
    def run(self) -> GameState:
        difficulty  = self.select_difficulty()
        scenarios   = self.loader.get_scenarios(difficulty)
        random.shuffle(scenarios)

        self.state.max_score = len(scenarios) * 10

        for i, scenario in enumerate(scenarios, 1):
            result = self.run_scenario(scenario, i, len(scenarios))
            self.state.results.append(result)

            points = 0
            if result.correct:
                points = 5 if result.used_hint else 10
            self.state.score += points
            self.state.hints_used += int(result.used_hint)

        return self.state


# ── Report generator ──────────────────────────────────────────────────────────
class ReportGenerator:
    def __init__(self, state: GameState):
        self.state = state

    def _grade(self) -> tuple[str, str]:
        pct = (self.state.score / self.state.max_score * 100) if self.state.max_score else 0
        if pct >= 90:
            return "A", C.GREEN
        elif pct >= 70:
            return "B", C.CYAN
        elif pct >= 50:
            return "C", C.YELLOW
        else:
            return "D", C.RED

    def _bar(self, value: int, maximum: int, width: int = 20) -> str:
        filled = int((value / maximum) * width) if maximum else 0
        bar    = "█" * filled + "░" * (width - filled)
        pct    = int((value / maximum) * 100) if maximum else 0
        return f"{C.CYAN}{bar}{C.RESET}  {C.BOLD}{pct}%{C.RESET}"

    def display(self):
        clear()
        results  = self.state.results
        total    = len(results)
        correct  = sum(1 for r in results if r.correct)
        grade, gcol = self._grade()

        section_header("FINAL REPORT", colour=C.MAGENTA)

        # Score summary
        print(f"\n  {C.BOLD}Score:{C.RESET}  "
              f"{C.BOLD}{self.state.score}{C.RESET} / {self.state.max_score}  "
              f"  {C.BOLD}Grade:{C.RESET}  {gcol}{C.BOLD}{grade}{C.RESET}")
        print(f"\n  {self._bar(self.state.score, self.state.max_score)}\n")

        print(f"  {C.BOLD}Correct:{C.RESET}  {C.GREEN}{correct}{C.RESET} / {total}"
              f"   {C.BOLD}Hints used:{C.RESET}  {C.YELLOW}{self.state.hints_used}{C.RESET}\n")

        # Per-category breakdown
        divider()
        print(f"\n  {C.BOLD}Breakdown by Category:{C.RESET}\n")
        categories: dict[str, list] = {}
        for r in results:
            categories.setdefault(r.category, []).append(r)

        for cat, cat_results in sorted(categories.items()):
            cat_correct = sum(1 for r in cat_results if r.correct)
            badge = category_badge(cat)
            bar   = self._bar(cat_correct, len(cat_results))
            print(f"  {badge}  {cat_correct}/{len(cat_results)}  {bar}")

        # Scenario breakdown
        divider()
        print(f"\n  {C.BOLD}Scenario Results:{C.RESET}\n")
        for r in results:
            icon  = C.green("✔") if r.correct else C.red("✘")
            hint  = C.yellow(" [hint]") if r.used_hint else ""
            diff  = difficulty_badge(r.difficulty)
            print(f"  {icon}  {C.BOLD}{r.title}{C.RESET}  {diff}{hint}")

        # Feedback message
        divider()
        pct = (self.state.score / self.state.max_score * 100) if self.state.max_score else 0
        print()
        if pct == 100:
            msg = f"{C.GREEN}{C.BOLD}🏆 Perfect score! You're a social engineering expert.{C.RESET}"
        elif pct >= 70:
            msg = f"{C.CYAN}{C.BOLD}👍 Good work! A few attacks slipped through — review the red flags above.{C.RESET}"
        elif pct >= 50:
            msg = f"{C.YELLOW}{C.BOLD}⚠  Room to improve. Attackers rely on urgency and trust — always verify.{C.RESET}"
        else:
            msg = f"{C.RED}{C.BOLD}🔴 High risk! Review each scenario carefully — awareness is your best defence.{C.RESET}"
        print(f"  {msg}\n")

        # Tip of the day
        tips = [
            "Always verify unexpected requests through a second channel.",
            "Urgency is a manipulation tool — slow down and think.",
            "Legitimate organisations never ask for passwords or CVVs unprompted.",
            "A convincing appearance (uniform, logo, email layout) proves nothing.",
            "When in doubt, report it to your IT or security team.",
            "Check URLs character by character — lookalike domains are common.",
        ]
        print(f"  {C.BOLD}{C.MAGENTA}💡 Tip of the day:{C.RESET}  {C.DIM}{random.choice(tips)}{C.RESET}\n")
        divider()