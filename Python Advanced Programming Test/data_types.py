from helper import *

help = Helper()

class Address(object):
    def __init__(self, line1, line2, line3):
        self.line1 = line1
        self.line2 = line2
        self.line3 = line3
        self.normalize_lines()
        self.abbreviate_lines()
        self.plausible = self.is_plausible()

    def __str__(self):
        """ DO NOT EDIT: This method is required by the test runner. """
        return '\t'.join((self.line1, self.line2, self.line3))

    def __eq__(self, other):
        """ DO NOT EDIT: This method is required by the test runner. """
        return (self.line1 == other.line1
                and self.line2 == other.line2
                and self.line3 == other.line3)

    def __hash__(self):
        """ DO NOT EDIT: This method is required by the test runner. """
        return hash((self.line1, self.line2, self.line3))

    def normalize_lines(self):
        """Normalizes lines."""
        self.normalized_line1 = help.normalize_line(self.line1)
        self.normalized_line2 = help.normalize_line(self.line2)
        self.normalized_line3 = help.normalize_line(self.line3)


    def abbreviate_lines(self):
        """Abbreviates lines."""
        self.abbr_line1 = help.abbreviate_line(self.line1)

    def compare(self, address):
        """Performs address comparison with current address and address parameter.
        
        The process starts with partial comparison of city,state and zipcode line,
        as well as street and apartment line. If an exact match is found in both
        instances, it is certainly the right destination and the score is bumped to
        pass the threshold for sure. If the sum of both scores is less than 1.5 it 
        is certain that, no matter who the recepient is, the threshold will not be
        passed.
        The next comparison is recepient name. In case of a weaker score, try with
        abbreviations, and choose abbreviation as the score if it is a strong match.

        Returns sum of all three scores.
        """
        s3r = help.partial_compare(self.normalized_line3, address.normalized_line3)
        s2r = help.partial_compare(self.normalized_line2, address.normalized_line2)
        stateaddrsum = s3r+s2r
        if stateaddrsum == 2:
            # certainly the right address, push for threshold
            stateaddrsum+=.5
        if stateaddrsum < 1.5:
            # certainly the wrong address, stop
            return stateaddrsum
        s1r = help.partial_compare(self.normalized_line1, address.normalized_line1)
        if s1r < 0.8:
            # rate_lines instead of partial_compare for exact abbreviation comparison
            s1abbr = help.rate_lines(self.abbr_line1, address.abbr_line1)
            if s1abbr > 0.8:
                # abbreviation much better match than line, choose it
                s1r = s1abbr
        return s1r + stateaddrsum

    def is_plausible(self):
        """Check if the address is a plausible destination.
        
        Checking is split into two logical parts, as street name and apartment number
        are contextually linked to the recipient name, while city, state and zipcode are
        a bit more isolated.

        Returns True if both are plausible, False if any isn't.
        """
        return self.is_plausible_line3() and self.is_plausible_line12()

    def is_plausible_line3(self):
        """Checks city, state and zipcode plausibility.
        
        Returns True if state or zipcode exist, else returns False.
        """
        city_state, zipcode, zipcode2 = help.extract_information(self.normalized_line3, 'city')
        if not zipcode:
            res = help.extract_information(city_state, 'state_abbr')
            if not res:
                return False
        return True

    def is_plausible_line12(self):
        """Checks street name and apartment number plausibility.
        
        Returns True if street and any one of apartment number and recepient exist,
        else returns False.
        """
        street, apartment = help.extract_information(self.normalized_line2, 'street_apt')
        if not street or (not self.normalized_line1 and not apartment):
            return False
        return True

class Letter(object):
    def __init__(self, id, address):
        self.id = id
        self.address = address

    def __eq__(self, other):
        """ DO NOT EDIT: This method is required by the test runner. """
        return self.id == other.id

    def __hash__(self):
        """ DO NOT EDIT: This method is required by the test runner. """
        return hash(self.id)

    def __str__(self):
        """ DO NOT EDIT: This method is required by the test runner. """
        return 'Letter id: %d\t%s' % (self.id, self.address)

    def rate_similarity(self, address):
        """Rates similarity between addresses.
        
        Returns rating as float[0,1].
        """
        return self.address.compare(address)


class Bundle(object):
    def __init__(self, address):
        self.address = address
        self.letters = set()

    def add_letter(self, letter):
        """ DO NOT EDIT: This method is required by the test runner. """
        self.letters.add(letter)

    def add_letters(self, letters):
        """ DO NOT EDIT: This method is required by the test runner. """
        for letter in letters:
            self.add_letter(letter)

    def is_letter_destination(self, letter):
        """Direct comparison of addresses."""
        return letter.address == self.address

    def rate_similarity(self, letter):
        """Rates similarity between letter's and bundle's address.
        
        Returns rating as float[0,1].
        """
        return letter.rate_similarity(self.address)
        

RETURN_TO_SENDER = Address('RETURN_TO_SENDER',
                           'RETURN_TO_SENDER',
                           'RETURN_TO_SENDER')
""" This special identifier is used in Level 3. See the INSTRUCTIONS.
"""
