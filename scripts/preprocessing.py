import re

def lowercasing(phrase_list: list):
    phrase_list = [ phrase.lower() for phrase in phrase_list ]
    return phrase_list

def replace_and_or(phrase_list: list):
    phrase_list = [ re.sub('&', 'and', phrase) for phrase in phrase_list ]
    phrase_list = [ re.sub('/', 'or', phrase) for phrase in phrase_list ]
    return phrase_list

def remove_noisy_words(phrase_list : list):
  common_titles = ["ceo ", "coo ", "cfo ", "cio ", "cmo ", "chro ", "cto ",
                 "director ", "chief ", "president ", "vice president ", "vp ",
                 "vice chair ", "board member ", "member ", "team member ", "team captain ",
                 "owner ", "chairman ", "co - chair ", "co - chairman ", "senior "
                 ]
  clean_list = []
  for phrase in phrase_list:
    phr = phrase
    for title in common_titles:
      phr = re.sub(title, '', phr)
    clean_list.append(phr)
  return clean_list

def keep_only_alnum(s): 
    s1 = re.sub(r'[^a-z0-9 ]+', ' ', s.lower())
    return " ".join(s1.split())

def keep_alnum_batch(phrase_list : list):
    phrase_list = [ keep_only_alnum(phrase) for phrase in phrase_list ]
    return phrase_list