import os

from dotenv import load_dotenv
import nltk

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    NLTK_DATA_DIR = os.path.join(basedir, "nltk_data")
    if not os.path.exists(NLTK_DATA_DIR):
        os.makedirs(NLTK_DATA_DIR)
        # Download packages and store in directory above
        nltk.download("punkt", download_dir=NLTK_DATA_DIR)
        nltk.download("averaged_perceptron_tagger", download_dir=NLTK_DATA_DIR)
    nltk.data.path.append(NLTK_DATA_DIR)
    
    SECRET_KEY = os.environ.get("SECRET_KEY") or "this-is-ricks-secret"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UNSPLASH_API_KEY = os.environ.get("UNSPLASH_API_KEY")

    STANDARD_IMAGE = (
        "https://images.unsplash.com/photo-1549619856-ac562a3ed1a3?ixlib=rb-1.2.1&q=80&fm=jpg&crop=entropy&cs=tinysrgb&w=1080&fit=max&ixid=eyJhcHBfaWQiOjk4NzE0fQ",
        "#DEE1E5",
        "lNeIjS1rXus",
    )
