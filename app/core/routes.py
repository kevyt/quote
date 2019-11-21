from datetime import datetime

from flask import render_template, url_for, redirect, request, jsonify

from flask_login import current_user, login_required

from app.core import bp
from app import db

from app.apicalls import get_quote
from app.core.imageprocessing import (
    get_image_by_id,
    get_matching_image,
    transform_hex_to_rgb,
    get_font_colour,
)
from app.core.quoteprocessing import get_nouns_from_quote

from app.models import User, Quote


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route("/_get_quote")
def _get_quote():
    """
    

    """
    print("hit")
    quote, author, quote_id = get_quote()
    nouns = get_nouns_from_quote(quote)
    image, image_colour, image_id = get_matching_image(nouns)

    r, g, b = transform_hex_to_rgb(image_colour)
    font_colour = get_font_colour(image_colour)

    response = {
        "url": url_for(
            "core.index", quote_id=quote_id, image_id=image_id, _external=True,
        ),
        "image": image,
        "image_id": image_id,
        "quote_id": quote_id,
        "quote": quote,
        "author": author,
        "image_colour_r": r,
        "image_colour_g": g,
        "image_colour_b": b,
        "font_colour": font_colour,
    }

    return jsonify(response)



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
    if quote_id and image_id:
        quote, author, quote_id = get_quote(f"quotes/{quote_id}")
        image, image_colour, image_id = get_image_by_id(image_id)
    else:
        quote, author, quote_id = get_quote()
        nouns = get_nouns_from_quote(quote)
        image, image_colour, image_id = get_matching_image(nouns)

    r, g, b = transform_hex_to_rgb(image_colour)
    font_colour = get_font_colour(image_colour)

    payload = {
        "url": url_for(
            "core.index", quote_id=quote_id, image_id=image_id, _external=True,
        ),
        "image": image,
        "image_id": image_id,
        "quote_id": quote_id,
        "quote": quote,
        "author": author,
        "image_colour_r": r,
        "image_colour_g": g,
        "image_colour_b": b,
        "font_colour": font_colour,
    }

    return render_template("index.html", image_view=True, payload=payload)


@login_required
@bp.route("/myquotes")
def myquotes():
    """
    The quote-drawer, gives a plain overview of saved quotes.

    Authentication needed
    """
    payload = dict()
    payload["quotes"] = Quote.query.filter_by(user=current_user)
    return render_template("myquotes.html", payload=payload)


def is_valid_request(request_args, keys):
    """
    Helper function to check valid request

    args:
        request_args (e.g. request.form, request.args, request.args_list)
        keys: list of keys

    raises:
        TypeError, if keys is not list

    returns: bool whether request has keys
    """
    if type(keys) != list:
        raise TypeError("Keys must be of type list")

    for key in keys:
        if key not in request_args:
            return False
    return True


@login_required
@bp.route("/save", methods=["POST"])
def save_quote():
    """
    Endpoint to save quote; called by js-function.

    Args:
        quote_id (str): id of quote
        image_id (str): id of image
        quote (str): quote (English language) to be processed
        author (str): author name

    Returns succes or failure

    For now, a manual check on constraints (check uniqueness), because
    SQLlite does not support these constrains.

    Authentication needed
    """
    if not is_valid_request(request.form, ["quote_id", "image_id", "quote", "author"]):
        return jsonify({"error": "Could not save quote, due to technical reasons"})
    quote_id = request.form["quote_id"]
    image_id = request.form["image_id"]
    quote = request.form["quote"]
    author = request.form["author"]

    check_uniqueness = (
        Quote.query.filter_by(user=current_user)
        .filter_by(quote_id=quote_id)
        .filter_by(image_id=image_id)
        .count()
    )

    if check_uniqueness == 0:
        quote = Quote(
            quote_id=quote_id,
            image_id=image_id,
            quote=quote,
            author=author,
            user=current_user,
        )
        db.session.add(quote)
        db.session.commit()
        return jsonify({"succes": "Quote saved"})
    else:
        return jsonify({"error": "Quote already saved"})
