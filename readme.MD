# Quote - image matcher

Flask-based website that matches (random) quotes with matching images (based on NLTK nouns)

User stories incorporated:
- [x] Fetch quotes from an external service 
- [x] Share ‘quotes’ on social media, like Facebook or Twitter
- [x] Create a mobile friendly application, keeping different devices in mind
- [ ] Allow users to rate quotes and view other people their ratings
- [ ] Tweak the random quote logic to prioritize showing highly rated quotes to new users
- [ ] Find quotes comparable to the currently shown quote
- [ ] Create a slideshow of random quotes being shown

Plus:
- [x] Match image with quote, based on nouns (NLTK)
- [x] Allow users to register and login
- [x] Allow users to store quote-image combination
- [x] Allow users to retrieve stored/bookmarked quote-image combinations

### Prerequisites

- Python3.6 : This website depends on features like f-strings that were introducing in Python3.6
- Internet connection, since we are calling API's
- API key of Unsplash (https://unsplash.com/documentation). See Building to incorporate this.

### Building

1. Clone this repo
2. Create a Python (at least 3.6) venv:

```
foo@bar:~$ python3 -m venv venv
```

3. Make sure that root contains a .env file with:

```
SECRET_KEY = your-custom-secret-key
UNSPLASH_API_KEY = your-unsplash-api-key

```

4. Either run Makefile, or adjust to local settings to install dependencies and initialise db:

```
foo@bar:~$ make build

OR manually:
foo@bar:~$ source venv\bin\activate
foo@bar:~$ pip install -r requirements.txt
foo@bar:~$ flask db upgrade
```

### Running

In the app folder run:

```
foo@bar:~$ flask run
```
Make sure that your venv is activated.

For the first run, make sure that you are connected to the internet, as the NLTK library will download additional dependencies.

Follow instructions on ip:port the website is served

### Project structure


* [app/]()
  * [auth/]() &larr; authentication blueprints
    * [__init__.py]()
    * [forms.py]()
    * [routes.py]()
  * [core/]() &larr; core blueprints
    * [__init__.py]()
    * [imageprocessing.py]()  &larr; image processing functions
    * [quoteprocessing.py]()  &larr; quotes processing functions
    * [routes.py]()
  * [errors/]() &larr; error blueprints
    * [__init__.py]()
    * [routes.py]()
  * [static/]()
    * [quote.css]()
  * [templates/]()
    * [404.html]()
    * [500.html]()
    * [base.html]()
    * [index.html]()
    * [login.html]()
    * [myquotes.html]()
  * [__init__.py]()
  * [apicalls.py]()
  * [models.py]()
* [logs/]()
* [migrations/]()
  * [versions/]()
    * [14de25ec54b9_mended_quotes_table.py]()
    * [a0459fed0538_added_quote_and_author_to_quote_table.py]()
  * [README]()
  * [alembic.ini]()
  * [env.py]()
  * [script.py.mako]()
* [nltk_data/]()
  * [taggers/]()
  * [tokenizers/]()
    * [punkt/]()
* [tests/]()
  * [test_unittests.py]()
* [.env]() &larr; dotenv file containing api keys
* [.gitignore]()
* [Makefile]()
* [app.db]()
* [config.py]()
* [quotes.py]()
* [readme.MD]()



Globally, the website is structured using an application factory with three blueprints:

1. auth, dealing with authentication
2. core, dealing with core application tasks (matching quotes with images)
3. errors, dealing with error handling

## Running the tests

In root run:

```
nose2 -v
```

to get verbose unit test results

## Authors

- **Rick Prins**
