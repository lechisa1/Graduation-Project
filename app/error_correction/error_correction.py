import re
import Levenshtein

from app.knowledge_base.knowledge_base import KnowledgeBase
from app.morphological_analyzer.morphological_analyzer import MorphologicalAnalyzer

class ErrorCorrection:
    def __init__(self, knowledge_base: KnowledgeBase, morphological_analyzer: MorphologicalAnalyzer, aff_file_path):
        self.knowledge_base = knowledge_base
        self.morphological_analyzer = morphological_analyzer
        self.replacement_rules = self.load_replacement_rules(aff_file_path)

    def load_replacement_rules(self, aff_file_path):
        replacement_rules = {}
        with open(aff_file_path, 'r') as f:
            for line in f:
                if line.startswith('REP'):
                    _, rule, replacement = line.strip().split()
                    replacement_rules[rule] = replacement
        
        return replacement_rules

    def apply_replacement_rules(self, error):
        for rule, replacement in self.replacement_rules.items():
            error = error.replace(rule, replacement)
            
        return error

    def custom_levenshtein(self, s1, s2):
        substitution_cost = 2
        insertion_cost = 1
        deletion_cost = 7

        matrix = [[0 for j in range(len(s2) + 1)] for i in range(len(s1) + 1)]

        for i in range(len(s1) + 1):
            matrix[i][0] = i * deletion_cost
        for j in range(len(s2) + 1):
            matrix[0][j] = j * insertion_cost

        for i in range(1, len(s1) + 1):
            for j in range(1, len(s2) + 1):
                if s1[i - 1] == s2[j - 1]:
                    substitution = matrix[i - 1][j - 1]
                else:
                    substitution = matrix[i - 1][j - 1] + substitution_cost
                insertion = matrix[i][j - 1] + insertion_cost
                deletion = matrix[i - 1][j] + deletion_cost
                matrix[i][j] = min(substitution, insertion, deletion)

        return matrix[len(s1)][len(s2)]

    def correct_error(self, error):
        # Apply the replacement rules to the error
        corrected_error = self.apply_replacement_rules(error)
        print("corrected_error: ", corrected_error)
        # Get all valid words from the knowledge base
        valid_words = self.knowledge_base.words.keys()
        

        # Find the valid words that have the minimum Levenshtein distance
        min_distance = float('inf')
        closest_words = []
        word_distances = {}

        for valid_word in valid_words:
            distance = self.custom_levenshtein(valid_word, corrected_error)
            word_distances[valid_word] = distance

            if distance < min_distance:
                min_distance = distance
                closest_words = [valid_word]
            elif distance == min_distance:
                closest_words.append(valid_word)

        # Sort closest_words based on their Levenshtein distance to corrected_error
        closest_words.sort(key=word_distances.get)

        # Analyze the morphemes of the corrected error
        valid_roots, valid_affixes = self.morphological_analyzer.analyze(corrected_error)

        # Check if roots are valid and affixes are not, return valid roots
        if valid_roots and not valid_affixes:
            return valid_roots

        # Check if affixes are valid and roots are not, return valid affixes
        elif not valid_roots and valid_affixes:
            return valid_affixes

        # If both roots and affixes are valid, you may want to decide which one to prioritize

        # For now, returning an empty list if both roots and affixes are valid
        else:
            print('closest_words: ',closest_words)
            return closest_words