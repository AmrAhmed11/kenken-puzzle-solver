from sys import stderr
from itertools import product, permutations
from functools import reduce

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

def satisfies(values, operation, target):
    for p in permutations(values):
        if reduce(operation, p) == target:
            return True

    return False

def conflicting(A, a, B, b):
    for i in range(len(A)):
        for j in range(len(B)):
            mA = A[i]
            mB = B[j]

            ma = a[i]
            mb = b[j]
            if RowXorCol(mA, mB) and ma == mb:
                return True

    return False

def gdomains(size, cliques):
    domains = {}
    for clique in cliques:
        members, operator, target = clique

        domains[members] = list(product(range(1, size + 1), repeat=len(members)))

        qualifies = lambda values: not conflicting(members, values, members, values) and satisfies(values, operation(operator), target)

        domains[members] = list(filter(qualifies, domains[members]))

    return domains

def gneighbors(cliques):
    neighbors = {}
    for members, _, _ in cliques:
        neighbors[members] = []

    for A, _, _ in cliques:
        for B, _, _ in cliques:
            if A != B and B not in neighbors[A]:
                if conflicting(A, [-1] * len(A), B, [-1] * len(B)):
                    neighbors[A].append(B)
                    neighbors[B].append(A)

    return neighbors


def validate(size, cliques):
    outOfBounds = lambda xy: xy[0] < 1 or xy[0] > size or xy[1] < 1 or xy[1] > size

    mentioned = set()
    for i in range(len(cliques)):
        members, operator, target = cliques[i]

        cliques[i] = (tuple(set(members)), operator, target)

        members, operator, target = cliques[i]

        if operator not in "+-*/.":
            print("Operation", operator, "of clique", cliques[i], "is unacceptable", file=stderr)
            exit(1)

        problematic = list(filter(outOfBounds, members))
        if problematic:
            print("Members", problematic, "of clique", cliques[i], "are out of bounds", file=stderr)
            exit(2)

        problematic = mentioned.intersection(set(members))
        if problematic:
            print("Members", problematic, "of clique", cliques[i], "are cross referenced", file=stderr)
            exit(3)

        mentioned.update(set(members))

    indexes = range(1, size + 1)

    problematic = set([(x, y) for y in indexes for x in indexes]).difference(mentioned)

    if problematic:
        print("Positions", problematic, "were not mentioned in any clique", file=stderr)
        exit(4)

def RowXorCol(xy1, xy2):
    return (xy1[0] == xy2[0]) != (xy1[1] == xy2[1])


def first(iterable, default=None):
    try:
        return iterable[0]
    except IndexError:
        return default
    except TypeError:
        return next(iterable, default)

def count(seq):
    return sum(bool(x) for x in seq)

class CSP():
    def __init__(self, variables, domains, neighbors, constraints):
        variables = variables or list(domains.keys())

        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.initial = ()
        self.curr_domains = None
        self.nassigns = 0

    def assign(self, var, val, assignment):
        assignment[var] = val
        self.nassigns += 1

    def unassign(self, var, assignment):
        if var in assignment:
            del assignment[var]
            
    def nconflicts(self, var, val, assignment):
        def conflict(var2):
            return (var2 in assignment and
                    not self.constraints(var, val, var2, assignment[var2]))
        return count(conflict(v) for v in self.neighbors[var])
        
    def actions(self, state):
        if len(state) == len(self.variables):
            return []
        else:
            assignment = dict(state)
            var = first([v for v in self.variables if v not in assignment])
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
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def suppose(self, var, value):
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    def prune(self, var, value, removals):
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    def choices(self, var):
        return (self.curr_domains or self.domains)[var]

    def infer_assignment(self):
        self.support_pruning()
        return {v: self.curr_domains[v][0]
                for v in self.variables if 1 == len(self.curr_domains[v])}

    def restore(self, removals):
        for B, b in removals:
            self.curr_domains[B].append(b)

    def conflicted_vars(self, current):
        return [var for var in self.variables
                if self.nconflicts(var, current[var], current) > 0]

class Kenken(CSP):

    def __init__(self, size, cliques):
        validate(size, cliques)
        variables = [members for members, _, _ in cliques]
        domains = gdomains(size, cliques)
        neighbors = gneighbors(cliques)
        CSP.__init__(self, variables, domains, neighbors, self.constraint)

        self.size = size
        self.checks = 0
        self.padding = 0

        self.meta = {}
        for members, operator, target in cliques:
            self.meta[members] = (operator, target)
            self.padding = max(self.padding, len(str(target)))        

    def constraint(self, A, a, B, b):
        self.checks += 1

        return A == B or not conflicting(A, a, B, b)