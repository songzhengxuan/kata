'''
csp problem of 8 quene 
'''

from csp import CSP

class QueenCSP(CSP):
    '''
    define the 8 queen problem
    '''

    def __init__(self, number):
        '''init method'''
        self._number = number

    def is_assignment_complete(self, assignment):
        '''check assignment number'''
        return self._number == len(assignment)

    def select_unassigned_variable(self, assignment):
        ''' select first unassigned variable'''
        for i in range(0, self._number):
            if i not in assignment:
                return i
        return None

    def get_ordered_domain_value(self, var, assignment):
        ''' get ordered domain value
        :param var: integer number of position index
        :param assignment: current assigned
        '''
        return [i for i in range(1, self._number + 1)]

    def is_consistant_with(self, var, value, assignment):
        ''' return true if we can assign value to position var
        :param var: integer number of position index
        :param assignment: current assigned
        '''
        for k, v in assignment.items():
            if value == v:
                return False
            if (k - var) == (value - v) or (k - var) == (v - value):
                return False

        return True




