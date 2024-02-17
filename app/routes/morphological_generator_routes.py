from flask import jsonify, Blueprint, request
from app.morphological_generator.morphological_generator import MorphologicalGenerator
from app.knowledge_base.knowledge_base import KnowledgeBase

morphological_generator_routes = Blueprint('morphological_generator_routes', __name__)

@morphological_generator_routes.route('/generate_words', methods=['POST'])
def generate_words():
    # print("Received request for generating words.")
    data = request.get_json()
    corrections = data.get('morphemes', [])
    # print(f"Received corrections: {corrections}")
    
    kb = KnowledgeBase('app/knowledge_base/resources/dictionary.dic', 'app/knowledge_base/resources/dictionary.aff')
    # print("KnowledgeBase initialized.")
   
    morphological_generator = MorphologicalGenerator(kb)
    # print("MorphologicalGenerator initialized.")

    words = []
    for correction in corrections:
        word = morphological_generator.generate_words(correction)
        words.extend(word)  # Extend the list of words
        # print(f"Generated words: {word}")

    # print(f"Returning generated words: {words}")
    return jsonify({'words': words})
