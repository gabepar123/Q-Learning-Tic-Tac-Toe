<!-- ABOUT THE PROJECT -->
## About The Project

* This project allows you to train, or play against a Tic-Tac-Toe AI that was taught using [Q-Learning](https://en.wikipedia.org/wiki/Q-learning). 
* The AI trains in a custom Gym environment which allows it to easily find the game's current state, reward and possible actions.
* The Tic-Tac-Toe itself was made in Pygame.
* Rewards are as follows:

  | Action       | Reward         |
  | ------------- |:-------------:| 
  | Normal Move     | -1 | 
  | Invalid Move | -1 |
  | Win    | 10      | 
  | Lose | -10       |
  | Draw | 5 |
  * **Normal Move** reward encourages the AI to attempt to beat its opponent as fast as possible, to minimize negative rewards.
  * **Invalid Move** reward allows the AI to determine a valid move without having to deal with specifying valid/invalid moves within the Q-Table.
  * **Win** and **Lose** rewards are clear. Encourage winning and discourage losing.
  * **Draw** reward is positive, but less than the **Win** reward because Tic-Tac-Toe is a solved game, meaning that perfect play will always result in a draw. However, we would still wish to win as much as possible.

### Built With

* [Pygame](https://www.pygame.org/news)
* [OpenAI Gym](https://gym.openai.com/)
* [Numpy](https://numpy.org/)

## Usage

* `gym_tictactoe/` contains a custom *OpenAI Gym* environment.
* `/gym_tictactoe/envs/tictactoe.py` contains the Pygame Tic-Tac-Toe that the AI uses to train.
* `main.py` allows you to train the AI against an opponent that chooses a random valid move.
  * **Usage**: `python main.py [# of games]`
* `playAI.py` allows you to play against the AI, the AI always goes first.


<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [Creating a Custom OpenAI Gym Environment](https://www.youtube.com/watch?v=ZxXKISVkH6Y&t=173s)
* [Reinforcement Q-Learning from Scratch in Python with OpenAI Gym](https://www.learndatasci.com/tutorials/reinforcement-q-learning-scratch-python-openai-gym/)
* [Pygame in 90 Minutes - For Beginners](https://www.youtube.com/watch?v=jO6qQDNa2UY&t=4855s)


