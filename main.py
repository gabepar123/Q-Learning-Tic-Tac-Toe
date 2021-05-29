import gym
import gym_tictactoe
import numpy as np
import random
from os import path
import sys

def train(games):

    if path.exists('q_table.npy'):
        q_table =  np.load('q_table.npy')
    else:
        num_box = tuple((env.observation_space.high + np.ones(env.observation_space.shape)).astype(int))
        q_table = np.zeros(num_box + (env.action_space.n,))
    

    alpha = 0.1
    gamma = 0.6
    epsilon = 0.1

    for i in range(1, games):
        state = env.reset()
        env.render()

        epochs, penalties, reward, = 0, 0, 0
        done = False

        while not done:
            if random.uniform(0,1) < epsilon:
                action = env.action_space.sample()
            else:
                action = np.argmax(q_table[state])

            next_state, reward, done, _ = env.step(action)
            #print(reward)

            old_value = q_table[state][action]
            next_max = np.max(q_table[next_state])
            #time.sleep(1)
            #print(reward)

            new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
            q_table[state][action] = new_value

            if reward < 0:
                penalties += 1
            
            state = next_state
            epochs += 1

        
        if i % 1000 == 0:
            print(f"Episode: {i}")
        if i % 10000 == 0:
            np.save("q_table.npy", q_table)

    np.save("q_table.npy", q_table)
    print("Training finished.\n")
    test(q_table)

def test(q_table):
    total_epochs, total_penalties = 0, 0
    episodes = 100
    
    for _ in range(episodes):
        state = env.reset()
        env.render()
        epochs, penalties, reward = 0, 0, 0
        
        done = False
        
        while not done:
            action = np.argmax(q_table[state])
            state, reward, done, _ = env.step(action)
            

            if reward == -10:
                penalties += 1

            epochs += 1

        total_penalties += penalties
        total_epochs += epochs

    print(f"Results after {episodes} episodes:")
    print(f"Average timesteps per episode: {total_epochs / episodes}")
    print(f"Average penalties per episode: {total_penalties / episodes}")


if __name__ == "__main__":
    env = gym.make("TicTacToe-v0")
    games = int(sys.argv[1])
    train(games)

