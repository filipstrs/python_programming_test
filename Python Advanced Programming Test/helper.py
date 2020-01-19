import re
import difflib

THRESHOLD = 2.49


REGEX_IGNORED_TERMS = [
    'apartment',
    'apt',
    'unit',
    'suite',
    'ste',
    '#',
    'resident',
    'postal',
    'customer',
    'avenue',
    'ave',
    'street',
    'str',
    'st',
    ', inc.'
]

REGEX_EXPRESSIONS = [
    (r"(" + "|".join(REGEX_IGNORED_TERMS) + r")\.?", r''),
    (r"circle", "cir"),
    (r"\bsf\b", "san francisco")
]

REGEX_SPECIAL = "[\.,]"
REGEX_WHITESPACE = "(\s+)"

REGEX_CITY_STATE_ZIPCODE = "(\D+)?\s?(\d+)?-?(\d+)?"
REGEX_STATE_ABBR = r"\b(([a][elkszr])|([c][aot])|([d][ec])|([f][ml])|([g][au])|([h][i])|([i][dlna])|([k][sy])|([l][a])|([m][ehdainsot])|([n][evhjmycd])|([m][p])|([o][hkr])|([p][war])|([r][i])|([s][cd])|([t][nx])|([u][t])|([v][tia])|([w][aviy]))\b"
REGEX_STREET_APARTMENT = r"(\d+ [a-z\s]+) ?(\d+)?"


class Helper(object):
    """
    This is a helper class, containing the logic needed for analyzing and 
    manipulating the lines of an address.
    It contains wrappers for some common operations that use re and difflib
    libraries, and other functions using them
    """

    def regex_sub(self, regexstr, replacement, string):
        """This is a wrapper for string substitution using regex.
        
        Returns the modified string.
        """
        return re.sub(regexstr, replacement, string)

    def regex_findall(self, regexstr, string):
        """This is a wrapper for finding patterns in a string using regex.
        
        Returns the list of all matches.
        """
        return re.findall(regexstr, string)

    def regex_search(self, regexstr, string):
        """This is a wrapper for finding a pattern in a string using regex.
        
        Returns a match object, or None if no match was found.
        """
        return re.search(regexstr, string)

    def rate_lines(self, line1, line2):
        """Compares the two lines with SequenceMatcher.
        
        Returns ratio of similarity as float[0,1]
        """
        return difflib.SequenceMatcher(a=line1, b=line2).ratio()

    def partial_compare(self, line1, line2):
        """Compares two lines, calculating rating the shorter line 
        with every substring of the longer line with the same length.
        
        Returns the best rating as float[0,1]
        """
        len1 = len(line1)
        len2 = len(line2)
        # set line1 to be the longer one 
        if len1<len2:
            line1, line2, len1, len2 = line2, line1, len2, len1
        lendiff = abs(len1-len2)
        maxrating = 0
        for x in range(lendiff+1):
            # extract the substring from position x and of length x+len2
            newline = line1[x:x+len2]
            rating = self.rate_lines(newline, line2)
            if rating > maxrating:
                maxrating=rating
        return maxrating

    def strip_specials_and_whitespace(self, line):
        """Replaces all patterns from REGEX_SPECIAL with nothing
        and from REGEX_WHITESPACE with a single space.
        
        Returns the modified line.
        """
        newline = self.regex_sub(REGEX_SPECIAL,'',line)
        newline = self.regex_sub(REGEX_WHITESPACE, ' ', newline)
        return newline

    def normalize_line(self, line):
        """Modifies a line to normalize its contents.
        
        The modifications are: making everything lowercase,
        removing common phrases(such as avenue, ave, street etc.),
        expanding certain phrases(namely SF as san francisco and cir as circle)
        and removing special characters and compressing whitespace.

        Returns the modified line.
        """
        newline = line.lower()
        for item in REGEX_EXPRESSIONS:
            newline = self.regex_sub(item[0], item[1], newline)
        newline = self.strip_specials_and_whitespace(newline)
        return newline

    def abbreviate_line(self, line):
        """If a line contains multiple words extracts an abbreviation.
        If it does not, writes the line instead.
        
        Returns the abbreviation.
        """
        if len(line.split(' ')) > 1:
            found = self.regex_findall(r'\b[a-zA-Z]', line)
            abbr = ''.join(found)
        else:
            abbr = line
        return abbr

    def extract_information(self, line, info_type):
        """Extracts information based on regexes and type of information requested.
        Options for info_type:
        city -- extracts three groups: 1. city name and state(as cityname, ST)
                                       2. zipcode first part
                                       3. zipcode second part
        state_abbr -- extracts state abbreviation
        street_apt -- extracts two groups: 1. street name
                                           2. apartment number
        
        Returns the data tuple if match is found, else returns 
        empty tuple of appropriate length if match is not found.
        Returns False if info_type match is not found.
        """
        if info_type == 'city':
            res = self.regex_findall(REGEX_CITY_STATE_ZIPCODE, line)
            res = res[0] if res else ('','','')
        elif info_type == 'state_abbr':
            res = self.regex_search(REGEX_STATE_ABBR, line)
        elif info_type == 'street_apt':
            res = self.regex_findall(REGEX_STREET_APARTMENT, line)
            res = res[0] if res else ('','')
        else:
            res = False
        return res
