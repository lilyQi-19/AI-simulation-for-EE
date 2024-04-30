from gymnasium import Env, spaces  # place holder for environment
from gymnasium.spaces import Discrete
import numpy as np
import random

from Player import Player
from Enemy import Enemy

class Environment (Env):
    def __init__(self):
        self.player = Player(random.randint(1,10), random.randint(1,10), random.randint(1,5))

        # initial enemy input
        self.ehealth = 5
        self.edamage = 5
        self.intelligence = 3
        self.attackSpace = 4

        self.action_space = Discrete(3*3*3*3*3)

        self.observation_space = spaces.Box(np.array([0,0,0,0]), np.array([101, 101, 251, 2]),dtype=int)
        # self.observation_space = spaces.Dict(
        #     {
        #         "healthChange": spaces.Box(0, 100, dtype=int),
        #         "health": spaces.Box(0, 100, dtype=int),
        #         "time": spaces.Box(0, 200, dtype=int),
        #         "death": spaces.Box(0,1,dtype=int)
        #     }
        # )

        self.state = np.array([0, 100, 0, 0])
        # self.state = spaces.Dict(
        #     {
        #         "healthChange": 0,
        #         "health": 100,
        #         "time": 0,
        #         "death": 0
        #     }
        # )

        # how many round
        self.round = 100

    def step(self, action):
        self.round -= 1

        # apply action
        self.ehealth += (action % 3) - 1
        action = action // 3
        self.edamage += (action % 3) - 1
        action = action // 3
        self.intelligence += (action % 3) - 1
        action = action // 3
        self.attackSpace += (action % 3) - 1
        action = action // 3
        regen = action * 10

        # check bound
        if self.ehealth <=0 or self.edamage <= 0 or self.intelligence <= 0 or self.intelligence > 10 or self.attackSpace <= 0:
            return self.state, -10, False, True, {}

        enemy = Enemy(self.ehealth, self.edamage, self.intelligence, self.attackSpace)
        self.player.faceEmeny(enemy,regen)

        # calculate reward
        reward = self.player.reward()

        # check done (required by gym)
        if self.round > 0:
            done = False
        else:
            done = True

        # change state
        self.state = np.array([self.player.healthChange, self.player.health, min(self.player.time,250), self.player.death])
        # self.state = spaces.Dict(
        #     {
        #         "healthChange": self.player.healthChange,
        #         "health": self.player.health,
        #         "time": self.player.time,
        #         "death": self.player.death
        #     }
        # )


        # placeholder for info (required by gym)
        info = {}

        # return state, reward, terminated(done), truncated, info
        return self.state, reward, done, False, info
        
    
    def render(self):
        print('ehealth:', str(self.ehealth), 'damage:', str(self.edamage),'intelligence:', str(self.intelligence),'attack Space:', str(self.attackSpace))       
        print('health:', str(self.player.health),'health change:', str(self.player.healthChange), 'time:', str(self.player.time), str(self.player.learn), str(self.player.death))
        print()

    def reset(self):
        self.player = Player(random.randint(1,10), random.randint(1,10), random.randint(1,5))

        self.ehealth = 5
        self.edamage = 5
        self.intelligence = 3
        self.attackSpace = 4

        self.state = np.array([0, 100, 0, 0])
        self.round = 100

        return self.state


    
