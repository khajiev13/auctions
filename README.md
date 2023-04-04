# Features
1. Users can create an account and login/logout
2. Users can create new auctions with a title, description, and starting bid
3. Users can bid on existing auctions
4. Auctions have a countdown timer and automatically close when the time runs out
5. Users can view their active bids and win auctions



## Installation

To run this application locally, follow these steps:

```bash
git clone https://github.com/khajiev13/auctions.git
cd auctions
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Usage
Once the server is running, open your web browser and navigate to 
``` http://localhost:8000/```. 
You should see the homepage, which displays a list of all active auctions. From there, you can create a new account, login, and start bidding on auctions.


## Contributing

Fork the repository
```
Create a new branch for your changes: 
   git checkout -b my-new-branch
Make your changes and commit them: 
   git commit -am 'Add some feature'
Push your changes to your fork: 
   git push origin my-new-branch
Create a pull request on the original repository
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.
[MIT](https://choosealicense.com/licenses/mit/)
