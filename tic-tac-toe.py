#---TIC TAC TOE WITH MINIMAX & ALPHA BETA PRUNING-------------------


#----------The player choose if he wants to be x or 0
def ChoosePlayer():
    ok = False
    while ok == False:
        choice = input("If you want to be X press 1 or if you want to be 0 press 0: ")
        if choice == '1':
            #print("You are X!")
            ok = True
        elif choice == '0':
            #print("You are 0!")
            ok = True
        else: 
            print("You pressed the wrong choice")
    return int(choice)


#----Initialize the game board
def InitializeGame():
    m = [['*' for _ in range(3)] for _ in range(3)]
    return m

#---Print the game board
def print_board(board):
    for row in board:
        print(" ".join(row))

#---Verify if there are any moves left
def isMovesLeft(board):
    for i in range(3):
        for j in range(3):
            if (board[i][j] == '*'):
                return True
    return False

#---Player move 
def playerMove(board, player):
    ok = 0
    while ok == 0:
        print("Enter the row and column where you want to place your move")
        row = int(input("Enter row (0-2): "))
        col = int(input("Enter column (0-2): "))
        if 0<=row <=2 and 0<=col<=2:
            if board[row][col] == '*':
                board[row][col] = player
                ok = 1
            else:
                print("Invalid move. Cell already occupied.")
        else:
            print("Invalid input. Row and column values must be between 0 and 2.")

#---Evaluation function (returns 10 if bot wins, -10 if player wins, 0 if it's a tie, 
#this is used in the minimax function to evaluate the board at each step of the game)
def evaluate(b, player, bot) :  
    # Checking for Rows for X or O victory.  
    for row in range(3) :      
        if (b[row][0] == b[row][1] and b[row][1] == b[row][2]) :         
            if (b[row][0] == bot) : 
                return 10
            elif (b[row][0] == player) : 
                return -10
  
    # Checking for Columns for X or O victory.  
    for col in range(3) : 
       
        if (b[0][col] == b[1][col] and b[1][col] == b[2][col]) : 
          
            if (b[0][col] == bot) :  
                return 10
            elif (b[0][col] == player) : 
                return -10
  
    # Checking for Diagonals for X or O victory.  
    if (b[0][0] == b[1][1] and b[1][1] == b[2][2]) : 
      
        if (b[0][0] == bot) : 
            return 10
        elif (b[0][0] == player) : 
            return -10
  
    if (b[0][2] == b[1][1] and b[1][1] == b[2][0]) : 
      
        if (b[0][2] == bot) : 
            return 10
        elif (b[0][2] == player) : 
            return -10
  
    # Else if none of them have won then return 0  
    return 0
  

#---Minimax algorithm with alpha-beta pruning
def minimax(board, depth, isMax, player, bot, alpha, beta) :  
    score = evaluate(board, player, bot) 
  
    # If Maximizer has won the game return his/her  
    # evaluated score  
    if (score == 10) :  
        return score 
  
    # If Minimizer has won the game return his/her  
    # evaluated score  
    if (score == -10) : 
        return score 
  
    # If there are no more moves and no winner then  
    # it is a tie  
    if (isMovesLeft(board) == False) : 
        return 0
  
    # If this maximizer's move  
    if (isMax) :      
        best = -1000 
  
        # Traverse all cells  
        for i in range(3) :          
            for j in range(3) : 
               
                # Check if cell is empty  
                if (board[i][j]=='*') : 
                  
                    # Make the move  
                    board[i][j] = bot  
  
                    # Call minimax recursively and choose  
                    # the maximum value  
                    best = max( best, minimax(board, 
                                              depth + 1, 
                                              not isMax, player, bot, alpha, beta) ) 
                    # Undo the move  
                    board[i][j] = '*'
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
        return best 
  
    # If this minimizer's move  
    else : 
        best = 1000 
  
        # Traverse all cells  
        for i in range(3) :          
            for j in range(3) : 
               
                # Check if cell is empty  
                if (board[i][j] == '*') : 
                  
                    # Make the move  
                    board[i][j] = player  
  
                    # Call minimax recursively and choose  
                    # the minimum value  
                    best = min(best, minimax(board, depth + 1, not isMax, player, bot, alpha, beta)) 
  
                    # Undo the move  
                    board[i][j] = '*'

                    beta = min(beta, best)
                    if beta <= alpha:
                        break
        return best 

