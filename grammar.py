import logging

import nltk

logger = logging.getLogger(__name__)


class GrammarBuilder:
    def __init__(self, spec_grammar):
        grammar = nltk.CFG.fromstring(spec_grammar)
        self.parser = nltk.ChartParser(grammar)
        self.trees = []

    def parse(self, spec):
        for entry in spec:
            try:
                for tree in self.parser.parse(entry):
                    self.trees.append(tree)
            except ValueError as e:
                logger.error(f'{entry}: {e}')

    def __dict__(self):
        pass
