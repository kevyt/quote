import requests

from flask import current_app


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


def get_quote(endpoint="random"):
    """
    Returns quote from quoateable api

    Returns:
        tuple with quote, author and id
    """
    response = get_api_data(f"https://api.quotable.io/{endpoint}")
    return response.json()["content"], response.json()["author"], response.json()["_id"]
