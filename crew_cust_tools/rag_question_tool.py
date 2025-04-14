from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from config.rag_config import rag
# from tools.schemas import AdmissionQueryToolSchema  # or define inline

class AdmissionQueryToolSchema(BaseModel):
    """Input schema for AdmissionQueryTool"""
    question: str = Field(..., description="This is the question that was asked by user and will be passed to a RAG chat bot to get answer")

class AdmissionQueryTool(BaseTool):
    name: str = "Admission Query Answering Tool"
    description: str = "Use this to answer any admission-related question using the brochure"
    args_schema = AdmissionQueryToolSchema

    def _run(self, question: str) -> str:
        return rag.ask_question(question)
