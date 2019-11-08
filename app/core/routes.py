# standard imports
from datetime import datetime
import string
from collections import Counter
import random
import re

# flask imports
from flask import render_template, current_app, url_for

# from flask_wtf import Form
from flask_login import current_user, login_required

import nltk
import requests

from app.core import bp
from app import db
from app.models import User


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


def get_api_data(url, headers={}):
    response = requests.get(url, headers=headers,)
    if response.status_code == 200:
        return response
    else:
        return None


def get_image_from_unsplash_api(endpoint):
    return get_api_data(
        f"https://api.unsplash.com/{endpoint}",
        {"Authorization": f"Client-ID {current_app.config['UNSPLASH_API_KEY']}"},
    )


def search_image_from_unsplash(noun):
    """
    Tries to fetch image with noun as keyword from unsplash

    Args:
       noun (str): noun

    Returns:
        results from response if succesful, or None if unsuccesful
    """
    response = get_image_from_unsplash_api(f"/search/photos?query={noun}")
    if response == None or response.json()["total"] == 0:
        return None
    return response.json()["results"]


def get_random_quote_from_quotable():
    """
    Returns random quote from quoateable api

    Returns:
        tuple with quote, author and id
    """
    response = get_api_data("https://api.quotable.io/random")
    return response.json()["content"], response.json()["author"], response.json()["_id"]


def get_quote_by_id(id):
    """
    Returns a quote from quotable based on known id

    Args:
       id (str): id of quotable quote
    
    Returns:
        tuple with quote, author and id
    """
    response = get_api_data(f"https://api.quotable.io/quotes/{id}")
    return response.json()["content"], response.json()["author"], response.json()["_id"]


def get_nouns_from_quote(quote):
    """
    To select the right image for the quote, we need to get the most
    frequent nouns of that quote

    Args:
        quote (str): quote (English language) to be processed

    Procedure:
        1) ensure that quote is lowercased and that punctuation is removed
        2) tag words with NLTK
        3) get nouns (tags starting with NN)
        4) return them; 
            --> if no nouns were found, return "wisdom" to get generic image
    
    Raises:
        TypeError: type quote not string
        ValueError: string of length 0

    Returns:
        Counter object with counts of nouns (NN, NNS, NNP, NNPS)
        
        for meaning of NLTK tags see: 
        https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
    """
    if type(quote) != str:
        raise TypeError("Quote must be of type str")

    if len(quote) == 0:
        raise ValueError("Quote must be at least of length 1")

    quote = quote.lower()

    parts_of_sentence = nltk.pos_tag(quote.split(" "))
    nouns = [word for word, tag in parts_of_sentence if tag[:2] == "NN"]

    if nouns:
        noun_counts = Counter(nouns)

    else:
        noun_counts = Counter(["wisdom"])

    sorted_noun_counts = [
        (noun, frequency)
        for noun, frequency in sorted(
            noun_counts.items(), key=lambda wf: (-wf[1], wf[0])
        )
    ]

    return sorted_noun_counts


def transform_hex_to_rgb(colour):
    """
    Convert hex input to seperate RGB colour channels (int)

    Args:
        colour (str): hex colour to be processed
    
    Raises:
        TypeError if input is non-string
        ValueError if colour does not match pattern ^#((0x){0,1}|#{0,1})([0-9A-F]{8}|[0-9A-F]{6})$
    
    Returns:
        Tuple with RGB values (int, int ,int)

    """
    if type(colour) != str:
        raise TypeError("Colour must be a string value")

    pattern = re.compile(r"^#((0x){0,1}|#{0,1})([0-9A-F]{8}|[0-9A-F]{6})$")
    if not pattern.match(colour):
        raise ValueError("Colour should be valid colour-hexcode with leading #")

    colour = colour.lstrip("#")
    RGB = tuple(int(colour[i : i + 2], 16) for i in (0, 2, 4))
    return RGB


