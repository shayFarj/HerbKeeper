import math
import random
from typing import Any
import torch
import torch.nn as nn
import numpy as np
from DQN import DQN

# epsilon Greedy
epsilon_start = 1
epsilon_final = 0.01
epsiln_decay = 5000

# epochs = 1000
# batch_size = 64
gamma = 0.99 
MSELoss = nn.MSELoss()

class DQN_Agent:
    def __init__(self, player = 1, parametes_path = None, train = True, env= None) -> None:
        self.DQN = DQN()
        if parametes_path:
            self.DQN.load_params(parametes_path)
        self.train(train)
        # self.train = train
        self.player = player
        self.env = env
        self.active = True

    def train (self, train):
          self.train = train
          if train:
              self.DQN.train()
          else:
              self.DQN.eval()

    def get_action (self, state, epoch = 0, events= None, train = True):
        if not self.active:
            return (0,0)
        epsilon = self.epsilon_greedy(epoch)
        rnd = random.random()
        actions = self.env.legal_actions(state)
        if self.train and train and rnd < epsilon:
            return random.choice(actions)
        
        state_tensor = state#.toTensor()
        action_np = np.array(actions)
        action_tensor = torch.from_numpy(action_np)
        expand_state_tensor = state_tensor.unsqueeze(0).repeat((len(action_tensor),1))
        # state_action = torch.cat((expand_state_tensor, action_tensor ), dim=1)
        with torch.no_grad():
            Q_values = self.DQN(expand_state_tensor, action_tensor)
        max_index = torch.argmax(Q_values)
        return actions[max_index]

    def get_actions (self, states, dones):
        actions = []
        for i, state in enumerate(states):
            if dones[i].item():
                actions.append((0,0))
            else:
                actions.append(self.get_action(state, train=True)) #SARSA = True / Q-learning = False
        return torch.tensor(actions)

    def epsilon_greedy(self,epoch, start = epsilon_start, final=epsilon_final, decay=epsiln_decay):
        res = final + (start - final) * math.exp(-1 * epoch/decay)
        return res
    
    def save_param (self, path):
        self.DQN.save_params(path)

    def load_params (self, path):
        self.DQN.load_params(path)

    def __call__(self, events= None, state=None) -> Any:
        return self.get_action(state)

