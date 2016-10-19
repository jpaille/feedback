What are memory feedback ?
--------------------------

A memory feedback is a short session in which we recall previously acquired knowledge.
This helps retaining the information in our long term memory.
(See the forgetting curve  https://en.wikipedia.org/wiki/Forgetting_curve


How to use the feedback application.
------------------------------------

1. Make some review cards on one subject you want to learn.
2. Enter this subject through the feedback admin page.
3. The feedback application will then schedule for you review sessions.
4. Review the subject and validate it through the admin page or Google calendar.

If you follow that method you will never forget that subject.


Installation
------------

    cd feedback
	pip install -r requirements.txt
	./manage.py migrate --run-syncdb

Set the weekly feedback scheduler.

	crontab -e

Enter this line at the end of the cron file and replace `/PATH/TO/FEEDBACK_DIRECTORY` by the full
path of the `feedback` directory.

	43 23 * * 7 cd /PATH/TO/FEEDBACK_DIRECTORY && /usr/bin/python manage.py update_feedbacks
	

Access the admin site
---------------------

1. Create admin credentials

	```
	./manage.py createsuperuser
	```
	
2. Start the web server

    ```
	./manage.py runserver 0:8000
	```
	
3. Go to the admin page through your favorite browser and search for:
	
	http://127.0.0.1:8000/admin


Use Google Calendar
-------------------

1. Set `USE_GOOGLE_CALENDAR = True` in feedback/feedback/settings.py

2. Create a file named `oauth_credentials.json` in the feedback root directory.

3.	Add the following json blob in `oauth_credentials.json`, and replace the XXX by your own credentials.

	```
	{
	"access_token" : "XXX",
	"client_id" : "XXX",
	"client_secret" : "XXX",
	"refresh_token" : "XXX",
	"token_expiry" : 3600,
	"token_uri" : "https://www.googleapis.com/oauth2/v4/token",
	"user_agent" : "Feedback application"
	}
	```
	
Receive weekly email updates.
-----------------------------

1. Set `USE_MAIL_REPORT_NOTIFICATION = True` in feedback/feedback/settings.py

2. Replace the following settings by your own credentials in feedback/feedback/settings.py

	```
	EMAIL_HOST = ''

	EMAIL_HOST_USER = ''
	
	EMAIL_HOST_PASSWORD = ''
	```
	
3. You will then receive an email each week with:
	
	* A list of validated or failed feedback sessions.
	* A state of your memory per subject with a progress bar.
	* A list of next week feedback sessions.
	
![alt tag](https://raw.githubusercontent.com/jpaille/feedback/master/static/img/email_report_example.png)
	





	
