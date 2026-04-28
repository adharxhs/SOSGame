import board
class GameEngine:
    def __init__(self,boardsize,playerCount,mode):
        self.board=board.Board(boardsize)
        self.lastplayer=playerCount
        self.playerScores=[0 for x in range(playerCount)]
        self.currentplayer=1
        self.finalScores=[0 for x in range(playerCount)]
        self.lastMove=[]
        if mode==1:
            self.singlePlayerMode=True
            import bot
            self.bot=bot.Bot(self.board)
        else:
            self.singlePlayerMode=False

    def getSinglePlayerMode(self):
        return self.singlePlayerMode
    
    def getBotMove(self):
        move=self.bot.getMove(self.lastMove)
        return move
    
    def getPlayerScores(self):
        return self.playerScores.copy()
    
    def getCurrentPlayer(self):
        return self.currentplayer
    
    def getBoardCell(self,i,j):
        return self.board.getCell(i,j)
    
    def getBoardSize(self):
        return self.board.getMAXSIZE()
    
    def gameOverCheck(self):
        return self.board.isFull()
    
    def updateCurrentPlayer(self,calledby):
        if calledby=="makeMove" or calledby=="playerQuit":
            if(self.currentplayer<self.lastplayer):
                self.currentplayer+=1
            else:
                self.currentplayer=1
        elif calledby=="cancelMove":
            if(self.currentplayer==1):
                self.currentplayer=self.lastplayer
            else:
                self.currentplayer-=1    
        else:
            return False
        return True        
         
    def makeMove(self,i,j,symb):
        success=self.board.insert(i,j,symb)
        scored=False
        if(success):
            matches=self.board.checkForMatches(i,j,symb)
            self.lastMove.append([i,j,symb])
            if(matches==0):
                success=self.updateCurrentPlayer("makeMove")
            else:
                scored=True
                self.playerScores[self.currentplayer-1]+=matches
        return success,scored
    
    def cancelMove(self,i,j,symb):
        matches=self.board.checkForMatches(i,j,symb)
        success=self.board.remove(i,j)
        if(success):
            self.lastMove.pop()
            if(matches!=0):
                self.playerScores[self.currentplayer-1]-=matches
                return success
            success=self.updateCurrentPlayer("cancelMove")
        return success
    
    def allPlayersQuitCheck(self):
        return all(x is None for x in self.playerScores)
    
    
    def updateQuittingPlayerScore(self,i):
        self.finalScores[i]= self.playerScores[i]
        self.playerScores[i]=None    
        
    def getFinalScores(self):
        return [ x if x is not None else self.finalScores[i] for i,x in enumerate(self.playerScores)]

