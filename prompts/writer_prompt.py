from langchain_core.prompts import ChatPromptTemplate

writer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are an expert research writer.
Write professional reports.
Never hallucinate.
Use headings.
Always include citations if available.
""",
        ),
        (
            "human",
            """
Topic:
{topic}
Research Material:
{research}
Write a report using the following structure.
# Introduction
# Key Findings
(Explain each finding thoroughly.)
# Analysis
# Conclusion
# Sources
(List every URL you found.)
""",
        ),
    ]
)