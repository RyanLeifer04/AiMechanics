#Ryan Leifer, Homework 1-P
import sys 

#counts number of lines in a .txt file
def count_lines(filepath):
    with open(filepath, 'r') as file:
        return sum(1 for line in file)

#loads all dictionary words into a single list
def loadWords(filename):
    words = open(filename,'r')
    lines = count_lines(filename)
    wlist = []
    i = 0
    while i < lines:
        wlist.append(words.readline().rstrip("\n "))
        i += 1
    return wlist

#checks is next word is 1 letter different
def checkOneDiffWeighted(w1,w2,target):
    if len(w1) != len(w2):
        return None
    
    i = 0
    count = 0
    while i < len(w1):
        if w1[i] != w2[i]:
            count += 1
        i += 1
        
    i = 0
    c2 = 0
    while i < len(w2):
        if w2[i] == target[i]:
            c2 += 1
        i += 1
        
    if count > 1 or c2 == 0:
        return False
    
    return True

#BFS search through dictionary to find path, returns None is no path is found
def search(word1, word2, dictionary):
    
    path = [word1]
    visited = set()
    visited.add(word1)
    currentWord = word1
    thing = True
    while thing is True:
        if currentWord == word2:
            return path
        falseCount = 0
        for word in dictionary:
            if falseCount > 5000:
                path.pop()
                currentWord = path.pop()
                path.append(currentWord)
                print(path)
                falseCount = 0
                
            if word not in visited:
                check = checkOneDiffWeighted(currentWord, word, word2)
                if check is True:
                    path.append(word)
                    currentWord = word
                    visited.add(word)
                    print(path)
                elif check is False:
                    falseCount += 1
                    
    return None

def main(dictFile, startWord, targetWord):
    if len(startWord) != len(targetWord):
        print("unequal length")
        return None

    dictionary = loadWords(dictFile)
    
    if startWord not in dictionary or targetWord not in dictionary:
        print(startWord)
        print(targetWord)
        print("not a word")
        return None
    
    solutionPath = search(startWord, targetWord, dictionary)
    
    if solutionPath == None:
        print("No solution")
    else:
        for word in solutionPath:
            print("worked")
            print(word)

# Program entry point
if __name__ == "__main__":
    dictFile = sys.argv[1]
    startWord = sys.argv[2]
    targetWord = sys.argv[3]
    main(dictFile, startWord, targetWord)

