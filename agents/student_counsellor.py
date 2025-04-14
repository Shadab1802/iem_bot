from crewai import Agent
from crew_cust_tools.email_sender import EmailSenderTool
from config.rag_config import rag
from config.llm_config import llm

institue_name = rag.ask_question("What is the name of the institute?")
institue_contact=rag.ask_question("What is the contact details of the admission cell?")

student_counsellor_agent = Agent(
    role="Student Counsellor",
    goal="Communicate with students at various stages of their admission process.Send attachment when generated",
    backstory=(
        f"You are a student counsellor responsible for informing students about their admission results. "
        f"You are expert in student communication through email and you are extremly poilite and professional"
        f"You are writing on behalf of {institue_name}'s admission cell. "
        f"For any queries, students should contact the admission cell at {institue_contact}."
    ),
    tools=[EmailSenderTool()],  # Optional if already in sender agent
    verbose=True,
    llm=llm,
    allow_delegation=True,  # <-- This is important
)