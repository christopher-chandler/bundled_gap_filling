# Standard
import subprocess

from api_nlp.fastsubs_wrapper.fastsubs import FastSubs

# Pip
# None

# Custom
from api_nlp.sentence_generator.bundled_gap_generator import *

fastsubs_instance = FastSubs(
    model="/Users/christopherchandler/code_repos/christopher-chandler/Python/nlp/rub/bundled_gap_filling/data/language_model/en-70k-0.2-pruned.lm",
    incoming_data="/Users/christopherchandler/code_repos/christopher-chandler/Python/nlp/rub/bundled_gap_filling/data/incoming_text_data/sentences.txt",
    fastsubs_m1="/Users/christopherchandler/code_repos/christopher-chandler/Python/nlp/rub/bundled_gap_filling/api_nlp/fastsubs_wrapper/fastsubs_m1",
    n_gram=2,
)


def main(corpus):
    # Korpus, aus dem Sätze gezogen werden sollen, und Target festlegen sowie leeres Bundle initiieren
    print("Initialisierung...")
    target = "eat"
    bundle = []
    # Sätze, die das Target enthalten, als Liste in Liste schreiben
    corpus_list = []
    for line in corpus:
        if target in line:
            # Target markieren
            line = line.replace(target, "<" + target + ">")
            list = line.split()
            # ... und als Liste an unsere Liste von in Frage kommenden Sätzen anhängen
            corpus_list.append(list)

    # Seed sentence auswählen
    seed_id, seed_sentence = choose_seed(target, corpus_list)

    # Satz zum Bundle hinzufügen
    bundle.append(seed_sentence)
    # Diesen Satz aus corpus_list entfernen (denn wir wollen ja keinen Satz doppelt im Bundle haben)
    corpus_list.remove(corpus_list[seed_id])

    print("Generiere Distraktoren mit Fastsubs...")
    # Von Fastsubs distractors generieren lassen
    distractor_list = fastsubs_distractor_generator(
        fastsubs_instance, seed_sentence, target
    )

    print("...")
    print("Unser erster Satz:")
    print("'" + " ".join(seed_sentence) + "'")
    print("Disambiguation level: " + str(disamb(bundle, target, distractor_list)))

    print("...")
    print("Jetzt fangen wir an, weitere Sätze zu suchen.")
    print("...")

    # Hier suchen wir mithilfe einer while-Schleife immer den nächsten Satz aus, der unser disambiguation level optimiert.
    count = 1
    while count < 4:
        best_sentence_id = best_next_sentence(
            corpus_list, bundle, target, distractor_list
        )
        if best_sentence_id != -1:
            bundle.append(corpus_list[best_sentence_id])
            corpus_list.remove(corpus_list[best_sentence_id])
            print("Satz Nr. " + str(count + 1) + " gefunden!")
            print(
                "Disambiguation level: " + str(disamb(bundle, target, distractor_list))
            )
        else:
            bundle.append(
                ["ERROR: target_prob/max_other_prob = 0. Noch einmal versuchen?"]
            )
            break
        count = count + 1

    # output
    output(bundle, target)


if __name__ == "__main__":
    corpus = open(
        "data/incoming_text_data/sentences.txt",
        "r",
    )
    main(corpus)
