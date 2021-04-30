Working Demo: https://www.youtube.com/watch?v=z4txFiFR6Jo

# Prerequisites

pip install -r requirments.txt

1. Install & Start redis-server OR create an instance on herokuapp.
2. Goto insta_scrapper -> insta_scrapper -> settings.py and modify CELERY_BROKER_URL, CELERY_RESULT_BACKEND.
3. Install npm.
4. Install firefox and geckodriver and add their paths in system path.
5. Change instagram username, password in insta_scrapper -> insta_scrapper -> scrapper_backend -> views.py (Line: 34)

# Get Started

1. Open 3 command prompts.
2. cd insta_scrapper -> python manage.py runserver
3. cd scrapper_frontend -> npm start
4. celery -A insta_scrapper worker -l info
5. Open browser goto 127.0.0.1:3000
6. Input hash-tag without '#'
7. Wait for the task to start and finish
8. creds for django superuser: danialahmed:danial
