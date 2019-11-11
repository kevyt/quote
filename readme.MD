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

1. Fork this repo
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
foo@bar:~$ pip install requirements.txt
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


* [app/](./quote/app)
  * [auth/](./quote/app/auth) &larr; authentication blueprints
    * [__init__.py](./quote/app/auth/__init__.py)
    * [forms.py](./quote/app/auth/forms.py)
    * [routes.py](./quote/app/auth/routes.py)
  * [core/](./quote/app/core) &larr; core blueprints
    * [__init__.py](./quote/app/core/__init__.py)
    * [imageprocessing.py](./quote/app/core/imageprocessing.py)  &larr; image processing functions
    * [quoteprocessing.py](./quote/app/core/quoteprocessing.py)  &larr; quotes processing functions
    * [routes.py](./quote/app/core/routes.py)
  * [errors/](./quote/app/errors) &larr; error blueprints
    * [__init__.py](./quote/app/errors/__init__.py)
    * [routes.py](./quote/app/errors/routes.py)
  * [static/](./quote/app/static)
    * [quote.css](./quote/app/static/quote.css)
  * [templates/](./quote/app/templates)
    * [404.html](./quote/app/templates/404.html)
    * [500.html](./quote/app/templates/500.html)
    * [base.html](./quote/app/templates/base.html)
    * [index.html](./quote/app/templates/index.html)
    * [login.html](./quote/app/templates/login.html)
    * [myquotes.html](./quote/app/templates/myquotes.html)
  * [__init__.py](./quote/app/__init__.py)
  * [apicalls.py](./quote/app/apicalls.py)
  * [models.py](./quote/app/models.py)
* [logs/](./quote/logs)
* [migrations/](./quote/migrations)
  * [versions/](./quote/migrations/versions)
    
    * [14de25ec54b9_mended_quotes_table.py](./quote/migrations/versions/14de25ec54b9_mended_quotes_table.py)
    * [a0459fed0538_added_quote_and_author_to_quote_table.py](./quote/migrations/versions/a0459fed0538_added_quote_and_author_to_quote_table.py)
  * [README](./quote/migrations/README)
  * [alembic.ini](./quote/migrations/alembic.ini)
  * [env.py](./quote/migrations/env.py)
  * [script.py.mako](./quote/migrations/script.py.mako)
* [nltk_data/](./quote/nltk_data)
  * [taggers/](./quote/nltk_data/taggers)
  * [tokenizers/](./quote/nltk_data/tokenizers)
    * [punkt/](./quote/nltk_data/tokenizers/punkt)
* [tests/](./quote/tests)
  * [test_unittests.py](./quote/tests/test_unittests.py)
* [.env](./quote/.env) &larr; dotenv file containing api keys
* [.gitignore](./quote/.gitignore)
* [Makefile](./quote/Makefile)
* [app.db](./quote/app.db)
* [config.py](./quote/config.py)
* [quotes.py](./quote/quotes.py)
* [readme.MD](./quote/readme.MD)



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