def get_perceived_brightness(colour):
    """
    Provide brightness of (background colour), to get a constrasting
    font colour.

    Args:
        colour (str): hex colour to be processed

    Procedure:
        1) convert hex colour to ints
        2) apply formula to get perceived brightness [1]
        
    Returns:
        Perceived brightness from 0 (dark) to 255 (bright)
    
    Source: [1] https://en.wikipedia.org/wiki/Relative_luminance

    """
    red, green, blue = transform_hex_to_rgb(colour)

    brightness = 0.2126 * red + 0.7152 * green + 0.0722 * blue
    return brightness


def get_matching_image(nouns):
    """
    Select random image, based on most frequent nouns

    Args:
        nouns (list): sorted list of tuples (noun, frequency)

    Procedure:
        1) loop through list
            2) check whether there is an image
                - if so; break out of loop and return
                - if not try next
            3) if image is returned, return that url.
                - If not, return standard image url
    Raises:
        TypeError: type nouns is not list
        ValueError: first element of list is not a tuple

    Returns:
        Tuple with:
            - URL to image (str)
            - Dominant image colour (str)
            - Image id
    """
    if type(nouns) != list:
        raise TypeError("Nouns must be list of tuples")
    if type(nouns[0]) != tuple:
        raise ValueError("List must contain tuples (noun, frequency)")
    image_url = None
    for noun, freq in nouns:
        images = search_image_from_unsplash(noun)
        if images:
            random_index = random.randrange(len(images))
            image = images[random_index]
            image_url = image["urls"]["regular"]
            image_colour = image["color"]
            image_id = image["id"]
            break

    if image_url:
        return image_url, image_colour, image_id
    return current_app.config["STANDARD_IMAGE"]


def get_image_by_id(id):
    """
    Select image based on id
    
    Args:
        id (str): image id

    Procedure:
        1) call unsplash api /photos/:id endpoint
        2) extract url, color and id from response

    Returns:
        Tuple with:
            - URL to image (str)
            - Dominant image colour (str)
            - Image id
        If no image is returned, will return standard image
    """

    image = get_image_from_unsplash_api(f"/photos/{id}")
    if image:
        image = image.json()
        image_url = image["urls"]["regular"]
        image_colour = image["color"]
        image_id = image["id"]
        return image_url, image_colour, image_id
    return current_app.config["STANDARD_IMAGE"]


@bp.route("/")
@bp.route("/<quote_id>/<image_id>")
def index(quote_id=None, image_id=None):
    """
    Landing page and main endpoint of Quote website
    
    Depending on provision of quote_id and image_id this either
        - loads the quote with image (used for social media links)
        - or provisions a random quote with matching image
    
    This routes outputs data to the view in payload:
        image - the image url of the image
        quote - quote text
        author - author of the quote
        dominant image colour, split out in RGB channels:
            image_colour_r - red
            image_colour_g - green
            image_colour_b - blue
        font_colour - font colour (black or white) based on brightness of dominant image colour

    """
    if current_user.is_authenticated:
        payload = "Je bent authenticated"
    else:
        payload = dict()
        if quote_id and image_id:
            payload["image"], image_colour, image_id = get_image_by_id(image_id)
            payload["quote"], payload["author"], quote_id = get_quote_by_id(quote_id)
        else:
            (
                payload["quote"],
                payload["author"],
                quote_id,
            ) = get_random_quote_from_quotable()
            nouns = get_nouns_from_quote(payload["quote"])
            (payload["image"], image_colour, image_id,) = get_matching_image(nouns)

        (
            payload["image_colour_r"],
            payload["image_colour_g"],
            payload["image_colour_b"],
        ) = transform_hex_to_rgb(image_colour)

        if get_perceived_brightness(image_colour) < 125:
            payload["font_colour"] = "#FFFFFF"
        else:
            payload["font_colour"] = "#000000"

        payload["url"] = url_for(
            "core.index", quote_id=quote_id, image_id=image_id, _external=True,
        )
    return render_template("index.html", title="Home", payload=payload)


# @bp.route("/user/<username>")
# @login_required
# def user(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     return render_template("user.html", user=user)
