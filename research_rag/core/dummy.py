import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Disable GPU

import torch
print(torch.__version__)
print(torch.cuda.is_available())  # Should be False
