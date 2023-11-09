# Standard 
# None 

# Pip
# None 

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


if __name__ == '__main__':
    pass
