import gen
import classes

def unordered_domain_values(var, assignment, csp):
    return csp.choices(var)

def first_unassigned_variable(assignment, csp):
    return classes.first([var for var in csp.variables if var not in assignment])

def no_inference(csp, var, value, assignment, removals):
    return True

def forward_checking(csp, var, value, assignment, removals):
    csp.support_pruning()
    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                if not csp.constraints(var, value, B, b):
                    csp.prune(B, b, removals)
            if not csp.curr_domains[B]:
                return False
    return True

def forward_checking(csp, var, value, assignment, removals):
    csp.support_pruning()
    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                if not csp.constraints(var, value, B, b):
                    csp.prune(B, b, removals)
            if not csp.curr_domains[B]:
                return False
    return True


def mac(csp, var, value, assignment, removals):
    return AC3(csp, [(X, var) for X in csp.neighbors[var]], removals)

def AC3(csp, queue=None, removals=None):
    if queue is None:
        queue = [(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]]
    csp.support_pruning()
    while queue:
        (Xi, Xj) = queue.pop()
        if revise(csp, Xi, Xj, removals):
            if not csp.curr_domains[Xi]:
                return False
            for Xk in csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))
    return True

def revise(csp, Xi, Xj, removals):
    revised = False
    for x in csp.curr_domains[Xi][:]:
        if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
            csp.prune(Xi, x, removals)
            revised = True
    return revised

def backtracking_search(csp,
                    select_unassigned_variable=first_unassigned_variable,
                    order_domain_values=unordered_domain_values,
                    inference=no_inference):

    def backtrack(assignment):
        if len(assignment) == len(csp.variables):
            return assignment
        var = select_unassigned_variable(assignment, csp)
        
        for value in order_domain_values(var, assignment, csp):
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None

    result = backtrack({})
    assert result is None or csp.goal_test(result)
    return result

def gui_input(assignment,size):
    result = [0]*(size*size)
    for cliques in assignment.items():
        for i,key in enumerate(cliques[0]):
            gIndex = (key[0]-1)*size + (key[1]-1)
            result[gIndex] = cliques[1][i]
    return result

if __name__ == "__main__":
    
    size,cliques = gen.generate(5)
    Kenken1 = classes.Kenken(size,cliques)

    assignment1 = backtracking_search(Kenken1)
    print(gui_input(assignment1,size),"\n")
    assignment2 = backtracking_search(Kenken1,inference = forward_checking)
    print(gui_input(assignment2,size),"\n")
    assignment3 = backtracking_search(Kenken1,inference = mac)
    print(gui_input(assignment3,size),"\n")