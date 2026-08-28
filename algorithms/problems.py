from algorithms import utils
from world.game import Directions, Actions
from world.station_state import StationState


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        utils.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        utils.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        utils.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        utils.raiseNotDefined()


def findLayoutSymbols(missionState: StationState, symbol):
    """
    Returns every grid position where a symbol appears in the raw layout text.
    """
    return missionState.data.layout.getSymbolPositions(symbol)


def findSingleLayoutSymbol(missionState: StationState, symbol):
    """
    Returns the single position of a required mission symbol.
    """
    positions = findLayoutSymbols(missionState, symbol)

    if len(positions) != 1:
        raise Exception(
            "Expected exactly one '%s' symbol in the layout, found %d"
            % (symbol, len(positions))
        )

    return positions[0]


class DiagnosticProblem(SearchProblem):
    """
    Reach a diagnostic terminal in the station.

    State: (x, y) position.
    Goal: diagnostic terminal cell marked with D.
    Terrain costs apply by default.
    """

    def __init__(
        self,
        missionState,
        costFn=None,
        goal=(1, 1),
        start=None,
        warn=True,
        visualize=True,
    ):
        """
        missionState: StationState
        costFn: function (x,y)->cost; if None, uses missionState.getTerrainCost
        goal: fallback goal if terminal auto-detect is not possible
        start: optional override for start position
        warn: print warnings if map doesn't match expectations
        visualize: enable visited bookkeeping for display/stats
        """

        self.walls = missionState.getWalls()

        # Start state (robot position unless overridden)
        self.startState = missionState.getRobotPosition()
        if start is not None:
            self.startState = start

        # --- AUTO-DETECT GOAL FROM DIAGNOSTIC TERMINAL ---
        terminals = findLayoutSymbols(missionState, "D")

        if len(terminals) == 1:
            # This is a normal diagnostic case: exactly one terminal on map
            self.goal = terminals[0]
        else:
            # Fallback to provided goal (default (1,1))
            self.goal = goal
            if warn:
                if len(terminals) == 0:
                    print(
                        "Warning: no diagnostic terminal found on the map; using goal=%s"
                        % (str(self.goal),)
                    )
                else:
                    print(
                        "Warning: %d diagnostic terminals found; using goal=%s"
                        % (len(terminals), str(self.goal))
                    )

        # Use terrain cost from mission state so search cost matches terrain rules
        if costFn is None:
            costFn = lambda pos: missionState.getTerrainCost(pos[0], pos[1])
        self.costFn = costFn
        self.visualize = visualize

        # For visualization/statistics
        self._visited, self._visitedlist, self._expanded = {}, [], 0

    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal

        # For visualization: mark nodes as visited
        if isGoal and self.visualize:
            self._visitedlist.append(state)
            import __main__

            if "_display" in dir(__main__):
                if "drawExpandedCells" in dir(__main__._display):
                    __main__._display.drawExpandedCells(self._visitedlist)

        return isGoal

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost.

        For a given state, this returns a list of triples:
        (successor, action, stepCost)

        This is where terrain costs come into play via costFn.
        """
        successors = []
        for action in [
            Directions.NORTH,
            Directions.SOUTH,
            Directions.EAST,
            Directions.WEST,
        ]:
            x, y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)

            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append((nextState, action, cost))

        # Bookkeeping for display
        self._expanded += 1
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return successors
      
    

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.
        """
        if actions is None:
            return 999999

        x, y = self.getStartState()
        cost = 0
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += self.costFn((x, y))
        return cost


