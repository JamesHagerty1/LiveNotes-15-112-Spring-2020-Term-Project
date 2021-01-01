import pickle
import string
import requests
import urllib
from bs4 import BeautifulSoup

# creates and returns a dictionary showing the locations of every typo
def findTypos(page):    
    typos = {}
    readingWord=False
    currWordStart=None
    currWordEnd=None
    for r in range(21):
        typos[r]=[]
        for c in range(56):
            # determines the end of a word
            if (page[r][c]==None or page[r][c][0]==' ' or 
                'image' in page[r][c] or 'table' in page[r][c] or 
                page[r][c][0] in {'.', ',', '!', ':', ';', '"'}):
                readingWord=False
                if currWordStart != None and currWordEnd != None:
                    formWord = ''
                    for charI in range(currWordStart, currWordEnd+1):
                        if page[r][charI]==None: continue
                        formWord += page[r][charI][0]
                    # determines if a word is a typo by seeing if it is not in
                    # common English or if the word is somehow blank or a 
                    # bullet or a number
                    if (not formWord.lower() in commonWords and 
                        not formWord.strip()=='' and
                        not formWord=='●' and
                        not formWord.isdigit()):
                        typos[r].append((currWordStart, currWordEnd))
                    currWordStart=None
                    currWordEnd=None
            elif currWordStart==None:
                currWordStart=c
                currWordEnd=c+1
            if currWordStart != None:
                currWordEnd=c
    return typos

# pickle method learned from:
# https://pythonprogramming.net/python-pickle-module-save-objects-serialization/
# downloaded from: https://github.com/dwyl/english-words/blob/master/words.txt  
dictionary = pickle.load(open('words.pkl', 'rb'))
# downloaded from: https://gist.github.com/h3xx/1976236
commonWords = pickle.load(open('moreCommonWords.pkl', 'rb'))

# ideas for autocorrect() and its helper functions from:
# https://medium.com/@willsentance/how-to-write-your-own-spellchecker-and-
# autocorrect-algorithm-in-under-80-lines-of-code-6d65d21bb7b6
# returns the correct spelling of an inputted word
def autocorrect(word):
    word = word.lower()
    if word in dictionary and word in commonWords:
        return word
    (error1, error2) = errorDistance1(word), errorDistance2(word)
    # words so common that are almost absolutely spelled right
    if not len(error1) == 0:
        if error1[0] in error2:
            return error1[0]
    # make decisions more complex and account for correct spellings
    if not len(error1) == 0:
        return error1[0]
    # accounts for less used but correctly spelled words if common word
    # replacements do not exist
    if len(error2) != 0:
        return error2[0]
    return None

# retrieves one character off correct word possibilities
def errorDistance1(word):
    realWords1 = []
    likelyWords1 = []
    if ((word in dictionary) and (word in commonWords)
       and (commonWords[word] <= 20000)):
       return word
    mistake1 = addLetter(word)
    mistake2 = removeLetter(word)
    mistake3 = substituteLetter(word)
    mistake4 = adjacentSwaps(word)
    realWords1.extend(mistake1)
    realWords1.extend(mistake2)
    realWords1.extend(mistake3)
    realWords1.extend(mistake4)
    for word in set(realWords1):
        if word in commonWords:
            likelyWords1.append(word)
    # sort words based on how commonly used they are
    likelyWords1 = quickSort(likelyWords1)
    if len(realWords1) < 3:
        return realWords1
    return likelyWords1

# all possibilities of adding one letter to any index of a word
def addLetter(word):
    combinations = []
    for i in range(len(word)+1):
        for alphabet in string.ascii_lowercase:
            newWord = word[:i]+alphabet+word[i:]
            if newWord in dictionary:
                combinations.append(newWord)
    return combinations

# all possibilities of removing one letter from a word
def removeLetter(word):
    combinations = []
    for i in range(len(word)):
        if not i == len(word):
            newWord = word[:i]+word[i+1:]
        else:
            newWord = word[:i]
        if newWord in dictionary:
            combinations.append(newWord)
    return combinations

