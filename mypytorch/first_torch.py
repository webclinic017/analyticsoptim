import torch
import numpy as np
a = np.ones(5)
b=torch.from_numpy(a)
np.add(a,1,out=a)
print(a)
print(b)
x=torch.empty(2)
y = torch.tensor([3,4])
print(x)