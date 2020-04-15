import pathlib
import re

import nltk

import snomed
import grammar

grammar_builder = grammar.GrammarBuilder(snomed.SPECIFICATION_GRAMMAR)
grammar_builder.parse(snomed.read_spec('grammar.txt'))

print('foo')
