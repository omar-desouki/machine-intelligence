from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers.utils import NotImplemented

# TODO: (Optional) Instead of Any, you can define a type for the parking state
ParkingState = List[List[str]]
# ParkingState = Any

# An action of the parking problem is a tuple containing an index 'i' and a direction 'd' where car 'i' should move in the direction 'd'.
ParkingAction = Tuple[int, Direction]


# This is the implementation of the parking problem
class ParkingProblem(Problem[ParkingState, ParkingAction]):
    passages: Set[
        Point
    ]  # A set of points which indicate where a car can be (in other words, every position except walls).
    cars: Tuple[Point]  # A tuple of points where state[i] is the position of car 'i'.
    slots: Dict[
        Point, int
    ]  # A dictionary which indicate the index of the parking slot (if it is 'i' then it is the lot of car 'i') for every position.
    # if a position does not contain a parking slot, it will not be in this dictionary.
    width: int  # The width of the parking lot.
    height: int  # The height of the parking lot.
    # cost: int = 0

    # This function should return the initial state
    def get_initial_state(self) -> ParkingState:
        initialstate = []

        for y in range(self.height):  # loop on every column
            row = list()

            for x in range(self.width):  # loop on every row
                position = Point(x, y)
                if position in self.passages:
                    # not a wall
                    if position in self.slots:
                        # If it's a parking slot -> add this car index
                        row.append(str(self.slots[position]))
                    elif position in self.cars:
                        # bageb el index we bahoto fe ascii
                        index = self.cars.index(position)
                        ascii_value = 65 + index
                        row.append(chr(ascii_value))
                    else:
                        # If it's an empty passage, mark it as empty
                        row.append(".")
                else:
                    # its a wall
                    row.append("#")
            initialstate.append(row)  # kol loop yhot el row dah we ynzel row

        #testing
        # print("omar's testt.....")
        # print(initialstate)
        # print("..........................\n")
        # print(initialstate[5][1])
        return initialstate

    # This function should return True if the given state is a goal. Otherwise, it should return False.
    def is_goal(self, state: ParkingState) -> bool:
        count = 0
        for row in range(self.height):  # loop on every column
            for col in range(self.width):  # loop on every row
                position = Point(col, row)
                if position in self.slots:
                    # bageb el index bta3 el car ely el mafrod yb2a mawgod hna
                    correctcarindex = self.slots[position]
                    if state[row][col].isalpha():
                        # bageb el index bta3 el actual car ely fe el position dah
                        char = state[row][col]
                        actualcarindex = ord(char) - ord("A")
                        # lw msh equal yb2a lsa mawsltsh llgoal state
                        if actualcarindex == correctcarindex:
                            count += 1
        if count == len(
            self.slots
        ):  # bashof lw dakhlt el condition ad 3dd el parking spaces ely 3andy
            return True
        else:
            return False

    # This function returns a list of all the possible actions that can be applied to the given state
    def get_actions(self, state: ParkingState) -> List[ParkingAction]:
        # RIGHT = 0
        # UP    = 1
        # LEFT  = 2
        # DOWN  = 3

        # if self.is_goal(state) == True:
        #   return None

        actions = []
        for row in range(self.height):  # loop on every column
            for col in range(self.width):  # loop on every row
                # position = Point(col,row)
                if state[row][
                    col
                ].isalpha():  # m3nah en fe car fe el mkan dah nshof eh el possible movements leha b2a
                    char = state[row][col]
                    carindex = ord(char) - ord("A")  # bageb index el car ely 3andy

                    if state[row][col + 1] != "#":  # consition byshof lw fe wall gambo
                        if (
                            state[row][col + 1].isalpha() == False
                        ):  # condition byshof lw feh car gambo
                            ParkingAction = (carindex, "R")
                            actions.append(ParkingAction)

                    if state[row + 1][col] != "#":  #down actions
                        if state[row + 1][col].isalpha() == False:
                            ParkingAction = (carindex, "D")
                            actions.append(ParkingAction)

                    if state[row][col - 1] != "#": #left actions
                        if state[row][col - 1].isalpha() == False:
                            ParkingAction = (carindex, "L")
                            actions.append(ParkingAction)
 
                    if state[row - 1][col] != "#": #up actions
                        if state[row - 1][col].isalpha() == False:
                            ParkingAction = (carindex, "U")
                            actions.append(ParkingAction)
        return actions

    # This function returns a new state which is the result of applying the given action to the given state
    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
        carindex = action[0]
        direction = action[1]

        ascii_value = 65 + carindex
        carchar = chr(ascii_value)  # bageb el car letter mn el index

        # for loops badwar 3ala el col we el row ely el car fehom
        for row in range(self.height):  # loop on every column
            for col in range(self.width):  # loop on every row
                if state[row][col] == carchar:
                    carrow = row
                    carcol = col

            # 3la hasab el direction baupdate el state
        if str(direction) == "R":
            state[carrow][carcol] = "."
            state[carrow][carcol + 1] = carchar

        if str(direction) == "U":
            state[carrow][carcol] = "."
            state[carrow - 1][carcol] = carchar

        if str(direction) == "L":
            state[carrow][carcol] = "."
            state[carrow][carcol - 1] = carchar

        if str(direction) == "D":
            state[carrow][carcol] = "."
            state[carrow + 1][carcol] = carchar

        return state

    # This function returns the cost of applying the given action to the given state
    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        # TODO: ADD YOUR CODE HERE

        cost = 0  # el cost bta3 el action ely mdholy

        # for actions in action:
        carindex = action[0]
        direction = action[1]

        ascii_value = 65 + carindex
        carchar = chr(ascii_value)  # bageb el car letter mn el index

        # for loops badwar 3ala el col we el row ely el car fehom
        for row in range(self.height):  # loop on every column
            for col in range(self.width):  # loop on every row
                if state[row][col] == carchar:
                    carrow = row
                    carcol = col

        costdependingonletter = 26 - carindex  # as explained in pdf
        cost += costdependingonletter

        if str(direction) == "R":
            position = Point(carcol + 1, carrow)
            if position in self.slots:  # el mkan dah parking 3arbya
                # lw mkan 8ery zawed el cost b100
                carparkingindex = self.slots[position]
                if carparkingindex != carindex:
                    cost += 100

        if str(direction) == "U":
            position = Point(carcol, carrow + 1)
            if position in self.slots:  # el mkan dah parking 3arbya
                # lw mkan 8ery zawed el cost b100
                carparkingindex = self.slots[position]
                if carparkingindex != carindex:
                    cost += 100

        if str(direction) == "L":
            position = Point(carcol - 1, carrow)
            if position in self.slots:  # el mkan dah parking 3arbya
                # lw mkan 8ery zawed el cost b100
                carparkingindex = self.slots[position]
                if carparkingindex != carindex:
                    cost += 100

        if str(direction) == "D":
            position = Point(carcol, carrow - 1)
            if position in self.slots:  # el mkan dah parking 3arbya
                # lw mkan 8ery zawed el cost b100
                carparkingindex = self.slots[position]
                if carparkingindex != carindex:
                    cost += 100

        return cost

    # Read a parking problem from text containing a grid of tiles
    @staticmethod
    def from_text(text: str) -> "ParkingProblem":
        passages = set()
        cars, slots = {}, {}
        lines = [line for line in (line.strip() for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != "#":
                    passages.add(Point(x, y))
                    if char == ".":
                        pass
                    elif char in "ABCDEFGHIJ":
                        cars[ord(char) - ord("A")] = Point(x, y)
                    elif char in "0123456789":
                        slots[int(char)] = Point(x, y)
        problem = ParkingProblem()
        problem.passages = passages
        problem.cars = tuple(cars[i] for i in range(len(cars)))
        problem.slots = {position: index for index, position in slots.items()}
        problem.width = width
        problem.height = height
        return problem

    # Read a parking problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> "ParkingProblem":
        with open(path, "r") as f:
            return ParkingProblem.from_text(f.read())


#              testttttttttttttttttttttt..testttttttttttttttttttttt

# text_representation =  """#########
# #####
# #A.0#
# #####"""
# actions = [(0,'R')]
# # actions = "[(0,'R'),(0,'R')]"

# parking_problem = ParkingProblem.from_text(text_representation)

# # # # # Call the get_initial_state method on the instance
# initial_state = parking_problem.get_initial_state()
# print(initial_state)

# cost = parking_problem.get_cost(initial_state,actions)
# print(cost)

# nextstate = parking_problem.get_successor(initial_state,actions)
# print(nextstate)

# possibleactions = parking_problem.get_actions(nextstate)
# print(possibleactions)

# isgoal= parking_problem.is_goal(nextstate)
# print(isgoal)


#         "52",
#         "True",
#         "None",
#         "'parks/park1.txt'"
