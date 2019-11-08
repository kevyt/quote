# standard imports
from datetime import datetime

# flask imports
from flask import render_template, url_for

# from flask_wtf import Form
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

from app.models import User


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


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
            "quote": quote,
            "author": author,
            "image_colour_r": r,
            "image_colour_g": g,
            "image_colour_b": b,
            "font_colour": font_colour,
        }

    return render_template("index.html", title="Home", payload=payload)


# @bp.route("/user/<username>")
# @login_required
# def user(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     return render_template("user.html", user=user)
