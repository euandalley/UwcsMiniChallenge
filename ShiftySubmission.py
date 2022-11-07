#!/usr/bin/env python

from sys import maxsize


# BASE OPERATIONS

def shiftRight(w):
  return w[1:] + w[0]


def shiftLeft(w):
  return w[-1] + w[:-1]


def letterShift(w):
  output = set()

  for k, l in enumerate(w):
    l1 = ord(l)+1 if ord(l) < 90 else 65
    l2 = ord(l)-1 if ord(l) > 65 else 90
    
    output.add(w[:k] + chr(l1) + w[k+1:])
    output.add(w[:k] + chr(l2) + w[k+1:])

  return output


def dupLeft(w):
  return w[0] + w


def delLeft(w):
  return w[1:]


# COMPOUNDED OPERATIONS


def getToLength(w1, w2): # Get form of w1 with same length as w2

  l1 = len(w1)
  l2 = len(w2)

  if l1 == l2:
    return w1

  elif l1 < l2:
    for _ in range(l2-l1):
      w1 = dupLeft(w1)

  else:
    for _ in range(l1-l2):
      w1 = delLeft(w1)

  return w1



def shiftWord(w, x): #Shift word left or right
  if x:
    return shiftRight(w)
  else:
    return shiftLeft(w)



# ====================================================================
# WORDS SCORES
# A measure of how close the word is to the target word


def calcLetterCycle(w1, w2): #Calc the number of letter cycles to match word

  shiftCount = 0

  for i in range(len(w1)):
    
    l1 = ord(w1[i]) # Get ASCII val of letters
    l2 = ord(w2[i])

    shift = abs(l1 - l2)

    shiftCount += min(shift, 26-shift)

  return shiftCount



def shiftCount(w1, w2): #Min no. of shifts needed

  n = len(w1)
  shiftCount = maxsize
  x = True

  for _ in range(2):
    x = not x
    for i in range(n):
      letterCount = calcLetterCycle(w1, w2) + i
      # print(w1, w2, letterCount) #Debug
      shiftCount = min(letterCount, shiftCount)
      w1 = shiftWord(w1, x)

  return shiftCount



def calcWordScore(w, w2): #Calc a score for each word, lower is better

  score = 0

  if len(w) == 0:
    return 0

  elif len(w) != len(w2):
    w1 = getToLength(w, w2)
    score += abs(len(w) - len(w2))

  else:
    w1 = w

  score += calcLetterCycle(w1, w2)

  return score



def calcScoresForTree(tree, w2, scores=dict()):

  if tree == dict():
    return dict()


  for w in tree:
    scores[w] = calcWordScore(w, w2)
    scores.update(calcScoresForTree(tree[w], w2))

  return scores
      



# ====================================================================
# NEXT STEP
# Getting the next possible step of a word


def generateLetterShiftSet(w):

  output = set()

  for i, l in enumerate(w):

    l1 = ord(l)
    l2 = ord(l)

    l1 = l1+1 if l1 < 90 else 65
    l2 = l2-1 if l2 > 65 else 90

    w1 = w[:i] + chr(l1) + w[i+1:]
    w2 = w[:i] + chr(l2) + w[i+1:]

    output = output | {w1, w2}

  return output



def generateNextStepSet(w): #Set of words made after one step

  output = set()

  output.add(dupLeft(w))
  output.add(delLeft(w))
  output.add(shiftLeft(w))
  output.add(shiftRight(w))
  output = output | generateLetterShiftSet(w)

  return (output - {'', w})



# ====================================================================
# TREE
# Creating a tree of possible steps



def expandTree(w, w2, step, branch=set()):

  if step < 1 or w == w2:
    return dict()

  nextStepSet = generateNextStepSet(w) - branch

  nextStepDict = dict.fromkeys(nextStepSet, dict())

  for key in nextStepDict.keys():
    nextStepDict[key] = expandTree(key, w2, step-1, branch | {w})

  return nextStepDict



def extendTreeBranches(tree, w2, branch=set()):

  for w in tree:
    
    if tree[w] != dict():
      tree[w] = extendTreeBranches(tree[w], w2, branch | {w})

    elif w != w2:
      nextStepSet = (generateNextStepSet(w) - {w}) - branch
      nextStepDict = dict.fromkeys(nextStepSet, dict())
      tree[w] = nextStepDict
      calcScoresForTree(tree[w], w2)

  return tree

    



def createTree(w, w2, noOfSteps=5):

  return { w: expandTree(w, w2, noOfSteps) }



def calcBestMove(tree, scores):

  if tree == dict():
    return ([], 100000)

  branchScores = []

  for w in tree:
    if tree[w] == dict():
      branchScores.append(([w], scores[w]))
    else:
      branchScores.append(calcBestMove(tree[w], scores))

  branchScores.sort(key=lambda x: (len(x[0]), scores[x[0][0]]))

  bestMove = branchScores[0]
  bestMove[0].append(w)

  return bestMove


# ====================================================================
# MAIN

def getSequence(w1, w2):

  currentStep = w1
  sequence = [w1]

  tree = createTree(currentStep, w2, 3)
  scores = calcScoresForTree(tree, w2)

  

  while (currentStep != w2):
    print(tree)
    print(sequence)
    nextStep = calcBestMove(tree[currentStep], scores)[0][0]
    sequence.append(nextStep)
    tree = extendTreeBranches(tree[currentStep], w2)
    scores = calcScoresForTree(tree, w2, scores)
    currentStep = nextStep

  output = ""

  for s in sequence:
    output += (s + " ")

  print(output[:-1])


# ====================================================================

# TEST
w1 = "A"
w2 = "FEED"

# a = createTree(w1, w2, 1)
# scores = calcScoresForTree(a, w2)

# print(a)

# print(calcBestMove(a, scores))

getSequence(w1, w2)



# SUBMISSION

# t = int(input())

# for _ in range(t):
#   w1, w2 = input().split()
#   getSequence(w1, w2)

