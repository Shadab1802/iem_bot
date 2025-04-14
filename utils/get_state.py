from config.supabase_client import supabase
def get_user_state(user_id):

    user_state = supabase.table("profiles").select("STATE").eq("user_id", user_id).single().execute().data('STATE')
    return user_state

    