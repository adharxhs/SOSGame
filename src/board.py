class Board:
    """Generates the board for SOS board Game 
    and handles insert,print,remove,validity checks and game state check"""
    emptyCell="-"
    def __init__(self,maxboardsize):
        self.MAX_BOARD_SIZE=maxboardsize
        self.board_array=[[self.emptyCell for j in range(self.MAX_BOARD_SIZE)] for i in range(self.MAX_BOARD_SIZE)]   
    
    def getEmptyCellRep(self):
        return self.emptyCell
    

    def getMAXSIZE(self):
        return self.MAX_BOARD_SIZE
    
    
    def getCell(self,i,j):
        return self.board_array[i][j]
    
    
    def isFull(self):
        """Checks whether all slots in the board is filled by players"""
        for i in range(self.MAX_BOARD_SIZE):
            for j in range(self.MAX_BOARD_SIZE):
                if(self.board_array[i][j]==self.emptyCell):
                    return False
        return True
    
    
    def validIndexCheck(self,i,j):
        """Checks validity of given row and col index for insertions and match checking,return"""
        if(i>=0 and i <self.MAX_BOARD_SIZE and j>=0 and j<self.MAX_BOARD_SIZE):
            return True
        else:
            return False
    
    
    def validSymbolCheck(self,symb):
        """Checks validity of given symbol when  input is taken,returns true symbol is valid"""
        symb=symb.upper()
        if(symb!="S" and symb!="O"):
            return False
        else:
            return True
    
    
    def insert(self,i,j,symb):
        """Inserts symbol symb at location i,j in the board,returns true if successfull,false if failed"""
        if(self.validIndexCheck(i,j) and self.validSymbolCheck(symb)):
            if(self.board_array[i][j] == self.emptyCell):
                self.board_array[i][j]=symb.upper()
                return True
        return False
        
        
    def remove(self,i,j):
        """Removes value at location i,j and sets it to empty,returns true id successfull"""
        if(self.validIndexCheck(i,j)):
                self.board_array[i][j]=self.emptyCell
                return True
        else:
            return False
        
    def checkForMatches(self,i,j,symb):
        """Checks for a match in valid locations around i,j
        and updates score if match is found,returns 0 otherwise"""
        if not(self.validSymbolCheck(symb) and self.validIndexCheck(i,j)):
            return 0
        matches=0
        if(symb=="S"):    
            #row left
            if(self.validIndexCheck(i,j-1) and self.validIndexCheck(i,j-2)):
                if(self.board_array[i][j-1]=="O" and self.board_array[i][j-2]=="S"):
                    matches+=1
            #row right
            if(self.validIndexCheck(i,j+1) and self.validIndexCheck(i,j+2)):
                if(self.board_array[i][j+1]=="O" and self.board_array[i][j+2]=="S"):
                    matches+=1
            #col up 
            if(self.validIndexCheck(i-1,j) and self.validIndexCheck(i-2,j)):
                if(self.board_array[i-1][j]=="O" and self.board_array[i-2][j]=="S"):
                    matches+=1
            #col down
            if(self.validIndexCheck(i+1,j) and self.validIndexCheck(i+2,j)):
                if(self.board_array[i+1][j]=="O" and self.board_array[i+2][j]=="S"):
                    matches+=1
            #diag top left
            if(self.validIndexCheck(i-1,j-1) and self.validIndexCheck(i-2,j-2)):
                if(self.board_array[i-1][j-1]=="O" and self.board_array[i-2][j-2]=="S"):
                    matches+=1
            #diag top right
            if(self.validIndexCheck(i-1,j+1) and self.validIndexCheck(i-2,j+2)):
                if(self.board_array[i-1][j+1]=="O" and self.board_array[i-2][j+2]=="S"):
                    matches+=1
            #diag bottom left
            if(self.validIndexCheck(i+1,j-1) and self.validIndexCheck(i+2,j-2)):
                if(self.board_array[i+1][j-1]=="O" and self.board_array[i+2][j-2]=="S"):
                    matches+=1
            #diag bottom right
            if(self.validIndexCheck(i+1,j+1) and self.validIndexCheck(i+2,j+2)):
                if(self.board_array[i+1][j+1]=="O" and self.board_array[i+2][j+2]=="S"):
                    matches+=1
        else:    
            #row 
            if(self.validIndexCheck(i,j-1) and self.validIndexCheck(i,j+1)):
                if(self.board_array[i][j-1]=="S" and self.board_array[i][j+1]=="S"):
                    matches+=1
            #col
            if(self.validIndexCheck(i-1,j) and self.validIndexCheck(i+1,j)):
                if(self.board_array[i-1][j]=="S" and self.board_array[i+1][j]=="S"):
                    matches+=1
            #diag left
            if(self.validIndexCheck(i-1,j-1) and self.validIndexCheck(i+1,j+1)):
                if(self.board_array[i-1][j-1]=="S" and self.board_array[i+1][j+1]=="S"):
                    matches+=1
            #diag right
            if(self.validIndexCheck(i-1,j+1) and self.validIndexCheck(i+1,j-1)):
                if(self.board_array[i-1][j+1]=="S" and self.board_array[i+1][j-1]=="S"):
                    matches+=1
        return matches