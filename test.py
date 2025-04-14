from crew.communicator import student_councellor
from crew.screener import screener
from config.supabase_client import supabase
from utils.crew_to_dict import fix_crew_output
# student_councellor("8da7aa28-9346-4214-87a6-ac7d58019de7")
user_id="8da7aa28-9346-4214-87a6-ac7d58019de7"
# screener(user_id)
# student_councellor(user_id)

screening_result=screener(user_id)
data=fix_crew_output(screening_result)
supabase.table("SCREENING_APPLICANT").update(screening_result).eq("user_id", user_id).execute()
student_councellor(user_id)