from crewai import Agent
from crew_cust_tools.rag_question_tool import AdmissionQueryTool

subject_screener = Agent(
    role="Academic Screener",
    goal="Evaluate whether a student is eligible for a specific course and stream based on eligibility criteria.",
    backstory=(
        "You're an expert in evaluating applicants. You determine if a student is eligible for a course and stream "
        "by querying eligibility rules from the AdmissionQueryTool (RAG tool)."
    ),
    tools=[AdmissionQueryTool()],
    verbose=True,
)


from crewai import Task

screen_applicant_task = Task(
    description="Check if the student is eligible for the course and stream they applied for.",
    agent=subject_screener,
    expected_output="Return 'accepted' or 'rejected' based on the eligibility criteria.",
    async_execution=False,
)


