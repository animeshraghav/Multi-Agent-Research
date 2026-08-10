from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from config import settings
from prompts.writer_prompt import writer_prompt

llm = ChatGoogleGenerativeAI(
    model=settings.gemini_model,
    google_api_key=settings.google_api_key,
    temperature=settings.temperature,
)

writer_chain = (
    writer_prompt
    | llm
    | StrOutputParser()
)