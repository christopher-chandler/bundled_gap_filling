# Standard 
# None 

# Pip
import kenlm

# Custom 
# None

"""
main body 
"""

def percentage_difference(value1, value2):
    if value1 == 0 and value2 == 0:
        return 0  # Avoid division by zero if both values are zero

    if value1 > value2:
        numerator = value2
        denominator = value1

    else:
        numerator = value1
        denominator = value2

    return round(abs((numerator - denominator) / ((numerator + denominator) / 2)) * 100,2)

def calcualte_sentence_score (sentence):
    model = kenlm.LanguageModel("data/en-70k-0.2-pruned.lm")
    return model.score(sentence)


if __name__ == '__main__':
    pass
