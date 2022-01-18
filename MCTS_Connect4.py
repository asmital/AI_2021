# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 21:42:06 2021

@author: mbee
"""

import copy
import numpy as np
import random
import pickle
import gzip
 
class board5x4:

    def __init__(self, p1= np.uint64(0), p2= np.uint64(0), highest_per_column=[0,5,10,15,20], n=0):
        self.bothboards = [np.uint64(p1), np.uint64(p2)]
        self.highest_per_column = copy.deepcopy(highest_per_column)
        self.moves_so_far = n
        
    def top_overflow(self):
        top_row= np.uint64(0b1000010000100001000010000)
        total_board=(self.bothboards[0] | self.bothboards[1])
        total_board_top=total_board & top_row
        return (total_board_top!= 0)
        
        
    def win_state(self):
        curr_player = (self.moves_so_far)
        curr_player-=1
        curr_player&=1
        board = self.bothboards[curr_player]
        temp= board & (board >> np.uint64(4))
        if temp & (temp >> np.uint64(2*4)):
            return True 
        
        temp= board & (board >> np.uint64(5))
        if(temp & (temp >> np.uint64(2*5)) ):
            return True
        temp= board & (board >> np.uint64(6))
        if(temp & (temp >> np.uint64(2* 6))):
            return True
        temp= board & (board >>np.uint64(1))
        if(temp & (temp >> np.uint64(2* 1))):
            return True
        return False
            
        
    def full_board(self):
        return (self.moves_so_far==5*4) 
        
    
    def show(self):
        
        array=[[ 3.,  8., 13., 18., 23.],
       [ 2.,  7., 12., 17., 22.],
       [ 1.,  6., 11., 16., 21.],
       [ 0.,  5., 10., 15., 20.]]
        
        toshow=[['.' for i in range (5)] for i in range(4)]
        
        for r in range(4):
            for c in range(5):
                
                check_board_1=(np.uint64(1) << np.uint64(array[r][c]))
                check_board_1&=self.bothboards[0]
                
                if(check_board_1 != 0):
                    toshow[r][c] = '1'
                    
                check_board_2=(np.uint64(1) << np.uint64(array[r][c]))
                check_board_2&=self.bothboards[1]
                if(check_board_2 != 0):
                    toshow[r][c] = '2'
                    
        PrintGrid(toshow)
        
        
    
    def my_hash(self):
        b = self.bothboards
        return str(b)
    
    

def ucb(U,N,C,Np):
    return U/N + C*np.sqrt(np.log(Np) / N)

class board5x6:

    def __init__(self, p1= np.uint64(0), p2= np.uint64(0), highest_per_column=[0,7,14,21,28], n=0):
        self.bothboards = [np.uint64(p1), np.uint64(p2)]
        self.highest_per_column = copy.deepcopy(highest_per_column)
        self.moves_so_far = n
        
    def top_overflow(self):
        top_row= np.uint64(0b10000001000000100000010000001000000)
        total_board=(self.bothboards[0] | self.bothboards[1])
        total_board_top=total_board & top_row
        return (total_board_top!= 0)
        
        
    def win_state(self):
        curr_player = (self.moves_so_far)
        curr_player-=1
        curr_player&=1
        board5x6 = self.bothboards[curr_player]
        temp= board5x6 & (board5x6 >> np.uint64(6))
        if temp & (temp >> np.uint64(2*6)):
            return True 
        
        temp= board5x6 & (board5x6 >> np.uint64(7))
        if(temp & (temp >> np.uint64(2*7)) ):
            return True
        temp= board5x6 & (board5x6 >> np.uint64(8))
        if(temp & (temp >> np.uint64(2* 8))):
            return True
        temp= board5x6 & (board5x6 >>np.uint64(1))
        if(temp & (temp >> np.uint64(2* 1))):
            return True
        return False
            
        
    def full_board(self):
        return (self.moves_so_far==5*6) 
        
    
    def show(self):
        
        array=[[ 5., 12., 19., 26., 33.],
       [ 4., 11., 18., 25., 32.],
       [ 3., 10., 17., 24., 31.],
       [ 2.,  9., 16., 23., 30.],
       [ 1.,  8., 15., 22., 29.],
       [ 0.,  7., 14., 21., 28.]]
        
        toshow=[['.' for i in range (5)] for i in range(6)]
        
        for r in range(6):
            for c in range(5):
                
                check_board_1=(np.uint64(1) << np.uint64(array[r][c]))
                check_board_1&=self.bothboards[0]
                
                if(check_board_1 != 0):
                    toshow[r][c] = '1'
                    
                check_board_2=(np.uint64(1) << np.uint64(array[r][c]))
                check_board_2&=self.bothboards[1]
                if(check_board_2 != 0):
                    toshow[r][c] = '2'
                    
        PrintGrid(toshow)
        
        
    
    def my_hash(self):
        b = self.bothboards
        return str(b)
    
    

def ucb(U,N,C,Np):
    return U/N + C*np.sqrt(np.log(Np) / N)
        
class MCTS_game_tree:
    
    def __init__(self, iterations = 400):
        self.board_currently_played = board5x6()
        self.state_list = {}
        self.backprop_list = []
        self.iterations = iterations
        
        state=board5x6()
        if not (bool(self.state_list)):
            self.state_list = {state.my_hash() : [0,1]}
        for i in range(156): #game tree with 4 levels has 1+5+25+125 nodes
            self.select_and_expand()
            winner=self.simulate()
            self.backprop(winner)
        
        
        

    def select_and_expand(self):
        

            
        while not (self.board_currently_played.full_board() or self.board_currently_played.win_state()):
            weight_child_nodes = [-1 for i in range(5)]      
            for x in range(5):
                
                new_board = copy.deepcopy(self.board_currently_played)
                new_board.bothboards[new_board.moves_so_far&1] ^= np.uint64(1 << new_board.highest_per_column[x])
                new_board.highest_per_column[x] += 1
                new_board.moves_so_far += 1
                if new_board.top_overflow():
                    new_board=None
                if new_board is None:
                    continue
            
                if new_board.my_hash() not in self.state_list:
                    self.state_list[new_board.my_hash()] = [0,0]
                    self.backprop_list.append(x)
                    self.board_currently_played = new_board
                    return
                
        
        
                U,N = self.state_list[new_board.my_hash()]
                
                
                
               
        
                Up,Np = self.state_list[self.board_currently_played.my_hash()]
        
                
                                
                #weight_child_nodes[x] = U/N + C*np.sqrt(np.log(Np) / N)
                weight_child_nodes[x]=ucb(U,N,np.sqrt(2),Np)
            input_list=[]
            input_range=[]
            for i in range(5):
                if weight_child_nodes[i]!=-1:
                    input_range.append(i)
                    input_list.append(weight_child_nodes[i])
                    
                    
            x = random.choices(input_range, weights=input_list, k=1)[0]
            self.backprop_list.append(x)
            new_board =copy.deepcopy(self.board_currently_played)
            new_board.bothboards[new_board.moves_so_far&1] ^= np.uint64(1 << new_board.highest_per_column[x])
            new_board.highest_per_column[x] += 1
            new_board.moves_so_far += 1
            if new_board.top_overflow():
                self.board_currently_played=None
            else:
                self.board_currently_played=new_board
            
            
            
    
        
        
    def simulate(self):
        b = copy.deepcopy(self.board_currently_played)
        while not (b.full_board() or b.win_state()):
            x = random.randint(0, 4)
            new_board = copy.deepcopy(b)
            new_board.bothboards[new_board.moves_so_far&1] ^= np.uint64(1 << new_board.highest_per_column[x])
            new_board.highest_per_column[x] += 1
            new_board.moves_so_far += 1
            if new_board.top_overflow():
                new_board=None
            if new_board is not None:
                b = new_board
        
        player = None
        if b.win_state():
            player = b.moves_so_far
            player-=1
            player&=1
        
        return player
    
    def backprop(self, player):
        
        while len(self.backprop_list) > 0:
    
            
            
            U,N = self.state_list[self.board_currently_played.my_hash()]
            
            winner=(self.board_currently_played.moves_so_far) & 1
            if winner != player:
                U += 5
            elif player is None:
                U += 1
            else:
                U += 0
            N += 5
            
            self.state_list[self.board_currently_played.my_hash()]=[U,N]
                
            col=self.backprop_list.pop()
            self.board_currently_played.moves_so_far -= 1
            self.board_currently_played.highest_per_column[col] -= 1
            bit_update=np.uint64(1 << self.board_currently_played.highest_per_column[col])
            self.board_currently_played.bothboards[self.board_currently_played.moves_so_far&1]^=bit_update
            
    
        
    def mcts_model_move(self, state):
        if not (bool(self.state_list)):
            self.state_list = {state.my_hash() : [0,1]}
        mby_hbash=state.my_hash()
        if mby_hbash not in self.state_list:
            self.state_list[mby_hbash] = [0,1]
            
        self.board_currently_played = copy.deepcopy(state)
        
        
        iterations=self.iterations
        for i in range(iterations):
            self.select_and_expand()
            winner=self.simulate()
            self.backprop(winner)
        
                
        weight_child_nodes = [-1 for i in range(5)]
        for x in range(5):
            new_board = copy.deepcopy(self.board_currently_played)
            new_board.bothboards[new_board.moves_so_far&1] ^= np.uint64(1 << new_board.highest_per_column[x])
            new_board.highest_per_column[x] += 1
            new_board.moves_so_far += 1
            if new_board.top_overflow():
                new_board=None
            if new_board is not None:
                b = new_board                
            if new_board is None:
                continue
        
            if new_board.my_hash() not in self.state_list:	
                self.state_list[new_board.my_hash()] = [0,0]
            U,N = self.state_list[new_board.my_hash()]
    
            weight_child_nodes[x] = N
            
        max_val = max(weight_child_nodes)
        input_list=[i for i in range(5) if weight_child_nodes[i] == max_val]
        x = random.choice([input_list])[0]
        
        new_board =copy.deepcopy(self.board_currently_played)
        new_board.bothboards[new_board.moves_so_far&1] ^= np.uint64(1 << new_board.highest_per_column[x])
        new_board.highest_per_column[x] += 1
        new_board.moves_so_far += 1
        if new_board.top_overflow():
            self.board_currently_played=None
        else:
            self.board_currently_played=new_board
        
        returnarray=(np.array(weight_child_nodes)/5)[x]
        return x, returnarray
    
    
class qlearn:
    def __init__(self):
        game=board5x4()
        game_hash=game.my_hash()
        self.state_table={}
        self.state_table[game_hash]=float(0)
        self.pre_state=game_hash
        
        
    def q_update(self, b, alpha, epsilon, gamma):
            
        next_Q_vals = [float(0)]*5
        for x in range(5):
            nb = copy.deepcopy(b)
            nb.bothboards[nb.moves_so_far&1] ^= np.uint64(1 << nb.highest_per_column[x])
            nb.highest_per_column[x] += 1
            nb.moves_so_far += 1
            if nb.top_overflow():
                nb=None
                next_Q_vals[x]=-1
            if nb is None:
                continue
            
            if nb.my_hash() not in self.state_table:
                self.state_table[nb.my_hash()] = float(random.random())
                next_Q_vals[x] = self.state_table[nb.my_hash()]
            else:
                next_Q_vals[x] = self.state_table[nb.my_hash()]
        
        
        x = np.argmax(next_Q_vals)
        max_after = copy.deepcopy(b)
        temp_player=max_after.moves_so_far&1
        shift_value=1 << max_after.highest_per_column[x]
        max_after.bothboards[temp_player] ^= np.uint64(1 << max_after.highest_per_column[x])
        max_after.highest_per_column[x] += 1
        max_after.moves_so_far += 1
        if max_after.top_overflow():
            max_after=None
        
        if(random.random() < epsilon):
            valid_flag=0
            while not valid_flag:
    
                x=random.randint(0,4)
                if (next_Q_vals[x]>0):
                    valid_flag=1
                    

        
        nb = copy.deepcopy(b)
        shift_value=1 << nb.highest_per_column[x]
        temp_player=nb.moves_so_far&1
        nb.bothboards[temp_player] ^= np.uint64(shift_value)
        nb.highest_per_column[x] += 1
        nb.moves_so_far += 1
        if nb.top_overflow():
            nb=None
        ab=nb
        
        pre_state_Q = self.state_table[self.pre_state]
        update_value=max_after.my_hash()
        S2 = self.state_table[update_value]
        
        R=0
        
        if b.full_board():
            R= 1
        elif b.win_state():
            R= 25 - b.moves_so_far  
        
        update_value= gamma * S2
        update_value_temp= R+update_value-pre_state_Q
        pre_state_Q += alpha * update_value_temp
        
        self.state_table[self.pre_state] = pre_state_Q
        updated_pre_state=ab.my_hash()   
        self.pre_state = updated_pre_state     
            
        return x, next_Q_vals[x]
        




def PrintGrid(positions):
    print('\n'.join(' '.join(str(x) for x in row) for row in positions))
    print()
    
    



    
    
def main():
    flag=int(input("Enter 0 for part a), enter 1 for part c)"))
    if(flag==0):
        agent1 = MCTS_game_tree(iterations = 200)
        agent2 = MCTS_game_tree(iterations = 40)
        game = board5x6()
        over_flag=game.full_board() or game.win_state()
        while not over_flag:
            x, playouts = agent1.mcts_model_move(game)
            print("Player 1 "+"MCTS with "+str(agent1.iterations)+" playouts")
            print("\n")
            print("Action selected "+ str(x))
            print("\n")
            print("Total playouts for next state "+str(playouts))
            print("\n")
            new_board = copy.deepcopy(game)
            new_board.bothboards[new_board.moves_so_far&1] ^= np.uint64(1 << new_board.highest_per_column[x])
            new_board.highest_per_column[x] += 1
            new_board.moves_so_far += 1
            if new_board.top_overflow():
                new_board=None
            if new_board is not None:
                game = copy.deepcopy(new_board)
            
            game.show()
            print()
            if game.win_state():
                print("Player 1 wins, with moves=", game.moves_so_far)
                return
            
            if (game.full_board() or game.win_state()):
                print("The game is a draw!,", game.moves_so_far)
                return
            x, playouts = agent2.mcts_model_move(game)
            print("Player 2"+" MCTS with "+str(agent2.iterations)+" playouts")
            print("\n")
            print("Action selected "+ str(x))
            print("\n")
            print("Total playouts for next state "+str(playouts))
            print("\n")
            new_board = copy.deepcopy(game)
            new_board.bothboards[new_board.moves_so_far&1] ^= np.uint64(1 << new_board.highest_per_column[x])
            new_board.highest_per_column[x] += 1
            new_board.moves_so_far += 1
            if new_board.top_overflow():
                new_board=None
            if new_board is not None:
                game = copy.deepcopy(new_board)
            
            game.show()
            print()
            if game.win_state():
                print("Player 2 wins, with moves=", game.moves_so_far)
                return
            if (game.full_board() or game.win_state()):
                print("The game is a draw!")
                return
            
            
            over_flag=game.full_board() or game.win_state()
                
        print("The game is a draw!")
    elif (flag==1):
        agent1=MCTS_game_tree(1)
        agent2=qlearn()
        f = gzip.GzipFile("2018B5A70881G_ASMITA.dat.gz", "r")
        agent2.state_table = pickle.load(f)
        f.close()
        game = board5x4()
        over_flag=game.full_board() or game.win_state()
        while not over_flag:
            x, playouts = agent1.mcts_model_move(game)
            print("Player 1 "+"MCTS with "+str(agent1.iterations)+" playouts")
            print("\n")
            print("Action selected "+ str(x))
            print("\n")
            print("Total playouts for next state "+str(playouts))
            print("\n")
            new_board = copy.deepcopy(game)
            new_board.bothboards[new_board.moves_so_far&1] ^= np.uint64(1 << new_board.highest_per_column[x])
            new_board.highest_per_column[x] += 1
            new_board.moves_so_far += 1
            if new_board.top_overflow():
                new_board=None
            if new_board is not None:
                game = copy.deepcopy(new_board)
            
            game.show()
            print()
            if game.win_state():
                print("Player 1 wins, with moves=", game.moves_so_far)
                return
            
            if (game.full_board() or game.win_state()):
                print("The game is a draw!,", game.moves_so_far)
                return

            x, playouts = agent2.q_update(game, 0.00, 0.1, 0.9)
            print("Player 2"+" qlearnz with playouts")
            print("\n")
            print("Action selected "+ str(x))
            print("\n")
            print("Q value for state "+str(playouts))
            print("\n")
            new_board = copy.deepcopy(game)
            new_board.bothboards[new_board.moves_so_far&1] ^= np.uint64(1 << new_board.highest_per_column[x])
            new_board.highest_per_column[x] += 1
            new_board.moves_so_far += 1
            if new_board.top_overflow():
                new_board=None
            if new_board is not None:
                game = copy.deepcopy(new_board)
            
            game.show()
            print()
            if game.win_state():
                print("Player 2 wins, with moves=", game.moves_so_far)
                return
            if (game.full_board() or game.win_state()):
                print("The game is a draw!")
                return
            
            
            over_flag=game.full_board() or game.win_state()
                
        print("The game is a draw!")
            
        


    
if __name__ == '__main__':
    main()
    
            
        


        
        
        
        
                
           
                 
                
            
            
            
            
        
        
        
        
        
        
        
        
        
            