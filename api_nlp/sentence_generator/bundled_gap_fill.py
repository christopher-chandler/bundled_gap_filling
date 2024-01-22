# Standard
import math
import random

# Pip
import kenlm

# Custom
# None

# Methode, die seed sentence aussucht und target darin markiert
m = "data/language_model/en-70k-0.2-pruned.lm"
model = kenlm.LanguageModel(m)


def choose_seed(target, corpus_list):
    seed_id = random.randint(0, (len(corpus_list) - 1))
    seed_sentence = corpus_list[seed_id]
    n = 0
    while n < len(seed_sentence):
        if target in seed_sentence[n]:
            marked = "<" + target + ">"
            seed_sentence[n] = seed_sentence[n].replace(target, marked)
            break
        n = n + 1
    # (hier einmal eine Version, wo das Target nicht markiert wird...)
    og_sentence = corpus_list[seed_id]
    # warum ist eat hier auch markiert??
    print(og_sentence)
    return (seed_id, seed_sentence, og_sentence)


def fastsubs(sentence, target):
    # Platzhaltermethode.
    # Bekommt einen Satz mit markiertem Target als input und sucht Wörter,
    # die das Target ersetzen könnten.
    distractors = ["digest", "drink" "medicine"]
    return distractors


###########Hilfsmethoden kenlm##############

# diese Methode gibt uns mit kenlm den Score für ein Trigramm zurück
def get_score(trigram):
    return model.score(trigram)


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
        #print(get_score(trigram))
        n = n + 1
    return (trigram_list, trigram_probs)


# diese methode bekommt als input einen satz (als Liste und mit einer markierten
# Lücke bzw. das Target ist markiert) und ein wort
# und gibt als output die wahrscheinlichkeit zurück, dass das wort in diesem
# kontext auftaucht
def prob_for_single(sentence, word):
    modified_sen = sentence
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


"""diese methode bekommt als input ein wort und ein bundle,
(eine liste von sätzen) und prüft für alle sätze die wahrscheinlichkeit, dass das wort zu diesem bundle passt"""


def prob_for_bundle(word, bundle):
    # wahrscheinlichkeit fängt bei 1 an und dann multiplizieren wir das einfach
    # immer mit der neuen wahrscheinlichkeit
    bundle_prob = 1
    # die schleife geht alle sätze unseres bundles durch
    for sentence in bundle:
        # ...und berechnet die wahrscheinlichkeit, mit der das wort in dieser lücke auftaucht
        sentence_prob = prob_for_single(word, sentence)
        # und dann multiplizieren wir das mit unserer aktuellen wahrscheinlichkeit
        # des wortes für das bundle!
        bundle_prob = bundle_prob * sentence_prob
    print(
        "ich bin eine wahrscheinlichkeit für ein wort für ein ganzes bundle: "
        + str(bundle_prob)
    )
    return bundle_prob


"""diese methode bekommt als input ein target word, unser bundle und eine liste mit dem rest unseres vocabularys
und gibt als output den disambiguation level des target words für dieses bundle und dieses rest-vocabs zurück
wir benutzen hierfür die formel aus dem paper"""


def disamb(target, bundle, rest_of_vocab):
    # wahrscheinlichkeit des targets für das bundle
    target_prob = prob_for_bundle(target, bundle)
    # liste, für die wahrscheinlichkeiten der anderen wörter aus dem vocab
    other_words_prob = []
    # für jedes wort im vocab berechnen wir die wahrscheinlichkeit
    # für unser bundle und hängen die an die liste an
    for word in rest_of_vocab:
        other_words_prob.append(prob_for_bundle(word, bundle))
    # dann nehmen wir den größten wert aus dieser liste von wahrscheinlichkeiten
    # (= die größte wahrscheinlichkeit, die nicht die des targets ist)
    max_other_prob = max(other_words_prob)
    # ... und berechnen hiermit unser disamb level. das ist einfach nur
    # log(wahrscheinlichkeit target/größte andere wahrscheinlichkeit)
    disambiguation = math.log(target_prob / max_other_prob)
    print(
        "ich bin ein beispiel für einen disambiguation level wert: "
        + str(disambiguation)
    )
    return disambiguation


if __name__ == "__main__":
    pass
