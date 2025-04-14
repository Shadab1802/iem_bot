from crew_cust_tools.rag_question_tool import AdmissionQueryTool
from crewai import Agent,LLM

import os 
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm=LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0.1,
)

# rag_tool = AdmissionQueryTool()

# Create your agent
admission_agent = Agent(
    role="Strict Admission and Loan Assistant",
    goal=(
        "Answer admission and loan-related queries using the admission brochure and basic loan logic. "
        "Be precise, avoid assumptions, and NEVER use external general knowledge. "
        "Use brochure contents for admission queries and perform basic calculations for loan-related queries if information is provided."
    ),
    backstory=(
        "You are an expert in college admissions and loan assistance. You rely strictly on the official admission brochure for all admission-related queries. "
        "For loan-related queries, you apply basic calculations only if the user provides necessary inputs like total loan amount, number of semesters, etc. "
        "Never fabricate any data. If information is missing in the brochure or the user’s query, clearly state it."
        "Don't make any information by yourself stickly to broucher information"
    ),
    tools=[AdmissionQueryTool()],
    verbose=True,
    llm=llm,
)