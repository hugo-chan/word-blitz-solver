import math
import copy
import random

def get_condensed_dict(board_letters):
    # returns a list of words that are comprised of only letters found on the board

    # load full dictionary
    f = open('wordlist-en.txt', 'r')
    full_dict = set(f.read().splitlines())

    # remove words that have letters not in the boards
    def valid_letters(word):
        # checks whether a word contains only letters found in the board
        for letter in word:
            if letter not in board_letters:
                return False
        return True

    return [word for word in full_dict if valid_letters(word)]


def generate_paths(board_letters):
    # generates the paths of valid words on the board

    assert len(board_letters) in [i ** 2 for i in range(10)] # square number length
    BOARD_LEN = int(math.sqrt(len(board_letters))) 

    # load board
    board = [board_letters[i * BOARD_LEN:(i + 1) * BOARD_LEN] for i in range(BOARD_LEN)]

    condensed_dict = get_condensed_dict(board_letters)
    # add all prefixes of valid words (for optimization purposes, can backtrack early if word is not in prefix dict)
    prefix_dict = [word[:i] for word in condensed_dict for i in range(1, len(word) + 1)] + ['']

    # contains valid words in the board and corresponding paths
    valid_words = []
    valid_paths = []

    visited = [[False for _ in range(BOARD_LEN)] for __ in range(BOARD_LEN)] # to keep track which cells we visited when exploring a path
    directions = [(1, 1), (-1, 1), (1, -1), (-1, -1), (0, -1), (0, 1), (-1, 0), (1, 0)] # direction of neighbors

    def find_words(row_num, col_num, curr_word, path):
        # helper function that DFS the board and checks if word created from the path is valid or not

        if row_num < 0 or row_num >= BOARD_LEN or col_num < 0 or col_num >= BOARD_LEN or visited[row_num][col_num] or curr_word not in prefix_dict:
            # out of bounds or cell is visited in the path already or the word is not in the prefix dict so no point continuing
            return

        # mark current cell as visited
        visited[row_num][col_num] = True

        # update current word and path
        curr_word += board[row_num][col_num]
        path.append((row_num, col_num))

        if curr_word in condensed_dict:
            # valid word
            valid_words.append(curr_word)
            valid_paths.append(copy.deepcopy(path)) # need to deepcopy because python will reuse path variable (pass by reference in python)

        for d in directions:
            # explore neighbors
            row_offset, col_offset = d[0], d[1]
            find_words(row_num + row_offset, col_num + col_offset, curr_word, path)
        
        # unmark visited status for cell after fully DFSing the cell (clean up after itself, beautiful property of recursion)
        visited[row_num][col_num] = False
        # pop cell from path because array is pass by reference instead of value, program will reuse path
        path.pop(-1)

    # finds words that start from each cell of the board
    for i in range(BOARD_LEN):
        for j in range(BOARD_LEN):
            find_words(i, j, curr_word="", path=[])

    assert len(valid_words) == len(valid_paths)
    print("Valid words:", valid_words)
    # shuffle paths so it is not obvious we are....
    random.shuffle(valid_paths)

    return valid_paths