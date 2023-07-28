# BidOut 

Commerce is an auction ecommerce website similar to Ebay where users can list items and put them up for auction and whoever has the highest bid for that particular auctions wins the item

## **Technologies used**

* Python
* Django
* HTML
* CSS
* Javascript
* SQlite3

## Users are able to:

1. Create account
2. Create a listing
3. Start an auction
4. Bid on a particular auction
5. Add items to their watchlist
6. Close an auction
7. Check active listings
8. Make comments on an auction
9. Win auctions

## Getting Started
To run this project on your machine. Make sure you have python3 installed on your machine.

1. Install Django by running the following command in your terminal


`pip install django`


2. Clone the project by using the command below in your terminal

`git clone https://github.com/LoneStarrD/BidOut`

3. Change directory into the cloned repository

`cd commerce`

4. Create and Activate Virtual Environment: 

`python -m venv env`

* On Windows, activate the virtual environment:

`env\Scripts\activate`

* On macOS and Linux, activate the virtual environment:

`source env/bin/activate`

5. Install Dependencies:

`pip install -r requirements.txt`

6. Run Database Migrations:

`python manage.py migrate`

7. Create Superuser Account:

`python manage.py createsuperuser`

8. Start the Development Server:

`python manage.py runserver`

Use the superuser account credentials to log in to the admin interface at http://localhost:8000/admin/ and manage the platform content.

## Preview

![](/bidout2.png)


![](/bidout1.png)