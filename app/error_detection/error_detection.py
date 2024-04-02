from app.knowledge_base.knowledge_base import KnowledgeBase
from app.morphological_analyzer.morphological_analyzer import MorphologicalAnalyzer
from app.knowledge_base.knowledge_base import nounClasses,verbClasses
class ErrorDetection:
    def __init__(self, knowledge_base: KnowledgeBase, morphological_analyzer: MorphologicalAnalyzer):
        self.knowledge_base = knowledge_base
        self.morphological_analyzer = morphological_analyzer

    def is_valid_word(self, word):
        affixClass= self.knowledge_base.get_affix_class_for_root(word)
        print('affixClasssss: ', affixClass)
        if self.knowledge_base.is_valid_word(word) and affixClass not in verbClasses :
            return True
        
 
        roots, affixes = self.morphological_analyzer.analyze(word)
        # print("roots: ",roots,"affixes: ",affixes)
        for root in roots:
            if self.knowledge_base.is_valid_word(root):
                root_affixes = self.knowledge_base.get_affixes_for_root(root)
                # print(f"roots on ED:{root_affixes}")
                if all(affix in root_affixes for affix in affixes):
                    return True
        return False
