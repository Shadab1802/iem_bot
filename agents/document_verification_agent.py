from crewai import Agent, Task
from config.llm_config import llm

ocr_agent = Agent(
    role="Document Field Extractor",
    goal="Extract required fields from given OCR text of a document",
    backstory="An expert at reading OCR-processed text and identifying important fields.",
    tools=[],  # No OCR tool needed now
    llm=llm
)

ocr_task = Task(
    description=(
        "You are provided OCR-processed lines from a user's 12th marksheet document. "
        "From this text, extract the fields listed in {required_fields}. "
        "Be careful about OCR noise and try to correct any obvious misreads. "
        "Use the lines below to locate field values:\n\n{ocr_lines}"
    ),
    expected_output="A dictionary of the extracted fields and their values.",
    agent=ocr_agent
)