from itertools import product, permutations
from functools import reduce
import copy
from random import shuffle, randint, choice

class Helper:
    @staticmethod
    def gui_input(assignment,size):
        result = [0]*(size*size)
        for cages in assignment.items():
            for i,key in enumerate(cages[0]):
                gIndex = (key[0]-1)*size + (key[1]-1)
                result[gIndex] = cages[1][i]
        return result

    @staticmethod
    def operation(operator):
        if operator == '+':
            return lambda a, b: a + b
        elif operator == '-':
            return lambda a, b: a - b
        elif operator == '*':
            return lambda a, b: a * b
        elif operator == '/':
            return lambda a, b: a / b
        else:
            return None

    @staticmethod
    def satisfies(values, operation, target):
        for p in permutations(values):
            if reduce(operation, p) == target:
                return True

        return False

    @staticmethod
    def same_row_column(xy1, xy2):
        return (xy1[0] == xy2[0]) != (xy1[1] == xy2[1])

    @staticmethod
    def first(iterable, default=None):
        try:
            return iterable[0]
        except IndexError:
            return default
        except TypeError:
            return next(iterable, default)
            
    @staticmethod
    def count(seq):
        return sum(bool(x) for x in seq)
    
class Board:
    def __init__(self,size):
        self.size =size
        self.cages = self.generate(size)

    def adjacent(self,xy1, xy2):
        x1, y1 = xy1
        x2, y2 = xy2
        dx, dy = x1 - x2, y1 - y2
        return (dx == 0 and abs(dy) == 1) or (dy == 0 and abs(dx) == 1)

    def generate(self,size):
        board = [ [0]*size for i in range(size)]

        for i in range(size):
            for j in range(size):
                board[i][j] = (i + j) % size + 1

        for i in range(size):
            shuffle(board)

        for column1 in range(size):
            for column2 in range(size):
                for element in range(size):
                    board[element][column1], board[element][column2] = board[element][column2], board[element][column1]

        board_dict = {}
        for i in range(size):
            for j in range(size):
                board_dict[(j + 1, i + 1)] = board[i][j]

        uncaged = sorted(board_dict.keys(), key=lambda var: var[1])

        cages = []
        while uncaged:
            cages.append([])
            csize = randint(1, 4)
            cell = uncaged[0]
            uncaged.remove(cell)
            cages[-1].append(cell)

            for _ in range(csize - 1):
                adjs = [other for other in uncaged if self.adjacent(cell, other)]
                cell = choice(adjs) if adjs else None
                if not cell:
                    break
                uncaged.remove(cell)
                cages[-1].append(cell)
            csize = len(cages[-1])
            if csize == 1:
                cell = cages[-1][0]
                cages[-1] = ((cell, ), '.', board_dict[cell])
                continue
            elif csize == 2:
                fst, snd = cages[-1][0], cages[-1][1]
                if board_dict[fst] / board_dict[snd] > 0 and not board_dict[fst] % board_dict[snd]:
                    operator = "/"
                else:
                    operator = "-"
            else:
                operator = choice("+*")

            target = reduce(Helper.operation(operator), [board_dict[cell] for cell in cages[-1]])
            
            cages[-1] = (tuple(cages[-1]), operator, int(target))

        return cages

