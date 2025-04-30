import torch
import Constants

tensor1 = torch.zeros(3,2,dtype=torch.float32)
tensor2 = torch.rand(4,dtype=torch.float32)
tensor3 = tensor2.repeat(3,1)
print(tensor3)
print(Constants.ACT_CARTEZ)