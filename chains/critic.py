from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from config import settings
from prompts.critic_prompt import critic_prompt

llm = ChatGoogleGenerativeAI(
    model=settings.gemini_model,
    google_api_key=settings.google_api_key,
    temperature=settings.temperature,
)

critic_chain = (
    critic_prompt
    | llm
    | StrOutputParser()
)