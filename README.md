# Email-Spam-Detection-Game
Website created in django meant to create a prototype of a game that helps users distinguish between suspicious emails that may have passed your spam filters, and simple emails that you may find in your everday inbox. Instructions on how to run the server on your local machine are listed below:

```bash
python -m venv venv 
.\venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Of course, if your using the database and session token we have most generously provided, you will not need to migrate the objects onto the database. 

Once you have done these steps, navigate to 127.0.0.1:8000 to arrive on the landing page of the website!
