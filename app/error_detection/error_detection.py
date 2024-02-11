from app.knowledge_base.knowledge_base import KnowledgeBase
from app.morphological_analyzer.morphological_analyzer import MorphologicalAnalyzer

class ErrorDetection:
    def __init__(self, knowledge_base: KnowledgeBase, morphological_analyzer: MorphologicalAnalyzer):
        self.knowledge_base = knowledge_base
        self.morphological_analyzer = morphological_analyzer

    def is_valid_word(self, word):
        if self.knowledge_base.is_valid_word(word):
            return True
 
        roots, affixes = self.morphological_analyzer.analyze(word)
        for root in roots:
            if self.knowledge_base.is_valid_word(root):
                root_affixes = self.knowledge_base.get_affixes_for_root(root)
                # print(f"roots on ED:{root_affixes}")
                if all(affix in root_affixes for affix in affixes):
                    return True
        return False
