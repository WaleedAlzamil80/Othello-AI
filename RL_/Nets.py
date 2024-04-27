from torch import nn
import torch

class Polivy_model(nn.Module):
    def __init__(self):
        super(Polivy_model, self).__init__()
        self.fc1 = nn.Linear(64, 128)
        self.fc2 = nn.Linear(128, 64)
        self.relu = nn.ReLU()
        self.softmax = nn.Softmax(dim = 1)

    def forward(self, x):
        x = self.relu(self.fc1(x))
        out = self.softmax(self.fc2(x))
        return out

    def predict(self, x):
        self.eval()
        return self.forward(x)

class Value_model(nn.Module):
    def __init__(self):
        super(Value_model, self).__init__()
        self.fc1 = nn.Linear(64, 128)
        self.fc2 = nn.Linear(128, 1)
        self.relu = nn.ReLU()
        self.tanh = nn.Tanh()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        out = self.tanh(self.fc2(x))
        return out

    def predict(self, x):
        self.eval()
        return self.forward(x)