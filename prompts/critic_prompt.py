from langchain_core.prompts import ChatPromptTemplate

critic_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a senior research reviewer.

Critically evaluate the report.

Focus on

- Accuracy
- Completeness
- Citations
- Readability
- Structure
- Logical flow

Be objective.
""",
        ),
        (
            "human",
            """
Review this report.
{report}
Respond exactly in the following format.
Score: X/10
Strengths
- ...
Weaknesses
- ...
Suggestions
- ...
Final Verdict
...
""",
        ),
    ]
)