from crewai import Crew, Task
from agents.student_counsellor import student_counsellor_agent
from config.supabase_client import supabase
from tasks.email_tasks import handle_student_status


def student_councellor(user_id):
    # Generate the email content based on the student's status
    email_gen_task = handle_student_status(user_id)  # returns a Task
    print("Type of email_geb_task: ",type(email_gen_task))

    # Retrieve the recipient's email from Supabase
    result = supabase.table("profiles").select("email").eq("user_id", user_id).execute()
    email = result.data[0]['email'] if result.data else None

    # Create the task for sending the email
    email_sender_task = Task(
        description=(
            "Use the output of the previous task to send an email. "
            "The input will include subject, body, and optional attachment_paths or attachment_streams. "
            "Send the email using the email_sender tool. "
            f"The recipient of this email is {email}."
        ),
        expected_output="Confirmation of email being sent or an error message.",
        agent=student_counsellor_agent,
        context=[email_gen_task]
    )

    # Create the Crew with the tasks and agents
    email_crew = Crew(
        agents=[student_counsellor_agent],
        tasks=[email_gen_task, email_sender_task],
        verbose=True,
    )

    # Run the Crew
    email_crew.kickoff()
