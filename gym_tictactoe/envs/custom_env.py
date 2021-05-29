import gym
from gym import spaces
import numpy as np
from gym_tictactoe.envs.tictactoe import TicTacToeGame

class CustomEnv(gym.Env):

    def __init__(self):
        self.pygame = TicTacToeGame()
        self.action_space = spaces.Discrete(9)
        self.observation_space = spaces.Box(np.array([0, 0, 0, 0, 0, 0, 0, 0, 0]), np.array([2, 2, 2, 2, 2, 2, 2, 2, 2]), dtype=np.int)

    def reset(self):
        del self.pygame
        self.pygame = TicTacToeGame()
        obs = self.pygame.observe()
        return obs
    
    def step(self, action):
        self.pygame.action(action)
        obs = self.pygame.observe()
        reward = self.pygame.evaluate()
        done =  self.pygame.is_done()
        return obs, reward, done, {}
    
    def render(self, mode="Human", close=False):
        self.pygame.view()