from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from prompts.critic_prompt import critic_prompt

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",

)

critic_chain = (
    critic_prompt
    | llm
    | StrOutputParser()
)