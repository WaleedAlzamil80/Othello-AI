# Othello AI
Welcome to the Othello AI project! This project implements an AI to play the game of Othello (also known as Reversi) with a graphical user interface (GUI). The AI supports various difficulty levels and different algorithms including MinMax and Monte Carlo Tree Search (MCTS).

## GUI

### Screens

1. The main screen is where you decide to play or end exit the game.
![Main_Menu.png](./assets/Main_Menu.png)
2. Players screen is where each player select the algorithm
![player1.png](./assets/algo1.png)
![player2.png](./assets/algo2.png)
3. Difficulty where we specify the difficulty of the algorithm
![difficulty.png](./assets/diff.png)
4. Game screen is where the game is played and the Othello board is displayed. The board is an 8x8 grid where the game pieces are placed.
You have the options to:
- Pause the game
- Resume the game
- Restart the game
- Go back to the Main Menu

![drawpng.png](./assets/drawpng.png)
![white.png](./assets/white.png)


## Main Algorithms:
1. **MinMax Algorithm**:

*Over View*
- A classic AI technique for perfect information games like Othello, where both players have complete knowledge of the game state.
- It works by recursively building a game tree, exploring all possible future moves for both players.
- At each node in the tree, a score is assigned based on how favorable the position is for the AI player (usually the number of discs flipped).
- The algorithm then chooses the move that leads to the highest score for the AI, assuming the opponent plays optimally.

*Strengths*
- Easy to implement.
- Provides a guaranteed optimal move for a given search depth. (Greedy algorithm on a certin depth and can find global optimal moves if the game is solved and a the choosen depth can reach the terminal state)

*Weaknesses*
- Computationally expensive for deep searches.
- Doesn't consider opponent's potential mistakes.

*Arguemnts*

| Argument         | Description                                                                                                                               |
|------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| --depth          |  The number of turns (plies) considered for future moves, impacting the balance between speed and strategic evaluation. Default: 2        |

2. **MinMax Alpha-Beta Pruning**:

*Over View*
- An enhancement of the MinMax algorithm that improves efficiency.
- It utilizes alpha and beta values to prune unnecessary branches in the game tree.
- Alpha represents the best score the AI can guarantee for itself, while beta represents the best score the opponent can achieve.
- When evaluating a move, if its score is worse than the current beta value (for the opponent), the entire branch can be ignored as the opponent wouldn't choose that path anyway.
- Similarly, if a move's score is better than the current alpha value, it becomes the new alpha, effectively cutting off branches that wouldn't lead to a better outcome for the AI.

*Strengths* 
- Significantly faster than vanilla MinMax for complex games.

*Weaknesses*
- Still limited by search depth, pruning might miss good moves in unexplored branches.

*Arguemnts*

| Argument         | Description                                                                                                                               |
|------------------|-------------------------------------------------------------------------------------------------------------------------------------------|
| --depth          |  The number of turns (plies) considered for future moves, impacting the balance between speed and strategic evaluation. Default: 2        |

3. **Monte Carlo Tree Search (MCTS)**:

*Over View*
- A powerful algorithm that utilizes simulations to explore the game tree.
- It starts by building a tree of possible moves, then iteratively selects branches based on a balance between exploitation (choosing proven good moves) and exploration (trying new possibilities).
- At each selected node, the AI plays out a simulated game from that point, using random moves for both players.
- The results of these simulations are used to update the tree, favoring nodes that lead to better outcomes for the AI in the simulations.
- Over time, MCTS converges towards finding the best move by focusing on promising branches while still exploring new possibilities.

*Strengths* 
- Efficiently explores the game tree
- Adapts to opponent's playing style.

*Weaknesses*
- Requires more computation than MinMax for a single move.
- Might not guarantee optimal play.

*Arguemnts*

| Argument         | Description                                                                                                      |
|------------------|------------------------------------------------------------------------------------------------------------------|
| --search         | The number of simulations used for searching and exploring the game space during inference. Default: 1000        |

4. **Actor-Critic (Reinforcement Learning)**:

*Over View*
- An approach from Reinforcement Learning (RL) where two neural networks work together.
- The Actor network predicts the best move for the AI in a given state.
- The Critic network evaluates the value of the state-action pair, indicating how good it was for the AI to take a specific move in a particular situation.
- Through training, both networks learn from the rewards received during gameplay (e.g., winning, losing, or intermediate rewards for disc advantage).
- The Critic's feedback helps the Actor improve its move selection over time.

*Strengths*
- Adapts to different strategies.
- Learns from experience, can be very strong with sufficient training data.

*Weaknesses*
- Requires significant training time and data.
- Might not be interpretable in terms of specific decision-making logic.

*Arguemnts*

| Argument         | Description                                                                                                      |
|------------------|------------------------------------------------------------------------------------------------------------------|
| --search         | The number of simulations used for searching and exploring the game space during inference. Default: 1000        |
| --NH             | Number of hidden layers in the neural network architecture. Default: 64                                          |
| --NB             | Number of residual blocks in the neural network architecture. Default: 4                                         |
| --BatchSize      | Batch size used during training. Default: 64                                                                     |
| --epochs         | Number of epochs for training. Default: 5                                                                        |
| --self_play      | Number of games the model plays against itself before training. Default: 500                                     |
| --iterations     | Number of iterations the model plays against itself before training. Default: 5                                  |
| --lr             | Learning rate used during training. Default: 0.001                                                               |
| --model_file     | Path to the saved model file. Default: "./Othello-AI/RL/SavedModels/model.pt"                                    |

### How to generate games from Agent for future Training?
1. Cloning the Repository

```shell
git clone https://github.com/WaleedAlzamil80/Othello-AI.git
```
2. Run the Following command

```shell
python Othello-AI/generate_eps.py --self_play 100
```
In case it takes too much reduce the number of games (self_play)

3. The results will be found in the `results` folder then you can download the 3 numpy arrays corresponding to (State, Policy, Value)

### How to Train with your custom dataset?
```shell
python training_eps.py --data_path ./path/to/custom_data --BatchSize 32 --lr 0.0001 --epochs 10
```

### How to learn?
```shell
python run.py --BatchSize 32 --lr 0.0001 --epochs 10 --self_play 1000 --search 1500 --iterations 10
```

## Explian MCTs
For more detailed documentation, see the [MCTs/README.md](MCTs/README.md).

## Explain Actor-Critic algorithm (RL)
For more detailed documentation, see the [RL/README.md](RL/README.md).

## Quick Start (Continued in next section...)
