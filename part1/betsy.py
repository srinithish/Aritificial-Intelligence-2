#!/usr/bin/env python3


# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 13:10:56 2018

@author: nithish k
"""


"""
Board States : is a list of lists and in literal , the list ends at when there is no pebble. 
We do not represent a empty slot with a '.' 
State space :
    All possible arrangements of the pebbles successively on the boards
Successor function:
    
    first checks if we have enough pebbles 
    Drops the pebbles in the columns that have spaces
    and rotates the columns
edge weights: in the graph are uniform for each move ,

evaluation function : 
1. we check if a max or min player is present in a row/column/diagonal 
that row column is not favaourable for the opposite player
2. there after if more than n/2 symbols present in a row ,diagonal then it means that atleast 
one of the symbol is adjacent and hence more favourable for the particular player
3.Since entire column comes into consideration while rotating , we consider entire column and 
check if the player being considered has more than n+3/2 pebles and mark it favourable
4. and in the we subtract the favourable for max and favourable for min and return it as the evaluation value

Terminal state : when any of the player has n consequitive pebbles in row colum or diagonal
Apart from the evaluation function when the returned values are equal, I take into considration the 
path that led to the value and its length to decide for max and min,
if max I choose the min path length to make the move
if min I choose the max path lenght to make the moves



    
    



