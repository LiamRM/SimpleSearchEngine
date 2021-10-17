"""
Name         : hw4.py
Author       : Liam Richards (lrm444)
Version      : 1.0
Date Created : October 7th, 2021
Description  : This is a simple search engine, matching queries to the best-fitting abstract 
               out of a collection of 1400 research paper abstracts.

IDF Scores
===================================
if the word that we are looking at is not found in any of the documents, just make the idf score 0
Remove all rows with a score of 0


"""

import stop_list
import math         # for log() function
import numpy        # for dot() dotproduct function

# Create a 'Word' object
class Word():
    def __init__(self,word):
        self.word = word
        self.IDFscore = 0
        self.freq = 1

# Create a 'Query' object
class Query():
    def __init__(self,queryNumber):
        self.queryNumber = queryNumber
        self.wordDict = {}                      # dictionary, {word: Word object}
        self.TFIDFscores = {}                   # dictionary, {word: TFIDF score}       --> TFIDF scores for all words in query (based on collection of queries)
        self.scores = {}                        # nested dictionary, {abstractNum: {query word: TFIDF score}}  --> TFIDF scores for query words for all abstracts
        self.cosineScores = {}                  # dictionary, {abstractNum: cosine score}

# Create a 'Abstract' object
class Abstract():
    def __init__(self,abstractNumber):
        self.num = abstractNumber
        self.title = ""
        self.author = ""
        self.bibliography = ""
        self.wordDict = {}                      # dictionary, {word: Word object}
        self.TFIDFscores = {}                   # dictionary, {word: TFIDF score}       --> TFIDF scores for all words in abstract

###         FEATURE VECTOR FOR WORDS IN QUERY (from cran.qry)   ###
queryObjList = []           # list of Query objects
wordsInQueries = {}         # {word: # of queries it's in}

# Loop through words of in each query, removing stop words
with open("cran.qry") as f:
    queryWords = []         # list of words (strings) in query
    for line in f:
        line = line.strip()
        for word in line.split():
            if(line.split()[0] == '.I'):
                # Save the next word as the Query #
                qNum = line.split()[1]
            elif (word == '.W'):                                        # Exclude .W from our list of words
                pass
            elif (word == '.'):                                         # keep adding to 'queryWords' list until we hit a '.' 
                # End of Query --> Save # and words to objects
                Q = Query(qNum)
                for word in queryWords:
                    # Check if word already exists in wordDict
                    if word in Q.wordDict:
                        Q.wordDict[word].freq += 1 # freq++ (num instances of each non-stop word)
                    else:
                        # first time word is appearing in query
                        Q.wordDict[word] = Word(word)
                        # Increase the count for # of queries word appears in
                        if(word in wordsInQueries):
                            wordsInQueries[word] += 1
                        else:
                            wordsInQueries[word] = 1
                queryObjList.append(Q)

                # clear list to create another query
                queryWords.clear()
            elif (word in stop_list.closed_class_stop_words):            # Exclude stop words
                pass
            else:
                queryWords.append(word)
    f.close()

def printQueries():
    for query in queryObjList:
        print("Query #:", query.queryNumber, "\n-----------------------------")
        for word, queryWordObj in query.wordDict.items():
            print(word, queryWordObj.freq)
        print("===========================")


###         CALCULATE IDF AND TFIDF SCORES FOR WORDS IN QUERIES         ###
# IDF = log(numberOfDocuments / numberOfDocumentsContaining(t))
numDocuments = len(queryObjList)
for query in queryObjList:
    for word, queryWordObj in query.wordDict.items():
        numOfDocumentsWithWord = wordsInQueries[word]
        queryWordObj.IDFscore = math.log(numDocuments / numOfDocumentsWithWord)

        # TFIDF = TF x IDF
        query.TFIDFscores[word] = queryWordObj.freq * queryWordObj.IDFscore


###         FEATURE VECTOR FOR WORDS IN ABSTRACT (from cran.all.1400)   ###
abstractObjList = []           # list of Abstract objects
wordsInAbstracts = {}         # {word: # of abstracts it's in}

