from typing import Callable, DefaultDict, Dict, Generic, List, Optional, Union
from agents import Agent
from environment import Environment, S, A
from helpers.mt19937 import RandomGenerator
from helpers.utils import NotImplemented

import json
from collections import defaultdict

# The base class for all Reinforcement Learning Agents required for this problem set


class RLAgent(Agent[S, A]):
    rng: RandomGenerator  # A random number generator used for exploration
    actions: List[A]  # A list of all actions that the environment accepts
    discount_factor: float  # The discount factor "gamma"
    epsilon: float  # The exploration probability for epsilon-greedy
    learning_rate: float  # The learning rate "alpha"

    def __init__(self,
                 actions: List[A],
                 discount_factor: float = 0.99,
                 epsilon: float = 0.5,
                 learning_rate: float = 0.01,
                 seed: Optional[int] = None) -> None:
        super().__init__()
        # initialize the random generator with a seed for reproducability
        self.rng = RandomGenerator(seed)
        self.actions = actions
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.learning_rate = learning_rate

    # A virtual function that returns the Q-value for a specific state and action
    # This should be overriden by the derived RL agents
    def compute_q(self, env: Environment[S, A], state: S, action: A) -> float:
        return 0

    # Returns true if we should explore (rather than exploit)
    def should_explore(self) -> bool:
        return self.rng.float() < self.epsilon

    def act(self, env: Environment[S, A], observation: S, training: bool = False) -> A:

        actions = env.actions()
        if training and self.should_explore():
            # TODO: Return a random action whose index is "self.rng.int(0, len(actions)-1)"
            #NotImplemented()
            
            x= len(actions)-1

            #"self.rng.int(0, len(actions)-1)"

            return actions[self.rng.int(0,x)]
            
        else:
            # TODO: return the action with the maximum q-value as calculated by "compute_q" above
            # if more than one action has the maximum q-value, return the one that appears first in the "actions" list
            #NotImplemented()

            #initialize it to -infinit
            max_q = float('-inf')

            #haloop 3al actions
            for action in actions:
                #hahsb el q value lel action dah
                curr_q = self.compute_q(env, observation, action)

                #haget el max
                if curr_q > max_q:
                    max_q = curr_q
                    #haset el max action
                    max_action = action
                    
            return max_action
            

#############################
#######     SARSA      ######
#############################

# This is a class for a generic SARSA agent


class SARSALearningAgent(RLAgent[S, A]):
    Q: DefaultDict[S, DefaultDict[A, float]]  # The table of the Q values
    # The first key is the string representation of the state
    # The second key is the string representation of the action
    # The value is the Q-value of the given state and action

    def __init__(self,
                 actions: List[A],
                 discount_factor: float = 0.99,
                 epsilon: float = 0.5,
                 learning_rate: float = 0.01,
                 seed: Optional[int] = None) -> None:
        super().__init__(actions, discount_factor, epsilon, learning_rate, seed)
        self.Q = defaultdict(lambda: defaultdict(
            lambda: 0))  # The default Q value is 0

    def compute_q(self, env: Environment[S, A], state: S, action: A) -> float:
        # Return the Q-value of the given state and action
        return self.Q[state][action]
        # NOTE: we cast the state and the action to a string before querying the dictionaries


    #11 bayza

    # Update the value of Q(state, action) using this transition via the SARSA update rule
    def update(self, env: Environment[S, A], state: S, action: A, reward: float, next_state: S, next_action: Optional[A]):
        # TODO: Complete this function to update Q-table using the SARSA update rule
        # If next_action is None, then next_state is a terminal state in which case, we consider the Q-value of next_state to be 0
        
        #NotImplemented()

        #initialize it to 0
        next_q = 0
        
        #lw el next action be none yb2a mafesh next state yb2a el next_q hatfdal be zero
         
        #hacheck 3ala el next action eno not none el awel
        if next_action is not None:
            #hahsb el next q for the next state and next action
            next_q = self.compute_q(env, next_state, next_action)
 

        #hahsb el current q for the state and action
        curr_q = self.compute_q(env, state, action)
        
        #haupdate el q value using the sarsa update rule ely fe el document
        updated_q = curr_q + self.learning_rate * (reward + self.discount_factor * (next_q - curr_q))
        
        #haupdate el table
        self.Q[state][action] = updated_q



    # Save the Q-table to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            Q = {
                env.format_state(state): {
                    env.format_action(action): value for action, value in state_q.items()
                } for state, state_q in self.Q.items()
            }
            json.dump(Q, f, indent=2, sort_keys=True)

    # load the Q-table from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            Q = json.load(f)
            self.Q = {
                env.parse_state(state): {
                    env.parse_action(action): value for action, value in state_q.items()
                } for state, state_q in Q.items()
            }

