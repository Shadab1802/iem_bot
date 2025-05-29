from crewai.tools import BaseTool
from pydantic import BaseModel
from config.supabase_client import supabase
from typing import Type  # <- important for typing

class GetStudentModel(BaseModel):
    user_id: str = "User id to fetch data"

class GetStudentTool(BaseTool):
    name: str = "get_student_data"
    description: str = "Fetches student data using a user ID."
    args_schema: Type[BaseModel] = GetStudentModel  # <-- fixed annotation

    def _run(self, user_id: str) -> dict:
        response = supabase.table("SCREENING_APPLICANT").select("*").eq("id", user_id).execute()
        return response.data if hasattr(response, "data") else {}
