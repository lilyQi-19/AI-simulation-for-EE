import random
import numpy as np
import matplotlib.pyplot as plt

import gymnasium as gym
import seaborn as sns
from IPython.display import clear_output

from Player import Player
from Enemy import Enemy
from environment import Environment
# import torch.optim as optim
# from torch.distributions import Categorical
sns.set()


env = Environment()
env.reset() # reset environment to a new, random state

state = env.state

q_table = np.zeros([101,101,251,2, env.action_space.n])
print(np.max(q_table[state[0],state[1],state[2],state[3]]))

# Hyperparameters
alpha = 0.1
gamma = 0.6
epsilon = 0.1

# For plotting metrics
all_rewards = []
episodeNum = []

reward = 0

frames = [] # for animation

done = False

for i in range(1, 400001):
    state = env.reset()

    reward = 0
    done = False
    truncated = False
    
    while not done and not truncated:
        if random.uniform(0, 1) < epsilon:
            action = env.action_space.sample() # Explore action space
        else:
            action = np.argmax(q_table[state[0],state[1],state[2],state[3]]) # Exploit learned values

        next_state, reward, done, truncated, info = env.step(action) 
        
        old_value = q_table[state[0],state[1],state[2],state[3], action]
        next_max = np.max(q_table[next_state[0], next_state[1],next_state[2],next_state[3]])
        
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        q_table[state[0],state[1],state[2],state[3], action] = new_value

        state = next_state
        
    if i % 100 == 0:
        clear_output(wait=True)
    #     print(f"Episode: {i}")

    # see how will is it doing
    if i % 10000 == 0:
        total_reward = 0
        testRound = 100

        for _ in range(testRound):
            state = env.reset()
            treward = 0 
    
            done = False
            truncated = False

            
            while not done and not truncated:
                action = np.argmax(q_table[state[0],state[1],state[2],state[3]])
                state, treward, done, truncated, info = env.step(action) 

                total_reward += treward

            

        print(f"Episode: {i}")
        episodeNum.append(i)
        print(f"Results after {testRound} testRound:")
        print(f"Average reward per testRound: {total_reward / testRound}")
        all_rewards.append((total_reward / testRound))


print("Training finished.\n")
print(all_rewards)

# control: random generated enemy
controlReward = 0
for i in range(100):
    state = env.reset()
    treward = 0 
    
    done = False
    truncated = False

            
    while not done and not truncated:
            action = env.action_space.sample()
            state, treward, done, truncated, info = env.step(action) 

            controlReward += treward
print(controlReward/100)


# plot average rewards per episodes trained
plt.style.use('_mpl-gallery')
fig, ax = plt.subplots()

ax.plot(episodeNum, all_rewards, linewidth=2.0)
ax.plot(episodeNum, np.full(len(episodeNum),(controlReward/100)), '-.')

ax.grid(True, which='both')

fig.suptitle('average rewards per episodes trained')
ax.set_xlabel("episode trained")
ax.set_ylabel("average reward")

plt.show()


# get data for round against reward
step = np.arange(101)
step_award = np.zeros(101)

for _ in range(10000):
    state = env.reset()
    
    done = False
    truncated = False

    round = 0

    while not done and not truncated:
        action = np.argmax(q_table[state[0],state[1],state[2],state[3]])
        state, r, done, truncated, info = env.step(action) 
        round += 1
        step_award[round] += r
        
step_award = step_award / 10000

# control: random step taken
controlReward = np.zeros(101)
for i in range(100):
    state = env.reset()
    
    done = False
    truncated = False

    round = 0
            
    while not done and not truncated:
            action = env.action_space.sample()
            state, r, done, truncated, info = env.step(action) 
            round += 1
            controlReward[round] += r

controlReward = controlReward / 100

# plot reward per step
plt.style.use('_mpl-gallery')
fig, ax = plt.subplots()

ax.plot(step, step_award, linewidth=2.0)
ax.plot(step, controlReward, '-.')

ax.grid(True, which='both')

fig.suptitle('average reward per enemy faced')
ax.set_xlabel("enemy count")
ax.set_ylabel("average reward")

plt.show()

# get data for player average levels and reward
level = np.arange(1,10.1,0.5)
levelCount = np.zeros(len(level))
level_reward = np.zeros(len(level))

for _ in range(10000):
    state = env.reset()
    
    done = False
    truncated = False
    plevel = (env.player.hit + env.player.dodge)-2
    levelCount[plevel] += 1
    while not done and not truncated:
        action = np.argmax(q_table[state[0],state[1],state[2],state[3]])
        state, r, done, truncated, info = env.step(action) 
        level_reward[plevel] += r
        
level_reward = np.divide(level_reward,levelCount)

# control: random step taken
ClevelCount = np.zeros(len(level))
Clevel_reward = np.zeros(len(level))

for _ in range(10000):
    state = env.reset()
    
    done = False
    truncated = False
    plevel = (env.player.hit + env.player.dodge)-2
    ClevelCount[plevel] += 1
    while not done and not truncated:
        action = env.action_space.sample()
        state, r, done, truncated, info = env.step(action) 
        Clevel_reward[plevel] += r
        
Clevel_reward = np.divide(Clevel_reward,ClevelCount)

# plot reward per step
plt.style.use('_mpl-gallery')
fig, ax = plt.subplots()

ax.plot(level, level_reward, linewidth=2.0)
ax.plot(level, Clevel_reward, '-.')

ax.grid(True, which='both')

fig.suptitle('average reward for different average player skill level')
ax.set_xlabel("average player skill level")
ax.set_ylabel("average reward")

plt.show()
    
    