#############################
#####   Q-Learning     ######
#############################

# This is a class for a generic Q-learning agent


class QLearningAgent(RLAgent[S, A]):
    Q: DefaultDict[str, DefaultDict[str, float]]  # The table of the Q values
    # The first key is the string representation of the state
    # The second key is the string representation of the action
    # The value is the Q-value of the given state and action

    def __init__(self,
                 actions: List[A],
                 discount_factor: float = 0.99,
                 epsilon: float = 0.5,
                 learning_rate: float = 0.01,
                 seed: Optional[int] = None) -> None:
        super().__init__(actions, discount_factor, epsilon, learning_rate, seed)
        self.Q = defaultdict(lambda: defaultdict(
            lambda: 0))  # The default Q value is 0

    def compute_q(self, env: Environment[S, A], state: S, action: A) -> float:
        # Return the Q-value of the given state and action
        return self.Q[state][action]
        # NOTE: we cast the state and the action to a string before querying the dictionaries


    # Given a state, compute and return the utility of the state using the function "compute_q"
    def compute_utility(self, env: Environment[S, A], state: S) -> float:
        # TODO: Complete this function.        
        #NotImplemented()

        #initialize it to -infinity
        max_q_value = float('-inf')

        #haloop 3ala kol el actions
        for action in self.actions:
            #print("testttttttttt")
            q_value = self.compute_q(env,state, action)

            #haget el max q value
            if q_value > max_q_value:
                max_q_value = q_value

        return max_q_value
        
    #4,8,10 bayzen -> fixed

    # Update the value of Q(state, action) using this transition via the Q-Learning update rule
    def update(self, env: Environment[S, A], state: S, action: A, reward: float, next_state: S, done: bool):
        # TODO: Complete this function to update Q-table using the Q-Learning update rule
        # If done is True, then next_state is a terminal state in which case, we consider the Q-value of next_state to be 0
        #NotImplemented()

        #initialize it to 0       
        max_q_next = 0

        if not done:
            #lw msh done yb2a msh terminal state

            if self.Q[next_state]:
                #lw true yb2a fe next state
                #zawedt el condition 3shan kan by3mel error 3shan by3mel max 3la empty list

                #haget the maximum q value among all actions for the next state using el fn ely 3amltha
                #max_q_next = max(self.Q[next_state].values())
                max_q_next = self.compute_utility(env, next_state)
  
        #ehsebl el cuur_q
        curr_q = self.compute_q(env, state, action)
        #curr_q = self.compute_utility(env, state)

        #ehsb el updated q nafs el sarsa bs gebt el max bs
        updated_q = curr_q + self.learning_rate * (reward + self.discount_factor * max_q_next - curr_q)

        #haupdate el value
        self.Q[state][action] = updated_q
    

    # Save the Q-table to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            Q = {
                env.format_state(state): {
                    env.format_action(action): value for action, value in state_q.items()
                } for state, state_q in self.Q.items()
            }
            json.dump(Q, f, indent=2, sort_keys=True)

    # load the Q-table from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            Q = json.load(f)
            self.Q = {
                env.parse_state(state): {
                    env.parse_action(action): value for action, value in state_q.items()
                } for state, state_q in Q.items()
            }

#########################################
#####   Approximate Q-Learning     ######
#########################################
# The type definition for a set of features representing a state
# The key is the feature name and the value is the feature value
Features = Dict[str, float]

# This class takes a state and returns the a set of features


