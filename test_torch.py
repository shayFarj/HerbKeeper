import torch
import Constants

tensor1 = torch.zeros(3,2,dtype=torch.float32)
tensor2 = torch.rand(4,dtype=torch.float32)
tensor3 = tensor2.repeat(3,1)

tensor4 = torch.zeros(1)
tensor4[0]= 0

print(Constants.dir_status_boun(28))