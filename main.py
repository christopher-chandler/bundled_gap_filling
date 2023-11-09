#!/usr/bin/env python
import argparse
import logging
import os
import sys

# Pip
import kenlm

# Custom
from api_nlp.language_model.model import calcualte_sentence_score

sentence = 'I liked fish market  .'
b = calcualte_sentence_score(sentence)


if __name__ == '__main__':
    pass
