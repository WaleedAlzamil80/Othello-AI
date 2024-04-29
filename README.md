# Othello AI
This repository implements various artificial intelligence (AI) algorithms for the classic game of Othello.

## Main Algorithms:
1. *MinMax Algorithm*:

- A classic AI technique for perfect information games like Othello, where both players have complete knowledge of the game state.
It works by recursively building a game tree, exploring all possible future moves for both players.
- At each node in the tree, a score is assigned based on how favorable the position is for the AI player (usually the number of discs flipped).
The algorithm then chooses the move that leads to the highest score for the AI, assuming the opponent plays optimally.
- Strengths: Easy to implement, provides a guaranteed optimal move for a given search depth.
- Weaknesses: Computationally expensive for deep searches, doesn't consider opponent's potential mistakes.

2. *MinMax Alpha-Beta Pruning*:

- An enhancement of the MinMax algorithm that improves efficiency.
It utilizes alpha and beta values to prune unnecessary branches in the game tree.
- Alpha represents the best score the AI can guarantee for itself, while beta represents the best score the opponent can achieve.
When evaluating a move, if its score is worse than the current beta value (for the opponent), the entire branch can be ignored as the opponent wouldn't choose that path anyway.
- Similarly, if a move's score is better than the current alpha value, it becomes the new alpha, effectively cutting off branches that wouldn't lead to a better outcome for the AI.
- Strengths: Significantly faster than vanilla MinMax for complex games.
- Weaknesses: Still limited by search depth, pruning might miss good moves in unexplored branches.
3. *Monte Carlo Tree Search (MCTS)*:

- A powerful algorithm that utilizes simulations to explore the game tree.
- It starts by building a tree of possible moves, then iteratively selects branches based on a balance between exploitation (choosing proven good moves) and exploration (trying new possibilities).
- At each selected node, the AI plays out a simulated game from that point, using random moves for both players.
- The results of these simulations are used to update the tree, favoring nodes that lead to better outcomes for the AI in the simulations.
- Over time, MCTS converges towards finding the best move by focusing on promising branches while still exploring new possibilities.
- Strengths: Efficiently explores the game tree, adapts to opponent's playing style.
- Weaknesses: Requires more computation than MinMax for a single move, might not guarantee optimal play.
4. *Actor-Critic (Reinforcement Learning)*:

- An approach from Reinforcement Learning (RL) where two neural networks work together.
- The Actor network predicts the best move for the AI in a given state.
- The Critic network evaluates the value of the state-action pair, indicating how good it was for the AI to take a specific move in a particular situation.
- Through training, both networks learn from the rewards received during gameplay (e.g., winning, losing, or intermediate rewards for disc advantage).
- The Critic's feedback helps the Actor improve its move selection over time.
- Strengths: Adapts to different strategies, learns from experience, can be very strong with sufficient training data.
- Weaknesses: Requires significant training time and data, might not be interpretable in terms of specific decision-making logic.

## Getting Started (Continued in next section...)
