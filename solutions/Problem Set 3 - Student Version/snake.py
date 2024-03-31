from typing import Dict, List, Optional, Set, Tuple
from mdp import MarkovDecisionProcess
from environment import Environment
from mathutils import Point, Direction
from helpers.mt19937 import RandomGenerator
from helpers.utils import NotImplemented
import json
from dataclasses import dataclass

"""
Environment Description:
    The snake is a 2D grid world where the snake can move in 4 directions.
    The snake always starts at the center of the level (floor(W/2), floor(H/2)) having a length of 1 and moving LEFT.
    The snake can wrap around the grid.
    The snake can eat apples which will grow the snake by 1.
    The snake can not eat itself.
    You win if the snake body covers all of the level (there is no cell that is not occupied by the snake).
    You lose if the snake bites itself (the snake head enters a cell occupied by its body).
    The action can not move the snake in the opposite direction of its current direction.
    The action can not move the snake in the same direction 
        i.e. (if moving right don't give an action saying move right).
    Eating an apple increases the reward by 1.
    Winning the game increases the reward by 100.
    Losing the game decreases the reward by 100.
"""

# IMPORTANT: This class will be used to store an observation of the snake environment
@dataclass(frozen=True)
class SnakeObservation:
    snake: Tuple[Point]     # The points occupied by the snake body 
                            # where the head is the first point and the tail is the last  
    direction: Direction    # The direction that the snake is moving towards
    apple: Optional[Point]  # The location of the apple. If the game was already won, apple will be None


