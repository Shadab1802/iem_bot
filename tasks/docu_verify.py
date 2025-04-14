from crewai import Task
from agents.document_verification_agent import fields_extractor_agent
from utils.doc_text_extracter import extract_text_from_image

IMAGE_PATH = r"C:\Users\HP\Downloads\SID_ClassXMarksheet.jpg"
ocr_text=extract_text_from_image(IMAGE_PATH)

doc="12th mark sheet"

if(doc=="adhar card"):
    req_fields = ["Name", "Father's Name", "Address", "PinCode","Aadhar no.","Date of Birth"]
elif(doc=="12th mark sheet"):
    req_fields = ["Name", "Father Name", "Mother Name", "Date of Birth","Mathematics","Physics","Chemistry","Marks Obtained","Total Marks"]


fields_extractor_task = Task(
    description=(
        "You are given an easyocr Extracted lines from an scanned documents.\n"
        f"{ocr_text}"
        f"Your work is to give me the values of {req_fields} fields from above easyocr extracted text.\n"
        f"Return the result as a dict, key begin the {req_fields} and its pair beign the field value that you have extracted from the easyocr lines provided above.\n"
    ),

    expected_output="A Disctonary having the required fields as key and its values that you exracted from the easyocr passed to you.",
    agent=fields_extractor_agent
)
