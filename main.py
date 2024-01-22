# Standard
# None

# Pip
# None

# Custom
from api_nlp.sentence_generator.bundled_gap_fill import (
    choose_seed,
    fastsubs,
    prob_for_single,
)


def generate_bundle(incoming_data):
    # Korpus, aus dem Sätze gezogen werden sollen,
    # und Target festlegen sowie leeres Bundle initiieren
    corpus = open(incoming_data, "r")
    target = "eat"
    bundle = []
    # macht aus dem Korpus eine Liste mit allen Sätzen, die unser Target enthalten
    corpus_list = []
    for line in corpus:
        if target in line:
            list = line.split()
            corpus_list.append(list)

    # Seed sentence auswählen und target darin markieren
    seed_id, seed_sentence, og_sentence = choose_seed(target, corpus_list)

    # Originalsatz (= Target unmarkiert) zum Bundle hinzufügen
    # (hier ist das Target aktuell noch eingeklammert?)
    bundle.append(og_sentence)
    print(bundle)

    # Von Fastsubs distractors generieren lassen
    distractor_list = fastsubs(seed_sentence, target)

    # für jeden der Distraktoren die Wahrscheinlichkeit, dass sie an Stelle
    # des Targets vorkommen, für alle Sätze mit dem Target im corpus berechnen
    # Achtung! Wir müssen noch Pseudoworte vor Satzanfang einfügen,
    # damit wir auch für das erste und zweite Wort des Satzes Trigramme erzeugen können.
    # Außerdem müssen wir Sätze, die wir ausgewählt haben, aus corpus_list entfernen
    for distr in distractor_list:
        for sent in corpus_list:
            x = prob_for_single(sent, distr)
            # print(x)

    # als nächstes müssen wir unseren zweiten satz aussuchen...
    # hierfür gehen wir corpus_list durch und gucken,
    # welcher satz das disamb level optimiert und
    # for schleife: für jeden satz in corpus list
    # single_prob benutzen
    # daraus disamb berechnen

    # dann alles irgendwie outputten. """


if __name__ == "__main__":
    incoming_data = "data/save_wiki_text/results.txt"
    generate_bundle(incoming_data)
