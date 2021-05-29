from gym.envs.registration import register

register(
    id='TicTacToe-v0',
    entry_point='gym_tictactoe.envs:CustomEnv',
    max_episode_steps=2000,
)