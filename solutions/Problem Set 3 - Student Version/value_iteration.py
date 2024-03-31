from typing import Dict, Optional
from agents import Agent
from environment import Environment
from mdp import MarkovDecisionProcess, S, A
import json
from helpers.utils import NotImplemented

# This is a class for a generic Value Iteration agent
class ValueIterationAgent(Agent[S, A]):
    mdp: MarkovDecisionProcess[S, A] # The MDP used by this agent for training 
    utilities: Dict[S, float] # The computed utilities
                                # The key is the string representation of the state and the value is the utility
    discount_factor: float # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        self.utilities = {state:0 for state in self.mdp.get_states()} # We initialize all the utilities to be 0
        self.discount_factor = discount_factor
    
    # Given a state, compute its utility using the bellman equation
    # if the state is terminal, return 0        
    def compute_bellman(self, state: S) -> float:

        #check if the state is terminal
        if self.mdp.is_terminal(state):
            return 0
        
        max_utility = float('-inf')

        #haloop 3la kol el possible actions from this state
        for action in self.mdp.get_actions(state):
            # get the next state
            next_states = self.mdp.get_successor(state, action)
            #hainitializo be 0 3shan hazwed 3aleh
            expec_utility = 0

            for next_state, probability in next_states.items():

                #hahsb el reward
                reward = self.mdp.get_reward(state, action, next_state)
                #hahsb el utility of the next state
                utility = self.utilities[next_state]

                #hahsb el expected utility
                expec_utility += probability * (reward + self.discount_factor * utility)

            #hastore feh fe kol loop el max bta3hom
            max_utility = max(max_utility, expec_utility)
            #dah for debugging reasons
            #print("testtttttttttt max_utility: ", max_utility)

        return max(max_utility, expec_utility)

    # Applies a single utility update
    # then returns True if the utilities has converged (the maximum utility change is less or equal the tolerance)
    # and False otherwise
    def update(self, tolerance: float = 0) -> bool:

        #initializationnnn
        new_utilities = dict()
        max_diff = float('-inf')

        #haloop 3la kol el states
        for state in self.mdp.get_states(): 

            #save el old utility
            old_utility = self.utilities[state]
            #get the new utility using bellman equationn
            new_utility = self.compute_bellman(state) 
            #hastore el new utility fe dictionary
            new_utilities[state] = new_utility 

            #calculate el diff
            diff = abs(new_utility - old_utility)
            #hastore el max diff
            max_diff = max(max_diff, diff)  

        #update el utilities using el dict ely 3amlto
        self.utilities = new_utilities 

        #el condition ely matlob fo2
        if max_diff <= tolerance:  
            return True
        else:
            return False
        

    # This function applies value iteration starting from the current utilities stored in the agent and stores the new utilities in the agent
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: Optional[int] = None, tolerance: float = 0) -> int:
        #TODO: Complete this function to apply value iteration for the given number of iterations

        count = 0
        #haloop lhd el number of iterations is reached or the utilities converge
        while iterations is None or count < iterations:

            count += 1

            #lazem abreak
            #self.update(tolerance)

            if self.update(tolerance):
              #if true break
              break

        return count
    
    
    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    def act(self, env: Environment[S, A], state: S) -> A:

        #initializationnnn
        best_action = None
        best_utility = float('-inf')

        #hacheck le el state deh state terminal
        if self.mdp.is_terminal(state):
            return None

        #hadwar 3la el action with the max utility
        #haloop 3la kol el actions
        for action in self.mdp.get_actions(state):
            #hagib el next stateS
            next_states = self.mdp.get_successor(state, action)
            #haintialize el expected utility be 0 3shan badd 3aleh
            expected_utility = 0

            #haloop 3la kol el next states lel action da we ahseblo el expected utility
            for next_state, probability in next_states.items():
                #hagib el reward
                reward = self.mdp.get_reward(state, action, next_state)
                #hagib el utility of the next state
                utility = self.utilities[next_state]

                #hahsb el expected utility using el reward w el utility w el probability
                expected_utility += probability * (reward + self.discount_factor * utility)

            #hastore el max utility w el action ely 3mlha lw kant akbr mn el best utility
            if expected_utility > best_utility:

                best_utility = expected_utility
                best_action = action

        #hareturn el best_action fe el akher

        return best_action
    
    # Save the utilities to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            utilities = {self.mdp.format_state(state): value for state, value in self.utilities.items()}
            json.dump(utilities, f, indent=2, sort_keys=True)
    
    # loads the utilities from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            utilities = json.load(f)
            self.utilities = {self.mdp.parse_state(state): value for state, value in utilities.items()}
