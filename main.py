# Standard
import logging
import os
import sys

# Pip
import kenlm

# Custom
from api_nlp.language_model.model import calculate_sentence_score


sentence = "I liked fish market  .", "I like fish market ."
model_results = calculate_sentence_score(sentence)

print(1, model_results)

if __name__ == "__main__":
    pass
