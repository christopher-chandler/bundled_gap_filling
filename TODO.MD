Sentence
1 the students have to take the test (take, have, ...)
2 the their cook will take three salmons (take, have, .. )
3 all passengers should take their seats (take, have, ..)
4 Both authors take credit (take, have, .. )

```
# read in corpus
def read_in_document():
   -  read all json files from the wiki data 
    
    Document 
       - s1
       - s2 
       - s3 
        [s1, s2, s3]
        - tokenize ()
        - clean (simple tokenize) 
    - Keep it simple with tokenizing, cleaning, etc. 
    dict(
     "META_INFO" : dict()
     # tokenize, clean, etc. 
     "SENTENCES" : [s1, s2, s3, s4, etc. ]     
   )
    

# Kenlm
#
```
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






