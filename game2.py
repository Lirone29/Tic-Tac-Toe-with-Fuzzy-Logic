# Tic Tac Toe
from math import floor
import random
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def evaluate(position, board, letter, angle):
    if letter == 'X':
        opponent = 'O'
    else:
        opponent = 'X';
    sum = 1;

    if angle == 'r':
        for i in range(floor(position / 3), floor(position / 3) + 4, 1):
            if board[i] == letter:
                sum = sum * 0.9;
            elif board[i] == opponent:
                sum = sum * 0.1;
            else:
                sum = sum * 1;
        return sum;

    elif angle == 'c':

        if (position % 3) == 1:
            firstColumn = 1;
        elif (position % 3) == 2:
            firstColumn = 2;
        else:
            firstColumn = 0;

        for i in range(firstColumn, firstColumn + 7, 3):
            if board[i] == letter:
                sum = sum * 0.9;
            elif board[i] == opponent:
                sum = sum * 0.1;
            else:
                sum = sum * 1;

        return sum;

    elif angle == 'd':
        # print("In diag ");
        # print(position)
        diagA = [1, 5, 9]
        diagB = [3, 5, 7]

        if position in diagA:
            for i in range(1, 10, 4):
                # print("In diag A");
                # print(sum)
                if board[i] == letter:
                    sum = sum * 0.9;
                elif board[i] == opponent:
                    sum = sum * 0.1;
                else:
                    sum = sum * 1;
        if position in diagB:
            for i in range(3, 8, 2):
                # print("In diag B");
                # print(sum);
                if board[i] == letter:
                    sum = sum * 0.9;
                elif board[i] == opponent:
                    sum = sum * 0.1;
                else:
                    sum = sum * 1;
        else:
            return 0;

        return sum;

    else:
        return 0;


def drawBoard(board):
    # This function prints out the board that it was passed.
    # "board" is a list of 10 strings representing the board (ignore index 0)
    print(board[1] + '|' + board[2] + '|' + board[3])
    print('-+-+-')
    print(board[4] + '|' + board[5] + '|' + board[6])
    print('-+-+-')
    print(board[7] + '|' + board[8] + '|' + board[9])


def inputPlayerLetter():
    # Lets the player type which letter they want to be.
    # Returns a list with the player's letter as the first item, and the computer's letter as the second.
    letter = ''
    while not (letter == 'X' or letter == 'O'):
        print("Do you want to be 'X' or 'O'?")
        letter = input().upper()

    if letter == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


def whoGoesFirst():
    print('Do you want to go first? (Yes or No)')
    if input().lower().startswith('y'):
        return 'player'
    else:
        return 'computer'
    '''
	# Randomly choose the player who goes first.
	if random.randint(0,1) == 0:
		return 'computer'
	else:
		return 'player'
	'''


def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False.
    print('Do you want to play again? (Yes or No)')
    return input().lower().startswith('y')


def makeMove(board, letter, move):
    board[move] = letter


def isWinner(board, letter):
    # Given a board and a player's letter, this function returns True if that player has won.
    return ((board[1] == letter and board[2] == letter and board[3] == letter) or
            (board[4] == letter and board[5] == letter and board[6] == letter) or
            (board[7] == letter and board[8] == letter and board[9] == letter) or
            (board[1] == letter and board[4] == letter and board[7] == letter) or
            (board[2] == letter and board[5] == letter and board[8] == letter) or
            (board[3] == letter and board[6] == letter and board[9] == letter) or
            (board[1] == letter and board[5] == letter and board[9] == letter) or
            (board[3] == letter and board[5] == letter and board[7] == letter))


def getBoardCopy(board):
    # Make a duplicate of the board list and return it the duplicate.
    dupBoard = []

    for i in board:
        dupBoard.append(i)

    return dupBoard


def isSpaceFree(board, move):
    return board[move] == ' '


def getPlayerMove(board):
    # Let the player type in their move.
    move = ''
    while move not in '1 2 3 4 5 6 7 8 9'.split() or not isSpaceFree(board, int(move)):
        print('What is your next move? (1-9)')
        move = input()
    return int(move)

