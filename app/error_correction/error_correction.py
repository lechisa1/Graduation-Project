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
            error = re.sub(r'\b' + re.escape(rule) + r'\b', replacement, error)
        return error

    def correct_error(self, error):
        # Apply the replacement rules to the error
        corrected_error = self.apply_replacement_rules(error)
        print(f"corrected_error:{corrected_error}")
       

        # Get all valid words from the knowledge base
        valid_words = self.knowledge_base.words.keys()
        

        # Find the valid words that have the minimum Levenshtein distance
        min_distance = float('inf')
        closest_words = []

        for valid_word in valid_words:
            distance = self.weighted_levenshtein(valid_word, corrected_error)
            if distance < min_distance:
                min_distance = distance
                closest_words = [valid_word]
            elif distance == min_distance:
                closest_words.append(valid_word)

        print(f"Closest Words: {closest_words}")

        # Analyze the morphemes of the corrected error
        valid_roots, valid_affixes = self.morphological_analyzer.analyze(corrected_error)
        print(f"roots from EC: {valid_roots}")
        print(f"affixes from EC: {valid_affixes}")

        # Check if roots are valid and affixes are not, return valid roots
        if valid_roots and not valid_affixes:
            return valid_roots

        # Check if affixes are valid and roots are not, return valid affixes
        elif not valid_roots and valid_affixes:
            return valid_affixes

        # If both roots and affixes are valid, you may want to decide which one to prioritize

        # For now, returning an empty list if both roots and affixes are valid
        else:
            return closest_words

    def weighted_levenshtein(self, s1, s2):
        # You can customize your own weights for insertion, deletion, and substitution here
        insertion_cost = 1
        deletion_cost = 1
        substitution_cost = 1

        rows = len(s1) + 1
        cols = len(s2) + 1

        distance_matrix = [[0 for _ in range(cols)] for _ in range(rows)]

        for i in range(1, rows):
            distance_matrix[i][0] = i * insertion_cost

        for j in range(1, cols):
            distance_matrix[0][j] = j * deletion_cost

        for j in range(1, cols):
            for i in range(1, rows):
                cost = 0 if s1[i - 1] == s2[j - 1] else substitution_cost
                distance_matrix[i][j] = min(
                    distance_matrix[i - 1][j] + insertion_cost,
                    distance_matrix[i][j - 1] + deletion_cost,
                    distance_matrix[i - 1][j - 1] + cost
                )

        return distance_matrix[rows - 1][cols - 1]
