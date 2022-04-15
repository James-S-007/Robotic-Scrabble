'''
    File taken from: https://github.com/adampirog/Scrabble and slightly modified
    All credit goes to the original author
'''

from Trie import index_to_char, char_to_index

import os.path
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from vision import Camera

import random
import string

class AI:

    def __init__(self, cam_num=2):
        self.rack=[None]*7
        self.score = 0
        self.camera = Camera.Camera(cam_num)

    def get_left_limit(self, board, row, column):
        if column == 0:
            return 0

        for i in range(0, column + 1):
            if board[row][column-i-1] != "-":
                if i == 1 and column - i - 2 > 0:
                    return 0
                return i-1

        return i


    def transpose(self, array):
        return list(map(list, zip(*array)))


    def intersection(self, lst1, lst2):
        if len(lst2) == 0:
            return ['!']

        if len(lst1) == 0:
            return lst2

        if lst1 == ['!'] or lst2 == ['!']:
            return ['!']

        temp = set(lst2)
        lst3 = [value for value in lst1 if value in temp]
        return lst3


    def get_cross_checks(self, board, dictionary):
        cross_checks = [[[]for i in range(15)]for j in range(15)]
        for i in range(len(board)):
            for j in range(len(board[0])):

                # check on top of the word
                if i + 1 < 15 and board[i][j] == '-' and board[i+1][j] != '-':
                    letters = []
                    k = i+1
                    word = ""
                    while k < 15 and board[k][j] != "-":
                        word += board[k][j]
                        k += 1
                    if len(word) > 0:
                        for letter in range(26):
                            newWord = index_to_char(letter)+word
                            if dictionary.is_word(newWord) == True:
                                letters += index_to_char(letter)

                        cross_checks[i][j] = self.intersection(cross_checks[i][j], letters)

                # check at the bottom of the word
                if i-1 > -1 and board[i][j] == '-' and board[i-1][j] != '-':
                    letters = []
                    k = i-1
                    word = ""
                    while k > -1 and board[k][j] != "-":
                        word += board[k][j]
                        k -= 1
                    if len(word) > 0:
                        word = word[::-1]
                        for letter in range(26):
                            newWord = word+index_to_char(letter)
                            if dictionary.is_word(newWord) == True:
                                letters += index_to_char(letter)

                        cross_checks[i][j] = self.intersection(cross_checks[i][j], letters)

        return cross_checks


    def get_anchors(self, board, dictionary):
        # anchor is [row,column]
        anchors = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] != '-':
                    if j+1 < 15 and board[i][j+1] == '-':
                        anchors.append([i, j+1])
                    if j-1 > 0 and board[i][j-1] == '-':
                        anchors.append([i, j-1])

                    if i+1 < 15 and board[i+1][j] == '-':
                        anchors.append([i+1, j])
                    if i-1 > 0 and board[i-1][j] == '-':
                        anchors.append([i-1, j])
        return anchors


    def extend_right(self, partial_word, node, square_row, square_column, legal_moves, cross_checks, board, temp_rack):
        if square_column < 15 and square_row < 15:
            if board[square_row][square_column] == '-':
                if node.isTerminal == True:
                    legal_moves.append([partial_word, square_row, square_column])
                for childIndex in range(26):
                    if node.children[childIndex] != None:
                        if index_to_char(childIndex) in temp_rack:
                            if (cross_checks[square_row][square_column] == [] or (index_to_char(childIndex) in cross_checks[square_row][square_column])):
                                temp_rack.remove(index_to_char(childIndex))
                                self.extend_right(partial_word+index_to_char(childIndex),
                                            node.children[childIndex], square_row, square_column+1, legal_moves, cross_checks, board, temp_rack)
                                temp_rack.append(index_to_char(childIndex))
            else:
                if node.children[char_to_index(board[square_row][square_column])] != None:
                    self.extend_right(partial_word+board[square_row][square_column],
                                node.children[char_to_index(board[square_row][square_column])], square_row, square_column+1, legal_moves, cross_checks, board, temp_rack)
        elif square_column == 16 or square_row == 16:
            if node.isTerminal:
                legal_moves.append([partial_word, square_row, square_column])


    def left_part(self, partial_word, node, limit, square_row, square_column, legal_moves, cross_checks, board, temp_rack):
        if limit >= 0:
            self.extend_right(partial_word, node, square_row,
                        square_column, legal_moves, cross_checks, board, temp_rack)

            if limit > 0:
                for childIndex in range(26):
                    if node.children[childIndex] != None:
                        if index_to_char(childIndex) in temp_rack:
                            temp_rack.remove(index_to_char(childIndex))
                            self.left_part(partial_word+index_to_char(childIndex),
                                    node.children[childIndex], limit-1, square_row, square_column, legal_moves, cross_checks, board, temp_rack)
                            temp_rack.append(index_to_char(childIndex))


    def get_random_rack(self):
        self.rack = []
        for i in range(8):
            self.rack.append(random.choice(string.ascii_lowercase))


    def evaluate_moves(self, moves):
        if len(moves) == 0:
            return []
        longest = moves[0]
        for item in moves:
            if item == []:
                continue
            if longest == [] or len(item[0]) > len(longest[0]):
                longest = item

        return longest


    def make_word(self, board, move):
        word = move[0]
        length = len(word)
        for i in range(length):
            board[move[1]][move[2]-1-i] = word[length-i-1]
            word = word[:-1]
        return


    def make_best_word(self, board, dictionary):
        # row moves
        temp_rack = self.rack.copy()  # will be modified throughout, need copy to pass
        anchors = self.get_anchors(board, dictionary)
        cross_checks = self.get_cross_checks(board, dictionary)
        globalMoves = []

        for item in anchors:
            legal_moves = []
            self.left_part("", dictionary.root, self.get_left_limit(board, item[0], item[1]),
                    item[0], item[1], legal_moves, cross_checks, board, temp_rack)
            globalMoves.append(self.evaluate_moves(legal_moves))

        rowMove = self.evaluate_moves(globalMoves)

        # transposed - column moves
        board = self.transpose(board)
        cross_checks = self.get_cross_checks(board, dictionary)
        globalMoves = []

        for item in anchors:
            legal_moves = []
            self.left_part("", dictionary.root, self.get_left_limit(board, item[1], item[0]),
                    item[1], item[0], legal_moves, cross_checks, board, temp_rack)
            globalMoves.append(self.evaluate_moves(legal_moves))

        columnMove = self.evaluate_moves(globalMoves)
        word_made = ""
        if len(rowMove[0]) > len(columnMove[0]):
            board = self.transpose(board)
            self.make_word(board, rowMove)
            word_made = rowMove[0]
        else:
            self.make_word(board, columnMove)
            board = self.transpose(board)
            word_made = columnMove[0]

        return board, word_made


    # Record pieces added to board by comparing old board and previous board for AI opponent
    # return --> dict: {rack piece: location [row, col], ...}
    def record_moves(self, prev_board, new_board):
        moves = {}
        for i in range(0, len(prev_board)):
            for j in range(0, len(prev_board)):
                if prev_board[i][j] != new_board[i][j]:
                    moves[new_board[i][j]] = [i, j]
        
        # verify all new letters in racks
        for move in moves.keys():
            if move not in self.rack:
                print(f'ERR: added letter {move}, not in rack {self.rack}')
                return {}
        return moves

    # AI makes best possible move and updates board
    # returns --> dict: {
        # "moves": dict: {letter, [row, col], ...},
        # "word": word played,
        # "score": score of word played }
    def generate_move(self, board, game_rules):
        ai_move = {}
        new_board, ai_move["word"] = self.make_best_word(board.board, game_rules.dictionary)
        ai_move["moves"] = self.record_moves(board.board, new_board)
        if not ai_move["moves"]:
            ai_move["word"] = ""  # word made not compatible with rack
        ai_move["score"] = game_rules.score_word(ai_move["word"])
        board.board = new_board
        return ai_move

    # Converts dict of moves to be made from letters to index in the rack
        # Input moves: dict: {letter: [board row, board col], ...}
        # returns --> dict: {rack_idx: [board row, board col], ...}
    def letters_to_rack_idx(self, moves):
        positional_moves = {}
        temp_rack = self.rack.copy()
        for letter, board_moves in moves.items():
            rack_idx = temp_rack.index(letter)
            temp_rack[rack_idx] = None  # mark letter as taken
            positional_moves[rack_idx] = board_moves
        return positional_moves

    # new_pieces: {rack_idx: letter, rack_idx: letter, ...}
    def update_state(self, new_pieces, word_score):
        for idx, letter in new_pieces.items():
            self.rack[idx] = letter
        self.score += word_score
