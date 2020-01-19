""" a. I used urllib2 to get the web page and beautifulsoup to parse the page using built-in python parser 'html.parser'.
After parsing I use any of available methods for traversing the page. 
Some of them are select(), find(), find_all(), find_next_sibling(), find_next_siblings() etc.
If a needed element has trailing whitespace, that is pruned by using replace() with all whitespace tags (\t\n\r) individually.
Afterwards I package the data into a dictonary, and using json package dump the dictionary to a file on the PC.
Find any links to other pages searching for href or form action and visit them.
"""

""" b. lists in python are denoted by [] while tuples are denoted by ().
both are used to store values, which can be accessed with [].
Lists are mutable, while tuples are immutable. As such, lists have more
built in functions that allow manipulation.
Lists are not hashable, while tuples are, so they can be used as a key in a dictionary.
"""

# c.

for x in range(1, 101):
    if x % 7 == 0 and x % 6 == 0:
            val = "Docket Alarm"
        elif x % 7 == 0:
            val = "Docket"
        elif x % 6 == 0:
            val = "Alarm"
        else:
            val = x
    print val

""" d. A generator is a function that returns a lazy iterator. 
That means that they can be looped over, but unlike lists they do not store the content in memory.
To make a generator, we use the keyword 'yield' to declare the returning value.
Iteration is done by using next(). Iteration is paused when the function yields a value.
Variable values inside the generator are persisted between calls.
Generators are iterated over only once. When it is done, StopIteration is raised.
To restart the iteration, a new generator must be created.
For loops can also iterate over generators because they use next() for the iterator.
"""

def test_value():
    for x in range(101):
        if x % 7 == 0 and x % 6 == 0:
            val = "Docket Alarm"
        elif x % 7 == 0:
            val = "Docket"
        elif x % 6 == 0:
            val = "Alarm"
        else:
            val = x
        yield val

for x in test_value():
    print x

# this solution is a bit slower than the one above
# def test_value():
#     for x in range(101):
#         val = ''
#         if x % 7 == 0:
#             val = "Docket"
#         elif x % 6 == 0:
#             val+= " Alarm"
#         val = val.lstrip() if val else str(x)
#         yield val
