'''
backtracking with inference
'''
def backtracking_search(csp):
    ''' returns a solution, or failure
    :param csp: the problem
    '''
    result = {}
    found = backtrack(csp, result)
    return found, result

def backtrack(csp, assignment):
    ''' private method for backtracking search,
    returns True or False
    :param csp: the problem
    :param assignment: current assignment of csp
    '''
    if csp.is_assignment_complete(assignment):
        return True
    var = csp.select_unassigned_variable(assignment)
    ordered_domain_value = csp.get_ordered_domain_value(var, assignment)
    for value in ordered_domain_value:
        if csp.is_consistant_with(var, value, assignment):
            assignment[var] = value
            csp.assign_var(var, value)
            inference_succeed, inference_results = csp.inference(var, value)
            if inference_succeed is True:
                assignment.update(inference_results)
                csp.assign(inference_results)
                if backtrack(csp, assignment):
                    return True
                else:
                    csp.undo_assign(inference_results)
                    csp.undo_assign_var(var, value)
                    for key in inference_results:
                        del assignment[key]
                    del assignment[var]
            else:
                csp.undo_assign_var(var, value)
                del assignment[var]
    return False
