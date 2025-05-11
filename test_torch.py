import torch
import Constants

tensor1 = torch.zeros(3,2,dtype=torch.float32)
tensor2 = torch.rand(4,dtype=torch.float32)
tensor3 = tensor2.repeat(3,1)

tensor4 = torch.zeros(1)
tensor4[0]= 0

print(Constants.RELEV_TRANS)
print(Constants.MAX_D)
print(tensor4 / Constants.MAX_D)
print(Constants.d_relev(tensor4))