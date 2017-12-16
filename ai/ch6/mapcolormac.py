'''
csp problem of map color
'''

from csp import CSP
import mapgraph

class MapColorMac(CSP):
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
            self.__default_domain_values[point] = set(range(1, color_number+1))
            self.__domain_values[point] = set(range(1, color_number+1))

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
        判断如果将var对应的点赋色彩value，是否与现有assignment能够不冲突
        '''
        edge = var.edges
        while edge is not None:
            if edge.end.color != 0 and value == edge.end.color:
                return False
            edge = edge.next
        return True

    def assign(self, new_assignment):
        '''
        对new_assignment中各个点按new_assignment的值进行上色
        '''
        for key, color in new_assignment.items():
            key.color = color
            self.__unassigned_points.remove(key)
    
    def undo_assign(self, new_assignment):
        '''
        取消对new_assignment中所有点的上色，同时恢复__unassigned_point, __domain_values
        各个变量
        '''
        for key, _ in new_assignment.items():
            key.color = 0
            self.__domain_values[key] = self.__default_domain_values[key]
            self.__unassigned_points.add(key)
    
    def inference(self, var, value):
        '''
        当确认给var点上value色后，重新计算其余未赋值的点的可选值域是否有缩小
        当遇到可选域变为空的点后，返回False,{}，说明推导无法满足对应的结果
        否则，将值所可选域只有1个值的点也作为可以直接赋值的点返回，此时返回值 
        的格式为True, {可选域只有1个值的点值对}
        mac算法要求将搜索的范围扩大
        '''
        result = {}

        edges_to_check = set()

        edge = var.edges
        while edge is not None:
            if edge.end in self.__unassigned_points:
                edges_to_check.add(mapgraph.Edge(edge.end, var))
            edge = edge.next

        refined = True
        while refined:
            refined = False

            while edges_to_check:
                edge = edges_to_check.pop()
                start = edge.start
                end = edge.end 
                start_domain_values = self.__domain_values[start]
                end_domain_values = self.__domain_values[end]
                if not start_domain_values or not end_domain_values:
                    return False, {}

                refined_start_domain_values = set(start_domain_values)
                if len(end_domain_values) == 1: #只有这种情况才需要检查,大于1的情况肯定都能满足
                    for start_value in start_domain_values:
                        if start_value in end_domain_values:
                            refined_start_domain_values.remove(start_value)
                            if not refined_start_domain_values: #发现已经无法满足条件了
                                return False, {}
                            refined = True

                if len(start_domain_values) != len(refined_start_domain_values):
                    self.__domain_values[start] = refined_start_domain_values
                    if len(refined_start_domain_values) == 1: #对于可选值已经变成只有1个的点加入result
                        result[start] = next(iter(refined_start_domain_values))
                    edge = start.edges
                    while edge is not None:
                        if edge.end in self.__unassigned_points and edge.end != end:
                            edges_to_check.add(mapgraph.Edge(edge.end, start))
                        edge = edge.next

        return True, result
