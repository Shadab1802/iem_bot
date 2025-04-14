import os 
from dotenv import load_dotenv
from crewai import LLM
# from langchain_google_genai import ChatGoogleGenerativeAI
# load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
## GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")

llm=LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0.7,
)

# llm= ChatGoogleGenerativeAI(
#     model="gemini-1.5-flash",
#     verbose=True,
#     temperature=0.2,
#     google_api_key=os.getenv("GEMINI_API_KEY")
# )

# import os
# from dotenv import load_dotenv
# from crewai import LLM

# load_dotenv()

# llm = LLM(
#     model="gemini/gemini-1.5-pro-latest",
#     temperature=0.4,
#     api_key=os.getenv("GEMINI_API_KEY")
# )
