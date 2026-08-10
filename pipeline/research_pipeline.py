from langchain_core.messages import HumanMessage
from agents.search_agent import search_agent
from agents.reader_agent import reader_agent
from chains import (
    writer_chain,
    critic_chain,
)
from utils.helpers import (
    print_header,
    print_success,
)


def run_research_pipeline(topic: str, on_step=None) -> dict:
    state = {}

    def emit(step: str, status: str):
        """Send pipeline progress updates to the caller."""
        if on_step:
            on_step(step, status)

    ########################################
    # STEP 1 : SEARCH AGENT
    ########################################

    emit("search", "running")

    print_header("STEP 1 : SEARCH AGENT")

    search_result = search_agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content=f"Find recent and reliable information about {topic}"
                )
            ]
        }
    )

    print("\nFULL SEARCH RESULT\n")
    print(search_result)

    search_text = search_result["messages"][-1].content
    state["search_results"] = search_text

    emit("search", "done")

    print_success("Search completed.")

    ########################################
    # STEP 2 : READER AGENT
    ########################################

    emit("read", "running")

    print_header("STEP 2 : READER AGENT")

    reader_result = reader_agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content=f"""
Read the following search result.
Extract the best URL.
Scrape it.

Search Results:

{search_text}
"""
                )
            ]
        }
    )

    scraped = reader_result["messages"][-1].content
    state["scraped_content"] = scraped

    emit("read", "done")

    print_success("Scraping completed.")

    ########################################
    # STEP 3 : WRITER
    ########################################

    emit("write", "running")

    print_header("STEP 3 : WRITER")

    research = f"""
SEARCH RESULTS
{search_text}

SCRAPED CONTENT
{scraped}
"""

    report = writer_chain.invoke(
        {
            "topic": topic,
            "research": research,
        }
    )

    state["report"] = report

    emit("write", "done")

    print_success("Report generated.")

    ########################################
    # STEP 4 : CRITIC
    ########################################

    emit("critique", "running")

    print_header("STEP 4 : CRITIC")

    feedback = critic_chain.invoke(
        {
            "report": report
        }
    )

    state["feedback"] = feedback

    emit("critique", "done")

    print_success("Critic completed.")

    ########################################

    return state