class Solver():
    def __init__(self, board):
        cages2 = copy.copy(board.cages)
        self.variables = [members for members, _, _ in cages2]
        self.domains = self.gdomains(board.size, cages2)
        self.neighbors = self.gneighbors(cages2)
        self.available_domains = None
        self.initial = ()
        self.nassigns = 0

        self.size = board.size
        self.checks = 0

    def gneighbors(self,cages):
        neighbors = {}
        for members, _, _ in cages:
            neighbors[members] = []

        for A, _, _ in cages:
            for B, _, _ in cages:
                if A != B and B not in neighbors[A]:
                    if self.conflicting(A, [-1] * len(A), B, [-1] * len(B)):
                        neighbors[A].append(B)
                        neighbors[B].append(A)

        return neighbors

    def gdomains(self,size, cages):
        domains = {}
        for clique in cages:
            members, operator, target = clique

            domains[members] = list(product(range(1, size + 1), repeat=len(members)))

            qualifies = lambda values: not self.conflicting(members, values, members, values) and Helper.satisfies(values, Helper.operation(operator), target)

            domains[members] = list(filter(qualifies, domains[members]))

        return domains

    def conflicting(self,A, a, B, b):
        for i in range(len(A)):
            for j in range(len(B)):
                mA = A[i]
                mB = B[j]

                ma = a[i]
                mb = b[j]
                if Helper.same_row_column(mA, mB) and ma == mb:
                    return True

        return False

    def constraint(self, A, a, B, b):
        self.checks += 1
        return A == B or not self.conflicting(A, a, B, b)

    def assign(self, var, val, assignment):
        assignment[var] = val
        self.nassigns += 1

    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]
            
    def nconflicts(self, var, val, assignment):
        def conflict(var2):
            return (var2 in assignment and
                    not self.constraint(var, val, var2, assignment[var2]))
        return Helper.count(conflict(v) for v in self.neighbors[var])
        
    def actions(self, state):
        if len(state) == len(self.variables):
            return []
        else:
            assignment = dict(state)
            var = Helper.first([v for v in self.variables if v not in assignment])
            return [(var, val) for val in self.domains[var]
                    if self.nconflicts(var, val, assignment) == 0]

    def result(self, state, action):
        (var, val) = action
        return state + ((var, val),)

    def goal_test(self, state):
        assignment = dict(state)
        return (len(assignment) == len(self.variables)
                and all(self.nconflicts(variables, assignment[variables], assignment) == 0
                        for variables in self.variables))

    def support_pruning(self):
        if self.available_domains is None:
            self.available_domains = {v: list(self.domains[v]) for v in self.variables}

    def suppose(self, var, value):
        self.support_pruning()
        removals = [(var, a) for a in self.available_domains[var] if a != value]
        self.available_domains[var] = [value]
        return removals

    def prune(self, var, value, removals):
        self.available_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    def choices(self, var):
        return (self.available_domains or self.domains)[var]

    def infer_assignment(self):
        self.support_pruning()
        return {v: self.available_domains[v][0]
                for v in self.variables if 1 == len(self.available_domains[v])}

    def restore(self, removals):
        for B, b in removals:
            self.available_domains[B].append(b)

    def conflicted_vars(self, current):
        return [var for var in self.variables
                if self.nconflicts(var, current[var], current) > 0]

    def AC3(self, queue=None, removals=None):
        if queue is None:
            queue = [(Xi, Xk) for Xi in self.variables for Xk in self.neighbors[Xi]]
        self.support_pruning()
        while queue:
            (Xi, Xj) = queue.pop()
            if self.revise(self, Xi, Xj, removals):
                if not self.available_domains[Xi]:
                    return False
                for Xk in self.neighbors[Xi]:
                    if Xk != Xj:
                        queue.append((Xk, Xi))
        return True

    def revise(self, Xi, Xj, removals):
        revised = False
        for x in self.available_domains[Xi][:]:
            if all(not self.constraint(Xi, x, Xj, y) for y in self.available_domains[Xj]):
                self.prune(Xi, x, removals)
                revised = True
        return revised

    def backtracking(self):
        def backtrack(assignment):
            if len(assignment) == len(self.variables):
                return assignment
            var = Helper.first([var for var in self.variables if var not in assignment])
            
            for value in self.choices(var):
                if 0 == self.nconflicts(var, value, assignment):
                    self.assign(var, value, assignment)
                    removals = self.suppose(var, value)
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                    self.restore(removals)
            self.unassign(var, assignment)
            return None

        result = backtrack({})
        return result

    def backtracking_forwardchecking(self):
        def backtrack(assignment):
            if len(assignment) == len(self.variables):
                return assignment
            var = Helper.first([var for var in self.variables if var not in assignment])
            
            for value in self.choices(var):
                if 0 == self.nconflicts(var, value, assignment):
                    self.assign(var, value, assignment)
                    removals = self.suppose(var, value)
                    fwchecking = True
                    self.support_pruning()
                    for B in self.neighbors[var]:
                        if B not in assignment:
                            for b in self.available_domains[B][:]:
                                if not self.constraint(var, value, B, b):
                                    self.prune(B, b, removals)
                            if not self.available_domains[B]:
                                fwchecking = False
                    if fwchecking:
                        result = backtrack(assignment)
                        if result is not None:
                            return result
                    self.restore(removals)
            self.unassign(var, assignment)
            return None

        result = backtrack({})
        return result

    def backtracking_arc(self):
        def backtrack(assignment):
            if len(assignment) == len(self.variables):
                return assignment
            var = Helper.first([var for var in self.variables if var not in assignment])
            
            for value in self.choices(var):
                if 0 == self.nconflicts(var, value, assignment):
                    self.assign(var, value, assignment)
                    removals = self.suppose(var, value)
                    arc_checking = True
                    queue = [(Xi, Xk) for Xi in self.variables for Xk in self.neighbors[Xi]]
                    self.support_pruning()
                    while queue:
                        (Xi, Xj) = queue.pop()
                        if self.revise(Xi, Xj, removals):
                            if not self.available_domains[Xi]:
                                arc_checking = False
                            for Xk in self.neighbors[Xi]:
                                if Xk != Xj:
                                    queue.append((Xk, Xi))
                    if arc_checking:
                        result = backtrack(assignment)
                        if result is not None:
                            return result
                    self.restore(removals)
            self.unassign(var, assignment)
            return None

        result = backtrack({})
        return result