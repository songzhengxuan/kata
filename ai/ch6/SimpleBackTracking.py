'''
Simple backtracking without inference or any other fancy thing
'''
def backtracking_search(csp):
    '''returns a solution, or failure
    :param csp: the problem
    '''
    result = {}
    found = backtrack(csp, result) #initial assignment is empty
    return found, result


def backtrack(csp, assignment):
    ''' private method for backtracking search,
    returns (True, result_assignment) or (False, None)
    :param csp: the problem
    :param assignment: curent no-conflicit assignment of csp
    '''
    if csp.is_assignment_complete(assignment):
        return True
    var = csp.select_unassigned_variable(assignment)
    ordered_domain_value = csp.get_ordered_domain_value(var, assignment)
    for value in ordered_domain_value:
        if csp.is_consistant_with(var, value, assignment):
            assignment[var] = value
            result = backtrack(csp, assignment)
            if result:
                return True
            else:
                del assignment[var]
    return False
