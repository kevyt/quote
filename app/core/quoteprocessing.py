from collections import Counter
import nltk


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
