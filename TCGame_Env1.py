# from gym import spaces
import numpy as np
import random
from itertools import groupby
from itertools import product



class TicTacToe():

    def __init__(self):
        """initialise the board"""
        
        # initialise state as an array
        self.state = [np.nan for _ in range(9)]  # initialises the board position, can initialise to an array or matrix
        # all possible numbers
        self.all_possible_numbers = [i for i in range(1, len(self.state) + 1)] # , can initialise to an array or matrix

        self.reset()


    def is_winning(self, curr_state):
        """Takes state as an input and returns whether any row, column or diagonal has winning sum
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan]
        Output = False"""
        agent_moves=[1,3,5,7,9]
        env_moves=[2,4,6,8]
        
        r1=[0,1,2]
        r2=[3,4,5]
        r3=[6,7,8]

        c1=[0,3,6]
        c2=[1,4,7]
        c3=[2,5,8]

        d1=[0,4,8]
        d2=[2,4,6]



        # row check
        r1_a_chk=all([curr_state[i] in agent_moves for i in r1])
        r1_e_chk=all([curr_state[i] in env_moves for i in r1])


        r2_a_chk=all([curr_state[i] in agent_moves for i in r2])
        r2_e_chk=all([curr_state[i] in env_moves for i in r2])
        
        r3_a_chk=all([curr_state[i] in agent_moves for i in r3])
        r3_e_chk=all([curr_state[i] in env_moves for i in r3])


        # col check
        c1_a_chk=all([curr_state[i] in agent_moves for i in c1])
        c1_e_chk=all([curr_state[i] in env_moves for i in c1])

        c2_a_chk=all([curr_state[i] in agent_moves for i in c2])
        c2_e_chk=all([curr_state[i] in env_moves for i in c2])

        c3_a_chk=all([curr_state[i] in agent_moves for i in c3])
        c3_e_chk=all([curr_state[i] in env_moves for i in c3])


        # diag check
        d1_a_chk=all([curr_state[i] in agent_moves for i in d1])
        d1_e_chk=all([curr_state[i] in env_moves for i in d1])

        d2_a_chk=all([curr_state[i] in agent_moves for i in d2])
        d2_e_chk=all([curr_state[i] in env_moves for i in d2])


        if((r1_a_chk  or r2_a_chk or r3_a_chk) or(r1_e_chk or r2_e_chk or r3_e_chk)):
            return True
        elif((c1_a_chk  or c2_a_chk or c3_a_chk) or(c1_e_chk or c2_e_chk or c3_e_chk)):
            return True
        elif((d1_a_chk  or d2_a_chk ) or(d1_e_chk or d2_e_chk ) ):
            return True
        else:
            return False
 

    def is_terminal(self, curr_state):
        # Terminal state could be winning state or when the board is filled up

        if self.is_winning(curr_state) == True:
            return True, 'Win'

        elif len(self.allowed_positions(curr_state)) ==0:
            return True, 'Tie'

        else:
            return False, 'Resume'


    def allowed_positions(self, curr_state):
        """Takes state as an input and returns all indexes that are blank"""
        return [i for i, val in enumerate(curr_state) if np.isnan(val)]


    def allowed_values(self, curr_state):
        """Takes the current state as input and returns all possible (unused) values that can be placed on the board"""

        used_values = [val for val in curr_state if not np.isnan(val)]
        agent_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 !=0]
        env_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 ==0]

        return (agent_values, env_values)


    def action_space(self, curr_state):
        """Takes the current state as input and returns all possible actions, i.e, all combinations of allowed positions and allowed values"""

        agent_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[0])
        env_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[1])
        return (agent_actions, env_actions)



    def state_transition(self, curr_state, curr_action):
        """Takes current state and action and returns the board position just after agent's move.
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = [1, 2, 3, 4, nan, nan, nan, 9, nan]
        """
        curr_state[curr_action[0]]=curr_action[1]
        return curr_state


    def step(self, curr_state, curr_action):
        """Takes current state and action and returns the next state, reward and whether the state is terminal. Hint: First, check the board position after
        agent's move, whether the game is won/loss/tied. Then incorporate environment's move and again check the board status.
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = ([1, 2, 3, 4, nan, nan, nan, 9, nan], -1, False)"""
        # make agents action
        new_state=self.state_transition(curr_state,curr_action)
        # determine the value of the action        
        if_terminal,step=self.is_terminal(new_state)
        # agent
        if step =='Win':
            return  new_state,10,if_terminal
        elif step == 'Tie':
            return new_state,0,if_terminal
        else:
            # evn turn 
            p_env_value=self.allowed_values(new_state)[1]
            p_position=self.allowed_positions(new_state)
            # env action
            new_state[np.random.choice(p_position)]=np.random.choice(p_env_value)
            # determine the value of the action        
            if_terminal,step=self.is_terminal(new_state)
            # env
            if step =='Win':
                return  new_state,-10,if_terminal
            elif step == 'Tie':
                return new_state,0,if_terminal
            else:
                return new_state,-1,if_terminal       

    def reset(self):
        return self.state
