import json 
import os

#Lucas Beal

def make_bi_gram(bi_dictionary):
    #===================
    #Create and save the data.json [inverted index] into a dictionary
    dictionary = {}
    with open('data.json', 'r') as f:
        dictionary = json.load(f)
        #print(dictionary)
    #===================
    for key in dictionary:
        #for every key/term in the dictionary ...
        #first, add $ to both front and back to signify location of the terms in question
        term = "$" + key + "$"
        for i in range(len(term)):
            #First, we must ensure that we are never trying to access a character beyond the final $.
            #Therefore, by checking that when we encounter a $, the i must be zero for us to consider it, otherwise its the final $
            if term[i] == '$' and i == 0:
                bi_term = term[i] + term[(i + 1)]
                if bi_term in bi_dictionary:
                    value = bi_dictionary.get(bi_term)
                    value.append(key)
                    bi_dictionary.pop(bi_term)
                    bi_dictionary[bi_term] = value
                else:
                    bi_dictionary[bi_term] = [key]
                #print(bi_term)
            elif term[i] != '$':
                #From here, as long as the first character we conisder isn't a $, then we are not yet at the end of the string
                bi_term = term[i] + term[(i + 1)]
                if bi_term in bi_dictionary:
                    value = bi_dictionary.get(bi_term)
                    value.append(key)
                    bi_dictionary.pop(bi_term)
                    bi_dictionary[bi_term] = value
                else:
                    bi_dictionary[bi_term] = [key]
                #print(bi_term)
                     
def main():
    bi_dictionary = {}
    make_bi_gram(bi_dictionary)
    print(bi_dictionary)
    with open('bigram.json', 'w') as fp:
        json.dump(bi_dictionary, fp)
main()
