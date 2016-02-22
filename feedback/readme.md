What are memory feedbacks ?
---------------------------

A memory feedback is a short session in which we recall previously acquired knowledge.
This helps retaining the information in our long term memory.
(See the forgetting curve  https://en.wikipedia.org/wiki/Forgetting_curve


This application is used to schedule weekly feedbacks sessions into google calendar.

INSTALLATION
------------

pip install -r feedbacks/requirements.txt
./manage.py runserver 0:8000

Add an "oauth_credentials.json" in the project root directory.

Copy this json blob and replace XXX by your oauth credentials.

{"access_token" : "XXXX",
 "client_id" : "XXX",
 "client_secret" : "XXXX",
 "refresh_token" : "XXX",
 "token_expiry" : 3600,
 "token_uri" : "https://www.googleapis.com/oauth2/v4/token",
 "user_agent" : "Feedbacks application"
}

In browser access the admin site to create new subjects.

http://127.0.0.1:8000/admin

Then to schedule feedbacks use the django command:

./manage.py update_feedbacks 

This can be  done manually once a week or automatized using cron for example.