def useFuzzyLogic(row_value, column_value, diagonal_value):
    # calculate value
    # New Antecedent/Consequent objects hold universe variables and membership functions

    row = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'row')
    column = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'column')
    diagonal = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'diagonal')
    result = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'result')

    # Auto-membership function population is possible with .automf(3, 5, or 7)
    # row.automf(3)

    # Generate fuzzy membership functions
    result['false'] = fuzz.trimf(result.universe, [0, 0, 1])
    result['true'] = fuzz.trimf(result.universe, [0, 1, 1])

    row['false'] = fuzz.trimf(row.universe, [0, 0, 1])
    row['true'] = fuzz.trimf(row.universe, [0, 1, 1])

    column['false'] = fuzz.trimf(column.universe, [0, 0, 1])
    column['true'] = fuzz.trimf(column.universe, [0, 1, 1])

    diagonal['false'] = fuzz.trimf(diagonal.universe, [0, 0, 1])
    diagonal['true'] = fuzz.trimf(diagonal.universe, [0, 1, 1])

    row.view()
    column.view()
    diagonal.view()

    rule1 = ctrl.Rule(column['true'] & diagonal['true'] & row['true'], result['true'])

    rule2 = ctrl.Rule(row['true'] & column['true'], result['true'])

    rule3 = ctrl.Rule(row['true'] & diagonal['true'], result['true'])

    rule4 = ctrl.Rule(column['true'] & diagonal['true'], result['true'])

    rule5 = ctrl.Rule(column['false'] & diagonal['false'] & row['false'], result['false'])

    rule6 = ctrl.Rule(column['false'] & row['false'], result['false'])

    rule7 = ctrl.Rule(diagonal['false'] & row['false'], result['false'])

    rule8 = ctrl.Rule(column['false'] & diagonal['false'], result['false'])

    result_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8])
    end_result = ctrl.ControlSystemSimulation(result_ctrl)

    # Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
    # Note: if you like passing many inputs all at once, use .inputs(dict_of_data)

    end_result.input['row'] = row_value;
    end_result.input['column'] = column_value;
    end_result.input['diagonal'] = diagonal_value;

    # Crunch the numbers
    end_result.compute();

    print(end_result.output['result'])
    result.view(sim=end_result);

    return end_result.output['result'];


def findBestMove(theBoard, computerLetter):
	possibleMoves = [];
	values = np.empty(9);
	values.fill(-1);
	print("IN");

	if (computerLetter == 'X'): playerLetter = 'O';
	else: playerLetter = 'X';

	for i in range(1, 10):
		if isSpaceFree(theBoard, i): possibleMoves.append(i);
		#print(i);

	for i in possibleMoves:
		print("Board NUmber")
		print(i);
		row = evaluate(i, theBoard, computerLetter, "r");
		column = evaluate(i, theBoard, computerLetter, "c");
		diagonal = evaluate(i, theBoard, computerLetter, "d");
		print("Row")
		print(row)
		print(column)
		print(diagonal)
		fuzzyLogic = useFuzzyLogic(row, column, diagonal);
		print("Fuzzy Logic")
		#print(fuzzyLogic);
		values[i-1] = fuzzyLogic;
	maximum = np.amax(values);

	print("Maximum")
	print(maximum)
	print("Index")
	print(np.argmax(values)+1);

	return np.argmax(values)+1;


def isBoardFull(board):
    # Return True if every space on the board has been taken. Otherwise return False.
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True


print('\nWelcome to Tic Tac Toe!\n')
print('Reference of numbering on the board')
drawBoard('0 1 2 3 4 5 6 7 8 9'.split())
print('')
a = np.empty(9)
a.fill(-1)
#print(a)
#print(a[1])
#computerLetter = 'X';
theBoard = [' '] * 10
#theBoard[1] = "X";
#theBoard[2] = "O";
#theBoard[5] = "X";
#theBoard[9] = "O";

# test
#findBestMove(theBoard, computerLetter)


while True:
    # Reset the board
    theBoard = [' '] * 10
    playerLetter, computerLetter = inputPlayerLetter()
    turn = whoGoesFirst()
    print('The ' + turn + ' will go first.')
    gameIsPlaying = True

    while gameIsPlaying:
        if turn == 'player':
            drawBoard(theBoard)
            move = getPlayerMove(theBoard)
            makeMove(theBoard, playerLetter, move)

            if isWinner(theBoard, playerLetter):
                drawBoard(theBoard)
                print('You won the game')
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('The game is a tie')
                    break
                else:
                    turn = 'computer'
        else:
            move = findBestMove(theBoard, computerLetter)
            makeMove(theBoard, computerLetter, move)

            if isWinner(theBoard, computerLetter):
                drawBoard(theBoard)
                print('You lose the game')
                gameIsPlaying = False
            else:
                if isBoardFull(theBoard):
                    drawBoard(theBoard)
                    print('The game is a tie')
                    break
                else:
                    turn = 'player'
    if not playAgain():
        break
        
