import string
import json
import os  # Add this import for working with file paths

class KnowledgeBase:
    def __init__(self, dictionary_file_path, affix_file_path):
        self.dictionary_file_path = dictionary_file_path
        self.affix_file_path = affix_file_path
        self.words = {}
        self.affixes = {}
        self.custom_dictionary = set()  # Custom dictionary
        self.ignored_words = set()  # Ignore list
        self.load_knowledge_base()
        self.loadLocalStorage()

    def load_knowledge_base(self):
        with open(self.affix_file_path, 'r') as f:
            for line in f:
                values = line.strip().split()
                
                if len(values) == 5:
                    option_name, flag, stripping, affix, condition = values
                    self.affixes[flag] = {
                        'option_name': option_name,
                        'stripping': stripping,
                        'affix': affix,
                        'condition': condition
                    }

        with open(self.dictionary_file_path, 'r') as f:
            for line in f:
                if '/' in line:
                    rootWord, affix_classes = line.strip().split('/')
                    self.words[rootWord] = [self.affixes[affix]['affix'] for affix in affix_classes.split(',') if affix in self.affixes]
                else:
                    rootWord = line.strip()
                    self.words[rootWord] = {}

    def loadLocalStorage(self):
        try:
            with open('custom_dictionary.json', 'r') as file:
                data = json.load(file)
                self.custom_dictionary = set(data['custom_dictionary'])
        except FileNotFoundError:
            pass  # File doesn't exist, which is fine

        try:
            with open('ignored_words.json', 'r') as file:
                data = json.load(file)
                self.ignored_words = set(data['ignored_words'])
        except FileNotFoundError:
            pass  # File doesn't exist, which is fine

    def saveLocalStorage(self):
        data_custom = {'custom_dictionary': list(self.custom_dictionary)}
        with open('custom_dictionary.json', 'w') as file:
            json.dump(data_custom, file)

        data_ignored = {'ignored_words': list(self.ignored_words)}
        with open('ignored_words.json', 'w') as file:
            json.dump(data_ignored, file)

    def is_valid_word(self, rootWord):
        # Remove punctuation from the rootWord
        rootWord_without_punctuation = rootWord.translate(str.maketrans('', '', string.punctuation))

        # Check if the rootWord without punctuation is in the words or custom_dictionary
        return any(
            rootWord_without_punctuation == word or rootWord_without_punctuation in affixes
            for word, affixes in self.words.items()
        ) or rootWord_without_punctuation in self.custom_dictionary or rootWord_without_punctuation in self.ignored_words

    def add_to_custom_dictionary(self, word):
        print(f"Adding {word} to custom dictionary...")
        self.custom_dictionary.add(word)
        self.saveLocalStorage()

    def ignore_word(self, word):
        print(f"Ignoring word {word}...")
        self.ignored_words.add(word)
        self.saveLocalStorage()

    def get_affixes_for_root(self, rootWord):
        return self.words.get(rootWord, [])

    def find_valid_root_for_affix(self, affix):
        valid_roots = []
        for root, affixes in self.words.items():
            if affix in affixes:
                valid_roots.append(root)
        return valid_roots

    def morphological_analysis(self, word):
        if word in self.ignored_words:
            return [word], []  # If the word is ignored, it's considered valid

        roots = []
        affixes = []

        for affix, rule in self.affixes.items():
            if word.endswith(rule['affix']):
                if rule['stripping'] != '0':
                    stripped_letter = rule['stripping']
                    root = word[:len(word) - len(rule['affix'])] + stripped_letter
                    roots.append(root)
                    affixes.append(rule['affix'])
                else:
                    root = word[:len(word) - len(rule['affix'])]
                roots.append(root)
                affixes.append(rule['affix'])
            
        for affix, rule in self.affixes.items():
            if word.startswith(rule['affix']):
                if rule['stripping'] != '0':
                    stripped_letter = rule['stripping']
                    root = word[len(rule['affix']):] + stripped_letter
                else:
                    root = word[len(rule['affix']):]
                roots.append(root)
                affixes.append(rule['affix'])

        valid_roots = []
        valid_affixes = []

        for root, affix in zip(roots, affixes):
            if self.is_valid_word(root) and affix in self.get_affixes_for_root(root):
                valid_roots.append(root)
                valid_affixes.append(affix)
        print(f"valid roots:{valid_roots}, valid affixes:{valid_affixes}")
        return valid_roots, valid_affixes
