import re
def tokenize(text):
    # Define a regular expression for tokenizing words (possibly followed by a dot or comma), digits, and standalone punctuation marks
    # pattern = re.compile(r'\b[\w\'-]+(?:[.,])?\b|\d+|.,')

    # Use the regular expression to find all tokens in the input text
    tokens = re.split(' ',text)

    return tokens
