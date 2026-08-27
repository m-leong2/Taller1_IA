from typing import Tuple
from algorithms import utils
from algorithms.problems import SystemRepairProblem


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def manhattanHeuristic(state, problem):
    """
    The Manhattan distance heuristic.

    Baseline rule for this workshop: estimate the direct distance to the next
    mandatory target:
    - K if the robot does not have the kit yet.
    - the nearest pending T if the robot has the kit and systems remain.
    - C if all systems have been repaired.
    """
    # TODO: Add your code here
    posicion, hasKit, pendingSystems = state
    
    if not hasKit:
        target = problem.kitLocation
        distancia = abs(posicion[0] - target[0])+abs(posicion[1] - target[1])
        return distancia
    
    if pendingSystems:
        distancias = []
        for sistema in pendingSystems:
            objetivo = problem.systemLocations[sistema]
            distancia = abs(posicion[0] - objetivo[0]) + abs(posicion[1] - objetivo[1])
            distancias.append(distancia)
        return min(distancias)
    
    objetivo = problem.controlCenter
    
    distancia = abs(posicion[0] - objetivo[0]) + abs(posicion[1] - objetivo[1])
    return distancia
    


def euclideanHeuristic(state, problem):
    """
    The Euclidean distance heuristic.

    Baseline rule for this workshop: estimate the direct distance to the next
    mandatory target:
    - K if the robot does not have the kit yet.
    - the nearest pending T if the robot has the kit and systems remain.
    - C if all systems have been repaired.
    """
    position, hasKit, pendingSystems = state

    if hasKit == False:
        objetivo = problem.kitPosition

        distancia = ((position[0] - objetivo[0]) ** 2 + (position[1] - objetivo[1]) ** 2) ** 0.5

        return distancia

    if hasKit == True and len(pendingSystems) > 0:

        distancias = []

        for sistema in pendingSystems:
            objetivo = sistema

            distancia = ((position[0] - objetivo[0]) ** 2 + (position[1] - objetivo[1]) ** 2) ** 0.5

            distancias.append(distancia)

        return min(distancias)

    if len(pendingSystems) == 0:
        objetivo = problem.controlPosition

        distancia = ((position[0] - objetivo[0]) ** 2 + (position[1] - objetivo[1]) ** 2) ** 0.5

        return distancia
    
    """
    Codigo inicial: 
    
    position, hasKit, pendingSystems = state
    
    if hasKit == False: 
        objetivo = problem.kitLocation
        distancia = ((position[0] - objetivo[0])**2 + (position[1] - objetivo[1])**2)**0.5
        return distancia
    
    if hasKit == True and pendingSystems != []:
        for sistema in pendingSystems:
            objetivo = problem.systemPositions[sistema]
            distancia = ((position[0] - objetivo[0])**2 + (position[1] - objetivo[1])**2)**0.5
        return distancia
    
    if pendingSystems == []:
        objetivo = problem.controlCenter
        distancia = ((position[0] - objetivo[0])**2 + (position[1] - objetivo[1])**2)**0.5
        return distancia
        
        
Cambios realizados con IA: Cambio como obtener la posicion de los sistemas, ya que cada elemento de pendingSystems ya corresponde 
directamente a la posición de un sistema T, por lo que el sistema es el objetivo.
    
Agrego una lista para guardar la distancia euclidiana desde la posición del robot hasta cada sistema pendiente. Antes devolvia solo
la ultima distancia calculada, ahora devuelve la mínima de todas las distancias calculadas.
    
Cambió la condición pendingSystems != [] por len(pendingSystems) > 0 y pendingSystems == [] por len(pendingSystems) == 0, ya que 
pendingSystems es una tupla y no una lista, por lo que no se puede comparar con una lista vacía.

        
Se utilizó IA como apoyo para comprender la estructura del proyecto, especialmente el funcionamiento de pendingSystems, luego se desarrolló 
la versión propia y posteriormente se consultó a ChatGPT y se realizaron los cambios necesarios y se probó la función.
   """

def systemRepairHeuristic(
    state: Tuple[Tuple, bool, Tuple], problem: SystemRepairProblem
):
    """
    Your heuristic for the SystemRepairProblem.

    state: (position, hasKit, pendingSystems)
    problem: SystemRepairProblem instance

    This must be admissible and preferably consistent.

    Hints:
    - Use problem.heuristicInfo to cache expensive computations
    - Go with some simple heuristics first, then build up to more complex ones
    - Consider the kit, pending systems, and the final return to control center
    - Balance heuristic strength vs. computation time (do experiments!)
    """
    # TODO: Add your code here
    utils.raiseNotDefined()
