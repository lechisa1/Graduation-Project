import re

def tokenize(text):
    # Define a regular expression for tokenizing words (possibly followed by a punctuation mark), digits, and standalone punctuation marks
    pattern = re.compile(r'\b[\w\'-]+(?:[.,;:!?\"\'])?\b|\d+|[.,;:!?()\"\']|\s')

    # Use the regular expression to find all tokens in the input text
    tokens = pattern.findall(text)
    

    return tokens
