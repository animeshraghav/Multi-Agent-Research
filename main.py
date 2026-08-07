import re
from pathlib import Path
from pipeline.research_pipeline import run_research_pipeline
from utils.helpers import (
    print_header,
    print_success,
)

def save_report(topic: str, report: str, feedback: str):
    output_dir = Path("outputs/reports")
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = re.sub(r'[<>:"/\\|?*]', "", topic)
    filename = filename.replace(" ", "_")
    filepath = output_dir / f"{filename}.md"
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(f"# {topic}\n\n")
        file.write(report)
        file.write("\n\n---\n\n")
        file.write("# Critic Review\n\n")
        file.write(feedback)
    return filepath


def main():
    print_header("Multi-Agent Research System")
    topic = input("\nEnter a research topic: ").strip()
    if not topic:
        print("Topic cannot be empty.")
        return
    state = run_research_pipeline(topic)
    print_header("FINAL REPORT")
    print(state["report"])
    print_header("CRITIC REVIEW")
    print(state["feedback"])

    path = save_report(
        topic,
        state["report"],
        state["feedback"],
    )
    print_success(f"Report saved successfully.\n{path}")


if __name__ == "__main__":
    main()