from data_types import *
from helper import THRESHOLD


def bundle_mail(letters):
    """ Given a collection of letters, return a list (or other iterable) of
    Bundles such that:

    - Every Letter is placed in exactly one Bundle
    - The destination of the Bundle matches the address of the Letter
    """
    # initialize the list
    res_list = [Bundle(RETURN_TO_SENDER)]
    for letter in letters:
        found = False
        maxrating = (-1, 0)
        # if letter is unclear return to sender
        if not letter.address.plausible:
            res_list[0].add_letter(letter)
            continue
        # check rating on every bundle except return to sender
        for i, bundle in enumerate(res_list[1:],1):
            rating = bundle.rate_similarity(letter)
            maxrating = (i, rating) if rating > maxrating[1] else maxrating
        
        if maxrating[1] >= THRESHOLD:
            # over threshold: add to existing bundle
            bundle = res_list[maxrating[0]]
        else:
            # below threshold: create new bundle and add
            bundle = Bundle(letter.address)
            res_list.append(bundle)
        bundle.add_letter(letter)
    return res_list
