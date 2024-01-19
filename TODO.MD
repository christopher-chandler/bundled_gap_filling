Sentence
1 the students have to take the test (take, have, ...)
2 the their cook will take three salmons (take, have, .. )
3 all passengers should take their seats (take, have, ..)
4 Both authors take credit (take, have, .. )

# Chris 
```
- Write the text data in extra file 
- One line is one sentence
- Save probabilities from Fastsubs in a pickle file. 

- I get a list with marked target words
- get 5 replacement words and save them in a list. 
```

# Niels 
```
# Enter seed sentence
def seed_sentence(sentence, gap_word, corpus):

    candidates = list()

    for sentence in corpus ,
       append all sentences to the list candidates
        if the gap word appears in the sentence

     return candidates

def find_most_probable sentence (candidates, gap_word)
    1) determine the likelihood that the gap_word can appear in the sentence
        using trigrams
    2) determine the second most likely word
```

# 
- Target as input 
- Wikidaten 
- Target in Spitzenklammern (< >)

trainingsdaten: en-70k usw
korpus für sätze: wiki data (animals only)

# to do:
seed sentence und target aussuchen
target markieren

target dem code als input geben
zufälligen satz mit diesem target aussuchen

target markieren mit <>
für diesen satz mit fastsubs plausible wörter generieren (das macht christoph)
du gibst mir die wörter zurück

mit kenlm nach den wahrscheinlichkeiten für alle wörter in diesem satz gucken
daraus disambiguation usw berechnen

dann: für alle weiteren sätze, in denen das target vorkommt, 
mit fastsubs andere kandidaten generieren

für die in kenlm die prob generieren...
dann mit greedy algorithm immer den nächstbesten nehmen...