# all possibilities of substituting a letter with any letter in the alphabet
# in any index of the word
def substituteLetter(word):
    combinations = []
    for i in range(len(word)):
        for alphabet in string.ascii_lowercase:
            newWord = word[:i]+alphabet+word[i+1:]
            if newWord in dictionary:
                combinations.append(newWord)
    return combinations

# all possibilities of swapping characters next to each other in a word
def adjacentSwaps(word):
    combinations = []
    for i in range(len(word)-1):
        swap1 = word[i] 
        swap2 = word[i+1]
        end = word[i+2:]
        newWord = word[:i]+swap2+swap1+end
        if newWord in dictionary:
            combinations.append(newWord)
    return combinations

# retrieves all correct word possibilities two characters off from the typo
def errorDistance2(word):
    realWords2 = []
    likelyWords2 = []
    if ((word in dictionary) and (word in commonWords)
       and (commonWords[word] <= 20000)):
       return word
    mistake1 = addLetter2(word)
    mistake2 = removeLetter2(word)
    mistake3 = substituteLetter2(word)
    mistake4 = adjacentSwaps2(word)
    realWords2.extend(mistake1)
    realWords2.extend(mistake2)
    realWords2.extend(mistake3)
    realWords2.extend(mistake4)
    for word in set(realWords2):
        if word in commonWords:
            likelyWords2.append(word)
    likelyWords2 = quickSort(likelyWords2)
    if len(realWords2) <= 3:
        return realWords2
    return likelyWords2

# adds all two letter combinations at all indexes of the word
def addLetter2(word):
    combinations = []
    for i in range(len(word)+1):
        for alphabet1 in string.ascii_lowercase:
            for alphabet2 in string.ascii_lowercase:
                newWord = word[:i]+alphabet1+alphabet2+word[i:]
                if newWord in dictionary:
                    combinations.append(newWord)
    return combinations

# removes two letters from all possible indexes of the word
def removeLetter2(word):
    combinations = []
    for i in range(len(word)-1):
        if not i == len(word):
            newWord = word[:i]+word[i+2:]
        else:
            newWord = word[:i]
        if newWord in dictionary:
            combinations.append(newWord)
    return combinations

# substitutes a letter with all two letter combinations on all indexes
def substituteLetter2(word):
    combinations = []
    for i in range(len(word)):
        for alphabet1 in string.ascii_lowercase:
            for alphabet2 in string.ascii_lowercase:
                newWord = word[:i]+alphabet1+alphabet2+word[i+1:]
                if newWord in dictionary:
                    combinations.append(newWord)
    return combinations

# swaps two characters to an adjacent character for every possible combinations
def adjacentSwaps2(word):
    combinations = []
    for i in range(len(word)-1):
        swap1 = word[i] 
        swap2 = word[i+1:i+3]
        if len(swap2) != 2:
            break
        end = word[i+3:]
        newWord = word[:i]+swap2+swap1+end
        if newWord in dictionary:
            combinations.append(newWord)
    return combinations

# minimally adapted quickSort (compares dictionary values here) from:
# https://www.cs.cmu.edu/~112/notes/notes-recursion-part1.html#quicksort
def quickSort(L):
    if (len(L) < 2):
        return L
    else:
        first = L[0]  
        rest = L[1:]
        lo = [x for x in rest if commonWords[x] < commonWords[first]]
        hi = [x for x in rest if commonWords[x] >= commonWords[first]]
        return quickSort(lo) + [first] + quickSort(hi)

# webscrapes an online dictionary to return the list of definitions of a word
# webscrapes definitions from: www.vocabulary.com   
def getDefinitions(word):
    url = 'https://www.vocabulary.com/dictionary/'+word
    r = requests.get(url)
    #soup parsing technique adapted from: 
    # https://www.youtube.com/watch?v=aIPqt-OdmS0
    soup = BeautifulSoup(r.content, 'lxml')
    definitions = soup.find_all('h3', class_='definition')
    definitionsList = []
    for d in definitions:
        # cleans definitions to be more readable
        definition = str(d)
        wordType = None
        titleIndex = definition.index('title="')
        definition = definition[titleIndex+len('title="'):-5]
        cutOutType = definition.index('"')
        wordType = definition[:cutOutType]+':'
        definition = definition[cutOutType+10:].strip()
        definitionsList.append(wordType+' '+definition)
    return definitionsList