# This will return the best possible move for the bot  
def findBestMove(board, player, bot) :  
    bestVal = -1000 
    bestMove = (-1, -1)  
  
    # Traverse all cells, evaluate minimax function for  
    # all empty cells. And return the cell with optimal  
    # value.  
    for i in range(3) :      
        for j in range(3) : 
          
            # Check if cell is empty  
            if (board[i][j] == '*') :  
              
                # Make the move  
                board[i][j] = bot 
  
                # compute evaluation function for this  
                # move.  
                moveVal = minimax(board, 0, False, player, bot, -1000, 1000)  
  
                # Undo the move  
                board[i][j] = '*' 
  
                # If the value of the current move is  
                # more than the best value, then update  
                # best/  
                if (moveVal > bestVal) :                 
                    bestMove = (i, j) 
                    bestVal = moveVal 
  
    #print("The value of the best Move is :", bestVal) 
    #print() 
    return bestMove 

#---Bot move
# the bot will choose the best possible move using the minimax algorithm
def botMove(board, opponent, player):
    ok = 0
    bestMove = findBestMove(board, player, opponent)
    board[bestMove[0]][bestMove[1]] = opponent
    
#---Decide who's turn is next
def next_turn(player, opponent, last, board):
    #last == '' when the game starts (the first move)
    if last == player or (last == '' and player == '0'):
        botMove(board, opponent, player)
        last = opponent
    else:
        playerMove(board, player)
        last = player
    return last

    

#---Decide the winner when the game is over
def decideWinner(board):
    for row in range(3):
        if (board[row][0] == board[row][1] and board[row][1] == board[row][2]):
            if (board[row][0] == 'X'):
                print("X wins!")
                return True
            elif (board[row][0] == '0'):
                print("0 wins!")
                return True
    for col in range(3):
        if (board[0][col] == board[1][col] and board[1][col] == board[2][col]):
            if (board[0][col] == 'X'):
                print("X wins!")
                return True
            elif (board[0][col] == '0'):
                print("0 wins!")
                return True
    if (board[0][0] == board[1][1] and board[1][1] == board[2][2]):
        if (board[0][0] == 'X'):
            print("X wins!")
            return True
        elif (board[0][0] == '0'):
            print("0 wins!")
            return True
    if (board[0][2] == board[1][1] and board[1][1] == board[2][0]):
        if (board[0][2] == 'X'):
            print("X wins!")
            return True
        elif (board[0][2] == '0'):
            print("0 wins!")
            return True
    if isMovesLeft(board) == False:
        print("It's a tie!")
        return True
    return False


def main():
    choice = ChoosePlayer()
    if choice == 1:
        print("You are X!")
        print("Bot is 0!")
        min = 'X'
        max = '0'
        #depth = 8
    elif choice == 0:
        print("You are 0!")
        print("Bot is X!")
        min = '0'
        max = 'X'
        #depth = 9
    last = ''
    m = InitializeGame()
    check_winner = False
    #print("Current board:")
    #print_board(m)
    #playerMove(m, min)
    #print("Board after your move:")
    #print_board(m)
    while isMovesLeft(m) and check_winner != True:
        print("Current board:")
        print_board(m)
        last = next_turn(min, max, last, m)
        
        check_winner = decideWinner(m)
        #print(check_winner)
    #decideWinner(m)
    print("Final board:")
    print_board(m)
            

if __name__ == "__main__":
    main()
# In this version, we are going to implement the game in a way that the user can choose if he wants to be X or 0
# We are going to use the ChoosePlayer function to do that
# We are going to use the main function to call the ChoosePlayer function and then print the result
# We are going to use the if __name__ == "__main__": to call the main function
# We are going to use the input function to get the user's choice
    
    