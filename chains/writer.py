from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from prompts.writer_prompt import writer_prompt

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",

)

writer_chain = (
    writer_prompt
    | llm
    | StrOutputParser()
)