from utils import (
   is_in, memoize,PriorityQueue
)

from logic import (WumpusPosition)


class Problem(object):
    """The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and slove them with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal
    
    def actions(self, state):
        """Return the acitons that can be executed in the given state.
        The result would typically be a list, but if there are
        many actions, consider yielding the one at a time in an 
        iterator, rather than building them all at once."""
        raise NotImplementedError
    
    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of 
        self.actions(state)."""
        raise NotImplementedError
    
    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the 
        state to self.goal of checkes for state in self.goal if it is a 
        list, as specified in the constructor. Override this method if 
        checking against a single self.gocal is not enough."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal
    
    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from 
        state1 via action, assuming cost c to get up to state1. if the problem
        is such that the path doesn't matter, this funciton will only look at
        state2. If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c+1
    
    def value(self, state):
        """For optimization problems, each state has a value. Hill-climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError

class Node:
    """ A node in a seach tree. Contains a pointer to the parent ( the node
    that this is a successor of) and to the actual state for this node. Node
    that if a state is arrived at by two paths, then there are two nodes with
    the same state. Also includes the action that got us to this state, and 
    the total path_cost(also known as g) to reach the node. Other functions
    may add an f and h values; the best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to 
    subclass this class."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1
    
    def __repr__(self):
        return "<Node {}>".format(self.state)
    
    def __lt__(self, node):
        return self.path_cost < node.path_cost
    
    def expand(self, problem):
        """List the nodes reachable in one step from this node."""
        result = [self.child_node(problem, action)
                for action in problem.actions(self.state)]
        print("expand " ,self, "result is", result)
        return result
            
    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        next_node = Node(next_state, self, action, 
            problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node
    
    def solution(self):
        """Return the sequence of acitons to go from the root to this node."""
        return [node.action for node in self.path()[1:]]
    
    def path(self):
        """Return a list of nodes forming the path from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))
    
    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state
    
    def __hash__(self):
        return hash(self.state)



def best_first_graph_search(problem, f):
    """Seach the nodes with the lowest f scores first.
    You specify the function f(node) that you waht to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            print("child is ", child)
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                incumbent = frontier[child]
                if f(child) < f(incumbent):
                    del frontier[incumbent]
                    frontier.append(child)
    print("explorered is ", explored)
    return None   

class PlanRoute(Problem):
    """ The problem of moving hte Hybrid Wumpus Agent from one place ot other."""

    def __init__(self, initial, goal, allowed, dimrow):
        """ Define goal state and initialize a problem """
        self.dimrow = dimrow
        self.goal = goal
        self.allowed = allowed
        Problem.__init__(self, initial, goal)
    
    def actions(self, state):
        """ Return the actions that can be executed in the given state.
        The result would be a list, since there are only three actions 
        in any iven state of theenvironment"""
        possible_actions = ['Forward', 'TurnLeft', 'TurnRight']
        x,y = state.get_location()
        orientation = state.get_orientation()

        #Prevent Bumps
        if x == 1 and orientation == 'LEFT':
            if 'Forward' in possible_actions:
                possible_actions.remove('Forward')
        if y == 1 and orientation == 'DOWN':
            if 'Forward' in possible_actions:
                possible_actions.remove('Forward')
        if x == self.dimrow and orientation == 'RIGHT':
            if 'Forward' in possible_actions:
                possible_actions.remove('Forward')
        if y == self.dimrow and orientation == 'UP':
            if 'Forward' in possible_actions:
                possible_actions.remove('Forward')
        
        return possible_actions
    
    def result(self, old_state, action):
        """ Given state and action, return a new state that is the result
        of the action. Action is assumed to be a valid action in the state """
        print("before result state is ", old_state)
        state = WumpusPosition(old_state.X, old_state.Y, old_state.orientation)
        x, y = state.get_location()
        proposed_loc = list()

        # Move Forward
        if action == 'Forward':
            if state.get_orientation() == 'UP':
                proposed_loc = [x, y+1]
            elif state.get_orientation() == 'DOWN':
                proposed_loc = [x, y-1]
            elif state.get_orientation() == 'LEFT':
                proposed_loc = [x-1, y]
            elif state.get_orientation() == 'RIGHT':
                proposed_loc = [x+1, y]
            else:
                raise Exception("InvalidOrientation")
        # Rotate counter-clockwise
        elif action == 'TurnLeft':
            if state.get_orientation() == 'UP':
                state.set_orientation('LEFT')
            elif state.get_orientation() == 'DOWN':
                state.set_orientation('RIGHT')
            elif state.get_orientation() == 'LEFT':
                state.set_orientation('DOWN')
            elif state.get_orientation() == 'RIGHT':
                state.set_orientation('UP')
            else:
                raise Exception("InvalidOrientation")
        # Rotate clockwise
        elif action == 'TurnRight':
            if state.get_orientation() == 'UP':
                state.set_orientation('RIGHT')
            elif state.get_orientation() == 'DOWN':
                state.set_orientation('LEFT')
            elif state.get_orientation() == 'LEFT':
                state.set_orientation('UP')
            elif state.get_orientation() == 'RIGHT':
                state.set_orientation('DOWN')
            else:
                raise Exception("InvalidOrientation")
        
        if proposed_loc in self.allowed:
            state.set_location(proposed_loc[0], proposed_loc[1])
        
        print("after result state is ", state)
        return state
    
    def goal_test(self, state):
        """ Given a state, return True if state is a goal state for False"""
        return state.get_location() == tuple(self.goal)
    
    def h(self, node):
        """ Return the hiristic value for a given state."""
        x1, y1 = node.state.get_location()
        x2, y2 = self.goal
        return abs(x2 - x1) + abs(y2 - y1)






def astar_search(problem, h=None):
    """ A* search is best-first graph search with f(n) = g(n) + h(n). 
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))