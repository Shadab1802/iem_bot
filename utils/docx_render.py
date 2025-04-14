from pathlib import Path
from docxtpl import DocxTemplate
from io import BytesIO
from utils.data_access import get_student_data
# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

def render_template(template_name: str, data: dict) -> BytesIO:
    """Render a .docx template with student data and return as BytesIO."""
    template_path = BASE_DIR / "templates" / template_name
    doc = DocxTemplate(template_path)
    doc.render(data)

    doc_io = BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)
    return doc_io


def generate_admission_letter(user_id: str) -> BytesIO:
    """Generate admission letter for the student."""
    student_data = get_student_data(user_id)
    return render_template("admission_letter_template.docx", student_data)


def generate_fees_letter(user_id: str) -> BytesIO:
    """Generate fee structure letter for the student."""
    student_data = get_student_data(user_id)
    return render_template("fees_template.docx", student_data)
