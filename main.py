#!/usr/bin/env python
import logging
import os
import sys

# Pip
import kenlm

# Custom
from api_nlp.language_model.model import calcualte_sentence_score


sentence = "I liked fish market  .", "I like fish market"
model_results = calcualte_sentence_score(sentence)

print(model_results)

if __name__ == "__main__":
    pass
