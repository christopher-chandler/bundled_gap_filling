# Standard
import math
import random

# Pip
import kenlm

# Custom
from api_nlp.fastsubs_wrapper.fastsubs import FastSubs

# kenlm initialisieren
model = kenlm.LanguageModel("data/language_model/en-70k-0.2-pruned.lm")

fastsubs_instance = FastSubs(
    model="data/language_model/en-70k-0.2-pruned.lm",
    incoming_data="data/incoming_text_data/sentences.txt",
    fastsubs_m1="api_nlp/fastsubs_wrapper/fastsubs_m1",
    n_gram=2,
)

# Methode, die uns einen zufälligen seed sentence (als Liste) aussucht und mit ID zurückgibt
def choose_seed(target, corpus_list):
    seed_id = random.randint(0, (len(corpus_list) - 1))
    seed_sentence = corpus_list[seed_id].copy()
    return (seed_id, seed_sentence)


# Schnittstelle zu Fastsubs
def fastsubs_distractor_generator(fastsubs_instance, sentence, target):
    # Platzhaltermethode.
    # Bekommt einen Satz mit markiertem Target als input und sucht Wörter, die das Target ersetzen könnten.
    distractors = ["digest", "drink", "medicine"]

    prob = fastsubs_instance.run_fastsubs(sentence)

    final_distractors = list()

    for row in prob.keys():
        if target in row:

            distractor = prob.get(row)

            # split distractor list:
            for d in distractor:
                d_res = d.split(" ")[0]
                final_distractors.append(d_res)

            return final_distractors
    else:
        return ["empty"]


# diese Methode gibt uns mit kenlm den Score für ein gegebenes Trigramm zurück
def get_score(trigram):
    score = model.score(trigram)
    result = pow(10, score)
    # Smoothing, da wir für viele Trigramme ein Ergebnis von 0 bekamen)
    result = result + (1 / 10000000000)
    return result


# macht aus einem Input-Text (gegeben als Liste) Trigramme und berechnet deren Score.
def make_trigram(sentence):
    # Leere Listen initialisieren
    trigram_list = []
    trigram_probs = []
    n = 0
    # Dann gehen wir unseren Input durch
    while n < (len(sentence) - 2):
        trigram = sentence[n] + " " + sentence[n + 1] + " " + sentence[n + 2]
        trigram_list.append(trigram)
        trigram_probs.append(get_score(trigram))
        n = n + 1
    return (trigram_list, trigram_probs)


# diese Methode bekommt als Input einen Satz (als Liste und mit einer markierten Stelle) und ein Wort
# und gibt als Output die Wahrscheinlichkeit zurück, dass das Wort an dieser Stelle auftaucht
def prob_for_single(sentence, word):
    modified_sen = sentence.copy()
    i = 0
    while i < len(sentence):
        if sentence[i][0] == "<":
            modified_sen[i] = word
            break
        i = i + 1
    trigram_list = make_trigram(modified_sen)[0]
    trigram_probs = make_trigram(modified_sen)[1]
    final_prob = 1
    for prob in trigram_probs:
        final_prob = final_prob * prob
    return final_prob


# berechnet, mit welcher Wahrscheinlichkeit ein gegebenes Wort die "Lösung" für ein ganzes Bundle ist
def prob_for_bundle(bundle, word):
    # wahrscheinlichkeit fängt bei 1 an und dann multiplizieren wir das einfach immer mit der neuen wahrscheinlichkeit
    bundle_prob = 1
    # die schleife geht alle sätze unseres bundles durch
    for sentence in bundle:
        # ...und berechnet die wahrscheinlichkeit, mit der das wort in dieser lücke auftaucht
        sentence_prob = prob_for_single(sentence, word)
        # und dann multiplizieren wir das mit unserer aktuellen wahrscheinlichkeit des wortes für das bundle!
        bundle_prob = bundle_prob * sentence_prob
    return bundle_prob


# diese Methode berechnet das aktuelle disambiguation level des Bundles (= wie viel wahrscheinlicher ist das target die lösung als ein distractor)
def disamb(bundle, target, distractor_list):
    # Wahrscheinlichkeit des Targets für das aktuelle Bundle
    target_prob = prob_for_bundle(bundle, target)
    # Liste für die Wahrscheinlichkeiten der Distraktoren für das Bundle
    distractors_prob = []
    for distr in distractor_list:
        distractors_prob.append(prob_for_bundle(bundle, distr))
    # dann nehmen wir den größten wert aus dieser liste von wahrscheinlichkeiten (= die größte wahrscheinlichkeit, die nicht die des targets ist)
    max_other_prob = max(distractors_prob)
    # ... und berechnen hiermit unser disambiguation level. das ist einfach nur log(wahrscheinlichkeit target/größte andere wahrscheinlichkeit)
    if max_other_prob != 0:
        disambiguation = math.log(target_prob / max_other_prob)
        return disambiguation
    else:
        # Hier hatten wir, trotz des Smoothings, oft einen Error, bei dem wir für die Wahrscheinlichkeiten 0 bekamen.
        # Aus Zeitgründen haben wir entschieden, hier dann stattdessen 1000 zurückzugeben - das wird später im Code dann zu einer Error-Nachricht gemacht.
        return 1000


# Diese Methode prüft für alle Sätze in corpus_list, ob sie das disambiguation level optimieren, und gibt dann die ID des besten zurück
def best_next_sentence(corpus_list, bundle, target, distractor_list):
    choosing_next_sen = []
    for sentence in corpus_list:
        new_bundle = bundle.copy()
        new_bundle.append(sentence)
        if disamb(new_bundle, target, distractor_list) == 1000:
            # Falls wir kein disambiguation level berechnen konnten, überspringen wir dieses Item.
            continue
        else:
            choosing_next_sen.append(disamb(new_bundle, target, distractor_list))
    maximum = 0
    i = 0
    best_sentence_id = 0
    while i < len(choosing_next_sen):
        if choosing_next_sen[i] > maximum > 1000:
            maximum = choosing_next_sen[i]
            best_sentence_id = i
        i = i + 1
    if best_sentence_id == 1000:
        # Hier nochmal Sicherheitsvorkehrung: Wenn wir hier wieder ein fehlerhaftes disambiguation level haben, geben wir als Index -1 zurück
        # Da das kein gültiger Listenindex ist, wird dann unten stattdessen ein Error geprintet
        return -1
    return best_sentence_id


# entfernt die Target-Markierung aus der Liste (nötig für manche Tests)
def remove_marker(sentence):
    i = 0
    while i < len(sentence):
        if sentence[i][0] == "<":
            sentence[i] = sentence[i].replace("<", "")
            sentence[i] = sentence[i].replace(">", "")
        i = i + 1
    return sentence


# printet nochmal unsere komplette Aufgabe.
def output(bundle, target):
    print("...")
    print("Hier ist die fertige Bundled Gap Filling Aufgabe:")
    print("")
    for sentence in bundle:
        sentence = "'" + " ".join(sentence) + "'"
        print(sentence)


def main():
    # Korpus, aus dem Sätze gezogen werden sollen, und Target festlegen sowie leeres Bundle initiieren
    print("Initialisierung...")
    corpus = open(
        "/data/incoming_text_data/sentences.txt",
        "r",
    )
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

    main()
