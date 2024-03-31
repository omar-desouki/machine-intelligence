from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented

#TODO: Import any modules you want to use

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.
def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)
    
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action) for index, (action , state) in enumerate(actions_states))
    return value, action

# Apply Minimax search and return the game tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that 
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].
#def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1 ) -> Tuple[float, A]:

    #TODO: Complete this function
    #initial_state = game.get_initial_state()
    #5,7,8,9 mhatgen ytzbto

    terminal, values = game.is_terminal(state) #lazem acheck hata fe el initial state
    #####################
    # if terminal or (max_depth != -1 and depth >= max_depth):#base case
    #     return heuristic(game, state, game.get_turn(state)), None
    
    if terminal: #lw termianl yrg3 el outcome
        #print("hnaaaa")
        return values[0], None  
    
    #el error hna
    if max_depth == 0:  # lw wsl lel max depth yreturn the heuristic value 
        #print("hnaaaa2")
        return heuristic(game, state, 0), None

    #####################

    ##########initalization
    #initalize the best_value depending on which player is playing
    if game.get_turn(state) == 0:
        best_value = float('-inf') 
    else:
        best_value = float('inf')

    #initialize best_value    
    best_action = None
    ##########

    for action in game.get_actions(state): #loop on all possible actions

        successor_state = game.get_successor(state, action) #haget el successor_state
        value, _ = minimax(game, successor_state, heuristic, max_depth-1) #ha get el value mm el successor_state we aminus el max_depth kol mara (recursion) lhd ma awsl le terminal aw max_depth == 0

        if game.get_turn(state) == 0:  # Max player turn

            if value > best_value: #store the highest value
                best_value, best_action = value, action

        else:  # Min player turn

            if value < best_value: #store the lowest value
                best_value, best_action = value, action

    return best_value, best_action 



# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.
#def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1, alpha: float = float('-inf'), beta: float = float('inf')) -> Tuple[float, A]:
    #TODO: Complete this function

    terminal, values = game.is_terminal(state) #lazem acheck hata fe el initial state
    #####################
    if terminal: #lw termianl yrg3 el outcome
        return values[0], None


    if max_depth == 0:  # lw wsl lel max depth yreturn the heuristic value
        return heuristic(game, state, 0), None

    #####################

    ##########initalization
    #initalize the best_value depending on which player is playing
    if game.get_turn(state) == 0:
        best_value = float('-inf') 
    else:
        best_value = float('inf')
    #initialize best_value    
    best_action = None
    ##########

    for action in game.get_actions(state): #loop on all possible actions

        successor_state = game.get_successor(state, action) #haget el succesor state
        value, _ = alphabeta(game, successor_state, heuristic, max_depth-1, alpha, beta) #ha get el value mm el successor_state we aminus el max_depth kol mara (recursion) lhd ma awsl le terminal aw max_depth == 0

        if game.get_turn(state) == 0:  # Max player turn

            if value > best_value: #store the highest value
                best_value, best_action = value, action

            alpha = max(alpha, best_value) #store el alpha

        else:  # Min player turn
            if value < best_value: #store the lowest value
                best_value, best_action = value, action

            beta = min(beta, best_value) #store el beta

        if beta <= alpha:
            break

    return best_value, best_action

# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: Read the hint for minimax.
#def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1, alpha: float = float('-inf'), beta: float = float('inf')) -> Tuple[float, A]:
    #TODO: Complete this function
    terminal, values = game.is_terminal(state)

    ###############base case
    if terminal:#lw termianl yrg3 el outcome
        return values[0], None
    
    if max_depth == 0: # lw wsl lel max depth yreturn the heuristic value
        return heuristic(game, state, 0), None
    ###############

    if game.get_turn(state) == 0:  # Max player turn

        #dakhlt el intialzarion gwa 3shan et2smo
        best_value = float('-inf') 
        best_action = None
        #######################################
        
        actions = game.get_actions(state)
        actions.sort(key=lambda a: heuristic(game, game.get_successor(state, a), 0), reverse=True)
        
        for action in actions: #haloop on all possible actions

            successor_state = game.get_successor(state, action) #haget el succesor state
            value, _ = alphabeta_with_move_ordering(game, successor_state, heuristic, max_depth-1, alpha, beta) #ha get el value mm el successor_state we aminus el max_depth kol mara (recursion) lhd ma awsl le terminal aw max_depth == 0
            
            if value > best_value:
                best_value, best_action = value, action
            
            #ekhtlaf 3n ely fo2
            alpha = max(alpha, best_value) 
            
            if alpha >= beta:
                break
            ###############
        
        return best_value, best_action
    
    else:  # Min player turn

        #dakhlt el intialzarion gwa 3shan et2smo
        best_value = float('inf')
        best_action = None
        #######################################

        actions = game.get_actions(state)
        actions.sort(key=lambda a: heuristic(game, game.get_successor(state, a), 0))
        
        #nafs el klam ely fo2
        for action in actions:
            successor_state = game.get_successor(state, action)
            value, _ = alphabeta_with_move_ordering(game, successor_state, heuristic, max_depth-1, alpha, beta)
            
            if value < best_value:
                best_value, best_action = value, action
            
            beta = min(beta, best_value)
            
            if alpha >= beta:
                break
        
        return best_value, best_action


# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).
#def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:

def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
   

    terminal, values = game.is_terminal(state) #lazem acheck hata fe el initial state
    #####################
    if terminal: #lw termianl yrg3 el outcome
        return values[0], None

    if max_depth == 0:   # lw wsl lel max depth yreturn the heuristic value
        return heuristic(game, state, 0), None

    #####################
    if game.get_turn(state) == 0:  # Max player turn

        #dakhlt el intialzarion gwa 3shan et2smo
        best_value = float('-inf') 
        best_action = None
        #######################################

        for action in game.get_actions(state):#loop on all action
            successor_state = game.get_successor(state, action) #haget el succesor state
            value, _ = expectimax(game, successor_state, heuristic, max_depth-1) #ha get el value mm el successor_state we aminus el max_depth kol mara (recursion) lhd ma awsl le terminal aw max_depth == 0

            if value > best_value:
                best_value, best_action = value, action

        return best_value, best_action
    
    else:  # change node

        total_value = 0

        for action in game.get_actions(state): 
            successor_state = game.get_successor(state, action)
            value, _ = expectimax(game, successor_state, heuristic, max_depth-1)
            total_value += value  # equal probability for each action

        avg_value = total_value / len(game.get_actions(state)) #get el average value
        return avg_value, None

