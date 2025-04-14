from crew_cust_tools.email_sender import EmailSenderTool
from utils.data_injecter import inject_data_to_docx  # Should return BytesIO
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

def main():
    # List of student records
    students = [
        {
            "NAME": "John Doe",
            "MOBILE_NO": "+1234567890",
            "EMAIL": "john@example.com",
            "AADHAR_NO": "1234-5678-9012",
            "TOTAL_FEES": "10000",
            "REMAINING_AMOUNT": "10000",
            "PER_SEMESTER_FEES": "5000",
            "BUS_FARE": "1000",
            "HOSTEL_CHARGE": "2000",
            "EXAM_FEES": "500",
            "LATE_FINE": "200",
            "FEES_DUE_DATE": "2023-12-31"
        },
        {
            "NAME": "Alice Smith",
            "MOBILE_NO": "+1987654321",
            "EMAIL": "alice@example.com",
            "AADHAR_NO": "5678-1234-9012",
            "TOTAL_FEES": "12000",
            "REMAINING_AMOUNT": "8000",
            "PER_SEMESTER_FEES": "4000",
            "BUS_FARE": "1200",
            "HOSTEL_CHARGE": "2500",
            "EXAM_FEES": "600",
            "LATE_FINE": "100",
            "FEES_DUE_DATE": "2023-12-31"
        }
    ]

    # Step 1: Generate all attachments
    attachments = []
    for student in students:
        buffer: BytesIO = inject_data_to_docx(student)
        file_name = f"invoice_{student['NAME'].replace(' ', '_').lower()}.docx"
        attachments.append((buffer, file_name))
        print(f"Prepared invoice for {student['NAME']}")

    # Step 2: Send them in one email
    tool = EmailSenderTool()
    result = tool._run(
        subject="Student Fee Invoices",
        body="Dear Admin,\n\nPlease find attached the fee invoices for multiple students.\n\nRegards,\nSystem",
        to="mohammad.shadab.6632@gmail.com",
        attachment_streams=attachments
    )

    print(result)

if __name__ == "__main__":
    main()