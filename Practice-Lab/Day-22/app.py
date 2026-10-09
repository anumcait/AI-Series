"""Command-line application for the Day 22 DevOps agent."""

import json

from agent import DevOpsAgent


DEFAULT_GOAL = (
    "Check the production environment and tell me whether it "
    "needs attention."
)


def main() -> None:
    print("=" * 65)
    print("DAY 22 — LOCAL AI DEVOPS AGENT")
    print("Mode: SIMULATED DATA ONLY")
    print("=" * 65)

    goal = input(
        "\nEnter an operational goal "
        f"(press Enter for default):\n[{DEFAULT_GOAL}]\n> "
    ).strip()

    if not goal:
        goal = DEFAULT_GOAL

    agent = DevOpsAgent()

    try:
        result = agent.run(goal)
    except ValueError as exc:
        print(f"\nInput error: {exc}")
        return

    print("\n" + "=" * 65)
    print("AGENT EXECUTION TRACE")
    print("=" * 65)

    for entry in result["trace"]:
        print(json.dumps(entry, indent=2))

    print("\n" + "=" * 65)
    print("FINAL OPERATIONAL REPORT")
    print("=" * 65)
    print(result["answer"])

    print("\n" + "=" * 65)
    print("OBSERVATIONS")
    print("=" * 65)
    print(json.dumps(result["observations"], indent=2))

    print("\nInvestigation finished.")


if __name__ == "__main__":
    main()