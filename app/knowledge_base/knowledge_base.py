class KnowledgeBase:
    def __init__(self, dictionary_file_path, affix_file_path):
        # print("Initializing KnowledgeBase...")
        self.dictionary_file_path = dictionary_file_path
        self.affix_file_path = affix_file_path
        self.words = {}
        self.affixes = {}
        self.custom_dictionary = set()  # Custom dictionary
        self.ignored_words = set()  # Ignore list
        self.load_knowledge_base()

    def load_knowledge_base(self):
        print("Loading knowledge base...")
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
                    print(f"Loaded affix: {flag} with details: {self.affixes[flag]}")
                    print(f"General affixes: {self.affixes}")

        with open(self.dictionary_file_path, 'r') as f:
            for line in f:
                if '/' in line:
                    rootWord, affix_classes = line.strip().split('/')
                    self.words[rootWord] = [self.affixes[affix]['affix'] for affix in affix_classes.split(',') if affix in self.affixes]
                    print(f"Loaded word: {rootWord} with affixes: {self.words[rootWord]}")
                    print(f"General words: {self.words}")
                else:
                    rootWord = line.strip()
                    self.words[rootWord] = {}

    def is_valid_word(self, rootWord):
        print(f"Checking if {rootWord} is a valid word...")
        return rootWord in self.words or rootWord in self.custom_dictionary
    
    def add_to_custom_dictionary(self, word):
        print(f"Adding {word} to custom dictionary...")
        self.custom_dictionary.add(word)

    def ignore_word(self, word):
        print(f"Ignoring word {word}...")
        self.ignored_words.add(word)

    def get_affixes_for_root(self, rootWord):
        print(f"Getting affixes for root word {rootWord}...")
        return self.words.get(rootWord, [])

    def morphological_analysis(self, word):
        print(f"Performing morphological analysis for word {word}...")
        if word in self.ignored_words:
            print(f"Word {word} is in ignored words list.")
            return [word], []  # If the word is ignored, it's considered valid

        roots = []
        affixes = []

        # Scan input word from right to left to look for valid suffix
        for affix, rule in self.affixes.items():
            if word.endswith(rule['affix']) :
                if rule['stripping'] != '0'  :
                    stripped_letter = rule['stripping']
                    print(f"stripped letter: {stripped_letter}")
                    root = word[:len(word) - len(rule['affix'])]+stripped_letter
                    roots.append(root)
                    affixes.append(rule['affix'])
                    print(f"Found valid suffix {rule['affix']} for word {word}, root is {root}")
                else:
                    root = word[:len(word) - len(rule['affix'])]
                roots.append(root)
                affixes.append(rule['affix'])
                print(f"Found valid suffix {rule['affix']} for word {word}, root is {root}")
            
        # Scan input word from left to right to look for valid prefixes
        for affix, rule in self.affixes.items():
            if word.startswith(rule['affix']):
                if rule['stripping'] != '0':
                    stripped_letter = rule['stripping']
                    print(f"stripped letter: {stripped_letter}")
                    root = word[len(rule['affix']):] + stripped_letter
                else:
                    root = word[len(rule['affix']):]
                roots.append(root)
                affixes.append(rule['affix'])
                print(f"Found valid prefix {rule['affix']} for word {word}, root is {root}")

        valid_roots = []
        valid_affixes = []

        # Check if the roots are valid words and if they can take the affixes
        for root, affix in zip(roots, affixes):
            if self.is_valid_word(root) and affix in self.get_affixes_for_root(root):
                valid_roots.append(root)
                valid_affixes.append(affix)
                print(f"Found valid root {root} for word {word} with affix {affix}")

        return valid_roots, valid_affixes
