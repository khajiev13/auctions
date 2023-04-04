# auctions
This is a project that I made while I was taking cs50 web programming course. I had so much fun building it with django and bootstrap 5.

Auctions
Auctions is a web application that allows users to create and bid on auctions. This application was built using Python and the Django framework.


Features
 Users can create an account and login/logout
 Users can create new auctions with a title, description, and starting bid
 Users can bid on existing auctions
 Auctions have a countdown timer and automatically close when the time runs out
 Users can view their active bids and won auctions
 
Installation
 To run this application locally, follow these steps:
  Clone the repository: git clone https://github.com/khajiev13/auctions.git
  Navigate to the project directory: cd auctions
  Install the required dependencies: pip install -r requirements.txt
  Create a database: python manage.py migrate
  Start the development server: python manage.py runserver
Usage
 Once the server is running, open your web browser and navigate to http://localhost:8000/. You should see the homepage, which displays a list of all active auctions. From there, you can create a new account, login, and start bidding on auctions.

Contributing
 If you'd like to contribute to this project, please follow these steps:
  Fork the repository
  Create a new branch for your changes: git checkout -b my-new-branch
  Make your changes and commit them: git commit -am 'Add some feature'
  Push your changes to your fork: git push origin my-new-branch
  Create a pull request on the original repository
License
 This project is licensed under the MIT License. See the LICENSE file for details.
