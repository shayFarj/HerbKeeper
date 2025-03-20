import math
import random
from typing import Any
import torch
import torch.nn as nn
import torch.nn.functional as F

import Constants

# Parameters
input_size = Constants.STATE_LEN
layer1 = 64
layer2 = 32
output_size = 9 # Q(s,a) number of all combinations of direction and gear
gamma = Constants.AGENT_GAMMA
MSELoss = nn.MSELoss()

class DQN (nn.Module):
    def __init__(self) -> None:
        super().__init__()
        if torch.cuda.is_available():
            self.device = torch.device('cuda')
        else:
            self.device = torch.device('cpu')
        
        self.linear1 = nn.Linear(input_size, layer1)
        self.linear2 = nn.Linear(layer1, layer2)
        self.output = nn.Linear(layer2, output_size)
        
    def forward (self, x):
        x = self.linear1(x)
        x = F.relu(x)
        x = self.linear2(x)
        x = F.relu(x)
        x = self.output(x)
        return x
    
    def load_params(self, path):
        self.load_state_dict(torch.load(path))

    def save_params(self, path):
        torch.save(self.state_dict(), path)

    def copy (self):
        new_DQN = DQN()
        new_DQN.load_state_dict(self.state_dict())
        return new_DQN
    
    def loss (self, Q_value, rewards, Q_next_Values, Dones ):
        Q_new = rewards + gamma * Q_next_Values * (1- Dones)
        return MSELoss(Q_value, Q_new)

    def __call__(self, states):
        return self.forward(states).to(self.device)