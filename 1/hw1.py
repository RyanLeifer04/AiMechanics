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

#BFS search through dictionary to find path, returns None is no path is found
def search(word1, word2, dictionary):
    visited = set(word1)
    visited.add(word1)
    currentWord = word1
    queue = [(word1,[word1])]
    while queue:
        currentWord, path = queue.pop(0)
        for i in range(len(word1)):
            for a in 'abcdefghijklmnopqrstuvwxyz':
                next = currentWord[:i] + a + currentWord[i+1:]
                
                if currentWord == word2:
                    return path
                
                if next in dictionary and next not in visited:
                    queue.append((next, path+[next]))
                    visited.add(next)
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
            print(word)

if __name__ == "__main__":
    dictFile = sys.argv[1]
    startWord = sys.argv[2]
    targetWord = sys.argv[3]
    main(dictFile, startWord, targetWord)

