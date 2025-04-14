from crewai import Task, Crew
from agents.rag_agent import admission_agent
task = Task(
    description="Answer this question: What is the eligibility criteria for MBA?",
    expected_output="Eligibility requirements as per the admission brochure.",
    agent=admission_agent
)

crew = Crew(tasks=[task])
crew.kickoff()
