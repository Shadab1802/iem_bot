# agents/course_stream_agent.py
from crewai import Agent, Task,Crew
from config.llm_config import llm
from config.rag_config import rag

course_agent = Agent(
    role="Stream and Course Extractor",
    goal="Extract the user's intended course and stream",
    backstory="An assistant who understands user input and maps it to valid fields",
    tools=[],
    llm=llm
)
course=rag.ask_question('Courses Offered by college?')
streams= rag.ask_question('List all streams of each courses from broucher')
maximum_loan=rag.ask_question(f'Tell me the maximum amount of loan i can get for course{course} and stream {streams}')
course_task = Task(
    description=(
        "The user has said: '{user_input}'. Extract fields 'STREAM' and 'COURSE'. "
        f"The Courses offered by college are: {course}. "
        f"The Streams offered are: {streams}. "
        f"The maximum amount of loan offered for course is mentioned {maximum_loan}"
    ),
    expected_output=(
    "Only return a Python dictionary with STREAM and COURSE and LOAN_AMOUNT. No other explanation or text. "
    "Example: {'STREAM': 'Science', 'COURSE': 'B.Tech','Loan Amount': 100000}"),
    agent=course_agent
)

import ast
import re

def extract_dict_from_output(output):
    """Extract dictionary from agent output (string or dict)."""
    if isinstance(output, dict):
        return output
    try:
        match = re.search(r"\{.*\}", str(output))
        if match:
            return ast.literal_eval(match.group(0))
    except Exception as e:
        print("❌ Failed to parse dict:", e)
    return {}

def extract_course_and_stream(user_input):
    crew = Crew(agents=[course_agent], tasks=[course_task])
    result = crew.kickoff({"user_input": user_input})
    
    print("🔍 Raw agent output:", result)

    return extract_dict_from_output(result)
