import re
import random

from flask import current_app

from app.apicalls import get_image_from_unsplash_api, search_image_from_unsplash


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


def get_font_colour(image_colour):

    if get_perceived_brightness(image_colour) < 125:
        font_colour = "#FFFFFF"
    else:
        font_colour = "#000000"

    return font_colour


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

