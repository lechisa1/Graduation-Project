# app/tokenizer/tokenizer.py
import re
from flask import jsonify

def tokenize(text):
    # Define a regular expression for tokenizing words, digits, and punctuation marks
    pattern = re.compile(r'\b[\w\']+\b|\d+|[.,;!?()]')


    # Use the regular expression to find all tokens in the input text
    tokens = re.findall(pattern, text)

    return tokens

def tokenize_endpoint(request):
    if request.method == 'POST':
        data = request.get_json()
        text = data.get('text', '')
        tokens = tokenize(text)
        return jsonify({'tokens': tokens})
