from RL.MCTs_Actor_Critic import *
import random
import torch.nn.functional as F

class AlphaZero:
  def __init__(self, model, optimizer, GAME, device, num_iteration = 5, play_iteration = 500, epochs = 5, batch_size = 64, num_simulation = 1000):
    self.model = model
    self.optimizer = optimizer
    self.game = GAME
    self.num_simulation = num_simulation
    self.num_iteration = num_iteration
    self.play_iteration = play_iteration
    self.epochs = epochs
    self.batch_size = batch_size
    self.mcts = MCTs_RL(GAME, num_simulation, model, device)
    self.device = device

  def selfPlay(self):
    memory = []
    state = self.game.initial_state()
    player = 1
    val, termination = self.game.value_termination(state)
    while not termination:
      if len(self.game.get_valid_moves(state, player)) == 0:
        player *= -1
      action_probs = self.mcts.search(state, player)
      memory.append((state, action_probs, player))
      action = np.random.choice(self.game.action_space, p = action_probs)

      state, value, isterminal = self.game.make_move(state, player, action // 8, action % 8)

      if isterminal:
        returnMemory = []
        for s, a, per in memory:
          outcome = value if per == player else -value
          returnMemory.append((self.game.encoded_state(s), a, outcome))
        return returnMemory

      player *= -1
      val, termination = self.game.value_termination(state)

  def learn(self):
    pol = []
    val = []
    for iteration in range(self.num_iteration):
      print("-------------------------------------------------")
      print(f"Iteration number {iteration + 1}")
      memory = []
      for playiter in range(self.play_iteration):
          print(f"Play iteration {playiter + 1}")
          memory += self.selfPlay()
      print("-------------------------------------------------")

      self.model.train()
      for epoch in range(self.epochs):

        p, v = self.train(memory)
        pol.append(p)
        val.append(v)

        print(f"Epoch {epoch + 1}: policy Loss: {p:.4f} | value Loss: {v:.4f}")

    return pol, val

  def generateEPS(self):
    for playiter in range(self.play_iteration):
        print(f"Play iteration {playiter + 1} Started")
        memory += self.selfPlay()
    return memory


  def train(self, memory):
      random.shuffle(memory)
      policyLOSS = 0
      valueLOSS = 0

      for batchIdx in range(0, len(memory), self.batch_size):
          sample = memory[batchIdx:min(len(memory) - 1, batchIdx + self.batch_size)]
          state, policy_targets, value_targets = zip(*sample)

          state, policy_targets, value_targets = np.array(state), np.array(policy_targets), np.array(value_targets).reshape(-1, 1)

          state = torch.tensor(state, dtype=torch.float32).to(self.device)
          policy_targets = torch.tensor(policy_targets, dtype=torch.float32).to(self.device)
          value_targets = torch.tensor(value_targets, dtype=torch.float32).to(self.device)

          out_policy, out_value = self.model.forward(state)

          policy_loss = F.cross_entropy(out_policy, policy_targets)
          value_loss = F.mse_loss(out_value, value_targets)
          loss = policy_loss + value_loss

          self.optimizer.zero_grad()
          loss.backward()
          self.optimizer.step()
          policyLOSS += policy_loss.item()
          valueLOSS += value_loss.item()

      policyLOSS /= len(memory)
      valueLOSS /= len(memory)

      return policyLOSS, valueLOSS