from utils.admission_rag_tool import AdmissionRAGTool

rag = AdmissionRAGTool()

def maximum_loan(course: str, stream: str,) -> str:
    """
    Checks if the requested loan amount is allowed and returns the loan breakout.
    """
    total_fees = rag.ask_question(f"What is the total fees for {course} in {stream}?")
    max_percent_loan = rag.ask_question(f"What is the maximum percentage of loan for {course} in {stream}?")
    
    total_fees = int(total_fees.strip().replace(',', '').replace('₹', ''))  # assuming ₹ is in response
    max_percent_loan = float(max_percent_loan.strip('%')) / 100
    max_loan = total_fees * max_percent_loan

    return max_loan