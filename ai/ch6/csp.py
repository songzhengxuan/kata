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

    def assign(self, new_assignment):#pylint: disable=unused-argument
        ''' virtual method
        :param new_assignment: new assignment
        '''
        pass

    def undo_assign(self, new_assignment):#pylint: disable=unused-argument
        ''' virtual method
        '''
        pass

    def assign_var(self, var, value):
        '''
        We'll fire you if you override this method
        assign
        '''
        assignment = {var:value}
        self.assign(assignment)

    def undo_assign_var(self, var, value):
        '''
        We'll fire you if you override this method
        '''
        assignment = {var:value}
        self.undo_assign(assignment)

    def is_consistant_with(self, var, value, assignment):#pylint: disable=unused-argument
        ''' virtual method
        :param var: target var
        :param value: value for target value
        :param assignment:
        '''
        pass

    def inference(self, var, value):#pylint: disable=unused-argument
        ''' virtual method
        return (True, decided var_value map during inference) andif inferences var=value is valid, otherwise return false
        ** hidden variables:
            assignment: current assigned vars and their values
            [var, domain] map: domains for each unassigned variabl
         **
        :param var: target var
        :param value: value for target value
        :param assignment: target assignment
        '''
        return True, {}
