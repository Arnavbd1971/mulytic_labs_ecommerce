How To Setup On Linux

Create a Virtual Environment python3 -m venv mulytic_labs_ecommerce
Clone This Project
Activate Virtual Environment source bin/activate
Copy cloned folder mulytic_store and paste it into mulytic_labs_ecommerce folder you just created. 
Go to Project Directory cd mulytic_store
Install Requirements Package python3 -m pip install -r requirements.txt
Migrate Database python3 manage.py migrate
Create Super User python3 manage.py createsuperuser
Admin Username: arnav, Password: abc123
Finally Run The Project python3 manage.py runserver