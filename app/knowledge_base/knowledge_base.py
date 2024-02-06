class KnowledgeBase:
    def __init__(self, dictionary_file_path, affix_file_path):
        self.dictionary_file_path = dictionary_file_path
        self.affix_file_path = affix_file_path
        self.words = {}
        self.affixes = {}
        self.custom_dictionary = set()  # Custom dictionary
        self.ignored_words = set()  # Ignore list
        self.load_knowledge_base()

    def load_knowledge_base(self):
        with open(self.dictionary_file_path, 'r') as f:
            for line in f:
                if '/' in line:
                    word, affix_classes = line.strip().split('/')
                    self.words[word] = affix_classes.split(',')
                else:
                    word = line.strip()
                    self.words[word] = []

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
                    print(f"self.affixes: {self.affixes.items()}")
                    

    def is_valid_word(self, word):
        return word in self.words or word in self.custom_dictionary
    
    def add_to_custom_dictionary(self, word):
        self.custom_dictionary.add(word)

    def ignore_word(self, word):
        self.ignored_words.add(word)

    def morphological_analysis(self, word):
        if word in self.ignored_words:
            return [word], []  # If the word is ignored, it's considered valid

        roots = []
        affixes = []

        # Scan input word from right to left to look for valid suffix
        for affix, rule in self.affixes.items():
            
            if word.endswith(rule['affix']):
               
                if rule['stripping'] != '0':
                    
                    root = word[:len(word) - len(rule['affix'])]+rule['stripping']
                   
                    
                    
                else:
                    
                    root = word[:len(word) - len(rule['affix'])]
                roots.append(root)
                affixes.append(affix)
                print(f"affixes:{affixes}")
                print(f"affixofwater:{affix}")
                print(roots)
                print(affixes)
            
                
                
                 
                
        # Scan input word from left to right to look for valid prefixes
        for affix, rule in self.affixes.items():
            if word.startswith(rule['affix']):
                if rule['stripping'] != '0':
                    stripped_letter = rule['stripping']
                    root = word[len(rule['affix']):] + stripped_letter
                else:
                    root = word[len(rule['affix']):]
                roots.append(root)
                affixes.append(affix)

        valid_roots = []
        valid_affixes = []

        # Check if the roots are valid words and if they can take the affixes
        for root in roots:
            if self.is_valid_word(root) and all(affix in self.get_affixes_for_root(root) for affix in affixes):
                valid_roots.append(root)

        # Check if the affixes are valid and if they can be attached to the roots
        for affix in affixes:
            if any(affix in self.get_affixes_for_root(root) for root in roots):
                valid_affixes.append(affix)

        # If the typed word does not have both valid root and valid affix, return empty list
        if not valid_roots and not valid_affixes:
            return [], []
       
        return valid_roots, valid_affixes

    def get_affixes_for_root(self, root):
        return self.words.get(root, [])

    def get_classes_for_root(self, root):
        return self.words.get(root, [])
