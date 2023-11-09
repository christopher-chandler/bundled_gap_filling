#!/usr/bin/env python
import os
import kenlm
import logging
import sys

# Set the logging level to suppress messages of INFO and below (e.g., DEBUG, INFO)
logging.basicConfig(level=logging.WARNING)

from lm import similarity

model = kenlm.LanguageModel("/Users/christopherchandler/CodeRepo/christopher-chandler/python/bundled_gap_fill/language_models/unpacked/en-70k-0.2-pruned.lm")
if not sys.platform.startswith('win'):
    sys.stdout = open(os.devnull, 'w')
sentence = 'I liked fish market '
print(sentence)
a = model.score(sentence)

sentence = 'I liked fish market  .'
print(sentence)
b = model.score(sentence)


print(similarity.percentage_difference(a,b))
print(a,b )