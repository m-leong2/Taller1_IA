from algorithms.problems import SearchProblem
import algorithms.utils as utils
from world.game import Directions
from algorithms.heuristics import nullHeuristic


def tinyDiagnosticSearch(problem: SearchProblem):
    """
    Returns a hard-coded sequence of moves for the tinyDiagnostic layout.
    For any other station layout, the sequence of moves will be incorrect.
    """
    s = Directions.SOUTH
    e = Directions.EAST
    return [s, e, s, e, e, e, e, s, e, e, s, s, e, s, s, e, s, e, e, e, e, e, e, e]


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    # TODO: Add your code here
    utils.raiseNotDefined()


def breadthFirstSearch(problem: SearchProblem):
    """
    Search the shallowest nodes in the search tree first.
    """
    # TODO: Add your code here
    
    #--- IA!!
    
    start = problem.getStartState()

    if problem.isGoalState(start):
        return []

    frontier = utils.Queue()
    frontier.push(start)

    reached = {start}

    parent = {}
    action_from_parent = {}

    while not frontier.isEmpty():

        state = frontier.pop()

        for successor, action, cost in problem.getSuccessors(state):

            if successor in reached:
                continue

            reached.add(successor)
            parent[successor] = state
            action_from_parent[successor] = action

            if problem.isGoalState(successor):

                path = []
                current = successor

                while current != start:
                    path.append(action_from_parent[current])
                    current = parent[current]

                path.reverse()
                return path

            frontier.push(successor)

    return None
    
    # --- Mi codigo
    """
    inicio = problem.getStartState()
    
    if problem.isGoalState(inicio):
        return []
    
    frontera = utils.Queue()
    frontera.push((inicio, []))
    
    alcanzados = {inicio}
    while not frontera.isEmpty():
        estado, camino = frontera.pop()
        for hijo, accion, costo in problem.getSuccessors(estado):
            if hijo not in alcanzados:
                if problem.isGoalState(hijo):
                    return camino + [accion]
                alcanzados.add(hijo)
                frontera.push((hijo, camino + [accion]))
                
    return None
    """

def uniformCostSearch(problem: SearchProblem):
    """
    Search the node of least total cost first.
    """
    pq = utils.PriorityQueue()
    inicio = problem.getStartState()
    pq.push((inicio, [], 0), 0)  
    menor_costo = {inicio: 0}  
    while not pq.isEmpty():
        psc, recorrido, costo = pq.pop() 
        if problem.isGoalState(psc):
            return recorrido
        
        for siguiente_valor, accion, costo_camino in problem.getSuccessors(psc):
            nuevo_costo = costo + costo_camino
            
            if siguiente_valor not in menor_costo or nuevo_costo < menor_costo[siguiente_valor]:
                menor_costo[siguiente_valor] = nuevo_costo
                pq.push((siguiente_valor, recorrido + [accion], nuevo_costo), nuevo_costo)
    return []  
    

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    # TODO: Add your code here
    utils.raiseNotDefined()


# Abbreviations (you can use them for the -f option in main.py)
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
