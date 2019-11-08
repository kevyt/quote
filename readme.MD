# Quote - image matcher

Flask-based website that matches (random) quotes with matching images (based on NLTK nouns)

### Prerequisites

- Python3.6 : This website depends on features like f-strings that were introducing in Python3.6
- Internet connection, since we are calling API's
- API key of Unsplash (https://unsplash.com/documentation). See Building to incorporate this.

### Building

1. Fork this repo
2. Create a Python (at least 3.6 venv):

```
python3 -m venv venv
```

3. Make sure that you are working in the venv:

```
source venv\bin\activate
```

4. pip install dependencies:

```
pip install requirements.txt
```

5. Make sure that root contains a .env file with:

```
SECRET_KEY = your-custom-secret-key
UNSPLASH_API_KEY = your-unsplash-api-key

```

### Running

In the app folder run:

```
flask run
```

For the first run, make sure that you are connected to the internet, as the NLTK library will download additional dependencies.

Follow instructions on ip:port the website is served

### Project structure

quote/
┣ app/ &larr; main app
┃ ┣ auth/ &larr; authentication blueprints
┃ ┃ ┣ **init**.py
┃ ┃ ┣ forms.py
┃ ┃ ┗ routes.py
┃ ┣ core/ &larr; core-application blueprints
┃ ┃ ┣ **init**.py
┃ ┃ ┗ routes.py
┃ ┣ errors/ &larr; error handling blueprints
┃ ┃ ┣ **init**.py
┃ ┃ ┗ routes.py
┃ ┣ static/ &larr; local css (and js) files
┃ ┃ ┗ quote.css
┃ ┣ templates/ &larr; jinja2 templates referred to by blueprints
┃ ┃ ┣ 404.html
┃ ┃ ┣ 500.html
┃ ┃ ┣ base.html
┃ ┃ ┣ index.html
┃ ┃ ┗ login.html
┃ ┣ **init**.py &larr; application factory
┃ ┗ models.py &larr; sqlalchemy models
┣ logs/ &larr; error logs
┃ ┗ quote.log
┣ migrations/ &larr; database migations (Alembic)
┃ ┣ versions/
┃ ┃ ┗ ac44a84db6d1_users_table.py
┃ ┣ README
┃ ┣ alembic.ini
┃ ┣ env.py
┃ ┗ script.py.mako
┣ nltk_data/ &larr; NLTK data (after initial run)
┃ ┣ taggers/
┃ ┗ tokenizers/
┣ tests/ &larr; (unit tests)
┃ ┗ test_unittests.py
┣ .gitignore
┣ app.db
┣ config.py &larr; Config of application
┗ quotes.py

Globally the website is structured using an application factory with three blueprints:

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
