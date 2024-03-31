    #sa

    # def update(self, tolerance: float = 0) -> bool:
    #     #TODO: Complete this function
    #     new_utility_dict=dict() #initialize a new dictionary to store the new utilities

    #     max_utility_change=float('-inf') #initialize the max utility change to -infinity

    #     for state in self.mdp.get_states(): #loop over all the states in the system

    #         old_utility=self.utilities[state]  #get the old utility before computing bellman

    #         new_utility=self.compute_bellman(state) #compute the bellman equation on the current state

    #         new_utility_dict[state]=new_utility #store the new utility in the new dictionary

    #         if abs(new_utility-old_utility)>max_utility_change: #calculate the max utility change
    #             max_utility_change=abs(new_utility-old_utility)

    #     self.utilities=new_utility_dict  #update the utilities dictionary with the new utilities

    #     if max_utility_change<=tolerance: #if the max utility change is less than the tolerance then return True
    #         return True
    #     else:
    #         return False




    # def compute_bellman(self, state: S) -> float:
    #     #TODO: Complete this function

    #     if (self.mdp.is_terminal(state)): #Return 0 if the state is terminal
    #         return 0
        
    #     else:  #if the state is not terminal then compute the bellman equation

    #         max_utility= float("-inf") #initialize the max utility to -infinity

    #         actions=self.mdp.get_actions(state)  #get all the actions of the current state and loop over them

    #         for action in actions:

    #             successors=self.mdp.get_successor(state,action) #get all the successors of the current state and current action taken
    #             utility_sum=0 #initialize the summation of the utilities of the next states on a certain action to 0

    #             for successor in successors:  #loop over successors

    #                 probability=successors[successor]    #this is a part of dictionary so successor is the next state which is the key and successors[successor] is the probability

    #                 reward=self.mdp.get_reward(state,action,successor) #calculate the rewrad of taking the action on the current state to the next state

    #                 next_state_utility=self.utilities[successor] #get the utility of the next state

    #                 new_utility=probability*(reward+(self.discount_factor*next_state_utility)) #calculate the utility on the current state and action and next state according to the bellman equation
                    
    #                 utility_sum+=new_utility #sigma part of the equation

    #             if utility_sum>max_utility: #if the summation is bigger than the max utility reached by now then update the max utility
    #                 max_utility=utility_sum
    #             print("testtttttttttt max_utility: ", max_utility)

    #         return max_utility  #return the max utility reached




#initialzied it to 0
        next_q = 0

        #hacheck 3ala el next action eno not none el awel 3shan le be none yb2a el next state terminal (next_q = 0)
        if next_action is not None:
            #hahsb el next q for the next state and next action
            next_q = self.compute_q(env, next_state, next_action)

        #hahsb el current q for the state and action
        curr_q = self.compute_q(env, state, action)
        
        #haupdate el q value using the sarsa update rule ely fe el document
        updated_q = curr_q + self.learning_rate * (reward + self.discount_factor * (next_q - curr_q))
        
        #haupdate el table
        self.Q[state][action] = updated_q


##################
 #Update the direction of the snake based on the action
        # self.direction = action

        # # Move the snake in the new direction
        # head = self.snake[0]
        # if self.direction == Direction.UP:
        #     new_head = Point(head.x, head.y - 1)
        # elif self.direction == Direction.DOWN:
        #     new_head = Point(head.x, head.y + 1)
        # elif self.direction == Direction.LEFT:
        #     new_head = Point(head.x - 1, head.y)
        # elif self.direction == Direction.RIGHT:
        #     new_head = Point(head.x + 1, head.y)
        # #yb2a el direction none
        # else:
        #     new_head = head

        # # Check if the new head collides with the snake's body or the boundaries of the grid
        # if (
        #     new_head in self.snake[1:] or
        #     new_head.x < 0 or new_head.x >= self.width or
        #     new_head.y < 0 or new_head.y >= self.height
        # ):
        #     # Game over, return the final state and reward
        #     self.snake.append(new_head)  # Add the new head to the snake's body
        #     done = True
        #     reward = -100
        #     observation = SnakeObservation(tuple(self.snake), self.direction, None)
        # else:
        #     # Move the snake by adding the new head and removing the tail
        #     self.snake.insert(0, new_head)
        #     if new_head == self.apple:
        #         # The snake has eaten the apple, generate a new apple and increase the reward
        #         self.apple = self.generate_random_apple()
        #         reward = 100
        #     else:
        #         # The snake has not eaten the apple, remove the tail
        #         self.snake.pop()
        #         reward = 0
        #     observation = SnakeObservation(tuple(self.snake), self.direction, self.apple)
        #     done = False