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
                trees = [tree for tree in self.parser.parse(entry)]
            except ValueError as e:
                logger.error(f'{entry}: {e}')
                trees = None
            else:
                if len(trees) == 0:
                    logger.error(f'did not provide rule: {entry}')
                else:
                    self.trees += trees

    def to_dict(self):
        res = []
        for tree in self.trees:
            res.append(gen_from_tree(tree))
        return res

    @staticmethod
    def _tree_to_dict(tree):
        DEF = 'def'

        spec = []
        for entry in tree:
            if isinstance(entry, nltk.Tree):
                label = entry.label()
                if label == 'words' or label == 'word':
                    spec.append((label, ''.join(entry.leaves())))
                elif label == 'number':
                    spec.append((label, ''.join(entry.leaves())))
                elif label == 'string':
                    spec.append((label, ''.join(entry.leaves())))
                elif label == 'ascii':
                    spec.append((label, ''.join(entry.leaves())))
                elif label == 'SP':
                    continue
                else:
                    spec.append((label, GrammarBuilder._tree_to_dict(entry)))
            else:
                spec.append(entry)

        for i in range(0, len(spec)):
            try:
                key, value = spec[i]
            except:
                continue
            else:
                if key == DEF and isinstance(value, tuple):
                    spec[i] = value

        if len(spec) == 1:
            spec = spec[0]

        if spec[0] == 'name':
            spec = spec[1]

        return spec


def gen_from_tree(tree):
    RULE = 'S'

    label = tree.label()

    if label == RULE:
        return Rule.from_tree(tree)
    else:
        return GrammarBuilder._tree_to_dict(tree)


class Rule:
    LABEL = 'label'
    DEFINITION = 'def'

    def __init__(self, label=None, definition=None):
        self.label = label
        self.definition = definition

    @staticmethod
    def from_tree(tree):
        label, definition = None, None
        for entry in tree:
            if isinstance(entry, nltk.Tree):
                if entry.label() == Rule.LABEL:
                    label = ''.join(entry.leaves())
                elif entry.label() == Rule.DEFINITION:
                    definition = gen_from_tree(entry)

        if label and definition:
            return Rule(label, definition)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.label} -> {self.definition}'
