# This file contains the options that you should modify to solve Question 2

#instructions pdf file:
# 1. For question2_1, we want the policy to seek the near terminal state (reward +1) via the short dangerous path (moving besides the row of -10 state).
# 2. For question2_2, we want the policy to seek the near terminal state (reward +1) via the long safe path (moving away from the row of -10 state).
# 3. For question2_3, we want the policy to seek the far terminal state (reward +10) via the short dangerous path (moving besides the row of -10 state).
# 4. For question2_4, we want the policy to seek the far terminal state (reward +10) via the long safe path (moving away from the row of -10 state).
# 5. For question2_5, we want the policy to avoid any terminal state and keep the episode going on forever.
# 6. For question2_6, we want the policy to seek any terminal state (even ones with the -10 penalty) and try to end the episode in the shortest time possible.


def question2_1():
    #TODO: Choose options that would lead to the desired results 
    
    return {
            "noise": 0,
            "discount_factor": 0.5,
            "living_reward": -1
        }


def question2_2():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.2,
        "discount_factor": 0.5,
        "living_reward": -1
    }

def question2_3():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0,
        "discount_factor": 0.8,
        "living_reward": -1
    }

#lsa
def question2_4():
    #TODO: Choose options that would lead to the desired results
        
        return {
        "noise": 0.2,
        "discount_factor": 1.0,
        "living_reward": -0.3
    }


def question2_5():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0,
        "discount_factor": 0.1,
        "living_reward": 10
    }

def question2_6():
    #TODO: Choose options that would lead to the desired results
    return {
        "noise": 0.4,
        "discount_factor": 0.9,
        "living_reward": -10
    }