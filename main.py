# Standard
import subprocess

from api_nlp.fastsubs_wrapper.fastsubs import FastSubs

# Pip
# None

# Custom
from api_nlp.sentence_generator.bundled_gap_fill import (
    choose_seed,
    fastsubs_gap_generator,
)

fastsubs_instance = FastSubs(
    model="/Users/christopherchandler/code_repos/christopher-chandler/Python/nlp/rub/bundled_gap_filling/data/language_model/en-70k-0.2-pruned.lm",
    incoming_data="/Users/christopherchandler/code_repos/christopher-chandler/Python/nlp/rub/bundled_gap_filling/data/incoming_text_data/sentences.txt",
    fastsubs_m1="/Users/christopherchandler/code_repos/christopher-chandler/Python/nlp/rub/bundled_gap_filling/api_nlp/fastsubs_wrapper/fastsubs_m1",
    n_gram=2,
)


def generate_bundle(incoming_data: str, target_word="") -> None:
    # Korpus, aus dem Sätze gezogen werden sollen,
    # und Target festlegen sowie leeres Bundle initiieren
    corpus = open(incoming_data, "r")

    bundle = []

    # macht aus dem Korpus eine Liste mit allen Sätzen, die unser Target enthalten
    corpus_list = []
    for line in corpus:
        line = line.strip()
        if target_word in line:
            list = line.split()
            corpus_list.append(list)

    count = 4
    for i in range(count):
        # Seed sentence auswählen und target darin markieren
        try:
            seed_id, seed_sentence, og_sentence = choose_seed(target_word, corpus_list)
        except ValueError:
            raise SystemExit(f"Target: '{target_word}' nicht vorhanden")

        # Originalsatz (= Target unmarkiert) zum Bundle hinzufügen
        # (hier ist das Target aktuell noch eingeklammert?)

        if og_sentence not in bundle:
            bundle.append(og_sentence)
            count += 1

    for b in bundle:
        b = " ".join(b)
        distractor_list = fastsubs_gap_generator(fastsubs_instance, [b], target_word)
        print(b, target_word, distractor_list)


if __name__ == "__main__":
    incoming_data = "data/incoming_text_data/sentences.txt"
    generate_bundle(incoming_data, target_word="pineapple")
