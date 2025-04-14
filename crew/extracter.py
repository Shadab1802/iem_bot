from crewai import Crew
from agents.document_verification_agent import fields_extractor_agent
from tasks.docu_verify import fields_extractor_task

extracter_crew = Crew(
    agents=[fields_extractor_agent],
    tasks=[fields_extractor_task],
    verbose=True,
)