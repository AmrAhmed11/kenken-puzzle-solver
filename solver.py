import gen
import classes

def unordered_domain_values(var, assignment, csp):
    return csp.choices(var)

def first_unassigned_variable(assignment, csp):
    return classes.first([var for var in csp.variables if var not in assignment])

def no_inference(csp, var, value, assignment, removals):
    return True

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
    size,cliques = gen.generate(3)

    Kenken = classes.Kenken(size,cliques)

    assignment = backtracking_search(Kenken)
    gui_input(assignment,size)