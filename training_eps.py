import os
import numpy as np
import argparse
import torch
from torch import nn
import torch.nn.functional as F
from torch.utils.data import TensorDataset, DataLoader

from RL.Nets import *


cuda = True if torch.cuda.is_available() else False
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
print(device)

parser = argparse.ArgumentParser(description="Specify the algorithms parameters.")

# Arguments for inference and play
parser.add_argument("--NH", type=int, default=64, help="Number of hidden layers")
parser.add_argument("--NB", type=int, default=4, help="Number of residual blocks")

# Arguments used just during training
parser.add_argument("--BatchSize", type=int, default=128, help="Batch Size")
parser.add_argument("--epochs", type=int, default=5, help="Epochs")
parser.add_argument("--lr", type=float, default=0.001, help="Learning rate used while training")
parser.add_argument("--model_file", type=str, default="./Othello-AI/RL/SavedModels/model.pt", help="Pretrained models")
parser.add_argument("--data_path", type=str, default="./Othello-AI/RL/DataGenerated/iteration00", help="Pretrained models")

args = parser.parse_args()

model = ResNet(args.NB, args.BatchSize)

print("Loading pretrained model to ", device)
if cuda:
    state_dict = torch.load(args.model_file)
else:
    state_dict = torch.load(args.model_file, map_location = torch.device('cpu'))

model.load_state_dict(state_dict)

optimizer = torch.optim.Adam(model.parameters(), lr = args.lr)

# Load your NumPy arrays (assuming you have them saved in .npy files)
states = np.load(os.path.join(args.data_path, "states_i00_sh.npy"))
policies = np.load(os.path.join(args.data_path, "policies_i00_sh.npy"))
values = np.load(os.path.join(args.data_path, "values_i00_sh.npy"))

# Convert NumPy arrays to PyTorch tensors
tensor1 = torch.from_numpy(states).float()
tensor2 = torch.from_numpy(policies).float()
tensor3 = torch.from_numpy(values).float()

# Create a TensorDataset
dataset = TensorDataset(tensor1, tensor2, tensor3)

# Create a DataLoader
dataloader = DataLoader(dataset, batch_size=args.BatchSize, shuffle=True)

model.train()
pol = []
val = []

for epoch in range(args.epochs):
    policyLOSS = 0
    valueLOSS = 0

    for batch in dataloader:
        state, policy, value = batch
        state, policy, value = state.to(device), policy.to(device), value.to(device)

        out_policy, out_value = model.forward(state)

        policy_loss = F.cross_entropy(out_policy, policy)
        value_loss = F.mse_loss(out_value, value)
        loss = policy_loss + value_loss

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        policyLOSS += policy_loss.item()
        valueLOSS += value_loss.item()
    policyLOSS /= len(dataloader)
    valueLOSS /= len(dataloader)
    pol.append(policyLOSS)
    val.append(valueLOSS)

    print(f"Epoch: {epoch + 1} | policy loss : {policyLOSS:.4f} | value loss : {valueLOSS:.4f}")


BASE_DIR = os.getcwd()

# Create the new folder
directory = os.path.join(BASE_DIR, "results")
os.makedirs(directory, exist_ok=True)

# Save NumPy arrays with specified directory
np.save(os.path.join(directory, 'poly_loss.npy'), np.array(pol))
np.save(os.path.join(directory, 'value_loss.npy'), np.array(val))

# Specify the file name for saving the model
model_file = os.path.join(directory, 'model_v1.pt')

# Save the model to the specified directory
torch.save(model.state_dict(), model_file)