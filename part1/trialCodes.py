# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 21:15:29 2018

@author: nithish k
"""
import numpy as np
l = [1,2]

l.append([2,3])

for i  in {}:
    print(i)
boardState[0] = ['o', 'x', 'x', 'x', 'x','x']
boardState[1] = ['x', 'x', 'x', 'o', 'o','o']
checkColumns(boardState)
a = {1:23,2:45}
a.values()
min(a.values())
a = np.array([[0,1,2,3], [2,3,4]])
a[[1,2]]


boardState[1] = boardState[1] + ['o','o']
checkColumns(boardState)
checkRows(boardState,lengthsOfColumns) 

[[] for i in range(3)]


    for column in range(widthOfBoard):
        if len(boardState[column]) < heightOfBoard:
            newBoardState = boardState[0:column]+[boardState[column]+[player]]+boardState[column+1:]
            if newBoardState != boardState:
                yield newBoardState

    
def rotateMove(boardState,player):
    
    for column in range(widthOfBoard):
#        boardStateCopy = copy.deepcopy(boardState)
        newBoardState = boardState[0:column] + [boardState[column][1:]+[boardState[column][0]]]+ boardState[column+1:]
#        boardStateCopy[column] = boardStateCopy[column][1:]+ [boardStateCopy[column][0]]
        if newBoardState != boardState:
            yield newBoardState
[i for i in rotateMove(boardState,'x')]




boardState = [['o', 'x', 'x', 'o', 'x','o'], ['x', 'x', 'o', 'o','o','x'], ['o', 'x', 'o', 'x','x','o']]







bool(False)










