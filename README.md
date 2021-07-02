# Mulytic labs Ecommerce
This is a very simple e-commerce website built with Django.

## Project Summary
This is a very simple Django e-commerce project, where we have Product Management, Order Management for a guest user or an authentic login user, Cart System, Checkout system, and at last generate order invoice with QRcode witch contains customer information and cart details. 

## Snapshots from the project
![LCO Mascot](http://ec2-54-237-160-80.compute-1.amazonaws.com/profilepic/11.png "LCO")
![LCO Mascot](http://ec2-54-237-160-80.compute-1.amazonaws.com/profilepic/22.png "LCO")
![LCO Mascot](http://ec2-54-237-160-80.compute-1.amazonaws.com/profilepic/33.png "LCO")
![LCO Mascot](http://ec2-54-237-160-80.compute-1.amazonaws.com/profilepic/55.png "LCO")
![LCO Mascot](http://ec2-54-237-160-80.compute-1.amazonaws.com/profilepic/66.png "LCO")

# How To Setup On Linux

Create a Virtual Environment `python3 -m venv mulytic_labs_ecommerce`

Activate Virtual Environment `source bin/activate`

Download this project.

Copy downloades folder mulytic_store and paste it into mulytic_labs_ecommerce folder you just created. 

Go to Project Directory `cd mulytic_store`

Install Requirements Package `python3 -m pip install -r requirements.txt`

Migrate Database `python3 manage.py migrate`

Create Super User `python3 manage.py createsuperuser`

Existing Admin Username: arnav, Password: abc123

Finally Run The Project `python3 manage.py runserver`



