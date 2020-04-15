import pathlib
import re

import nltk

import snomed

spec = snomed.read_spec('grammar.txt')

grammar = nltk.CFG.fromstring(snomed.SPECIFICATION_GRAMMAR)

parser = nltk.ChartParser(grammar)

trees = []
for i, entry in enumerate(spec):
    try:
        for tree in parser.parse(entry):
            trees.append(tree)
    except ValueError as e:
        print(f'{i}: {entry}: {e}')

spec = spec.replace(' = ',  ' -> ')
spec = spec.replace('\"', '\'')
spec = spec.replace('/', '|')

# remove comments
spec = [entry.split(' ; ')[0] for entry in spec]

# handle acsii
spec = [re.sub(r'(%x[A-F0-9]{2}(-\w{2})?)', '\'\\1\'', entry)
        for entry in spec]

# handle optional parts
optional_re = re.compile(r' \[(.+)\]')
new_entries = []
remove_entries = []
for entry in spec:
    match = optional_re.search(entry)
    if match:
        new_entries.append(entry.replace(match[0], ''))
        new_entries.append(entry.replace(match[0], f' ({match[1]})'))
        remove_entries.append(entry)

for entry in remove_entries:
    spec.remove(entry)

spec += new_entries

spec.sort()

print('foo')
