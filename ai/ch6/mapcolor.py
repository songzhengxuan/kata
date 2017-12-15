'''
csp problem of map color
'''

from csp import CSP

class MapColor(CSP):
    '''
    define the map color problem
    '''

    def __init__(self, _map, color_number):
        '''
        constructor
        __domain_values: 是一个map, 记录每一个点当前还可以有多少值可以选
        __unassigned_points: 记录还没有赋值的点的集合
        __default_domain_values: 是一个map, 在回溯时，将一个变量的domain_value恢复到对应的值
        '''
        _map.reset()
        self.__map = _map
        self.__domain_values = {}
        self.__unassigned_points = set()
        self.__default_domain_values = {}
        for point in _map.points:
            self.__unassigned_points.add(point)
            self.__default_domain_values[point] = set(range(1,color_number+1))
            self.__domain_values[point] = set(range(1,color_number+1))

    def is_assignment_complete(self, assignment):
        '''
        判断assignment是否已经对self的__map中所有点都完成了着色
        '''
        if len(self.__map.points) != len(assignment):
            return False
        else:
            return all((p in assignment) for p in self.__map.points)
    
    def select_unassigned_variable(self, assignment):
        '''
        返回一个末着色的点
        '''
        return next(iter(self.__unassigned_points))

    def get_ordered_domain_value(self, var, assignment):
        '''
        返回一个var对应的点还存在的所有color, 注意如果var不在unassigned列表时会抛出异常
        '''
        return list(self.__domain_values[var])

    def is_consistant_with(self, var, value, assignment):
        '''
        判断var对应的点赋色彩value时，是否与现有assignment能够不冲突
        '''
        edge = var.edges
        while edge is not None:
            if edge.end.color != 0 and var.color == edge.end.color:
                return False
            edge = edge.next
        return True

    def assign(self, new_assignment):
        '''
        对new_assignment中各个点按new_assignment的值进行上色
        '''
        for key, _ in new_assignment.items():
            self.__unassigned_points.remove(key)
    
    def undo_assign(self, new_assignment):
        '''
        取消对new_assignment中所有点的上色，同时恢复__unassigned_point, __domain_values
        各个变量
        '''
        for key, _ in new_assignment.items():
            self.__domain_values[key] = self.__default_domain_values[key]
            self.__unassigned_points.add(key)
    
    def inference(self, var, value):
        '''
        当确认给var点上value色后，重新计算其余未赋值的点的可选值域是否有缩小
        当遇到可选域变为空的点后，返回False,{}，说明推导无法满足对应的结果
        否则，将值所可选域只有1个值的点也作为可以直接赋值的点返回，此时返回值 
        的格式为True, {可选域只有1个值的点值对}
        '''
        result = {}
        edge = var.edges
        while edge is not None:
            if edge.end in self.__unassigned_points:
                if value in self.__domain_values[edge.end]:
                    self.__domain_values[edge.end].remove(value)
                remain_num = len(self.__domain_values[edge.end])
                if remain_num == 0:
                    return False, {}
                elif remain_num == 1:
                    result[edge.end] = next(iter(self.__domain_values[edge.end]))
            edge = edge.next

        return True, result       
                


        


        