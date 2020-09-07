import os
import json

# Query by Lucas Beal
# The purpose of this file is to handle a query from a user, search the relevant indexes, and then return 
# ... a result, whilst checking for potential misspellings by offering alternative words



def search_with_bigram_query(input):
    #Search and return all the bi-gram terms that match our query
    query = "$" + input + "$"
    possible_docs = []
    with open('bigram.json', 'r') as f:
        bi_dictionary = json.load(f)
    for i in range(len(query)):
            #First, we must ensure that we are never trying to access a character beyond the final $.
            #Therefore, by checking that when we encounter a $, the i must be zero for us to consider it, otherwise its the final $
        if query[i] == '$' and i == 0:
            bi_term = query[i] + query[(i + 1)]
            if bi_term in bi_dictionary:
                value = bi_dictionary.get(bi_term)
                possible_docs.append(value)
        elif query[i] != '$':
                #From here, as long as the first character we conisder isn't a $, then we are not yet at the end of the string
            bi_term = query[i] + query[(i + 1)]
            if bi_term in bi_dictionary:
                value = bi_dictionary.get(bi_term)
                possible_docs.append(value)
    return possible_docs


def analyze_docs(all_alternatives, input):
    #Analyze all the terms that were given, and return the ones that are within an acceptable range of our Jaccard Coefficient
    top_alternatives = []
    query = "$" + input + "$"
    for posting_l in all_alternatives:
        for item in posting_l:
            j_numerator   = 0
            j_denominator = 0
            new_item = "$" + item + "$"
            item_list = list(new_item)
            query_list = list(query)
            if (len(item_list) > len(query_list)):
                for i in range(len(item_list)):
                    #to ensure we don't access an element out of bounds, and that we count the elements in item_list that go beyond the string of the query
                    if(len(query_list) > (i + 1)):
                        if query_list[i] == '$' and i == 0:
                            query_term = query_list[i] + query_list[(i + 1)]
                            alt_term = item_list[i] + item_list[(i + 1)]
                            if query_term == alt_term:
                                j_numerator = j_numerator + 1
                                j_denominator = j_denominator + 1
                            else:
                                j_denominator = j_denominator + 1
                        elif query[i] != '$':
                            query_term = query_list[i] + query_list[(i + 1)]
                            alt_term = item_list[i] + item_list[(i + 1)]
                            if query_term == alt_term:
                                j_numerator = j_numerator + 1
                                j_denominator = j_denominator + 1
                            else:
                                j_denominator = j_denominator + 1
                    else:
                        if item_list[i] != '$':
                            j_denominator = j_denominator + 1
                #Here, we compute the Jaccard Coefficient and Account for an Acceptable Range
                if (j_numerator != 0 and j_denominator != 0):
                    j_coefficient = (float(j_numerator)) / (float(j_denominator))
                    #Round the J-Coefficient to 2 decimal places
                    j_coefficient = round(j_coefficient, 2)
                    if(j_coefficient > 0.50):
                        top_alternatives.append(item)
            elif (len(item_list) < len(query_list)):
                for i in range(len(query_list)):
                    #to ensure we don't access an element out of bounds, and that we count the elements in item_list that go beyond the string of the query
                    if(len(item_list) > (i + 1)):
                        if query_list[i] == '$' and i == 0:
                            query_term = query_list[i] + query_list[(i + 1)]
                            alt_term = item_list[i] + item_list[(i + 1)]
                            if query_term == alt_term:
                                j_numerator = j_numerator + 1
                                j_denominator = j_denominator + 1
                            else:
                                j_denominator = j_denominator + 1
                        elif query[i] != '$':
                            query_term = query_list[i] + query_list[(i + 1)]
                            alt_term = item_list[i] + item_list[(i + 1)]
                            if query_term == alt_term:
                                j_numerator = j_numerator + 1
                                j_denominator = j_denominator + 1
                            else:
                                j_denominator = j_denominator + 1
                    else:
                        if query_list[i] != '$':
                            j_denominator = j_denominator + 1
                #Here, we compute the Jaccard Coefficient and Account for an Acceptable Range
                if (j_numerator != 0 and j_denominator != 0):
                    j_coefficient = (float(j_numerator)) / (float(j_denominator))
                    #Round the J-Coefficient to 2 decimal places
                    j_coefficient = round(j_coefficient, 2)
                    if(j_coefficient > 0.50):
                        top_alternatives.append(item)
            elif (len(item_list) == len(query_list)): 
                for i in range(len(query_list)):
                    #to ensure we don't access an element out of bounds, and that we count the elements in item_list that go beyond the string of the query
                    if query_list[i] == '$' and i == 0:
                        query_term = query_list[i] + query_list[(i + 1)]
                        alt_term = item_list[i] + item_list[(i + 1)]
                        if query_term == alt_term:
                            j_numerator = j_numerator + 1
                            j_denominator = j_denominator + 1
                        else:
                            j_denominator = j_denominator + 1
                    elif query[i] != '$':
                        query_term = query_list[i] + query_list[(i + 1)]
                        alt_term = item_list[i] + item_list[(i + 1)]
                        if query_term == alt_term:
                            j_numerator = j_numerator + 1
                            j_denominator = j_denominator + 1
                        else:
                            j_denominator = j_denominator + 1
                    else:
                        if query_list[i] != '$':
                            j_denominator = j_denominator + 1
                #Here, we compute the Jaccard Coefficient and Account for an Acceptable Range
                if (j_numerator != 0 and j_denominator != 0):
                    j_coefficient = (float(j_numerator)) / (float(j_denominator))
                    #Round the J-Coefficient to 2 decimal places
                    j_coefficient = round(j_coefficient, 2)
                    if(j_coefficient > 0.50):
                        top_alternatives.append(item)
    return top_alternatives


def main():
    answer = ""
    while(answer != "ExitApp"):
        print("=====")
        print("Hello, and welcome to Luke's Query Search Engine for all your Shakespeare Needs!")
        print("Please enter a term you wish to search for or enter 'ExitApp' to quit this application...")
        print("Input:")
        answer = input()
        with open('data.json', 'r') as f:
            dictionary = json.load(f)
        if(answer == "ExitApp"):
            print("Goodbye!")
            break
        #Check to See if Query Term is In our Dictionary
        print("Query: " + answer)
        if(answer in dictionary):
            postingslist = dictionary[answer]
            for doc in postingslist:
                #Present, to ensure that we don't include the integer value for occurences of a term within our results to the user
                if isinstance(doc, int) == True:
                    pass
                else:
                    print(doc)
        #If the Query Term is not in the dictionary, then offer alternative spellings of the query term
        else:
            print ("ERROR: Could not Find Query in Search...")
            alternative_queries = search_with_bigram_query(answer)
            #for item in alternative_queries:
            #    print(item)
            top_alternatives = analyze_docs(alternative_queries, answer)
            #ensuring that no duplicates are in the list
            temp = []
            for item in top_alternatives:
                if item not in temp:
                    temp.append(item)
            for item in temp:
                print("Possible Alternative: " + item)
        print("=====")
main()