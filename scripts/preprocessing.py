import re

def lowercasing(phrase_list: list):
    phrase_list = [ phrase.lower() for phrase in phrase_list ]
    return phrase_list

def replace_and_or(phrase_list: list):
    phrase_list = [ re.sub('&', 'and', phrase) for phrase in phrase_list ]
    phrase_list = [ re.sub('/', 'or', phrase) for phrase in phrase_list ]
    return phrase_list

if __name__ == "__main__" : 
    lowercasing()