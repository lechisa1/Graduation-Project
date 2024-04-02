from flask import jsonify, Blueprint, request
from app.morphological_generator.morphological_generator import MorphologicalGenerator
from app.knowledge_base.knowledge_base import KnowledgeBase
import Levenshtein

morphological_generator_routes = Blueprint('morphological_generator_routes', __name__)

@morphological_generator_routes.route('/generate_words', methods=['POST'])
def generate_words():
    data = request.get_json()
    corrections = data.get('morphemes', [])
    misspelled_word = data.get('errors', "")

    kb = KnowledgeBase('app/knowledge_base/resources/dictionary.dic', 'app/knowledge_base/resources/dictionary.aff')
    morphological_generator = MorphologicalGenerator(kb)

    words = []
    for correction in corrections:
        word = morphological_generator.generate_words(correction)
        # Using Levenshtein edit distance algorithm to compare generated words with errors
        for w in word:
            if Levenshtein.distance(w, misspelled_word) <= 10:  # Adjust the threshold as needed
                words.append(w)

    return jsonify({'words': words})
