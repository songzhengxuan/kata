'''
csp problem defination
'''

class CSP(object):
    '''
    define the basic csp problemn
    '''

    def is_assignment_complete(self, assignment):#pylint: disable=unused-argument
        ''' virtual method
        :param assignment: dict of {var: value}
        '''
        return False

    def select_unassigned_variable(self, assignment):#pylint: disable=unused-argument
        ''' virtual method
        :param assignment: dict of {var: value}
        '''
        return None

    def get_ordered_domain_value(self, var, assignment):#pylint: disable=unused-argument
        ''' virtual method
        :param var: target var
        :param assignment: current assignment
        '''
        return []

    def is_consistant_with(self, var, value, assignment):#pylint: disable=unused-argument
        ''' virtual method
        :param var: target var
        :param value: value for target value
        :param assignment:
        '''
        pass
