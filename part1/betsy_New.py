
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 13:10:56 2018

@author: nithish k
"""


import sys
import threading

n = 3
widthOfBoard = n
heightOfBoard = n+3
stateOfTheBoardInString = '...x..o.ox.oxxxoxo'
#stateOfTheBoardInString = 'o.oxoxoxoxxoxxxoxo'
#stateOfTheBoardInString = '..oxoxxxoxooxxxoxo'
#stateOfTheBoardInString = '..x.oxxxoxoooxoxxo'

MaxPlayerSymbol = 'x'
MinPlayerSymbol = 'o'
EmptyPlaceSymbol = '.'

maxRecursionDepth = 225
def changeBoardToColumnList(stateOfTheBoardInString):
    ##initialise the board with empty lists
    listOfColumns = [[] for column in range(widthOfBoard)]
    
    for position,playerMark in enumerate(reversed(stateOfTheBoardInString)):
        if playerMark != EmptyPlaceSymbol:
#            print(n-1-(position%n))
            listOfColumns[widthOfBoard-1-(position%widthOfBoard)].append(playerMark)
    
    return listOfColumns

#dict of lists have chose 
boardState = changeBoardToColumnList(stateOfTheBoardInString)
#Board = {column :  for (column,ColumnList) in zip }


def dropMove(boardState,column,player):
    ##generates a combinations for column a column  and specified player
    
    if len(boardState[column]) < heightOfBoard:
        newBoardState = boardState[0:column]+[boardState[column]+[player]]+boardState[column+1:]
        if newBoardState != boardState:
            return (newBoardState,column+1) #state and the movemade
 
def rotateMove(boardState,column,player):
    
    newBoardState = boardState[0:column] + [boardState[column][1:]+[boardState[column][0]]]+ boardState[column+1:]

    if newBoardState != boardState:
        return (newBoardState,-(column+1))#state and the movemade


def successors(boardState, player):
    
    dropSucc = [dropMove(boardState,column,player) for column in range(widthOfBoard) if dropMove(boardState,column,player) !=None]
    rotateSucc = [rotateMove(boardState,column, player) for column in range(widthOfBoard) if rotateMove(boardState,column,player) !=None]
    return dropSucc + rotateSucc     #list of both rotate and dropmoves with the move made

#### for checing terminal state
def checkColumns(boardState,lengthsOfColumns):
    ##returns player/s  and the column of  win
    ## greedy need to change DS if wins from different columns make a difference
    
    

    AllWinsPlayerAndColumn = {}
    for column in range(widthOfBoard):
        lengthsOfColumns[column] = len(boardState[column]) # can skip this if globally calculated
       
        if lengthsOfColumns[column] == heightOfBoard:
            consideredPositionList = boardState[column][3:]
            if(consideredPositionList.count(consideredPositionList[0]) == heightOfBoard - 3): #ignored rows
                #if something is there and if the enrty was not made then enter it and return of since you already
                #have two wins
                #optimistaion to not complete all the loops when 2 wins from different players are already achieved
                if  bool(AllWinsPlayerAndColumn) and boardState[column][3] not in AllWinsPlayerAndColumn: 
                    AllWinsPlayerAndColumn[boardState[column][3]] = column
                    return AllWinsPlayerAndColumn
                AllWinsPlayerAndColumn[boardState[column][3]] = column
                
    return AllWinsPlayerAndColumn # change if needed  



def checkRows(boardState,lengthsOfColumns):
     #would fail outside terminal fnc due to dependency on lengths of Columns
     ##returns player/s  and the row of  win
    
    AllWinsPlayerAndRow = {}
    minLengthColumn  = min(lengthsOfColumns.values())
    
    if minLengthColumn >= 4:
        for row in range(3,minLengthColumn):##iterate over row
            
            for column in range(widthOfBoard):
                
                if column+1 <= widthOfBoard-1: ##not to throw index error
                    
                    if(boardState[column][row] != boardState[column+1][row]):
                         
                         break
                     
                else:
                     AllWinsPlayerAndRow[boardState[column][row]] = row
                     if(bool(AllWinsPlayerAndRow) and boardState[column][row] not in AllWinsPlayerAndRow): 
                    ##index has reached till the end without breaking so, all elemets are equal
                    
                         AllWinsPlayerAndRow[boardState[column][row]] = row
                         return AllWinsPlayerAndRow
    return AllWinsPlayerAndRow                 
 
    
def checkDiagonal(boardState,lengthsOfColumns):
    AllWinsPlayerAndDiagonal = {}

        #forward diagonal
    fwdDiag = [] #\#+1
    bwdDiag = [] #/#-1
    for boardColumn, boardRow in zip(range(widthOfBoard), range(3,heightOfBoard)):
        try:
            bwdDiag = bwdDiag + [boardState[boardColumn][boardRow]]
        except IndexError:
            pass
#            distOfCurrentRowFrmCenter = (boardRow - (heightOfBoard))//2
        try:
            fwdDiag = fwdDiag + [boardState[boardColumn][(heightOfBoard - 1) - boardRow + 3]]                             #/
        except IndexError: 
            pass
    #check for all elemets being equla
    if len(set(fwdDiag)) == 1  and len(fwdDiag) == widthOfBoard:
        AllWinsPlayerAndDiagonal[fwdDiag[0]] = 'fwdDiag'
        
    if len(set(bwdDiag)) == 1 and len(bwdDiag) == widthOfBoard :
        AllWinsPlayerAndDiagonal[bwdDiag[0]] = 'bwdDiag'
#        print(AllWinsPlayerAndDiagonal)
    return AllWinsPlayerAndDiagonal
                


def is_terminal(boardState,playerWhoPlayed= None): #is a draw or a win to keep track of whose win
    
    #board state as tuple of (baord, move)
    lengthsOfColumns = {}    
    ##iterate for row only till the shortest column
    ## for colun need to iterate all
    ## keep in memory the player who played the last so that if the change causes a win for 
    
    
    AllWinsPlayerAndColumn = checkColumns(boardState,lengthsOfColumns) #fills lengths of columns
    AllWinsPlayerAndRow = checkRows(boardState,lengthsOfColumns) #takes in lengths of columns manipulated byy checkColumns
    AllWinsPlayerAndDiagonal  = checkDiagonal(boardState,lengthsOfColumns)
    
    if bool(AllWinsPlayerAndColumn) or bool(AllWinsPlayerAndRow) or bool(AllWinsPlayerAndDiagonal):
        return AllWinsPlayerAndColumn,AllWinsPlayerAndRow,AllWinsPlayerAndDiagonal #dict of player and the row/column where the player won
    
    return False
    

    

def evaluationFunc(boardState):
    
    ###favourable rows columns of max - min
    FavourableMax = 0
    FavourableMin = 0
    #Function to check existence and increment favourability
    def CheckExistence(consideredPositionList,FavourableMax,FavourableMin,MaxExists,MinExists):
        if consideredPositionList == [] :
            FavourableMax +=1
            FavourableMin +=1        
        else:
#            print(column)
            try:
                consideredPositionList.index(MaxPlayerSymbol)             
            except ValueError:
                MaxExists = False             
            else:           
                MaxExists = True             
            ######
            
            try:
                consideredPositionList.index(MinPlayerSymbol)
            except ValueError:
                MinExists = False             
            else:             
                MinExists = True         
            #####
            
            if MinExists and not MaxExists:
                FavourableMin+=1
                
            if MaxExists and not MinExists:
                FavourableMax+=1
        return FavourableMax,FavourableMin
        
    #check columns 
    for column in range(widthOfBoard):
        MaxExists = False
        MinExists = False
        
        consideredPositionList = boardState[column][3:]
        FavourableMax,FavourableMin=CheckExistence(consideredPositionList,FavourableMax,FavourableMin,MaxExists,MinExists)

    #####check rows
    for row in range(3,heightOfBoard):##iterate over row
        MaxExists = False
        MinExists = False
        AllRowElements=[]
        for column in range(widthOfBoard):
            
         ##not to throw index error

            try :
                AllRowElements = AllRowElements + [boardState[column][row]]
            except IndexError: 
                pass
        FavourableMax,FavourableMin=CheckExistence(AllRowElements,FavourableMax,FavourableMin,MaxExists,MinExists)

    
        #forward diagonal
    fwdDiag = [] #\#+1
    bwdDiag = [] #/#-1
        
    for boardColumn, boardRow in zip(range(widthOfBoard), range(3,heightOfBoard)):
        try:
            bwdDiag = bwdDiag + [boardState[boardColumn][boardRow]]
#            distOfCurrentRowFrmCenter = (boardRow - (heightOfBoard))//2
        except:
            pass
        
        try:
            fwdDiag = fwdDiag + [boardState[boardColumn][(widthOfBoard - 1) - boardRow]]                             #/
        except:
            pass
        #check for all elemets being equla

    MaxExists = False
    MinExists = False
    FavourableMax,FavourableMin=CheckExistence(bwdDiag,FavourableMax,FavourableMin,MaxExists,MinExists)
    MaxExists = False
    MinExists = False
    FavourableMax,FavourableMin=CheckExistence(fwdDiag,FavourableMax,FavourableMin,MaxExists,MinExists)
#         
#        
#        
        
    return FavourableMax,FavourableMin
                
def chooseMax(boardStateAndMove,horizon,currentAlpha,currentBeta):
    #choose max value of all max successors 
    #but the values of them are arrived from min choosing the mimum
    #at every new value that is backed up frm the leaf if the new value is gretaer than present beta
    # the tree will not be explored , break expanding thos successors and return the current value
#    
#    global count 
#    
#    count+=1
#    print(count)
#    print(boardStateAndMove)
    
  
    listOfUtilityValues = []
    listOfPaths = []
    MoveSoFar = str(boardStateAndMove[1])
    DepthSoFar = len(MoveSoFar.split("_"))
    
    terminalWins = is_terminal(boardStateAndMove[0])
   
    if bool(terminalWins):
#        print(terminalWins)
#        print(boardStateAndMove[0])
            
        for wins in terminalWins:
#            print("Moves so far: ", MoveSoFar)
            
            
            if MaxPlayerSymbol in wins:
                
                return 1000 ,MoveSoFar
            if MinPlayerSymbol in wins:
                return -1000 , MoveSoFar
            
         #returns value
    
    
    elif DepthSoFar > horizon:
        MaxFavourable,MinFavourable = evaluationFunc(boardStateAndMove[0])
        return MaxFavourable-MinFavourable,MoveSoFar
    

    for successorBoard , move in successors(boardStateAndMove[0],MaxPlayerSymbol):
        MoveSoFarPlusCurrentMove = MoveSoFar + "_" + str(move)
      
        
        newEvaluationValue,path = chooseMin((successorBoard,MoveSoFarPlusCurrentMove),horizon,currentAlpha,currentBeta)
        
        listOfUtilityValues.append(newEvaluationValue)
        listOfPaths.append(path)
        if newEvaluationValue >= currentBeta:
            
            break
        
        
        
        currentAlpha = max(currentAlpha,newEvaluationValue) #update alpha if the the loop hasnt broken
    return max(listOfUtilityValues),listOfPaths[listOfUtilityValues.index(max(listOfUtilityValues))]
    


def chooseMin(boardStateAndMove,horizon,currentAlpha,currentBeta):
    #choose min value of all the mins successors
    #but the values of the mins successors are arrived from the max choosing the maximums
    ##at ever new value that is backed up frm the leaf if the new value is less than the present alpha
    #the branch will not be explored
#    print("min :" , boardStateAndMove)
    listOfUtilityValues = []
    listOfPaths = []
    MoveSoFar = str(boardStateAndMove[1])
    DepthSoFar = len(MoveSoFar.split("_"))
    
    terminalWins = is_terminal(boardStateAndMove[0])
    if bool(terminalWins):
        for wins in terminalWins:
            
            
           
            if MinPlayerSymbol in wins:

                return -1000 ,MoveSoFar
            
            if MaxPlayerSymbol in wins:
            
                return 1000 , MoveSoFar
            #returns wins of 
    
    elif DepthSoFar > horizon:
        MaxFavourable,MinFavourable = evaluationFunc(boardStateAndMove[0])
        return MaxFavourable -MinFavourable,MoveSoFar
     #get the moves part 
    
    
    
    for successorBoard , move in successors(boardStateAndMove[0],MinPlayerSymbol):
        MoveSoFarPlusCurrentMove = MoveSoFar + "_" + str(move)
        newEvaluationValue , path = chooseMax((successorBoard,MoveSoFarPlusCurrentMove),horizon,currentAlpha,currentBeta)
        listOfUtilityValues.append(newEvaluationValue)
        listOfPaths.append(path)
        
        
        if newEvaluationValue <= currentAlpha:
            
            break
        currentBeta = min(currentBeta,newEvaluationValue)    
        
    return min(listOfUtilityValues),listOfPaths[listOfUtilityValues.index(min(listOfUtilityValues))]









def MiniMaxAB(boardState,horizon):
    alpha = - float("inf")
    beta = float("inf")

    for successorBoard , move in successors(boardState,MaxPlayerSymbol):
#        MoveSoFarPlusCurrentMove = MoveSoFar + "_" + str(move)
      
        
        newEvaluationValue ,path = chooseMin((successorBoard,'_'+str(move)),horizon,alpha,beta)
#        print(newEvaluationValue)
        if newEvaluationValue > alpha:
            alpha = newEvaluationValue
            bestMove = successorBoard
            maxPath = path
#    evaluationValue = chooseMax((boardState,0),horizon,alpha,beta)
    
    return bestMove , maxPath


#MiniMaxAB(boardState,None)
    

#boardState[1] = boardState[2] + ['o']

#print(is_terminal(boardState))

#print(chooseMax((boardState,0),10,- float("inf"),float("inf")))

def findBestMoveIteratively():
    try:
        for horizon in range(0,maxRecursionDepth,4):
            print("Horizon : ",horizon)
            print("bestMove : ", MiniMaxAB(boardState,horizon))
    
    except RecursionError :
        print("depth too much")
        


def findBestMoveDirect():
#    print("bestMove : ", MiniMaxAB(boardState,10))
    try:
        for horizon in range(0,maxRecursionDepth,9):
            print("Horizon : ",horizon)
            print("bestMove : ", MiniMaxAB(boardState,horizon))
    
    except RecursionError :
        print("depth too much")

threadIterative = threading.Thread(target = findBestMoveIteratively)
threadDirect = threading.Thread(target = findBestMoveDirect)
threadDirect.start()
threadIterative.start()

print(evaluationFunc(boardState))
