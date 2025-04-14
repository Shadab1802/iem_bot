from agents.admission_query import admission_agent
# from agents.student_loan_agent import student_loan_agent
from crewai import Crew, Task

def query_crew(query: str):
    user_query_answer = Task(
        description=f"""
            Answer the user query: "{query}" related to admission to the college.
            Make sure the information is correct based on the RAG output you get by calling the AdmissionQueryTools with the query.
        """,
        expected_output="A concise and to-the-point answer to the user query.",
        agent=admission_agent,
    )
    
    student_loan_task = Task(
        description=f"""
            Answer this user query: "{query}" regarding education loans.
            Only use information available from the admission brochure.
            If the exact answer is not written, derive it using logic and calculations based on what is mentioned.
            Do NOT invent information. For example, if brochure mentions a loan of up to 85% and fee is mentioned, calculate the amount instead of guessing.
        """,
        expected_output="A factual and logically derived answer based strictly on the brochure.",
        agent=student_loan_agent,
    )

    crew = Crew(
        agents=[admission_agent],
        tasks=[user_query_answer],
        verbose=True
    )

    result = crew.kickoff(inputs={"query": query})
    return result
