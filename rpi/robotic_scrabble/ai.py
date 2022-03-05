'''
    File taken from: https://github.com/adampirog/Scrabble and slightly modified
    All credit goes to the original author
'''

from Trie import import_dictionary
from Trie import index_to_char
from Trie import char_to_index


import random
import string
import time


def get_left_limit(board, row, column):

    if(column == 0):
        return 0

    for i in range(0, column+1):
        if(board[row][column-i-1] != "-"):
            if(i == 1 and column-i-2 > 0):
                return 0
            return i-1

    return i


def transpose(array):
    return list(map(list, zip(*array)))


def intersection(lst1, lst2):

    if(len(lst2) == 0):
        return ['!']

    if(len(lst1) == 0):
        return lst2

    if(lst1 == ['!'] or lst2 == ['!']):
        return ['!']

    temp = set(lst2)
    lst3 = [value for value in lst1 if value in temp]
    return lst3


def get_cross_checks(board, dictionary):

    cross_checks = [[[]for i in range(15)]for j in range(15)]

    for i in range(len(board)):
        for j in range(len(board[0])):

            # check on top of the word
            if(i+1 < 15 and board[i][j] == '-' and board[i+1][j] != '-'):
                letters = []
                k = i+1
                word = ""
                while(k < 15 and board[k][j] != "-"):
                    word += board[k][j]
                    k += 1
                if(len(word) > 0):
                    for letter in range(26):
                        newWord = index_to_char(letter)+word
                        if(dictionary.is_word(newWord) == True):
                            letters += index_to_char(letter)

                    cross_checks[i][j] = intersection(
                        cross_checks[i][j], letters)

            # check at the bottom of the word
            if(i-1 > -1 and board[i][j] == '-' and board[i-1][j] != '-'):
                letters = []
                k = i-1
                word = ""
                while(k > -1 and board[k][j] != "-"):
                    word += board[k][j]
                    k -= 1
                if(len(word) > 0):
                    word = word[::-1]
                    for letter in range(26):
                        newWord = word+index_to_char(letter)
                        if(dictionary.is_word(newWord) == True):
                            letters += index_to_char(letter)

                    cross_checks[i][j] = intersection(
                        cross_checks[i][j], letters)

    return cross_checks


def get_anchors(board, dictionary):
    # anchor is [row,column]
    anchors = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if(board[i][j] != '-'):
                if(j+1 < 15 and board[i][j+1] == '-'):
                    anchors.append([i, j+1])
                if(j-1 > 0 and board[i][j-1] == '-'):
                    anchors.append([i, j-1])

                if(i+1 < 15 and board[i+1][j] == '-'):
                    anchors.append([i+1, j])
                if(i-1 > 0 and board[i-1][j] == '-'):
                    anchors.append([i-1, j])
    return anchors


def extend_right(partial_word, node, square_row, square_column, legal_moves, rack, cross_checks, board):
    if(square_column < 15 and square_row < 15):
        if(board[square_row][square_column] == '-'):
            if(node.isTerminal == True):
                legal_moves.append([partial_word, square_row, square_column])
            for childIndex in range(26):
                if(node.children[childIndex] != None):
                    if(index_to_char(childIndex) in rack):
                        if(cross_checks[square_row][square_column] == [] or (index_to_char(childIndex) in cross_checks[square_row][square_column])):
                            rack.remove(index_to_char(childIndex))
                            extend_right(partial_word+index_to_char(childIndex),
                                         node.children[childIndex], square_row, square_column+1, legal_moves, rack, cross_checks, board)
                            rack.append(index_to_char(childIndex))
        else:
            if(node.children[char_to_index(board[square_row][square_column])] != None):
                extend_right(partial_word+board[square_row][square_column],
                             node.children[char_to_index(board[square_row][square_column])], square_row, square_column+1, legal_moves, rack, cross_checks, board)
    elif(square_column == 16 or square_row == 16):
        if(node.isTerminal == True):
            legal_moves.append([partial_word, square_row, square_column])


def left_part(partial_word, node, limit, square_row, square_column, legal_moves, rack, cross_checks, board):
    if(limit >= 0):
        extend_right(partial_word, node, square_row,
                     square_column, legal_moves, rack, cross_checks, board)

        if(limit > 0):
            for childIndex in range(26):
                if(node.children[childIndex] != None):
                    if(index_to_char(childIndex) in rack):
                        rack.remove(index_to_char(childIndex))
                        left_part(partial_word+index_to_char(childIndex),
                                  node.children[childIndex], limit-1, square_row, square_column, legal_moves, rack, cross_checks, board)
                        rack.append(index_to_char(childIndex))


def get_random_rack():
    rack = []
    for i in range(8):
        rack.append(random.choice(string.ascii_lowercase))
    return rack


def evaluate_moves(moves):
    if(len(moves) == 0):
        return []
    longest = moves[0]
    for item in moves:
        if(item == []):
            continue
        if(longest == [] or len(item[0]) > len(longest[0])):
            longest = item

    return longest


def make_move(board, move):
    word = move[0]
    length = len(word)
    for i in range(length):
        board[move[1]][move[2]-1-i] = word[length-i-1]
        word = word[:-1]
    return


def make_best_move(board, rack, dictionary):
    # row moves
    anchors = get_anchors(board, dictionary)
    cross_checks = get_cross_checks(board, dictionary)
    globalMoves = []

    for item in anchors:
        legal_moves = []
        left_part("", dictionary.root, get_left_limit(board, item[0], item[1]),
                  item[0], item[1], legal_moves, rack, cross_checks, board)
        globalMoves.append(evaluate_moves(legal_moves))

    rowMove = evaluate_moves(globalMoves)

    # transposed - column moves
    board = transpose(board)
    cross_checks = get_cross_checks(board, dictionary)
    globalMoves = []

    for item in anchors:
        legal_moves = []
        left_part("", dictionary.root, get_left_limit(board, item[1], item[0]),
                  item[1], item[0], legal_moves, rack, cross_checks, board)
        globalMoves.append(evaluate_moves(legal_moves))

    columnMove = evaluate_moves(globalMoves)

    if(len(rowMove[0]) > len(columnMove[0])):
        board = transpose(board)
        make_move(board, rowMove)
    else:
        make_move(board, columnMove)
        board = transpose(board)

    return board


def main():
    board_file = "board.csv"
    dictionary_file = "DictionaryENG.txt"

    dictionary = import_dictionary(dictionary_file, "")
    board = import_board(board_file)
    rack = get_random_rack()

    print(rack)
    draw(board)
    board = make_best_move(board, rack, dictionary)
    draw(board)


if __name__ == "__main__":
    main()