class SnakeEnv(Environment[SnakeObservation, Direction]):

    rng: RandomGenerator  # A random generator which will be used to sample apple locations

    snake: List[Point]
    direction: Direction
    apple: Optional[Point]

    def __init__(self, width: int, height: int) -> None:
        super().__init__()
        assert width > 1 or height > 1, "The world must be larger than 1x1"
        self.rng = RandomGenerator()
        self.width = width
        self.height = height
        self.snake = []
        self.direction = Direction.LEFT
        self.apple = None

    def generate_random_apple(self) -> Point:
        """
        Generates and returns a random apple position which is not on a cell occupied 
        by the snake's body.
        """
        snake_positions = set(self.snake)
        possible_points = [Point(x, y) 
            for x in range(self.width) 
            for y in range(self.height) 
            if Point(x, y) not in snake_positions
        ]
        return self.rng.choice(possible_points)

    def reset(self, seed: Optional[int] = None) -> Point:
        """
        Resets the Snake environment to its initial state and returns the starting state.
        Args:
            seed (Optional[int]): An optional integer seed for the random
            number generator used to generate the game's initial state.

        Returns:
            The starting state of the game, represented as a Point object.
        """
        if seed is not None:
            self.rng.seed(seed) # Initialize the random generator using the seed
        # TODO add your code here
        # IMPORTANT NOTE: Define the snake before calling generate_random_apple
        #NotImplemented()
            
        #harg3 el snake fe el nos
        # // 3shan y3mel floor maytl3sh 2.5 mslan dah msh point
        x = self.width // 2
        y = self.height // 2
        self.snake = [Point(x, y)]

        #el snake bybda2 yemshy left
        self.direction = Direction.LEFT

        #hagenerate a random apple
        self.apple = self.generate_random_apple()

        return SnakeObservation(tuple(self.snake), self.direction, self.apple)
        


    def actions(self) -> List[Direction]:
        """
        Returns a list of the possible actions that can be taken from the current state of the Snake game.
        Returns:
            A list of Directions, representing the possible actions that can be taken from the current state.

        """
        
        # TODO add your code here
        # a snake can wrap around the grid
        # NOTE: The action order does not matter
        #NotImplemented()
        possible_actions = []
        possible_actions.append(Direction.NONE)


        #hadefine el opposite direction
        if self.direction == Direction.UP:
            opposite_direction = Direction.DOWN
        elif self.direction == Direction.DOWN:
            opposite_direction = Direction.UP
        elif self.direction == Direction.LEFT:
            opposite_direction = Direction.RIGHT
        elif self.direction == Direction.RIGHT:
            opposite_direction = Direction.LEFT
        #yb2a el direction none
        else:
            opposite_direction = Direction.NONE

        #3la hasab el opposite direction happend fe el possible actions
        if opposite_direction == Direction.LEFT:
            #possible_actions.append(Direction.RIGHT)
            possible_actions.append(Direction.UP)
            possible_actions.append(Direction.DOWN)
        elif opposite_direction == Direction.RIGHT:
            #possible_actions.append(Direction.LEFT)
            possible_actions.append(Direction.UP)
            possible_actions.append(Direction.DOWN)
        elif opposite_direction == Direction.UP:
            possible_actions.append(Direction.RIGHT)
            possible_actions.append(Direction.LEFT)
            #possible_actions.append(Direction.DOWN)
        elif opposite_direction == Direction.DOWN:
            possible_actions.append(Direction.RIGHT)
            #possible_actions.append(Direction.UP)
            possible_actions.append(Direction.LEFT)

        #yb2a el direction none
        else:
            possible_actions.append(Direction.RIGHT)
            possible_actions.append(Direction.UP)
            possible_actions.append(Direction.LEFT)
            possible_actions.append(Direction.DOWN)

        #mazonsh leha lazma
        #sort the possible_actions descending
        #possible_actions.sort(reverse=True)
            
        return possible_actions
    
        

    def step(self, action: Direction) -> Tuple[SnakeObservation, float, bool, Dict]:
        """
        Updates the state of the Snake game by applying the given action.

        Args:
            action (Direction): The action to apply to the current state.

        Returns:
            A tuple containing four elements:
            - next_state (SnakeObservation): The state of the game after taking the given action.
            - reward (float): The reward obtained by taking the given action.
            - done (bool): A boolean indicating whether the episode is over.
            - info (Dict): A dictionary containing any extra information. You can keep it empty.
        """
        # TODO Complete the following function
        #NotImplemented()

        done = False
        reward = 0
        observation = SnakeObservation(tuple(self.snake), self.direction, self.apple)
        
        # return observation, reward, done, {}

        #lazem el if deh 3shan lw galy el action none
        if action != Direction.NONE:
            self.direction = action

        #3ayz a3rf el head fen
        head_x = self.snake[0].x
        head_y = self.snake[0].y

        #haset el new head
        if self.direction == Direction.UP:
            head_y -= 1
        elif self.direction == Direction.DOWN:
            head_y += 1
        elif self.direction == Direction.LEFT:
            head_x -= 1
        elif self.direction == Direction.RIGHT:
            head_x += 1

        #3shan el wrap around
        #lw wsl le fo2 ynzel taht and vice versa
        #lw wsl le shmal yro7 ymeen and vice versa
        head_x = head_x % self.width
        head_y = head_y % self.height

        #dah el new head b3d el action
        new_head = Point(head_x, head_y)

        
        



        #check if the snake bites itself
        #lw el new head b2a fe heta el snake feha
        if new_head in self.snake[1:]:
            #haupdate el reward
            reward = -100
            #kda el game khls
            done = True

        #hna new head b2a el head of the snake
        self.snake.insert(0, new_head) 

        #hacheck if the snake eats the apple
        #el head b2a 3nd el apple
        if new_head == self.apple:

            #hacheck lw 3ml occupy lel whole grid (ksb)
            if len(self.snake) == self.width * self.height:
                #print("\n")
                #print("testtttttt\n",len(self.snake))
                # ,self.width * self.height)
                
                #zawed el reward
                # +1 3shan akl tofaha kman
                reward = 101
                done = True
                observation = SnakeObservation(tuple(self.snake), self.direction, self.apple)

                return observation, reward, done, {}  # info can be left empty
            
            #lw lsa maksbtsh
            else:
                
                #zawed el reward
                reward = 1
                #hazwed apple gdeda
                #error lw mazwedtsh el apple gdeda
                self.apple = self.generate_random_apple()
            
        else:
            #maklsh apple fa lazem ams7 el tail
            self.snake.pop()

        #print("testttttt2\n")
        

        #nafs el line ely fo2 3shan areturn
        observation = SnakeObservation(tuple(self.snake), self.direction, self.apple)

        return observation, reward, done, {}  # info can be left empty



    ###########################
    #### Utility Functions ####
    ###########################

    def render(self) -> None:
        # render the snake as * (where the head is an arrow < ^ > v) and the apple as $ and empty space as .
        for y in range(self.height):
            for x in range(self.width):
                p = Point(x, y)
                if p == self.snake[0]:
                    char = ">^<v"[self.direction]
                    print(char, end='')
                elif p in self.snake:
                    print('*', end='')
                elif p == self.apple:
                    print('$', end='')
                else:
                    print('.', end='')
            print()
        print()

    # Converts a string to an observation
    def parse_state(self, string: str) -> SnakeObservation:
        snake, direction, apple = eval(str)
        return SnakeObservation(
            tuple(Point(x, y) for x, y in snake), 
            self.parse_action(direction), 
            Point(*apple)
        )
    
    # Converts an observation to a string
    def format_state(self, state: SnakeObservation) -> str:
        snake = tuple(tuple(p) for p in state.snake)
        direction = self.format_action(state.direction)
        apple = tuple(state.apple)
        return str((snake, direction, apple))
    
    # Converts a string to an action
    def parse_action(self, string: str) -> Direction:
        return {
            'R': Direction.RIGHT,
            'U': Direction.UP,
            'L': Direction.LEFT,
            'D': Direction.DOWN,
            '.': Direction.NONE,
        }[string.upper()]
    
    # Converts an action to a string
    def format_action(self, action: Direction) -> str:
        return {
            Direction.RIGHT: 'R',
            Direction.UP:    'U',
            Direction.LEFT:  'L',
            Direction.DOWN:  'D',
            Direction.NONE:  '.',
        }[action]