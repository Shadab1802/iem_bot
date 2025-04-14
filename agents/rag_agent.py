import os
from dotenv import load_dotenv
from crewai.llm import LLM
from crewai import Agent
from crew_cust_tools.rag_question_tool import AdmissionQueryTool
# from crew_tools.doc_extract_tool import ExtractTextTool  # example
# from crew_tools.db_tool import SaveToDBTool  # example

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm=LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0.0,
)

# Instantiate the tools
rag_tool = AdmissionQueryTool()

# Create your agent
admission_agent = Agent(
    role="Strict Admission Brochure Assistant",
    goal=(
        "Only answer admission-related questions using the brochure. "
        "Never fabricate or assume information. Be concise and to the point."
    ),
    backstory=(
        "You are an expert in admission policies. You have access to the official admission brochure, "
        "which is your ONLY source of truth. NEVER answer questions from general knowledge. "
        "If the brochure does not contain the answer, say 'This information is not available in the brochure.'"
    ),
    tools=[rag_tool],
    verbose=True,
    llm=llm,
)