class ModuleRepairProblem(SearchProblem):
    """
    Pick up the energy module M before reaching the control center C.

    State: (position, hasModule)
    - position: (x, y) tuple
    - hasModule: True if the robot already picked up the module

    Goal: reach the control center after picking up the module.

    Students must complete this problem definition.
    """

    def __init__(self, startingMissionState: StationState):
        self.startingMissionState = startingMissionState
        self.walls = startingMissionState.getWalls()

        self.startPosition = startingMissionState.getRobotPosition()
        self.modulePosition = findSingleLayoutSymbol(startingMissionState, "M")
        self.controlPosition = findSingleLayoutSymbol(startingMissionState, "C")

        self.start = (self.startPosition, False)
        self._expanded = 0

    def getStartState(self):
        """
        Returns the start state for the module repair problem.
        """
        return self.start

    def isGoalState(self, state):
        """
        Returns True if the robot reached C after picking up M.
        """
        psc, hasModule = state
        return psc == self.controlPosition and hasModule


    def _getStepCost(self, nextPosition, hasModule):
        """
        Returns the movement cost for entering nextPosition.

        """
        x, y = nextPosition
        costo_paso = self.startingMissionState.getTerrainCost(x, y)
        stepCost = costo_paso
        if hasModule:
            stepCost = 2 * costo_paso
        return stepCost

    def getSuccessors(self, state):
        """
        Returns a list of successors from the current state.

        Each successor must have the format:
            (nextState, direction, stepCost)

        where:
        - nextState keeps the problem state format: (nextPosition, nextHasModule)
        - direction is the action used to reach nextState
        - stepCost is the cost of that single movement

        Use the auxiliary function defined above to calculate the cost of each step.

        Mission rules:
        - The robot picks up the module when it enters M.
        - Movement uses normal terrain cost while the robot is not carrying M.
        - Once the robot is carrying M, movement costs twice the normal terrain cost.
        - The movement used to enter M still has normal terrain cost.
        """

        successors = []
        self._expanded += 1
        psc, hasModule = state
        for direccion in [
            Directions.NORTH,
            Directions.SOUTH,
            Directions.EAST,
            Directions.WEST,
        ]:
            dx, dy = Actions.directionToVector(direccion)
            nX, nY = int(psc[0] + dx), int(psc[1] + dy)
            if not self.walls[nX][nY]:
                pscnueva = (nX, nY)
                stepCost = self._getStepCost(pscnueva, hasModule)
                newHasModule = hasModule or pscnueva == self.modulePosition
                nextState = (pscnueva, newHasModule)
                successors.append((nextState, direccion, stepCost))
        return successors
    
    # mi codigo esta comentado en las siguentes lineas.
    # prompt usado fue "Al ejecutar el 
    # punto 4 me aparece un error relacionado con Directions.ACTIONS. 
    # ¿Qué significa este error y cómo debería corregirlo"
    # La respuesta dada Por ChatGPT fue: "El error relacionado con 
    # Directions.ACTIONS significa que la variable ACTIONS no está 
    # definida en la clase Directions. Esto puede ocurrir si estás intentando
    # acceder a una constante o lista de acciones que no existe en la 
    # implementación actual de la clase Directions.""
    # Al momento de recibir la respuesta también me indico que lo mejor era 
    # reemplazar Directions.ACTIONS por una lista de acciones 
    # definidas manualmente, como [Directions.NORTH, Directions.SOUTH, 
    # Directions.EAST, Directions.WEST].
    
    # Además me ayudo al corregir la construcción del siguiente estado usando el siguiente prompt:
    #“¿Así va bien esta parte de getSuccessors? 
    # No sé si estoy guardando bien el estado después de que el robot recoge M."
    # Respuesta: "para que no solo guardara la nueva posición del robot, sino también si ya 
    # había recogido el módulo. Además, el costo del movimiento pasó a calcularse
    # usando la posición a la que el robot realmente entra.""
     
    """def getSuccessors(self, state):
    successors = []
    self._expanded += 1
    psc, hasModule = state
    for direccion in Directions.ACTIONS:
        dx, dy = Actions.directionToVector(direccion)
        nx, ny = int(psc[0] + dx), int(psc[1] + dy)
        if not self.walls[nx][ny]:
            psc = (nx, ny)
            stepCost = self._getStepCost(psc, hasModule)
            newHasModule = hasModule or psc == self.modulePosition
            successors.append(
                (psc, direccion, stepCost)
            )
    return successors
    """

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.

        This method is used to report and validate the final path cost.
        """
        if actions is None:
            return 999999

        position, hasModule = self.getStartState()
        x, y = position
        cost = 0

        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)

            if self.walls[x][y]:
                return 999999

            nextPosition = (x, y)
            cost += self._getStepCost(nextPosition, hasModule)

            position = nextPosition
            hasModule = hasModule or position == self.modulePosition

        return cost


class SystemRepairProblem(SearchProblem):
    """
    Pick up the repair kit K, repair all damaged systems T, and finish at C.

    State: (position, hasKit, pendingSystems)
    - position: (x, y) tuple
    - hasKit: True if the robot already picked up the repair kit
    - pendingSystems: tuple with the T positions that still need repair

    Goal: all systems repaired and robot at C.
    Movement cost is uniform in this problem.
    """

    def __init__(self, startingMissionState: StationState):
        self.startingMissionState = startingMissionState
        self.walls = startingMissionState.getWalls()

        self.startPosition = startingMissionState.getRobotPosition()
        self.kitPosition = findSingleLayoutSymbol(startingMissionState, "K")
        self.controlPosition = findSingleLayoutSymbol(startingMissionState, "C")
        self.systemPositions = tuple(
            sorted(findLayoutSymbols(startingMissionState, "T"))
        )

        if len(self.systemPositions) == 0:
            raise Exception("Expected at least one 'T' system in the layout")

        self.start = (self.startPosition, False, self.systemPositions)
        self._expanded = 0
        self.heuristicInfo = {}  # For caching heuristic computations

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        position, hasKit, pendingSystems = state
        return position == self.controlPosition and hasKit and len(pendingSystems) == 0

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a unit cost.
        """
        successors = []
        self._expanded += 1

        position, hasKit, pendingSystems = state

        for direction in [
            Directions.NORTH,
            Directions.SOUTH,
            Directions.EAST,
            Directions.WEST,
        ]:
            x, y = position
            dx, dy = Actions.directionToVector(direction)
            nextx, nexty = int(x + dx), int(y + dy)

            if not self.walls[nextx][nexty]:
                nextPosition = (nextx, nexty)
                nextHasKit = hasKit or nextPosition == self.kitPosition
                nextPendingSystems = pendingSystems

                if nextHasKit and nextPosition in pendingSystems:
                    nextPendingSystems = tuple(
                        system for system in pendingSystems if system != nextPosition
                    )

                successors.append(
                    ((nextPosition, nextHasKit, nextPendingSystems), direction, 1)
                )

        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.
        Uses uniform movement cost.
        """
        if actions is None:
            return 999999

        position, hasKit, pendingSystems = self.getStartState()
        x, y = position
        cost = 0

        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)

            if self.walls[x][y]:
                return 999999

            position = (x, y)
            hasKit = hasKit or position == self.kitPosition

            if hasKit and position in pendingSystems:
                pendingSystems = tuple(
                    system for system in pendingSystems if system != position
                )

            cost += 1

        return cost
