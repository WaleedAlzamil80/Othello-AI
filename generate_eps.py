import os
import copy
import numpy as np
import argparse

from RL.MCTs_Actor_Critic import *
from RL.OthelloGame import *
from Othello_Game import *
from RL.Nets import *
from RL.RL import *

cuda = True if torch.cuda.is_available() else False
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
print(device)

parser = argparse.ArgumentParser(description="Specify the algorithms parameters.")

# Arguments for inference and play
parser.add_argument("--search", type=int, default=1000, help="Searching and exploring the Game Space (Simulation)")
parser.add_argument("--NH", type=int, default=64, help="Number of hidden layers")
parser.add_argument("--NB", type=int, default=4, help="Number of residual blocks")

# Arguments used just during training
parser.add_argument("--BatchSize", type=int, default=64, help="Batch Size")
parser.add_argument("--epochs", type=int, default=5, help="Epochs")
parser.add_argument("--self_play", type=int, default=500, help="Number of Games the model play before training")
parser.add_argument("--iterations", type=int, default=5, help="Number of iteration the model play against  itself before training")
parser.add_argument("--lr", type=float, default=0.001, help="Learning rate used while training")
parser.add_argument("--model_file", type=str, default="./Othello-AI/RL/SavedModels/model.pt", help="Pretrained models")

args = parser.parse_args()

othello = OthelloGame()
game = OthelloGAME()
model = ResNet(args.NB, args.BatchSize)

print("Loading pretrained model")
if cuda:
    state_dict = torch.load(args.model_file)
else:
    state_dict = torch.load(args.model_file, map_location = torch.device('cpu'))

model.load_state_dict(state_dict)

mcts = MCTs_RL(othello, args.search, model, device, cuda)

optimizer = torch.optim.Adam(model.parameters(), lr = args.lr)

BASE_DIR = os.getcwd()

LaylaZero = AlphaZero(GAME = othello, model = model, device = device, cuda = cuda, optimizer = optimizer, num_iteration = args.iterations, play_iteration = args.self_play, epochs = args.epochs, batch_size = args.BatchSize, num_simulation = args.search)
memory = LaylaZero.generateEPS()

state, policy_targets, value_targets = zip(*memory)
state, policy_targets, value_targets = np.array(state), np.array(policy_targets), np.array(value_targets).reshape(-1, 1)

# Create the new folder
directory = os.path.join(BASE_DIR, "results")
os.makedirs(directory, exist_ok=True)

# Save NumPy arrays with specified directory
np.save(os.path.join(directory, 'state_v0.npy'), np.array(state))
np.save(os.path.join(directory, 'policy_v0.npy'), np.array(policy_targets))
np.save(os.path.join(directory, 'value_v0.npy'), np.array(value_targets))

print("----------------------------- Finished -----------------------------")