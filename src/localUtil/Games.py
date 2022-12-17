class Game:
    def __init__(self):
        pass
    
    def __str__(self):
        return 'this is a game object'


def minimax(gameState, evalFunc):
    """
    A recursive implementation of the mini-max algorithm.
    
    Args:
        gameState: The current state of the game.
        evalFunc: A function that takes a game state and returns a numeric score
                  indicating how good that state is for the current player.
    
    Returns:
        The best move to make in the current game state.
    """
    
    # Initialize the best score and best move to None.
    bestScore = float("-inf")
    bestMove = None
    
    # Loop over all possible moves in the current game state.
    for move in gameState.possibleMoves():
        
        # Apply the current move to the game state to create a new state.
        newState = gameState.applyMove(move)
        
        # Recursively compute the best move in the new state.
        score = minimax(newState, evalFunc)
        
        # If the score for the current move is better than the best score so far,
        # update the best score and best move.
        if score > bestScore:
            bestScore = score
            bestMove = move
    
    # Return the best move that was found.
    return bestMove


class GameState:
    def __init__(self, grid):
        """
        Initialize a new game state with the given grid of values.
        
        Args:
            grid: A 2D list of integers representing the values in the game grid.
        """
        self.grid = grid

    def getGrid(self):
        """
        Return the current grid of values.
        
        Returns:
            A 2D list of integers representing the values in the game grid.
        """
        return self.grid

    def applyMove(self, move):
        """
        Apply the given move to the game state and return a new game state.
        
        Args:
            move: A tuple (i, j) representing the position of the cell to move.
        
        Returns:
            A new game state with the updated grid of values.
        """
        i, j = move
        grid = [row[:] for row in self.grid]  # Make a deep copy of the grid.
        grid[i][j] = 0  # Apply the move to the copied grid.
        return GameState(grid)  # Return a new game state with the updated grid.

    def possibleMoves(self):
        """
        Return a list of all possible moves that can be made in the current game state.
        
        Returns:
            A list of tuples (i, j) representing the positions of the cells that can be moved.
        """
        moves = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] != 0:
                    moves.append((i, j))
        return moves
        
        
class ConnectFour:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]
        self.currentPlayer = 1
        
    def __repr__(self):
        
        return "\n".join(str(row) for row in self.grid)

    def __str__(self):
       
        return self.__repr__()

    def dropPiece(self, col):
        if col < 0 or col >= self.cols:
            return None
        for row in range(self.rows-1, -1, -1):
            if self.grid[row][col] == 0:
                self.grid[row][col] = self.currentPlayer
                return (row, col)
        return None

    def checkWin(self):
        for row in range(self.rows):
            for col in range(self.cols-3):
                if self.grid[row][col] == self.currentPlayer and self.grid[row][col+1] == self.currentPlayer and self.grid[row][col+2] == self.currentPlayer and self.grid[row][col+3] == self.currentPlayer:
                    return True
        for row in range(self.rows-3):
            for col in range(self.cols):
                if self.grid[row][col] == self.currentPlayer and self.grid[row+1][col] == self.currentPlayer and self.grid[row+2][col] == self.currentPlayer and self.grid[row+3][col] == self.currentPlayer:
                    return True
        for row in range(self.rows-3):
            for col in range(self.cols-3):
                if self.grid[row][col] == self.currentPlayer and self.grid[row+1][col+1] == self.currentPlayer and self.grid[row+2][col+2] == self.currentPlayer and self.grid[row+3][col+3] == self.currentPlayer:
                    return True
        for row in range(self.rows-3):
            for col in range(3, self.cols):
                if self.grid[row][col] == self.currentPlayer and self.grid[row+1][col-1] == self.currentPlayer and self.grid[row+2][col-2] == self.currentPlayer and self.grid[row+3][col-3] == self.currentPlayer:
                    return True
        return False

    def switchPlayer(self):
        if self.currentPlayer == 1:
            self.currentPlayer = 2
        else:
            self.currentPlayer = 1
