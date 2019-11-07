import unittest
from unittest.mock import patch

from nose2.tools import params

from app import create_app
from app.core.routes import (
    get_nouns_from_quote,
    get_matching_image,
    transform_hex_to_rgb,
    get_perceived_brightness,
    get_image_by_id
)

"""
For some patching we need to setup and application context
"""
app = create_app()
app.app_context().push()


class TestNounParser(unittest.TestCase):
    """Tests noun parser"""

    def test_nouns_from_string(self):
        """Quote is parsed correctly."""
        input = "This is a quote"
        result = get_nouns_from_quote(input)
        expected = [("quote", 1)]
        self.assertEqual(result, expected)

    def test_multiple_nouns(self):
        """With multiple nouns, multiple times, should return a count"""
        input = "The tree and the car and the other car collided"
        result = get_nouns_from_quote(input)
        expected = [("car", 2), ("tree", 1)]
        self.assertEqual(result, expected)

    def test_no_nouns(self):
        """If no nouns, should return generic wisdom ."""
        input = "The is open, and are."
        result = get_nouns_from_quote(input)
        expected = [("wisdom", 1)]
        self.assertEqual(result, expected)

    @params(0, None, ["list", "of", "words"], {"test": "dict"})
    def test_nouns_input_other_than_string(self, input):
        """TypeError raised if input not string"""
        with self.assertRaises(TypeError) as error:
            get_nouns_from_quote(input)
        self.assertTrue("Quote must be of type str" in error.exception.args)

    def test_nouns_input_empty_string(self):
        """TypeError raised if input not string"""
        with self.assertRaises(ValueError) as error:
            get_nouns_from_quote("")
        self.assertTrue("Quote must be at least of length 1" in error.exception.args)


class TestImageSelecter(unittest.TestCase):
    """Tests image selecter"""

    @patch("app.core.routes.search_image_from_unsplash", return_value=None)
    def test_no_image(self, patched_function):
        result = get_matching_image([("test", 0)])
        expected = app.config["STANDARD_IMAGE"]
        self.assertEqual(result, expected)

    @patch(
        "app.core.routes.search_image_from_unsplash",
        return_value=[
            {
                "image": "testimage",
                "color": "black",
                "id": "my_id",
                "urls": {"regular": "regular_url", "full": "full_url"},
            }
        ],
    )
    def test_one_image(self, patched_function):
        result = get_matching_image([("test", 0)])
        expected = ("regular_url", "black", "my_id")
        self.assertEqual(result, expected)

    @params(0, None, {"test": "dict"}, "b")
    def test_imageselecter_input_other_than_string(self, input):
        """TypeError raised if input not liust"""
        with self.assertRaises(TypeError) as error:
            get_matching_image(input)
        self.assertTrue("Nouns must be list of tuples" in error.exception.args)

    @params([0], [None, "bla"], ["list", "of", "words"], [{"test": "dict"}])
    def test_imageselecter_input_no_tuples(self, input):
        """TypeError raised if input not string"""
        with self.assertRaises(ValueError) as error:
            get_matching_image(input)
        self.assertTrue(
            "List must contain tuples (noun, frequency)" in error.exception.args
        )

class TestImageById(unittest.TestCase):
    """Tests image by id selecter"""

    class MockResponse:
        """Small helper class to mock response data"""
        def __init__(self, json_data):
            self.json_data = json_data

        def json(self):
            return self.json_data

    @patch("app.core.routes.get_image_from_unsplash_api", return_value=None)
    def test_no_image(self, patched_function):
        result = get_image_by_id('fake')
        expected = app.config["STANDARD_IMAGE"]
        self.assertEqual(result, expected)

    @patch(
        "app.core.routes.get_image_from_unsplash_api",
        return_value=MockResponse(
            {
                "image": "testimage",
                "color": "black",
                "id": "my_id",
                "urls": {"regular": "regular_url", "full": "full_url"},
            }
        )
    )
    def test_one_image(self, patched_function):
        result = get_image_by_id('fake')
        expected = ("regular_url", "black", "my_id")
        self.assertEqual(result, expected)
    
class TestHexToRGB(unittest.TestCase):
    """Tests Hex to RGB converter"""

    def test_hex_to_rgb_happy1(self):
        """Colour white is parsed correctly."""
        input = "#FFFFFF"
        result = transform_hex_to_rgb(input)
        expected = (255, 255, 255)
        self.assertEqual(result, expected)

    def test_hex_to_rgb_happy2(self):
        """Colour black is parsed correctly."""
        input = "#000000"
        result = transform_hex_to_rgb(input)
        expected = (0, 0, 0)
        self.assertEqual(result, expected)

    @params(0, ["#FFFFFF"])
    def test_hex_to_rgb_unhappy1(self, input):
        """Colour is parsed correctly."""
        with self.assertRaises(TypeError) as error:
            transform_hex_to_rgb(input)
        self.assertTrue("Colour must be a string value" in error.exception.args)

    @params("FFFFFF", "#FFF", "#GFGF01", "#FFFFFG")
    def test_imageselecter_input_no_tuples(self, input):
        """TypeError raised if input not string"""
        with self.assertRaises(ValueError) as error:
            transform_hex_to_rgb(input)
        self.assertTrue(
            "Colour should be valid colour-hexcode with leading #"
            in error.exception.args
        )


class TestPerceivedBrighness(unittest.TestCase):
    """Tests perceived brightness calculator"""

    def test_brighness_happy1(self):
        """Colour white is parsed correctly."""
        input = "#000000"
        result = get_perceived_brightness(input)
        expected = 0
        self.assertEqual(result, expected)
