# agents/ocr_correction_agent.py
from crewai import Agent, Task, Crew
from config.llm_config import llm

ocr_correction_agent = Agent(
    role="Field Correction Agent",
    goal="Understand user's corrections to extracted fields",
    backstory="You help users fix small errors in auto-extracted data.",
    tools=[],
    llm=llm
)

ocr_correction_task = Task(
    description=(
        "Original extracted fields:\n{extracted_data}\n\n"
        "User said: '{user_input}'\n\n"
        "Update the fields according to the user's correction. Return a corrected dictionary."
    ),
    expected_output="A dictionary with corrected fields.",
    agent=ocr_correction_agent
)

def parse_user_corrections(user_input, extracted_data):
    crew = Crew(
        agents=[ocr_correction_agent],
        tasks=[ocr_correction_task]
    )
    result = crew.kickoff({
        "user_input": user_input,
        "extracted_data": extracted_data
    })
    return result.output if hasattr(result, "output") else {}
