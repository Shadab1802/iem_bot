# Example Run (replace '12345' with actual user_id when calling)
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append("..")
from crewai import Agent, Task, Crew
from crew_cust_tools.rag_question_tool import AdmissionQueryTool
from crew_cust_tools.data_fetcher import GetStudentTool
from config.llm_config import llm
from utils.crew_to_dict import fix_crew_output

def screener(user_id):# Agent Definition
    subject_screener = Agent(
        role="Academic Screener",
        goal="Evaluate whether a student is eligible for a specific course and stream based on eligibility criteria.",
        backstory=(
            "You're an expert in evaluating applicants. You determine if a student is eligible for a course and stream "
            "by querying eligibility rules from the AdmissionQueryTool (RAG tool)."
        ),
        tools=[AdmissionQueryTool(), GetStudentTool()],
        verbose=True,
        llm=llm
    )


    # Task to perform both academic screening and loan check
    student_academic_screening = Task(
        description=(
            "1. Use the GetStudentTool to fetch the student data using user_id: {user_id}.\n"
            "2. Extract the student's course and stream information.\n"
            "3. Use AdmissionQueryTool to find the eligibility criteria for that course and stream.\n"
            "4. Compare with the student's data. If eligible, return 'ACCEPTED', else 'REJECTED'.\n"
            "5. If 'ACCEPTED', fetch the student's requested loan amount and again use AdmissionQueryTool to fetch the maximum loanable fee for that course and stream.\n"
            "6. If loan amount is <= maximum loanable amount, return 'APPROVED', else 'DENIED'.\n"
        ),
        agent=subject_screener,
        expected_output=(
            "A dictionary object with SCREENING_STATUS and LOAN_STATUS fields based on eligibility rules."
            "\nReturn format:\n"
            "{\n"
            "  'SCREENING_STATUS': 'ACCEPTED' or 'REJECTED',\n"
            "  'LOAN_STATUS': 'APPROVED' or 'DENIED' or 'NA'\n"
            "}"
        ),
        async_execution=False,
    )

    # Optional: if you want to run it directly with Crew
    crew = Crew(
        agents=[subject_screener],
        tasks=[student_academic_screening],
        verbose=True,
    )

    # Example Run (replace '12345' with actual user_id when calling)
    result = crew.kickoff({"user_id": user_id})
    return fix_crew_output(result)
    