class FeatureExtractor(Generic[S, A]):

    # Returns a list of feature names.
    # This will be used by the Approximate Q-Learning agent to initialize its weights dictionary.
    @property
    def feature_names(self) -> List[str]:
        return []

    # Given an enviroment and an observation (a state), return a set of features that represent the given state
    def extract_features(self, env: Environment[S, A], state: S) -> Features:
        return {}

# This is a class for a generic Q-learning agent


class ApproximateQLearningAgent(RLAgent[S, A]):
    weights: Dict[A, Features]    # The weights dictionary for this agent.
    # The first key is action and the second key is the feature name
    # The value is the weight
    # The feature extractor used to extract the features corresponding to a state
    feature_extractor: FeatureExtractor[S, A]

    def __init__(self,
                 feature_extractor: FeatureExtractor[S, A],
                 actions: List[A],
                 discount_factor: float = 0.99,
                 epsilon: float = 0.5,
                 learning_rate: float = 0.01,
                 seed: Optional[int] = None) -> None:
        super().__init__(actions, discount_factor, epsilon, learning_rate, seed)
        feature_names = feature_extractor.feature_names
        self.weights = {action: {feature: 0 for feature in feature_names}
                        for action in actions}  # we initialize the weights to 0
        self.feature_extractor = feature_extractor

    # Given the features of state and an action, compute and return the Q value
    def __compute_q_from_features(self, features: Dict[str, float], action: A) -> float:
        # TODO: Complete this function
        # NOTE: Remember to cast the action to string before quering self.weights
        #NotImplemented()

        #hsbet el q value
        sum_q_value = 0

        #haloop 3la kol el features
        for feature, value in features.items():

            #get el weight of this action and feature
            weight = self.weights[action][feature]

            #hadd 3la el variable el weights x value
            sum_q_value += weight * value


        return sum_q_value


    # Given the features of a state, compute and return the utility of the state using the function "__compute_q_from_features"
    def __compute_utility_from_features(self, features: Dict[str, float]) -> float:
        # TODO: Complete this function
        #NotImplemented()

        #hahsb el utility
        #el utility hya el maximum q value fe kol el actions

        #initializo to -infinity 3shan max
        max_utility = float('-inf')

        #haloop 3ala kol el actions
        for action in self.actions:

            #hahsb el q value for the current action
            q_value = self.__compute_q_from_features(features, action)

            #haget el max
            if q_value > max_utility:
                max_utility = q_value

        return max_utility

    def compute_q(self, env: Environment[S, A], state: S, action: A) -> float:
        features = self.feature_extractor.extract_features(env, state)
        return self.__compute_q_from_features(features, action)

    # Update the value of Q(state, action) using this transition via the Q-Learning update rule
    def update(self, env: Environment[S, A], state: S, action: A, reward: float, next_state: S, done: bool):
        # TODO: Complete this function to update weights using the Q-Learning update rule
        # If done is True, then next_state is a terminal state in which case, we consider the Q-value of next_state to be 0
        #NotImplemented()

        #initialize it
        target_q = reward

        #lw msh done yb2a msh terminal state
        if not done:
            #lw true yb2a fe next state

            #hahsb el features of the next state
            next_features = self.feature_extractor.extract_features(env, next_state)
            #hahsb el max q value for the next state
            max_q_next = self.__compute_utility_from_features(next_features)
            #haupdate el target q
            target_q = reward + self.discount_factor * max_q_next

        #ehsb el features of the current state
        features = self.feature_extractor.extract_features(env, state)

        #ehsb el curr_q value
        curr_q = self.__compute_q_from_features(features, action)

        #ehsb el difference between the current estimate and the target
        diff = target_q - curr_q

        #haupdate kol el weights
        #haloop 3alehom kolhom
        for feature, value in features.items():
            self.weights[action][feature] += self.learning_rate * diff * value


    # Save the weights to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            weights = {env.format_action(
                action): w for action, w in self.weights.items()}
            json.dump(weights, f, indent=2, sort_keys=True)

    # load the weights from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            weights = json.load(f)
            self.weights = {env.parse_action(
                action): w for action, w in weights.items()}
