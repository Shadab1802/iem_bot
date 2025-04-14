import ast
import re

def fix_crew_output(output) -> dict:
    try:
        # Extract from CrewOutput.content if available
        if hasattr(output, "content"):
            output = output.content
        elif not isinstance(output, str):
            output = str(output)

        # Remove leading/trailing whitespace
        output = output.strip()

        # Fix: remove multiple commas or commas at the beginning
        output = re.sub(r",\s*,", ",", output)  # replace double commas
        output = re.sub(r"^{,\s*", "{", output)  # opening with comma
        output = re.sub(r",\s*}", "}", output)  # trailing comma before }

        # Optionally: add missing quotes around unquoted values (if needed)
        output = re.sub(r":\s*([a-zA-Z0-9_]+)(?=[,\}])", r": '\1'", output)

        # Safely evaluate
        return ast.literal_eval(output)
    except Exception as e:
        print("Failed to parse Crew output:", e)
        print("Raw string was:", output)
        return {}
