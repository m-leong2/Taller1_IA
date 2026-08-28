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
    
    
    """"
    Mi codigo inicial:
    
    inicio = problem.getStartState()
    pila = utils.Stack()
    visitado = set()
    
    while not pila.isEmpty():
        
        elemento = pila.pop()
        estado = elemento[0]
        camino = elemento[1]
        
        if estado not in visitado:
            visitado.add(estado)
            
            if problem.isGoalState(estado)
                return camino
            
            sucesores = problem.getSuccessors
            
            for sucesor in sucesores:
                
                next = sucesor[0]
                
                if next not in visitado:
                    
                    pila.push(next, camino)
                    
                    
    return []
    
    
    Promp: podrias decirme  en que esta fallando mi algoritmno de DFS
    Utilice Gemini
    
    pq no funcionaba ?
    
    1. no empiece bien la pila, entonces inicia vacia cuando deberia tener 
    la parte de inicio para poder ejecutarse bien. El error mas grande dee logica 
    estuvo ahi 
    
    2. se me olvidop los : en un if 
    
    3. sucesores tiene tiene que recibir estado y no le puse ningun parametro
    algo que pase por alto ya que en el anterior if siesta
    
    4. No se agrga la acicion al camino, ni tampoco guarde la ccion, ya que 
    para poder saber cual es el camino necesito guardar las acciones, luego
    no agregue la nueva accion que no tenia al  camino anterior ya que asi se
    guarda la secuencia del camino que es lo importante. Ademas, al final intente 
    hacer push en la pila poniendo 2 cosas cuando solo recibe una
         
"""
    
    inicio = problem.getStartState()
    pila = utils.Stack()
    visitado = set()
    caminoInicial = []
    pila.push((inicio, caminoInicial))
        
    while not pila.isEmpty():
            
        elemento = pila.pop()
        estado = elemento[0]
        camino = elemento[1]
            
        if estado not in visitado:
            visitado.add(estado)
            
            if problem.isGoalState(estado):
                return camino
                
            sucesores = problem.getSuccessors(estado)
                
            for sucesor in sucesores: 
                next = sucesor[0]
                accion = sucesor[1]
                    
                if next not in visitado:  
                    new_camino = camino + [accion]
                    pila.push((next, new_camino))
                        
                        
    return []
    
    
    


def breadthFirstSearch(problem: SearchProblem):
    """
    Search the shallowest nodes in the search tree first.
    """
    # TODO: Add your code here
    
    
    """
    Prompt:
    Revisa esta implementacion de BFS e identifica los errores presentes teniendo en cuenta el psudo codigo proporcionado
    
    A partir de esta revision, se identifico un error al no agregar el estado inicial al cojunto de los alcanzados
    y me la estructura en la que debia retornar el camino al estado objetivo
    
    Posteriormente le pedi que realizara su propia version del algoritmo. La IA propuso utilizar diccionarios para almacenar
    el estado padre y la acción realizada para llegar a cada estado. Esto permite reconstruir el camino solamente cuando se
    encuentra la meta, evitando almacenar y copiar el camino completo en cada elemento de la Queue.
    """
    
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
    # mi codigo 
    
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

#IA 
# Use ChatGPT para confirmar el funcionamiento de mi codigo, sin embargo, mi codigo corrio bien y no hice
# cambios al codigo mio original
# El prompt que use fue: "¿Así va bien uniformCostSearch? No sé si estoy guardando bien el estado después de que el robot recoge M."
# lo cual me respondio con el siguiente codigo y respuestas, no obstante, no lo entendi del todo
# por esta razón mantuve mi codigo original, su respuesta fue la siguiente: "La IA confirmó que la implementación
# de UCS ya era correcta y sugirió una pequeña mejora para evitar expandir rutas antiguas de mayor costo. La modificación 
# era opcional y buscaba hacer el código más limpio y eficiente."
# Sin embargo no use la sugerencia de la IA, ya que no entendí del todo su respuesta y mi código original corrio bien.

""""
def uniformCostSearch(problem: SearchProblem):
    pq = utils.PriorityQueue()

    start_state = problem.getStartState()
    pq.push((start_state, [], 0), 0)

    menor_costo = {start_state: 0}

    while not pq.isEmpty():
        state, actions, costo = pq.pop()

        if costo > menor_costo[state]:
            continue

        if problem.isGoalState(state):
            return actions

        for siguiente_valor, action, costo_camino in problem.getSuccessors(state):
            nuevo_costo = costo + costo_camino

            if siguiente_valor not in menor_costo or nuevo_costo < menor_costo[siguiente_valor]:
                menor_costo[siguiente_valor] = nuevo_costo

                pq.push(
                    (siguiente_valor, actions + [action], nuevo_costo),
                    nuevo_costo
                )

    return []

   """

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    pq = utils.PriorityQueue()

    inicio = problem.getStartState()
    costo_inicial = 0

    prioridad_inicial = costo_inicial + heuristic(inicio, problem)

    pq.push((inicio, [], costo_inicial), prioridad_inicial)

    menor_costo = {inicio: costo_inicial}

    while not pq.isEmpty():

        estado, recorrido, costo = pq.pop()

        if costo <= menor_costo[estado]:

            if problem.isGoalState(estado):
                return recorrido

            for siguiente_estado, accion, costo_movimiento in problem.getSuccessors(estado):

                nuevo_costo = costo + costo_movimiento

                if siguiente_estado not in menor_costo or nuevo_costo < menor_costo[siguiente_estado]:

                    menor_costo[siguiente_estado] = nuevo_costo

                    prioridad = nuevo_costo + heuristic(siguiente_estado, problem)

                    pq.push(
                        (siguiente_estado, recorrido + [accion], nuevo_costo),
                        prioridad
                    )

    return []
"""
Codigo inicial: 

   pq = utils.PriorityQueue()
    inicio = problem.getStartState()
    costo = 0
    prioridad_inicial = costo + heuristic(inicio, problem)
    
    pq.push((inicio, [], costo), prioridad_inicial)
    
    while not pq.isEmpty():
        
        estado = pq.pop(1)
        recorrido = pq.pop(2)
        costo = pq.pop(3)

        if problem.isGoalState(estado):
            return recorrido
        
        for siguiente_nodo, movimiento, costo_camino in problem.getSuccessors(estado):
            nuevo_costo = costo + costo_camino
            prioridad = nuevo_costo + heuristic(siguiente_nodo, problem)
            
            if siguiente_nodo not in nuevo_costo:
                pq.push((siguiente_nodo, recorrido + [movimiento], nuevo_costo), prioridad)
                
                
Cambios realizados con IA: Agregó un diccionario que almacena el menor costo del camino para cada nodo visitado. 
Solo guarda el camino con menor costo, asi se evita que se repitan nodos en la pq. 
    
Igualmente cambio la implementación de pop() de la pq, ya que la pq devuelve toda la tupla y no solo un elemento que yo necesite.
    
Por otro lado, al crear el diccionario de menor costo, más adelante verifica si el nodo no se habia visitado antes y comparara si el
nuevo camino al nodo es menor que el que esta guardado en el diccionario, y si es así, se actualiza el diccionario y se agrega a la pq. 
    
    
Se utilizó IA como apoyo para comprender la estructura del proyecto, especialmente el funcionamiento de problem, luego se desarrolló 
la versión propia y posteriormente se consultó a ChatGPT y realizaron los cambios necesarios y se probó la función.. 
 """
     
    


# Abbreviations (you can use them for the -f option in main.py)
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
