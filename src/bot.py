import random
import board
class Bot:
    def __init__(self, board: board):
        self.board = board

    def getMove(self, lastMove):
        move = self.tryScore()
        if move: return move
        move = self.tryBlock(lastMove)
        if move: return move
        move = self.trySetup()
        if move: return move
        return self.fallback()

    def tryScore(self):
        """Tier 1: Find any move that scores immediately"""
        size = self.board.getMAXSIZE()
        best = None
        bestScore = 0
        for i in range(size):
            for j in range(size):
                if self.board.getCell(i, j) != self.board.getEmptyCellRep():
                    continue
                for symb in ["S", "O"]:
                    self.board.insert(i, j, symb)
                    score = self.board.checkForMatches(i, j, symb)
                    self.board.remove(i, j)
                    if score > bestScore:
                        bestScore = score
                        best = (i, j, symb)
        return best

    def tryBlock(self, lastMove: list):
        """Tier 2: Block opponent threats near the last move"""
        if not lastMove:
            return None
        candidates = self.getNearby(lastMove[-1])
        for (i, j) in candidates:
            for symb in ["S", "O"]:
                self.board.insert(i, j, symb)
                threat = self.board.checkForMatches(i, j, symb)
                self.board.remove(i, j)
                if threat > 0:
                    return (i, j, symb)
        return None

    def trySetup(self):
        """Tier 3: Place S or O on the cell with the most adjacent S/O pieces (randomly if tied)"""
        size = self.board.getMAXSIZE()
        best_cells = []
        bestScore = -1
        for i in range(size):
            for j in range(size):
                if self.board.getCell(i, j) != self.board.getEmptyCellRep():
                    continue
                score = self.setupScore(i, j)
                if score > bestScore:
                    bestScore = score
                    best_cells = [(i, j)]
                elif score == bestScore:
                    best_cells.append((i, j))
        if not best_cells:
            return None
        i, j = random.choice(best_cells)
        symb = random.choice(["S", "O"])
        return (i, j, symb)

    def fallback(self):
        """Last resort: pick a random empty cell and random symbol ('S' or 'O')"""
        size = self.board.getMAXSIZE()
        empty_cells = [(i, j) for i in range(size) for j in range(size) if self.board.getCell(i, j) == self.board.getEmptyCellRep()]
        if not empty_cells:
            return None, None, None
        i, j = random.choice(empty_cells)
        symb = random.choice(["S", "O"])
        return (i, j, symb)

    def setupScore(self, i, j):
        """Counts adjacent S/O pieces to score setup potential of a cell"""
        score = 0
        # row left
        if self.board.validIndexCheck(i, j-1):
            c = self.board.getCell(i, j-1)
            score += 1 if c == "S" else 0.5 if c == "O" else 0
        # row right
        if self.board.validIndexCheck(i, j+1):
            c = self.board.getCell(i, j+1)
            score += 1 if c == "S" else 0.5 if c == "O" else 0
        # col up
        if self.board.validIndexCheck(i-1, j):
            c = self.board.getCell(i-1, j)
            score += 1 if c == "S" else 0.5 if c == "O" else 0
        # col down
        if self.board.validIndexCheck(i+1, j):
            c = self.board.getCell(i+1, j)
            score += 1 if c == "S" else 0.5 if c == "O" else 0
        # diag top left
        if self.board.validIndexCheck(i-1, j-1):
            c = self.board.getCell(i-1, j-1)
            score += 1 if c == "S" else 0.5 if c == "O" else 0
        # diag top right
        if self.board.validIndexCheck(i-1, j+1):
            c = self.board.getCell(i-1, j+1)
            score += 1 if c == "S" else 0.5 if c == "O" else 0
        # diag bottom left
        if self.board.validIndexCheck(i+1, j-1):
            c = self.board.getCell(i+1, j-1)
            score += 1 if c == "S" else 0.5 if c == "O" else 0
        # diag bottom right
        if self.board.validIndexCheck(i+1, j+1):
            c = self.board.getCell(i+1, j+1)
            score += 1 if c == "S" else 0.5 if c == "O" else 0
        return score

    def getNearby(self, lastMove: list):
        """Returns empty cells within distance 2 of the last move, per direction"""
        li, lj = lastMove[0], lastMove[1]
        candidates = set()
        # row left
        if self.board.validIndexCheck(li, lj-1) and self.board.getCell(li, lj-1) == self.board.getEmptyCellRep():
            candidates.add((li, lj-1))
        if self.board.validIndexCheck(li, lj-2) and self.board.getCell(li, lj-2) == self.board.getEmptyCellRep():
            candidates.add((li, lj-2))
        # row right
        if self.board.validIndexCheck(li, lj+1) and self.board.getCell(li, lj+1) == self.board.getEmptyCellRep():
            candidates.add((li, lj+1))
        if self.board.validIndexCheck(li, lj+2) and self.board.getCell(li, lj+2) == self.board.getEmptyCellRep():
            candidates.add((li, lj+2))
        # col up
        if self.board.validIndexCheck(li-1, lj) and self.board.getCell(li-1, lj) == self.board.getEmptyCellRep():
            candidates.add((li-1, lj))
        if self.board.validIndexCheck(li-2, lj) and self.board.getCell(li-2, lj) == self.board.getEmptyCellRep():
            candidates.add((li-2, lj))
        # col down
        if self.board.validIndexCheck(li+1, lj) and self.board.getCell(li+1, lj) == self.board.getEmptyCellRep():
            candidates.add((li+1, lj))
        if self.board.validIndexCheck(li+2, lj) and self.board.getCell(li+2, lj) == self.board.getEmptyCellRep():
            candidates.add((li+2, lj))
        # diag top left
        if self.board.validIndexCheck(li-1, lj-1) and self.board.getCell(li-1, lj-1) == self.board.getEmptyCellRep():
            candidates.add((li-1, lj-1))
        if self.board.validIndexCheck(li-2, lj-2) and self.board.getCell(li-2, lj-2) == self.board.getEmptyCellRep():
            candidates.add((li-2, lj-2))
        # diag top right
        if self.board.validIndexCheck(li-1, lj+1) and self.board.getCell(li-1, lj+1) == self.board.getEmptyCellRep():
            candidates.add((li-1, lj+1))
        if self.board.validIndexCheck(li-2, lj+2) and self.board.getCell(li-2, lj+2) == self.board.getEmptyCellRep():
            candidates.add((li-2, lj+2))
        # diag bottom left
        if self.board.validIndexCheck(li+1, lj-1) and self.board.getCell(li+1, lj-1) == self.board.getEmptyCellRep():
            candidates.add((li+1, lj-1))
        if self.board.validIndexCheck(li+2, lj-2) and self.board.getCell(li+2, lj-2) == self.board.getEmptyCellRep():
            candidates.add((li+2, lj-2))
        # diag bottom right
        if self.board.validIndexCheck(li+1, lj+1) and self.board.getCell(li+1, lj+1) == self.board.getEmptyCellRep():
            candidates.add((li+1, lj+1))
        if self.board.validIndexCheck(li+2, lj+2) and self.board.getCell(li+2, lj+2) == self.board.getEmptyCellRep():
            candidates.add((li+2, lj+2))
        return candidates