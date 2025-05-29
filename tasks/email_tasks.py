from crewai import Task
from agents.student_counsellor import student_counsellor_agent
from config.rag_config import rag
from config.supabase_client import supabase

def handle_student_status(user_id):
    # Get the student's status
    status_resp = supabase.table("SCREENING_APPLICANT").select("SCREENING_STATUS").eq("id", user_id).execute()
    status = status_resp.data[0]["SCREENING_STATUS"] if status_resp.data else None
    status=status.lower()
    # print(status)
     # Fetch email
    email_resp = supabase.table("profiles").select("email").eq("id", user_id).execute()
    email = email_resp.data[0]["email"] if email_resp.data else None

    if status == "missing_docs":
        student_resp = supabase.table("SCREENING_APPLICANT").select("*").eq("id", user_id).execute()
        student = student_resp.data[0]
        missing_items = [key for key, val in student.items() if val is None]
        last_date = rag.ask_question("What is the last date of submission of the documents? just give the date")

        return Task(
            description="Generate a JSON containing email subject, body, and recipient email",
            expected_output=(
                f'''JSON with fields:
                "subject": Subject line of the email,
                "body": Body of the email (with proper formatting, bold for name and app number),
                "to": "{email}
                f"Proper formatting of the email with line breaks. "
                f"Name **{student['NAME']}** and application number: **{student['APPLICATION_NO']}** should be bold. "
                f"Do mention the following missing documents: {', '.join(missing_items)}. "
                f"Mention the last date of submission as {last_date}. "
                "Be polite and professional.'''),
            agent=student_counsellor_agent
        )

    elif status == "accepted":
        columns = ["STREAM", "COURSE", "NAME", "APPLICATION_NO", "LOAN_AMOUNT"]
        student_resp = supabase.table("SCREENING_APPLICANT").select(",".join(columns)).eq("id", user_id).execute()
        student = student_resp.data[0]

        doc_need = rag.ask_question(
            f"What are the documents needed after screening acceptance for admission in stream {student['STREAM']} and course {student['COURSE']} with {student['LOANED']} loan?"
        )
        last_date = rag.ask_question("What is the last date of submission of the documents? Just give the date")

        return Task(
            description="Generate a JSON containing email subject, body, and recipient email",
            expected_output=(
                f'''JSON with fields:
                "subject": Subject line of the email,
                "body": Body of the email (with proper formatting, bold for name and app number),
                "to": "{email}
                f"Proper formatting of the email with line breaks. "
                f"Name **{student['NAME']}** and application number: **{student['APPLICATION_NO']}** should be bold. "
                f"Congratulate the student for being accepted. "
                f"Tell the student that they now need to log in to the portal and upload the following documents: {doc_need}. "
                f"Mention the last date of submission as {last_date}. "
                "Be polite and professional."'''
            ),
            agent=student_counsellor_agent
        )

    elif status == "submitted":
        screening_result_date = rag.ask_question("What is the screening result announcement date?")
        student_resp = supabase.table("SCREENING_APPLICANT").select("STREAM,COURSE,NAME,APPLICATION_NO,LOAN_AMOUNT").eq("id", user_id).execute()
        student = student_resp.data[0]

        return Task(
            description="Generate a JSON containing email subject, body, and recipient email",
            expected_output=(
                f'''JSON with fields:
                "subject": Subject line of the email,
                "body": Body of the email (with proper formatting, bold for name and app number),
                "to": "{email}
                f"Proper formatting of the email with line breaks. "
                f"Name **{student['NAME']}** and application number: **{student['APPLICATION_NO']}** should be bold. "
                f"Do mention that college has received the screening request for course {student['COURSE']} in stream {student['STREAM']}. "
                f"With loan amount {student['LOAN_AMOUNT']}. "
                f"Tell the student they will be notified about the screening result on {screening_result_date}. "
                "Be polite and professional."'''
            ),
            agent=student_counsellor_agent,
        )

    elif status == "rejected":
        columns = ["STREAM", "COURSE", "NAME", "APPLICATION_NO"]
        student_resp = supabase.table("SCREENING_APPLICANT").select(",".join(columns)).eq("id", user_id).execute()
        student = student_resp.data[0]

        return Task(
            description="Generate a JSON containing email subject, body, and recipient email",
            expected_output=(
                f'''JSON with fields:
                "subject": Subject line of the email,
                "body": Body of the email (with proper formatting, bold for name and app number),
                "to": "{email}
                f"Proper formatting of the email with line breaks. "
                f"Name **{student['NAME']}** and application number: **{student['APPLICATION_NO']}** should be bold. "
                "Inform the student that their application has been rejected. And inform them that college has moved on with other applications. "
                "Do wish them luck for their future. "
                "Be polite and professional."'''
            ),
            agent=student_counsellor_agent
        )

    elif status == "final_selected":
        from utils.data_render import generate_admission_letter, generate_fees_letter
        columns = ["STREAM", "COURSE", "NAME", "APPLICATION_NO"]
        student_resp = supabase.table("STUDENT").select(",".join(columns)).eq("id", user_id).execute()
        student = student_resp.data[0]

        attachments = [
            generate_admission_letter(user_id),
            generate_fees_letter(user_id)
        ]

        last_date = rag.ask_question(
            "What is the last date of report to college for fee payment and physical document verification of selected students?"
        )
        guidelines_physical = rag.ask_question(
            "What are the guidelines for physical document verification and document verification?"
        )
        modes_of_payment = rag.ask_question("What are the modes of payment for the fee?")

        return Task(
            description="Generate a JSON containing email subject, body, and recipient email",
            expected_output=(
                f'''JSON with fields:
                "subject": Subject line of the email,
                "body": Body of the email (with proper formatting, bold for name and app number),
                "to": "{email}
                f"Proper formatting of the email with line breaks. "
                f"Name **{student['NAME']}** and application number: **{student['APPLICATION_NO']}** should be bold. "
                f"Do mention course {student['COURSE']} in stream {student['STREAM']}. "
                f"Inform the student that their admission letter and fee structure is attached. "
                f"Ask the student to print and sign the admission letter and bring it along during physical reporting to the college within the deadline of {last_date}. "
                f"Include the following guidelines for physical document verification: {guidelines_physical}. "
                f"Also mention the available modes of fee payment: {modes_of_payment}. "
                f"Attach admission letter {attachments[0]} and as well as fees structure {attachments[1]}. "
                "Be polite and professional."'''
            ),
            agent=student_counsellor_agent
        )

    else:
        print(f"⚠️ No handler for status: {status}")
        return None
