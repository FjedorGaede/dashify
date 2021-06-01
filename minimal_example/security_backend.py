""" 
This mimics a fully functional security backend. In this case it is a simple version returning true if a user is in a certain usergroup
"""

# Returns the "current" user 
def get_current_user():
    return "Alex"

# Checks if the "current" user is in a certain list of user names.
def security_method(allowed_users):
    if get_current_user() in allowed_users:
        return True 
    else:
        return False
