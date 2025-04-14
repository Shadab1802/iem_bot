from config.supabase_client import supabase
from crewai import Task,Crew
from agents.admission_query import admission_agent
import re
from utils.doc_text_extracter import extract_text_from_image
import streamlit as st
from crew.communicator import student_councellor

def basefunction(user_id,user_state,chat_history,user_text,file):
    # user_state = supabase.table("profiles").select("STATE").eq("user_id", user_id).single().execute().data('STATE')
    # if re.search(r"\b(start|begin|initiate)\b.*\b(screening|registration)\b", user_query.lower()):
    #     response = supabase.table("profiles").update({"STATE": "SCREENIG_REGISTRATION"}).eq("user_id", user_id).execute()
    print(user_state)
    if user_state=="CHAT":
        # agents/chat_logic.py

        context = "\n".join([f"User: {q}" for q in chat_history])

        # 4. Define CrewAI task
        user_query_task = Task(
            description=f"""
            Based on this conversation history:
            {context}
            
            Respond to the latest question: "{user_text}" related to admission to the college.
            Make sure to use RAG via AdmissionQueryTool if needed.
            And at end of every response ask user if they want to Start Screening Process. If they then ask them to write 'Start Screening Registration' """,
            expected_output="A concise and accurate answer.",
            agent=admission_agent
        )

        crew = Crew(
            agents=[admission_agent],
            tasks=[user_query_task],
            verbose=True
        )

        result = crew.kickoff(inputs={"query": user_text})
        return result
    if user_state == "SCREENING_REGISTRATION":
    # Check if course or stream are missing
        response = supabase.table("SCREENING_APPLICANT").select("*").eq("user_id", user_id).execute()
        record = response.data[0] if response.data else {}

        if record.get("STREAM") is None or record.get("COURSE") is None:
            supabase.table("profiles").update({"STATE": "WAITING_FOR_STREAM_COURSE"}).eq("user_id", user_id).execute()
            return "Please tell me which course, stream and amount of loan you are interested in."

    elif user_state == "WAITING_FOR_STREAM_COURSE":
        # Use Crew agent to extract STREAM/COURSE from user_text
        from agents.course_stream_agent import extract_course_and_stream

        parsed_fields = extract_course_and_stream(user_text)

        # Safely extract values (normalize keys to uppercase)
        course = parsed_fields.get("COURSE") or parsed_fields.get("course")
        stream = parsed_fields.get("STREAM") or parsed_fields.get("stream")
        loan_amount = parsed_fields.get("LOAN_AMOUNT") or parsed_fields.get("loan_amount")

        if course and stream:
            # Save to DB
            supabase.table("SCREENING_APPLICANT").update({
                "COURSE": course,
                "STREAM": stream,
                "LOAN_AMOUNT": loan_amount
            }).eq("user_id", user_id).execute()
            supabase.table("profiles").update({"STATE":"WAITING_FOR_MARKSHEET"}).eq("user_id", user_id).execute()

            return f"Got it! Course: {course}, Stream: {stream} and Loan amount {loan_amount}. Now please upload your Class 12th marksheet."
        else:
            return "Hmm, I couldn't extract course , stream and loan amount. Could you please rephrase your input?"


    elif user_state == "WAITING_FOR_MARKSHEET":
        from agents.document_verification_agent import ocr_agent,ocr_task
        from crew.screener import screener
        from utils.crew_to_dict import fix_crew_output
        if file is None:
            return "Please upload your Class 12th marksheet image."
        
        ocr_lines = extract_text_from_image(file)

        docVeri = Crew(agents=[ocr_agent], tasks=[ocr_task], verbose=True)

        response = supabase.table("SCREENING_APPLICANT").select("*").eq("user_id", user_id).execute()

        extracted_data = {}  # ✅ initialize early

        if response.data and response.data[0].get("NAME") is None:
            required_fields = set()

            for record in response.data:
                for key, value in record.items():
                    if value is None:
                        required_fields.add(key)

            result = docVeri.kickoff({
                "ocr_lines": ocr_lines,
                "required_fields": list(required_fields)
            })

            extracted_data=fix_crew_output(result)
            print(extracted_data)
            supabase.table("SCREENING_APPLICANT").update(extracted_data).eq("user_id",user_id).execute()
            # Update user state
            supabase.table("profiles").update({"STATE": "SCREENING_REVIEWING"}).eq("user_id", user_id).execute()
            supabase.table("SCREENING_APPLICANT").update({"SCREENING_STATUS":"SUBMITTED"}).eq("user_id", user_id).execute()
            student_councellor(user_id)
            screening_result=screener(user_id)
            supabase.table("SCREENING_APPLICANT").update(screening_result).eq("user_id", user_id).execute()
            student_councellor(user_id)
            return "Data Uploaded Sucessfully !!!"

    elif user_state == "REVIEW_OCR_DATA":
        return "hi"