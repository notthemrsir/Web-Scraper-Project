import os 
import json
import nltk
from nltk import word_tokenize,sent_tokenize
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from random import randrange
#Tokenizer

#Lucas Beal 2/11/2020 CS 3150

#================================================================================================================================
#IMPORTANT: In order for this file to work correctly, please replace all the addresses to somewhere on your drive where you have
#the file located, so it will know where to grab all the files and where to save the JSON file
#================================================================================================================================

#Goal of this file is to find all the saved html files, and then tokenize the text, normalize it, and then save as a JSON file

#Finding all the html files and save them as txt files
def find_all_html_files():
    links      = []
    documentID = []
    for file in os.listdir(r"C:\Users\lukeb\Documents\cs3150"):
        output = ""
        if file.endswith(".html"):
            linktopath = os.path.join(r"C:\Users\lukeb\Documents\cs3150", file)
           #Generate a Random Number for A Document ID
           # while True:
           #     txtID = randrange(100000)
           #     if txtID not in documentID:
           #         documentID.append(txtID)
           #         break
            txtIDNAME = file.split('html')
            txtID = txtIDNAME[0] + ".txt"
            txtDocument = txtID
            textofwork = open(txtDocument, "w")
            soup = BeautifulSoup(open(linktopath), "html.parser")
            text = soup.find_all(text=True)
            for t in text:
                output = output + t.lower()
            #print (output)
            print("File was saved as txt: " + file)
            textofwork.write(output)
            textofwork.close()
            #From here, send the HTML file to be stripped and tokenized
def tokenize_documents(dictionary,stopwords):
    for file in os.listdir(r"C:\Users\lukeb\Documents\cs3150"):
        filename = []
        tokens   = []
        alltext  = []
        if file.endswith(".txt"):
            print (file)
            filename = file.split('.txt')
            print(filename[0])
            txtfile = open(os.path.join(r"C:\Users\lukeb\Documents\cs3150", file))
            while True:
                line = txtfile.readline()
                tokens = word_tokenize(line)
                for word in tokens:
                    #With Normalization, if a word is within the stopwords list, merely pass, as we don't want it as a token
                    if word in stopwords:
                        pass
                    elif word in dictionary:
                        #if a word is in the dictionary, get its ID value already, and then add the new ID value onto it
                        # while also unsuring that we aren't adding the same value, if document1 is already in there, don't add 1 again!
                        value = dictionary.get(word) 
                        if filename[0] in value:
                            frequency = value[0]
                            frequency = frequency + 1
                            value[0]  = frequency
                            dictionary.pop(word)
                            dictionary[word] = value
                        else:
                            #=================
                            #This section grabs the frequency of that term, and then adds 1 to it, as we have found another instance of it
                            #This is the same process, minus adding the document name to the dictionary for the first time
                            frequency = value[0]
                            frequency = frequency + 1
                            value[0]  = frequency
                            #=================
                            value.append(filename[0])
                            dictionary.pop(word)
                            dictionary[word] = value
                    else:
                        #The word is not in the dictionary, so add the word, along with the frequency of the term
                        #Therefore, we add a 1 in the first location, as we have, so far, exactly one occurence of the term
                        dictionary[word] = [1, filename[0]]
                if not line:
                    break
            txtfile.close()


def main():
    #I had numerous problems getting nltk to work with a downloaded corupus of
    #english stop words, so I decided to extract all the words and put them
    #in a list within the code
    import json
    find_all_html_files()
    stopwords = ["i","me","my","myself","we","our","ours","ourselves","you","you're"
                        ,"you've","you'll","you'd","your","yours","yourself","yourselves","he"
                        ,"him","his","himself","she","she's","her","hers","herself","it","it's"
                        ,"its","itself","they","them","their","theirs","themselves","what","which"
                        ,"who","whom","this","that","that'll","these","those","am","is","are","was"
                        ,"were","be","been","being","have","has","had","having","do","does","did","doing"
                        ,"a","an","the","and","but","if","or","because","as","until","while","of","at","by","for"
                        ,"with","about","against","between","into","through","during","before","after","above","below"
                        ,"to","from","up","down","in","out","on","off","over","under","again","further","then","once","here"
                        ,"there","when","where","why","how","all","any","both","each","few","more","most","other","some","such"
                        ,"no","nor","not","only","own","same","so","than","too","very","can","will","just","don"
                        ,"don't","should","should've","now","aren't","n't", "http"
                        ,",","0","1","2","3","4","5","6","7","8","9","/","|", " "]
    print (stopwords)
    dictionary = {}
    tokenize_documents(dictionary,stopwords)
    print(dictionary)
    with open('data.json', 'w') as fp:
        json.dump(dictionary, fp)

main()