"""
try:
    import queue 
except:
    import Queue 
    
import random
import sys
import threading
from collections import Counter
from collections import defaultdict
import multiprocessing as mp

valueQueue = mp.Queue()
try:
    
    n = int(sys.argv[1])
    playerPlaying = sys.argv[2]
    stateOfTheBoardInString = sys.argv[3]
    timeInSeconds = sys.argv[4]
    stepSize = int(timeInSeconds)
    MaxPlayerSymbol = playerPlaying

    if playerPlaying == 'x':
        MinPlayerSymbol = 'o'
    elif playerPlaying == 'o':
        MinPlayerSymbol = 'x'


except:
        
    #defaults
   n = 5
   stateOfTheBoardInString = '...................................ox.ox'

   
   MaxPlayerSymbol = 'x'
   MinPlayerSymbol = 'o'
   


widthOfBoard = n
heightOfBoard = n+3
EmptyPlaceSymbol = '.'
terminalStateReturnValue = 100000
maxRecursionDepth = 225

boardFull = False
#stateOfTheBoardInString = 'o.oxoxoxoxxoxxxoxo'
#stateOfTheBoardInString = '..oxoxxxoxooxxxoxo'
#stateOfTheBoardInString = '..x.oxxxoxoooxoxxo'


    
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



def changeBoardToString(BoardAsListOfList):
    boardString  = ''
    for row in range(heightOfBoard-1,-1,-1):
        
        for column in range( widthOfBoard):

            try:
               boardString  +=  BoardAsListOfList[column][row]
               

            except:
                boardString += '.'
                
    return boardString


#print(changeBoardToString(testState))
    
def countTotalPebbles(boardState):
    global boardFull
    dictOfColumnCount = defaultdict(int)
    dictOfCounter = defaultdict(int)
    for column in boardState:
        dictOfCounter = dict(Counter(column))
        try:
#            print(dictOfColumnCount)
            dictOfColumnCount[MaxPlayerSymbol] += dictOfCounter[MaxPlayerSymbol]
        except:
            pass
        
    
    
    if dictOfColumnCount[MaxPlayerSymbol] >= (widthOfBoard* heightOfBoard) / 2:
        boardFull = True

countTotalPebbles(boardState)


def dropMove(boardState,column,player):
    ##generates a combinations for column a column  and specified player
    
    if len(boardState[column]) < heightOfBoard:
        newBoardState = boardState[0:column]+[boardState[column]+[player]]+boardState[column+1:]
        if newBoardState != boardState:
            return (newBoardState,column+1) #state and the movemade
 
#testState = dropMove(boardState,0,'x')[0]


def rotateMove(boardState,column,player):
    
    
    try:
        newBoardState = boardState[0:column] + [boardState[column][1:]+[boardState[column][0]]]+ boardState[column+1:]
    
        if newBoardState != boardState:
            return (newBoardState,-(column+1))#state and the movemade
    except:
        pass

def successors(boardState, player):
    dropSucc = []
    if not boardFull :
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
    ###triied two different functions 
    
    ###favourable rows columns of max - min
    FavourableMax = 0
    FavourableMin = 0
#    Function to check if more number of x or o are present
    def MaxExistence(consideredPositionList,FavourableMax,FavourableMin,CountMax,CountMin,n):
       
        if len(consideredPositionList) > 1:
            for symbol in consideredPositionList:
                if symbol == MaxPlayerSymbol:
                    CountMax +=1
                if symbol == MinPlayerSymbol:
                    CountMin +=1
            
            
            if CountMax > (n/2 ):
                FavourableMax +=1
               
            if CountMin > (n/2):
                FavourableMin +=1
               
        return FavourableMax,FavourableMin    
    
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
        CountMax = 0
        CountMin = 0         
        #changig  column list considered
        consideredPositionList = boardState[column]
        FavourableMax,FavourableMin=CheckExistence(consideredPositionList,FavourableMax,FavourableMin,MaxExists,MinExists)
        FavourableMax,FavourableMin=MaxExistence(consideredPositionList,FavourableMax,FavourableMin,CountMax,CountMin,widthOfBoard+3)
        
    #####check rows
    for row in range(3,heightOfBoard):##iterate over row
        MaxExists = False
        MinExists = False 
        CountMax = 0
        CountMin = 0
        AllRowElements=[]
        for column in range(widthOfBoard):
            
         ##not to throw index error
            try :
                AllRowElements = AllRowElements + [boardState[column][row]]
            except IndexError: 
                pass
        FavourableMax,FavourableMin=CheckExistence(AllRowElements,FavourableMax,FavourableMin,MaxExists,MinExists)
        FavourableMax,FavourableMin=MaxExistence(AllRowElements,FavourableMax,FavourableMin,CountMax,CountMin,widthOfBoard)
        
        
        ###adding wiegths 
        FavourableMax = FavourableMax
        FavourableMin = FavourableMin
    
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
            fwdDiag = fwdDiag + [boardState[boardColumn][(heightOfBoard - 1) - boardRow+3]]                             #/
        except:
            pass
        #check for all elemets being equla

    MaxExists = False
    MinExists = False
    CountMax = 0
    CountMin = 0 
    FavourableMax,FavourableMin=CheckExistence(bwdDiag,FavourableMax,FavourableMin,MaxExists,MinExists)
    FavourableMax,FavourableMin=MaxExistence(bwdDiag,FavourableMax,FavourableMin,CountMax,CountMin,widthOfBoard)

    MaxExists = False
    MinExists = False
    CountMax = 0
    CountMin = 0 
    FavourableMax,FavourableMin=CheckExistence(fwdDiag,FavourableMax,FavourableMin,MaxExists,MinExists)
    FavourableMax,FavourableMin=MaxExistence(fwdDiag,FavourableMax,FavourableMin,CountMax,CountMin,widthOfBoard)    
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
                
                return terminalStateReturnValue ,MoveSoFar
            if MinPlayerSymbol in wins:
                return - terminalStateReturnValue , MoveSoFar
            
         #returns value
    
    
    elif DepthSoFar > horizon:
        MaxFavourable,MinFavourable = evaluationFunc(boardStateAndMove[0])
        return MaxFavourable-MinFavourable,MoveSoFar
    

    for successorBoard , move in successors(boardStateAndMove[0],MaxPlayerSymbol):
        MoveSoFarPlusCurrentMove = MoveSoFar + "_" + str(move)
      
        
        newEvaluationValue,path = chooseMin((successorBoard,MoveSoFarPlusCurrentMove),horizon,currentAlpha,currentBeta)
        
        listOfUtilityValues.append(newEvaluationValue)
        listOfPaths.append(path)
        
        currentAlpha = max(currentAlpha,newEvaluationValue)
        if newEvaluationValue >= currentBeta:
            
            break
        
        
        
        
         #update alpha if the the loop hasnt broken
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

                return - terminalStateReturnValue ,MoveSoFar
            
            if MaxPlayerSymbol in wins:
            
                return terminalStateReturnValue , MoveSoFar
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
        
        currentBeta = min(currentBeta,newEvaluationValue)
        if newEvaluationValue <= currentAlpha:
            
            break
            
        
    return min(listOfUtilityValues),listOfPaths[listOfUtilityValues.index(min(listOfUtilityValues))]









def MiniMaxAB(boardState,horizon):
    alpha = - float("inf")
    beta = float("inf")
    
    ListOfBoardAndMove = []

    
    
    for successorBoard , move in successors(boardState,MaxPlayerSymbol):
#        MoveSoFarPlusCurrentMove = MoveSoFar + "_" + str(move)
      
        
        newEvaluationValue ,path = chooseMin((successorBoard,str(move)),horizon,alpha,beta)
#        print("evaluation Value :" ,newEvaluationValue)
#        print("Board  :" ,successorBoard)
#        print("Path :",path)
        
        if newEvaluationValue >= alpha :
            
            alpha = newEvaluationValue
            bestMove = successorBoard
            maxPath = path
            ListOfBoardAndMove.append((bestMove,maxPath,len(maxPath),newEvaluationValue))
   
   
    #if i have equal maximum evaluation values make a raandom choice
#    ListWithMaxPathLengths = 
    if all([tup[3] < 0 for tup in ListOfBoardAndMove ]):
        random.shuffle(ListOfBoardAndMove)
        ListOfBoardAndMove.sort(key= lambda x : x[2],reverse = True )
        
    elif all([tup[3] >= 0 for tup in ListOfBoardAndMove ]):
        random.shuffle(ListOfBoardAndMove)
        ListOfBoardAndMove.sort(key= lambda x : x[2],reverse = False )
        
        
    bestMove,maxPath,maxPathLen,evaluationValue = ListOfBoardAndMove[0]
    
    return bestMove , maxPath


#print(MiniMaxAB(boardState,20))
    

#boardState[1] = boardState[2] + ['o']

#print(is_terminal(boardState))
#
#print(chooseMax((boardState,0),10,- float("inf"),float("inf")))

def findBestMoveIterativelyMultiProcessing(step):
    try:
        for horizon in range(0,maxRecursionDepth,step):

            try:
                value = valueQueue.get(block=False)
            except queue.Empty :
                
               
                bestBoard = changeBoardToString(MiniMaxAB(boardState,horizon)[0])
                bestMove = MiniMaxAB(boardState,horizon)[1].split("_")[0]
                print(bestMove ," " , bestBoard )
            
            else: 
                break                
                
    except RecursionError :
        print("depth too much")
    
def findBestMoveIteratively(step):
    try:
        for horizon in range(0,maxRecursionDepth,step):


            
           
            bestBoard = changeBoardToString(MiniMaxAB(boardState,horizon)[0])
            bestMove = MiniMaxAB(boardState,horizon)[1].split("_")[0]
            print(bestMove ," " , bestBoard )
           
                
    except RecursionError :
        print("depth too much")


def findBestMoveDirect():
#    print("bestMove : ", MiniMaxAB(boardState,10))
    try:

        for horizon in range(0,maxRecursionDepth,20):
#            print("Horizon : ",horizon)
            bestBoard = changeBoardToString(MiniMaxAB(boardState,horizon)[0])
            bestMove = MiniMaxAB(boardState,horizon)[1].split("_")[1]
            print(bestMove ," " , bestBoard )
            valueQueue.put(bestBoard)
    
    except RecursionError :
        print("depth too much")

#threadIterative = mp.Process(target = findBestMoveIteratively)
#threadDirect = mp.Process(target = findBestMoveDirect)
#
#threadIterative.start()
#threadIterative.join()
##threadDirect.start()
#threadIterative.start()

#valueQueue.put(1)
findBestMoveIteratively(7)
#findBestMoveDirect()
##print(evaluationFunc(boardState))
#print(MiniMaxAB(boardState,5))