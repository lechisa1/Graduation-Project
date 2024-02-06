class MorphologicalGenerator:
    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base

    def generate_words(self, input_morphemes):
        correct_words = []

        for morpheme in input_morphemes:
            if self.knowledge_base.is_valid_word(morpheme):  # If the morpheme is a valid root
                word_forms = self.generate_word_forms_from_root(morpheme)
            else:  # If the morpheme is an affix
                word_forms = self.generate_word_forms_from_affix(morpheme)
            correct_words.extend(word_forms)

        return correct_words

    def generate_word_forms_from_root(self, root):
        word_forms = []
        affix_classes = self.knowledge_base.get_classes_for_root(root)

        for affix_class in affix_classes:
            affix = self.knowledge_base.affixes.get(affix_class)
            if affix:
                word_form = root + affix['affix']
                word_forms.append(word_form)

        return word_forms

    def generate_word_forms_from_affix(self, affix):
        word_forms = []
        roots = self.knowledge_base.words.keys()

        for root in roots:
            affix_classes = self.knowledge_base.get_classes_for_root(root)
            if affix in affix_classes:
                word_form = root + affix
                word_forms.append(word_form)

        return word_forms