# Loop through words of in each abstract, removing stop words
with open("cran.all.1400") as f:
    abstractWords = []         # list of words (strings) in abstract
    betweenWandI = False
    for line in f:
        line = line.strip()
        for word in line.split():
            # save the information after the .W tag and before .I tag
            if(line.split()[0] == '.I'):
                if(len(abstractWords) != 0):
                    # End of Abstract --> Save # and words to objects
                    A = Abstract(aNum)
                    for word in abstractWords:
                        # Check if word already exists in wordDict
                        if word in A.wordDict:
                            A.wordDict[word].freq += 1 # freq++ (num instances of each non-stop word)
                        else:
                            # first time word is appearing in abstract
                            A.wordDict[word] = Word(word)
                            # Increase the count for # of abstracts word appears in
                            if(word in wordsInAbstracts):
                                wordsInAbstracts[word] += 1
                            else:
                                wordsInAbstracts[word] = 1
                    abstractObjList.append(A)
                
                # Save the next word as the Abstract #
                aNum = line.split()[1]
                betweenWandI = False
                
                # clear list to create another abstract
                abstractWords.clear()
            elif (word == '.W'):                                        
                betweenWandI = True
            elif (word in stop_list.closed_class_stop_words or word == '.'):            # Exclude stop words and punctuation
                pass
            elif (betweenWandI):
                abstractWords.append(word)

    # save the last abstract
    A = Abstract(aNum)
    for word in abstractWords:
        # Check if word already exists in wordDict
        if word in A.wordDict:
            A.wordDict[word].freq += 1 # freq++ (num instances of each non-stop word)
        else:
            # first time word is appearing in abstract
            A.wordDict[word] = Word(word)
            # Increase the count for # of abstracts word appears in
            if(word in wordsInAbstracts):
                wordsInAbstracts[word] += 1
            else:
                wordsInAbstracts[word] = 1
    abstractObjList.append(A)
    f.close()

def printAbstracts():
    for abstract in abstractObjList:
        print("Abstract #: ", abstract.num, "\n--------------------------")
        for word, abstractObj in abstract.wordDict.items():
            print(word, abstractObj.freq)
        print("==========================")

print(len(abstractObjList))

"""

###     IDF SCORES FOR WORDS IN ABSTRACTS       ###
# IDF = log(numberOfDocuments / numberOfDocumentsContaining(t))
numDocuments = len(abstractObjList)
for abstract in abstractObjList:
    for word, abstractWordObj in abstract.wordDict.items():
        numOfDocumentsWithWord = wordsInAbstracts[word]
        abstractWordObj.IDFscore = math.log(numDocuments / numOfDocumentsWithWord)

        # TFIDF = TF x IDF
        abstract.TFIDFscores[word] = abstractWordObj.freq * abstractWordObj.IDFscore



###         RANKING OF DOCUMENTS (ABSTRACTS) FOR EACH QUERY         ###
# for each word in query, save abstract's TF-IDF score of query words to the scores dictionary of Query obj
for query in queryObjList:
    for abstract in abstractObjList:
        wordScores = {}
        for word in query.wordDict:
            if word in abstract.TFIDFscores:
                wordScores[word] = abstract.TFIDFscores[word]
            else:
                wordScores[word] = 0
        
        #print(wordScores)
        # append wordScores dictionary within the Query.scores dictionary {1: {'similarity': 0, 'true': 2.2, 'mine': 0}, '2': {.....}}
        query.scores[abstract.num] = wordScores

###         CALCULATE COSINE SIMILARITY BETWEEN QUERY / ABSTRACT TFIDF VECTORS      ###
# Calculate cosine similarity between query TFIDF scores and query.scores[abstractNum] TFIDF scores
# cosine = (dot product vec A and vec B) / (sqr root (sum of a^2 values * sum of b^2 values))
for query in queryObjList:
    vec_a = []
    vec_b = []
    vec_a_squared = []
    vec_b_squared = []
    for key, value in query.TFIDFscores.items():
        vec_a.append(int(value))
        vec_a_squared.append(value*value)
    for abstractNum, TFIDFscore in query.scores.items():
        vec_b = list(TFIDFscore.values())
        
        for v in vec_b:
            vec_b_squared.append(int(v) * int(v))
        # calculate dot product
        dot = numpy.dot(vec_a, vec_b, out = None)
        # calculate sqr root of product of squares
        sqr = math.sqrt(sum(vec_a_squared) * sum(vec_b_squared))

        # Calculate cosine similarity score (option to drop 0 cosine similarity scores)
        if sqr != 0:
            cosine = dot / sqr
        else:  
            cosine = 0

        query.cosineScores[abstractNum] = cosine

        #print(query.queryNumber, abstractNum, query.cosineScores[abstractNum])

###         SORT THROUGH COSINE SIMILARITY SCORES VECTORS              ###
# output results to file: query #, abstract #, cosine similarity score
f = open("output.txt", "w", newline="\n")

for query in queryObjList:
    #print(query.cosineScores.items())
    s = sorted(query.cosineScores.items(), key=lambda x: x[1], reverse=True)    # results in a list of tuples

    for t in s:                             # for each tuple in sorted list
        # eliminate 0 scores 
        if(str(t[1]) == "0" or str(t[1]) == "0.0"):
            pass
        else:
            outputline = query.queryNumber + " " + str(t[0]) + " " + str(t[1]) + "\n"    # query #, abstract #, cosine similarity score
            f.write(outputline)      
    
f.close()
"""