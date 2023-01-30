# activities.py

# Verbs
# need to track from post matrimony profile creation on user signup
USER_SIGNEDUP = "signed up"
# Need to track from profile_edit view
USER_REGISTERED = "completed registration"

# The actor for the activities below will be usually a staff user. When the actor is a staff user,
# we will not display the actor user
# Need to track admin actions from MatrimonyProfileAdmin methods
USER_REQUEST_MORE_INFO = "You need to provide more info for your profile"
USER_BLOCKED = "Your profile got blocked"
USER_DEACTIVATED = "Your profile got deactivated"
USER_ACTIVATED = "Your profile got activated"
USER_MATCH_SEARCH_IN_PROGRESS = "We are searching for a match for you"
USER_MATCHED = "You have a match"
USER_COMPLETED_QUESTIONNAIRE = "completed marriage questionnaire"
USER_STARTED_MARRIAGE_DISCUSSION = "You can now start discussion with your active match"
USER_MARRIED_EXTERNALLY = "You got married outside our system"
USER_MARRIED = "You got married"

# Need to track from match related views
MATCH_REQUEST_SENT = "sent a match request to"
MATCH_REQUEST_ACCEPTED = "accepted the match request from"
MATCH_REQUEST_REJECTED = "rejected the match request from"
# Need to track from Match admin save method
MATCH_SUGGESTED = "You have received a few match suggestions"