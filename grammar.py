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
    SYMBOL = 'ascii'
    OPTION = 'OR'
    DEFINITION = 'def'
    COMMENT = 'comment'
    STRING = 'string'
    LABEL = 'label'

    label = tree.label()

    actions = {
        RULE: lambda x: Rule.from_tree(x),
        SYMBOL: lambda x: Symbol.from_tree(x),
        OPTION: lambda x: Option.from_tree(tree),
        DEFINITION: lambda x: gen_from_tree(x[0]),
        COMMENT: lambda x: gen_from_tree(x[0]),
        STRING: lambda x: join_leaves(tree),
        LABEL: lambda x: join_leaves(tree),
    }
    def default(x): return GrammarBuilder._tree_to_dict(x)

    return actions.get(label, default)(tree)


def join_leaves(tree):
    return ''.join(tree.leaves())


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
                    label = join_leaves(entry)
                else:
                    definition = gen_from_tree(entry)

        if label and definition:
            return Rule(label, definition)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.label} -> {self.definition}'


class Symbol:
    def __init__(self, value=None, min=None, max=None):
        self.value = value
        self.min = min
        self.max = max

    @staticmethod
    def from_tree(tree):
        string = join_leaves(tree)
        values = string.replace('%x', '').split('-')

        if len(values) == 1:
            return Symbol(value=int(values[0], 16))
        elif len(values) == 2:
            return Symbol(min=int(values[0], 16), max=int(values[1], 16))

    def __repr__(self):
        return str(self)

    def __str__(self):
        if self.value:
            return f'\'{chr(self.value)}\''
        else:
            return ' | '.join([f'\'{chr(entry)}\'' for entry in range(self.min, self.max+1)])


class Option:
    def __init__(self, first=None, second=None):
        self.first = first
        self.second = second

    @staticmethod
    def from_tree(tree):
        first = gen_from_tree(tree[0])
        second = gen_from_tree(tree[4])
        return Option(first, second)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'{self.first} | {self.second}'
