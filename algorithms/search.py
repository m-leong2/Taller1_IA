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
    
    # --- Ignorar esto:
    """ 
        función BÚSQUEDA-EN-ANCHURA(problema) devuelve nodo-solución o fracaso
        nodo ← NODO(estado = problema.INICIAL)
        si problema.ES-META(nodo.estado) entonces devolver nodo
        frontera ← cola FIFO con nodo como único elemento
        alcanzados ← {problema.INICIAL}
        mientras frontera no esté vacía hacer
            nodo ← EXTRAER(frontera)
            para cada hijo en EXPANDIR(problema, nodo) hacer
                s ← hijo.estado
                si problema.ES-META(s) entonces devolver hijo
                si s no está en alcanzados entonces
                    agregar s a alcanzados
                    agregar hijo a frontera
        devolver fracaso
    """

def uniformCostSearch(problem: SearchProblem):
    """
    Search the node of least total cost first.
    """

    # TODO: Add your code here
    utils.raiseNotDefined()


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
