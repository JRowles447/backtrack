from sudoku import Sudoku
import argparse


class CSP_Solver(object):
    """
    This class is used to solve the CSP with backtracking.
    """
    def __init__(self, puzzle_file):
        self.sudoku = Sudoku(puzzle_file)
        self.guesses = 0


    ################################################################
    ### YOU MUST EDIT THIS FUNCTION!!!!!
    ### We will test your code by constructing a csp_solver instance
    ### e.g.,
    ### csp_solver = CSP_Solver('puz-001.txt')
    ### solved_board, num_guesses = csp_solver.solve()
    ### so your `solve' method must return these two items.
    ################################################################
    ########
    #  Use a dictionary for "assignment", map each key (tuple) to a single value
    #
    #
    ########
    def solve(self):
        """
        Solves the Sudoku CSP and returns a list of lists representation
        of the solved sudoku puzzle as well as the number of guesses
        (assignments) required to solve the problem.
        """
        if(self.sudoku.complete()): # Base case, the board is complete
            return self.sudoku, self.guesses

        # State all the valid nums
        order_dom = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        # find the empty space
        (line, pos) = self.find_empty()

        for value in order_dom:
            self.guesses += 1
            if value in self.find_domain(line, pos):
                self.sudoku.board[line][pos] = value
                self.solve()
                if self.sudoku.complete():
                    return self.sudoku.board_str(), self.guesses
                self.sudoku.board[line][pos] = 0
        return None

    def find_empty(self):
        """
        Find an empty space on the board, traversing from left to right and from top to bottom

        :return: a (line_num, pos) coordinate of the empty space
        """
        line_num = 0
        while line_num < 9:
            pos = 0
            while pos < 9:
                if self.sudoku.board[line_num][pos] == 0:
                    return (line_num, pos)
                pos += 1
            line_num += 1
        return None

    def find_domain(self, line_num, pos):
        """
        Find the domain of valid inputs [1, .., 9] for an empty space

        :param line_num: the line number of the empty space
        :param pos: the position of the empty space
        :return: a list of valid inputs for the empty space
        """
        domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # check the row
        for x in self.sudoku.board[line_num]:
            if x in domain:
                domain.remove(x)
        # check the column
        column = [line[pos] for line in self.sudoku.board]
        for x in column:
            if x in domain:
                domain.remove(x)
        # check the box
        rows = self.sudoku.board[((line_num // 3)*3): ((line_num//3)*3 + 3)]
        box = [line[((pos // 3)*3): ((pos // 3)*3 + 3)] for line in rows]
        for x in box:
            for y in x:
                if y in domain:
                    domain.remove(y)
        return domain

class CSP_Solver_MRV(object):
    """
    This class is used to solve the CSP with backtracking and the MRV
    heuristic.
    """
    def __init__(self, puzzle_file):
        self.sudoku = Sudoku(puzzle_file)
        self.guesses = 0

    ################################################################
    ### YOU MUST EDIT THIS FUNCTION!!!!!
    ### We will test your code by constructing a csp_solver instance
    ### e.g.,
    ### csp_solver_mrv = CSP_Solver_MRV('puz-001.txt')
    ### solved_board, num_guesses = csp_solver_mrv.solve()
    ### so your `solve' method must return these two items.
    ################################################################
    def solve(self):
        """
        Solves the Sudoku CSP and returns a list of lists representation
        of the solved sudoku puzzle as well as the number of guesses
        (assignments) required to solve the problem.
        YOU MUST EDIT THIS FUNCTION!!!!!
        """
        # Base case, the board is complete
        if (self.sudoku.complete()):
            return self.sudoku, self.guesses

        # if the mrv is 0, that means that there was a failure
        if self.find_mrv() == None:
            return None

        order_dom = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        (line, pos) = self.find_mrv()
        domain = self.find_domain(line, pos)
        for value in order_dom:
            self.guesses += 1
            if value in domain:
                self.sudoku.board[line][pos] = value
                self.solve()
                if self.sudoku.complete():
                    return self.sudoku.board_str(), self.guesses
                self.sudoku.board[line][pos] = 0
        return None


    def find_mrv(self):
        """
        Finds the mrv and returns the positional coordinates for the board.

        :return: (line number, position)
        """
        empty_spaces = self.find_all_empty()
        # Map tuples to list of valid domain
        domain_list = [self.find_domain(x[0], x[1]) for x in empty_spaces]
        dict = {}
        for x in empty_spaces:
            dict[(x[0], x[1])] = len(self.find_domain(x[0], x[1]))
        # determine the next space to place
        domain_size = 0
        (line, pos) = (-1, -1)
        while domain_size < 10:
            # find the key (coordinate of board) with the most restricted domain and return it
            for key, value in dict.items():
                # return None if there are any spaces with 0, since these are invalid boards
                if value == 0:
                    return None
                if value == domain_size:
                    (line, pos) = key
                    return (line, pos)
            domain_size += 1

    def find_all_empty(self):
        """
        Find an empty space on the board, traversing from left to right and from top to bottom

        :return: a (line_num, pos) coordinate of the empty space
        """
        line_num = 0
        empty_spaces = []
        while line_num < 9:
            pos = 0
            while pos < 9:
                if self.sudoku.board[line_num][pos] == 0:
                    empty_spaces.append((line_num, pos))
                pos += 1
            line_num += 1
        return empty_spaces

    def find_domain(self, line_num, pos):
        """
        Find the domain of valid inputs [1, .., 9] for an empty space

        :param line_num: the line number of the empty space
        :param pos: the position of the empty space
        :return: a list of valid inputs for the empty space
        """
        domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # check the row
        for x in self.sudoku.board[line_num]:
            if x in domain:
                domain.remove(x)
        # check the column
        column = [line[pos] for line in self.sudoku.board]
        for x in column:
            if x in domain:
                domain.remove(x)
        # check the box
        rows = self.sudoku.board[((line_num // 3)*3): ((line_num//3)*3 + 3)]
        box = [line[((pos // 3)*3): ((pos // 3)*3 + 3)] for line in rows]
        for x in box:
            for y in x:
                if y in domain:
                    domain.remove(y)
        return domain


class CSP_Solver_MRV_FC(object):
    """
    This class is used to solve the CSP with backtracking and the MRV
    heuristic.
    """
    def __init__(self, puzzle_file):
        self.sudoku = Sudoku(puzzle_file)
        self.guesses = 0

    ################################################################
    ### YOU MUST EDIT THIS FUNCTION!!!!!
    ### We will test your code by constructing a csp_solver instance
    ### e.g.,
    ### csp_solver_mrv = CSP_Solver_MRV('puz-001.txt')
    ### solved_board, num_guesses = csp_solver_mrv.solve()
    ### so your `solve' method must return these two items.
    ################################################################
    def solve(self):
        """
        Solves the Sudoku CSP and returns a list of lists representation
        of the solved sudoku puzzle as well as the number of guesses
        (assignments) required to solve the problem.
        YOU MUST EDIT THIS FUNCTION!!!!!
        """
        # Base case, the board is complete
        if (self.sudoku.complete()):
            return self.sudoku, self.guesses

        # if the mrv is 0, that means that there was a failure
        if self.find_mrv() == None:
            return None

        (line, pos) = self.find_mrv()
        domain = self.find_domain(line, pos)
        for value in domain:
            self.guesses += 1
            if value in self.find_domain(line, pos):
                self.sudoku.board[line][pos] = value
                self.solve()
                if self.sudoku.complete():
                    return self.sudoku.board_str(), self.guesses
                self.sudoku.board[line][pos] = 0
        return None


    def find_mrv(self):
        """
        Finds the mrv and returns the positional coordinates for the board.

        :return: (line number, position)
        """
        empty_spaces = self.find_all_empty()
        # Map tuples to list of valid domain
        domain_list = [self.find_domain(x[0], x[1]) for x in empty_spaces]
        dict = {}
        for x in empty_spaces:
            dict[(x[0], x[1])] = len(self.find_domain(x[0], x[1]))
        # determine the next space to place
        domain_size = 0
        (line, pos) = (-1, -1)
        while domain_size < 10:
            # find the key (coordinate of board) with the most restricted domain and return it
            for key, value in dict.items():
                # return None if there are any spaces with 0, since these are invalid boards
                if value == 0:
                    return None
                if value == domain_size:
                    (line, pos) = key
                    return (line, pos)
            domain_size += 1

    def find_all_empty(self):
        """
        Find an empty space on the board, traversing from left to right and from top to bottom

        :return: a (line_num, pos) coordinate of the empty space
        """
        line_num = 0
        empty_spaces = []
        while line_num < 9:
            pos = 0
            while pos < 9:
                if self.sudoku.board[line_num][pos] == 0:
                    empty_spaces.append((line_num, pos))
                pos += 1
            line_num += 1
        return empty_spaces

    def find_domain(self, line_num, pos):
        """
        Find the domain of valid inputs [1, .., 9] for an empty space

        :param line_num: the line number of the empty space
        :param pos: the position of the empty space
        :return: a list of valid inputs for the empty space
        """
        domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # check the row
        for x in self.sudoku.board[line_num]:
            if x in domain:
                domain.remove(x)
        # check the column
        column = [line[pos] for line in self.sudoku.board]
        for x in column:
            if x in domain:
                domain.remove(x)
        # check the box
        rows = self.sudoku.board[((line_num // 3)*3): ((line_num//3)*3 + 3)]
        box = [line[((pos // 3)*3): ((pos // 3)*3 + 3)] for line in rows]
        for x in box:
            for y in x:
                if y in domain:
                    domain.remove(y)
        return domain

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Solves sudoku with MRV.')

    parser.add_argument('type', help='type of heuristic')
    parser.add_argument('file', help='file to read puzzle from')

    args = parser.parse_args()

    # a regular csp solver without heuristics
    file_name = args.file
    if(args.type == 'r'):
        csp_solver = CSP_Solver(file_name)
        solved_board, num_guesses = csp_solver.solve()
    # csp solver utilizing minimum remaining value heuristic
    if (args.type == 'mrv'):
        csp_solver = CSP_Solver_MRV(file_name)
        solved_board, num_guesses = csp_solver.solve()
    # csp solver utilizing forward checking and minimum remaining value heuristic
    if (args.type == 'f'):
        csp_solver = CSP_Solver_MRV_FC(file_name)
        solved_board, num_guesses = csp_solver.solve()

    print(solved_board + '\n')
    print("Took " + str(num_guesses) + " guesses")

